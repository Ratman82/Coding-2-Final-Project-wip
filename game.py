import curses
import random
import os
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder

from pokemon import build_pokemon_list
from moves import build_move_list

pokemon_dex = build_pokemon_list()
move_dex    = build_move_list()

battle_history = []

knn = KNeighborsClassifier(n_neighbors=3)

encoders = {
    "player_type": LabelEncoder(),
    "enemy_type":  LabelEncoder(),
    "action":      LabelEncoder(),
}

model_trained = False

class Move:
    def __init__(self, name, power, accuracy, pp, category, mtype, effect=""):
        self.name     = name
        self.power    = power
        self.accuracy = accuracy
        self.max_pp   = pp
        self.pp       = pp
        self.category = category
        self.type     = mtype
        self.effect   = effect

TYPE_CHART = {
    "normal":   {"rock": 0.5, "ghost": 0.0, "steel": 0.5},
    "fire":     {"grass": 2.0, "ice": 2.0, "bug": 2.0, "steel": 2.0,
                 "water": 0.5, "rock": 0.5, "dragon": 0.5},
    "water":    {"fire": 2.0, "ground": 2.0, "rock": 2.0, "grass": 0.5, "dragon": 0.5},
    "electric": {"water": 2.0, "flying": 2.0, "ground": 0.0, "grass": 0.5, "dragon": 0.5},
    "grass":    {"water": 2.0, "ground": 2.0, "rock": 2.0, "fire": 0.5, "poison": 0.5,
                 "flying": 0.5, "bug": 0.5, "dragon": 0.5, "steel": 0.5},
    "ice":      {"grass": 2.0, "ground": 2.0, "flying": 2.0, "dragon": 2.0,
                 "fire": 0.5, "water": 0.5, "steel": 0.5},
    "fighting": {"normal": 2.0, "ice": 2.0, "rock": 2.0, "dark": 2.0, "steel": 2.0,
                 "fairy": 0.5, "ghost": 0.0},
    "poison":   {"grass": 2.0, "fairy": 2.0, "steel": 0.0},
    "ground":   {"fire": 2.0, "electric": 2.0, "poison": 2.0, "rock": 2.0, "steel": 2.0,
                 "flying": 0.0},
    "flying":   {"grass": 2.0, "fighting": 2.0, "bug": 2.0,
                 "electric": 0.5, "rock": 0.5, "steel": 0.5},
    "psychic":  {"fighting": 2.0, "poison": 2.0, "dark": 0.0},
    "bug":      {"grass": 2.0, "psychic": 2.0, "dark": 2.0},
    "rock":     {"fire": 2.0, "ice": 2.0, "flying": 2.0, "bug": 2.0},
    "ghost":    {"psychic": 2.0, "normal": 0.0},
    "dragon":   {"dragon": 2.0, "fairy": 0.0},
    "dark":     {"psychic": 2.0, "ghost": 2.0},
    "steel":    {"ice": 2.0, "rock": 2.0, "fairy": 2.0},
    "fairy":    {"dragon": 2.0, "fighting": 2.0, "dark": 2.0},
}

STATUS_NONE      = None
STATUS_BURN      = "burn"
STATUS_PARALYSIS = "paralysis"

def apply_status(target, status):
    if target.status is not None:
        return f"{target.name} already has a condition!"
    if target.status == STATUS_BURN:
         return f"{target.name} was burned! 🔥"
    if status == STATUS_PARALYSIS:
        return f"{target.name} was paralyzed! ⚡"
    return ""

