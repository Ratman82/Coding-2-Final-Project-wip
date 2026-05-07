import requests

moves = """
pin-missile
u-turn
x-scissor
sucker-punch
night-slash
knock-off
dragon-claw
scale-shot
draco-meteor
thunder-punch
thunder-wave
thunderbolt
play-rough
moonblast
fairy-wind
drain-punch
focus-blast
close-combat
flamethrower
flame-charge
fire-punch
air-slash
acrobatics
hurricane
shadow-ball
shadow-punch
shadow-sneak
horn-leech
mega-drain
razor-leaf
earth-power
earthquake
drill-run
blizzard
ice-punch
ice-beam
boomburst
shell-smash
swords-dance
yawn
poison-fang
sludge-wave
toxic
psychic
psybeam
psychic-fangs
rock-blast
ancient-power
stone-edge
bullet-punch
will-o-wisp
aqua-jet
recover
dragon-dance
calm-mind
nasty-plot
bulk-up
stealth-rock
spikes
toxic-spikes
rapid-spin
defog
substitute
surf
dark-pulse
energy-ball
flash-cannon
encore
iron-tail
iron-head
flip-turn
hydro-pump
scald
""".strip().splitlines()

def get_move_data(move):
    move = move.strip().lower().replace(" ", "-")

    url = f"https://pokeapi.co/api/v2/move/{move}"
    response = requests.get(url)

    if response.status_code != 200:
        return move, None

    data = response.json()

    power = data["power"] or 0
    accuracy = data["accuracy"] or 0
    pp = data["pp"]
    category = data["damage_class"]["name"]
    move_type = data["type"]["name"]

    effect = next(
        (e["short_effect"] for e in data["effect_entries"] if e["language"]["name"] == "en"),
        "No additional effects"
    )

    name = move.replace("-", " ")
    return name, [power, accuracy, pp, category, move_type, effect]


def build_move_list():
    move_list = {}

    for move in moves:
        name, data = get_move_data(move)
        if data:
            move_list[name] = data

    return move_list