def process_end_of_turn_status(pokemon):
    if pokemon.fainted:
        return ""
    if pokemon.status == STATUS_BURN:
        dmg = max(1, pokemon.max_hp // 8)
        pokemon.take_damage(dmg)
        return f"{pokemon.name} is hurt by its burn! (-{dmg} HP)"
    return ""

def paralysis_check(pokemon):
    if pokemon.status == STATUS_PARALYSIS:
        if random.random() < 0.25:
            return True
    return False

def burn_atk_modifier(pokemon):
    return 0.5 if pokemon.status == STATUS_BURN else 1.0

def speed_after_status(pokemon):
    spd = pokemon.speed
    if pokemon.status == STATUS_PARALYSIS:
        spd = spd // 2
    return spd

def apply_effect(user, target, move):
    if not move.effect:
        return ""
    if move.effect == "lower_def":
        target.stages["defense"] = max(-6, target.stages["defense"] - 1)
        return f"{target.name}'s DEF fell!"
    if move.effect == "raise_atk":
        user.stages["attack"] = min(6, user.stages["attack"] + 1)
        return f"{user.name}'s ATK rose!"
    if move.effect == "heal":
        heal = int(user.max_hp * 0.25)
        user.hp = min(user.max_hp, user.hp + heal)
        return f"{user.name} healed! (+{heal} HP)"
    if move.effect == "burn":
        return apply_status(target, STATUS_BURN)
    if move.effect == "paralysis":
        return apply_status(target, STATUS_PARALYSIS)

    return ""

def stage_mult(stage):
    return {
        -6: 0.25, -5: 0.28, -4: 0.33,
        -3: 0.40, -2: 0.50, -1: 0.67,
         0: 1.00,
         1: 1.50,  2: 2.00,
         3: 2.50,  4: 3.00,
         5: 3.50,  6: 4.00,
    }[stage]



class Pokemon:
    def __init__(self, name, stats, types, moves):
        self.name   = name
        self.types  = types
        self.moves  = moves

        self.max_hp = stats["hp"]
        self.hp     = stats["hp"]

        self.attack     = stats["attack"]
        self.defense    = stats["defense"]
        self.sp_attack  = stats["special-attack"]
        self.sp_defense = stats["special-defense"]
        self.speed      = stats["speed"]

        self.stages = {
            "attack": 0, "defense": 0,
            "sp_attack": 0, "sp_defense": 0, "speed": 0,
        }

        self.status  = STATUS_NONE
        self.fainted = False

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.hp      = 0
            self.fainted = True

class Trainer:
    def __init__(self, name, team):
        self.name   = name
        self.team   = team
        self.active = 0

    def current(self):
        return self.team[self.active]
    
    def alive(self):
        return any(not p.fainted for p in self.team)
    
    def switch(self, i):
        if i is None:
            return False
        if 0 <= i < len(self.team) and not self.team[i].fainted:
            self.active = i
            return True
        return False
    
def pick_moves_for(poke_name):

    poke_data  = pokemon_dex[poke_name]
    poke_types = poke_data["types"]
    stats      = poke_data["stats"]

    atk   = stats["attack"]
    spatk = stats["special-attack"]

    if atk >= spatk * 1.2:
        preferred = "physical"
    elif spatk >= atk * 1.2:
        preferred = "special"
    else:
        preferred = None

    def sorted_pool(pool):
        if preferred is None:
            shuffled = list(pool)
            random.shuffle(shuffled)
            return shuffled
        
        pref  = [n for n in pool if move_dex[n][3] == preferred]
        other = [n for n in pool if move_dex[n][3] != preferred]
        random.shuffle(pref)
        random.shuffle(other)
        return pref + other
    damaging = {n: d for n, d in move_dex.items() if d[0] > 0}
    status   = {n: d for n, d in move_dex.items() if d[0] == 0}

    stab     = [n for n, d in damaging.items() if d[4] in poke_types]
    coverage = [n for n, d in damaging.items() if d[4] not in poke_types]

    stab     = sorted_pool(stab)
    coverage = sorted_pool(coverage)

    chosen = []
    chosen += stab[:2]

    for m in coverage:
        if m not in chosen:
            chosen.append(m)
            break

    status_pool = [n for n in status if n not in chosen]
    random.shuffle(status_pool)
    if status_pool:
        chosen.append(status_pool[0])
        
    all_moves = [n for n in move_dex if n not in chosen]
    random.shuffle(all_moves)
    while len(chosen) < 4 and all_moves:
        chosen.append(all_moves.pop())
    return chosen[:4]

def create_move(name):
    d = move_dex[name]
    return Move(name, d[0], d[1], d[2], d[3], d[4], d[5])

def create_pokemon(name):
    data       = pokemon_dex[name]
    move_names = pick_moves_for(name)
    moves      = [create_move(m) for m in move_names]
    return Pokemon(name, data["stats"], data["types"], moves)

def random_team():
    names = list(pokemon_dex.keys())
    return [create_pokemon(random.choice(names)) for _ in range(6)]

def type_effect(move_type, defender_types):
    mult = 1.0
    for t in defender_types:
        mult *= TYPE_CHART.get(move_type, {}).get(t, 1.0)
    return mult

def damage(a, d, move):
    if move.power == 0:
        return 0
    if move.category == "physical":
        atk = a.attack  * stage_mult(a.stages["attack"])   * burn_atk_modifier(a)
        df  = d.defense * stage_mult(d.stages["defense"])
    else:
        atk = a.sp_attack  * stage_mult(a.stages["sp_attack"])
        df  = d.sp_defense * stage_mult(d.stages["sp_defense"])
        
    base = (((2 * 50 / 5) + 2) * move.power * atk / df) / 50 + 2
    stab = 1.5 if move.type in a.types else 1.0
    eff  = type_effect(move.type, d.types)
    rnd  = random.uniform(0.85, 1.0)
    return max(1, int(base * stab * eff * rnd))

def train_model():
    global model_trained
    if len(battle_history) < 50:
        return
    df = pd.DataFrame(battle_history)
    action_counts = df["action"].value_counts()
    common_actions = action_counts[action_counts >= 3].index
    df = df[df["action"].isin(common_actions)]
    if len(df) < 50:
        return

    df["player_type"] = encoders["player_type"].fit_transform(df["player_type"])
    df["enemy_type"]  = encoders["enemy_type"].fit_transform(df["enemy_type"])
    df["action"]      = encoders["action"].fit_transform(df["action"])
    X = df.drop("action", axis=1)
    y = df["action"]
    knn.fit(X, y)

    model_trained = True
    
    df = pd.DataFrame(battle_history)
    df["player_type"] = encoders["player_type"].fit_transform(df["player_type"])
    df["enemy_type"]  = encoders["enemy_type"].fit_transform(df["enemy_type"])
    df["action"]      = encoders["action"].fit_transform(df["action"])

    X = df.drop("action", axis=1)
    y = df["action"]
    knn.fit(X, y)
    model_trained = True

def predict_player_action(p1, p2):
    if not model_trained:
        return None
    try:
        player_type = encoders["player_type"].transform([p1.current().types[0]])[0]
        enemy_type  = encoders["enemy_type"].transform([p2.current().types[0]])[0]
    except Exception:
        return None
    
    sample = [[
        p1.current().hp,
        p2.current().hp,
        p1.current().speed,
        p2.current().speed,
        player_type,
        enemy_type
    ]]
    pred = knn.predict(sample)[0]
    return encoders["action"].inverse_transform([pred])[0]
def ai_choose_move(p1,p2):
    prediction = predict_player_action(p1,p2)
    enemy = p2.current()

    if prediction is None:
        return random.choice(enemy.moves)
    
    best_move  = None
    best_score = -999

    for moves in enemy.moves:
        score = max(moves.power, 10)
        score *= type_effect(moves.type, p1.current().types)
        if moves.name == prediction:
            score += 20
        if score > best_score:
            best_score = score
            best_move  = moves

    return best_move

def best_switch(t):
    best, score = None, -999
    for i, p in enumerate(t.team):
        if p.fainted or i == t.active:
            continue
        s = p.hp + p.speed + p.attack
        if s > score:
            best, score = i, s
    return best

def switch_menu(stdscr, t):
    idx     = 0
    options = t.team + ["BACK"]    
    while True:
        stdscr.clear()
        stdscr.addstr(1, 2, "Switch Pokémon:")
        for i, opt in enumerate(options):
            sel = ">" if i == idx else " "
            if opt == "BACK":
                stdscr.addstr(3 + i, 4, f"{sel} BACK")
            else:
                if opt.fainted:
                    status_str = "FAINTED"
                else:
                    status_str = f"{opt.hp} HP"
                    if opt.status:
                        status_str += f" [{opt.status.upper()[:3]}]"
                stdscr.addstr(3 + i, 4, f"{sel} {opt.name} ({status_str})")
        key = stdscr.getch()
        if key == curses.KEY_UP:
            idx = (idx - 1) % len(options)
        elif key == curses.KEY_DOWN:
            idx = (idx + 1) % len(options)
        elif key in (10, 13):
            if options[idx] == "BACK":
                return
            if not options[idx].fainted:
                t.switch(idx)
                return
        elif key == 27:
            return
def faint_switch_menu(stdscr, t):
    idx = 0
    living = [i for i, p in enumerate(t.team) if not p.fainted]

    while True:
        stdscr.clear()
        stdscr.addstr(1, 2, f"{t.current().name} fainted! Choose your next Pokemon:")

        for row, i in enumerate(living):
            p   = t.team[i]
            sel = ">" if row == idx else " "
            status_str = f"{p.hp} HP"
            if p.status:
                status_str += f" [{p.status.upper()[:3]}]"
            stdscr.addstr(3 + row, 4, f"{sel} {p.name} ({status_str})")

        key = stdscr.getch()

        if key == curses.KEY_UP:
            idx = (idx - 1) % len(living)
        elif key == curses.KEY_DOWN:
            idx = (idx + 1) % len(living)
        elif key in (10, 13):
            t.switch(living[idx])
            return
def move_menu(stdscr, t):
    idx     = 0
    options = t.current().moves + ["BACK"]

    while True:
        stdscr.clear()
        stdscr.addstr(1, 2, "Choose Move:")

        for i, opt in enumerate(options):
            sel = ">" if i == idx else " "
            if opt == "BACK":
                stdscr.addstr(3 + i, 4, f"{sel} BACK")
            else:
                pp_str   = f"PP {opt.pp}/{opt.max_pp}"
                type_str = f"[{opt.type}]"
                eff_str  = f"{opt.effect}" if opt.effect else ""
                stdscr.addstr(3 + i, 4,
                    f"{sel} {opt.name} {type_str} {pp_str} {eff_str}")

        key = stdscr.getch()

        if key == curses.KEY_UP:
            idx = (idx - 1) % len(options)
        elif key == curses.KEY_DOWN:
            idx = (idx + 1) % len(options)
        elif key in (10, 13):
            if options[idx] == "BACK":
                return None
            return options[idx]
        elif key == 27:
            return None

def hp_bar(p, w=20):
    if p.max_hp == 0:
        return ""
    r = p.hp / p.max_hp
    return "🟩" * int(r * w) + "🟥" * (w - int(r * w))

STATUS_ICONS = {
    STATUS_BURN:      "🔥BRN",
    STATUS_PARALYSIS: "⚡PAR",
}

def draw(stdscr, p1, p2, msg):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    def safe(y, x, text):
        if 0 <= y < h and 0 <= x < w:
            stdscr.addstr(y, x, text[:max(0, w - x - 1)])

    e = p2.current()
    p = p1.current()
    e_status = STATUS_ICONS.get(e.status, "")
    p_status = STATUS_ICONS.get(p.status, "")
    safe(1, 2, f"ENEMY: {e.name} [{'/'.join(e.types)}] {e_status}")
    safe(2, 2, hp_bar(e) + f"  {e.hp}/{e.max_hp}")
    safe(4, 2,  "MOVES:")
    safe(4, 40, "LOG:")
    for i, m in enumerate(p.moves):
        type_str = f"[{m.type}]"
        pp_str   = f"PP {m.pp}/{m.max_pp}"
        eff_str  = f" ({m.effect})" if m.effect else ""
        safe(5 + i, 4, f"{i+1}. {m.name} {type_str} {pp_str}{eff_str}")

    for i, line in enumerate(msg.split("|")):
        safe(5 + i, 40, line.strip())
    safe(h - 5, 2, f"YOU:   {p.name} [{'/'.join(p.types)}] {p_status}")
    safe(h - 4, 2, hp_bar(p) + f"  {p.hp}/{p.max_hp}")
    safe(h - 2, 2, "m=move | s=switch")
    stdscr.refresh()
    #heavily searched for what to put in these loops

TYPE_MOVES = {}

def build_type_pools():
    global TYPE_MOVES
    TYPE_MOVES = {}
    for name, data in move_dex.items():
        TYPE_MOVES.setdefault(data[4], []).append(name)

def resolve_turn(attacker, att_move, defender):
    att_move.pp = max(0, att_move.pp - 1)   # add this
    dmg = damage(attacker.current(), defender.current(), att_move)
    defender.current().take_damage(dmg)
    eff = apply_effect(attacker.current(), defender.current(), att_move)
    return dmg, eff

def battle(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    p1  = Trainer("Player", random_team())
    p2  = Trainer("AI",     random_team())
    msg = ""

    while p1.alive() and p2.alive():

        draw(stdscr, p1, p2, msg)
        key = stdscr.getch()
        if key == ord("s"):
            switch_menu(stdscr, p1)

            enemy_move = random.choice(p2.current().moves)
            dmg = damage(p2.current(), p1.current(), enemy_move)
            p1.current().take_damage(dmg)

            eot1 = process_end_of_turn_status(p1.current())
            eot2 = process_end_of_turn_status(p2.current())

            msg = f"Enemy used {enemy_move.name} (-{dmg} HP) | {eot1} {eot2}".strip()
            continue
        if key == ord("m"):

            move = move_menu(stdscr, p1)
            if move is None:
                continue

            enemy_move = ai_choose_move(p1, p2)

            p1_speed = speed_after_status(p1.current())
            p2_speed = speed_after_status(p2.current())
            first, second = (p1, p2) if p1_speed >= p2_speed else (p2, p1)
            fm = move if first is p1 else enemy_move
            sm = enemy_move if first is p1 else move
            #Copied this in then modified

            lines        = []
            turn_over    = False
                      
            if paralysis_check(first.current()):
                lines.append(f"{first.current().name} is fully paralyzed!")
            else:
                dmg, eff = resolve_turn(first, fm, second)
                lines.append(f"{first.current().name} used {fm.name} (-{dmg} HP) {eff}".strip())

                if second.current().fainted:
                    lines.append(f"{second.current().name} fainted!")
                    msg = " | ".join(l for l in lines if l)

                    if not second.alive():
                        draw(stdscr, p1, p2, msg)
                        break

                    if second is p1:
                        faint_switch_menu(stdscr, p1)
                    else:
                        swap_to = best_switch(second)
                        second.switch(swap_to)

                    lines.append(f"{second.name} sent out {second.current().name}!")
                    msg = " | ".join(l for l in lines if l)
                    draw(stdscr, p1, p2, msg)  
                    turn_over = True    

            if not turn_over and not second.current().fainted:
                if paralysis_check(second.current()):
                    lines.append(f"{second.current().name} is fully paralyzed!")
                else:
                    dmg, eff = resolve_turn(second, sm, first)
                    lines.append(f"{second.current().name} used {sm.name} (-{dmg} HP) {eff}".strip())
                    if first.current().fainted:
                        lines.append(f"{first.current().name} fainted!")
                        msg = " | ".join(l for l in lines if l)

                        if not first.alive():
                            draw(stdscr, p1, p2, msg)
                            break

                        if first is p1:
                            faint_switch_menu(stdscr, p1)
                        else:
                            swap_to = best_switch(first)
                            first.switch(swap_to)
                        lines.append(f"{first.name} sent out {first.current().name}!")
                        msg = " | ".join(l for l in lines if l)
                        draw(stdscr, p1, p2, msg)
                        turn_over = True
            if not turn_over:
                for trainer in (p1, p2):
                    eot = process_end_of_turn_status(trainer.current())
                    if eot:
                        lines.append(eot)
            msg = " | ".join(l for l in lines if l)

            battle_history.append({
                "player_hp":    p1.current().hp,
                "enemy_hp":     p2.current().hp,
                "player_speed": p1.current().speed,
                "enemy_speed":  p2.current().speed,
                "player_type":  p1.current().types[0],
                "enemy_type":   p2.current().types[0],
                "action":       move.name,
            })
    train_model()
    pd.DataFrame(battle_history).to_csv("battle_history.csv", index=False)

    winner = "Player" if p1.alive() else "AI"
    draw(stdscr, p1, p2, f"*** {winner} wins! Press any key. ***")
    stdscr.getch()

if __name__ == "__main__":

    if os.path.exists("battle_history.csv"):
        df = pd.read_csv("battle_history.csv")
        battle_history = df.to_dict("records")
        #modified from google search code
        if len(battle_history) >= 10:
            train_model()

    build_type_pools()

    curses.wrapper(battle)