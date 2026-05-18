import requests

moves = """
Absorb
Accelerock
Acid
Acid Armor
Acid Spray
Acrobatics
Acupressure
Aerial Ace
Aeroblast
After You
Agility
Air Cutter
Air Slash
Ally Switch
Amnesia
Anchor Shot
Ancient Power
Apple Acid
Aqua Cutter
Aqua Jet
Aqua Ring
Aqua Step
Aqua Tail
Arm Thrust
Armor Cannon
Aromatherapy
Aromatic Mist
Assist
Assurance
Astonish
Astral Barrage
Attack Order
Attract
Aura Sphere
Aura Wheel
Aurora Beam
Aurora Veil
Autotomize
Avalanche
Axe Kick
Baby-Doll Eyes
Baneful Bunker
Baton Pass
Beak Blast
Beat Up
Behemoth Bash
Behemoth Blade
Belly Drum
Bestow
Bide
Bind
Bite
Bitter Blade
Bitter Malice
Blast Burn
Blaze Kick
Blizzard
Block
Blue Flare
Body Press
Body Slam
Bolt Beak
Bone Club
Bone Rush
Bonemerang
Boomburst
Bounce
Branch Poke
Brave Bird
Breaking Swipe
Brick Break
Brine
Brutal Swing
Bubble
Bubble Beam
Bug Bite
Bug Buzz
Bulk Up
Bulldoze
Bullet Punch
Bullet Seed
Burning Jealousy
Burn Up
Calm Mind
Camouflage
Captivate
Ceaseless Edge
Celebrate
Charge
Charge Beam
Charm
Chatter
Chilling Water
Chloroblast
Circle Throw
Clamp
Clanging Scales
Clangorous Soul
Clear Smog
Close Combat
Coil
Collision Course
Combat Torque
Comet Punch
Confide
Confuse Ray
Confusion
Constrict
Conversion
Conversion 2
Copycat
Core Enforcer
Cosmic Power
Cotton Guard
Cotton Spore
Counter
Court Change
Covet
Crabhammer
Crafty Shield
Cross Chop
Cross Poison
Crunch
Crush Claw
Crush Grip
Curse
Cut
Dark Pulse
Dark Void
Darkest Lariat
Dazzling Gleam
Decorate
Defend Order
Defense Curl
Defog
Destiny Bond
Detect
Diamond Storm
Dig
Dire Claw
Disable
Disarming Voice
Discharge
Dive
Dizzy Punch
Doom Desire
Double Hit
Double Iron Bash
Double Kick
Double Slap
Double Team
Double-Edge
Draco Meteor
Dragon Ascent
Dragon Breath
Dragon Cheer
Dragon Claw
Dragon Dance
Dragon Darts
Dragon Energy
Dragon Hammer
Dragon Pulse
Dragon Rage
Dragon Rush
Dragon Tail
Drain Punch
Draining Kiss
Dream Eater
Drill Peck
Drill Run
Dual Chop
Dual Wingbeat
Dynamax Cannon
Dynamic Punch
Earth Power
Earthquake
Echoed Voice
Eerie Impulse
Eerie Spell
Egg Bomb
Electric Terrain
Electro Ball
Electro Drift
Electroweb
Embargo
Ember
Encore
Endeavor
Endure
Energy Ball
Entrainment
Eruption
Esper Wing
Eternabeam
Expanding Force
Explosion
Extrasensory
Extreme Speed
Facade
Fairy Lock
Fairy Wind
Fake Out
Fake Tears
False Surrender
False Swipe
Feather Dance
Feint
Fiery Dance
Fiery Wrath
Final Gambit
Fire Blast
Fire Fang
Fire Lash
Fire Punch
Fire Spin
First Impression
Fishious Rend
Fissure
Flame Burst
Flame Charge
Flame Wheel
Flamethrower
Flare Blitz
Flash
Flash Cannon
Fleur Cannon
Flip Turn
Floral Healing
Flower Shield
Flower Trick
Fly
Flying Press
Focus Blast
Focus Energy
Focus Punch
Follow Me
Force Palm
Foresight
Forest’s Curse
Foul Play
Freeze-Dry
Freeze Shock
Freezing Glare
Frenzy Plant
Frost Breath
Frustration
Fury Attack
Fury Cutter
Fury Swipes
Fusion Bolt
Fusion Flare
Future Sight
Gastro Acid
Gear Grind
Gear Up
Geomancy
Giga Drain
Giga Impact
Gigaton Hammer
Glacial Lance
Glaciate
Glaive Rush
Glare
Grass Knot
Grassy Glide
Grassy Terrain
Grav Apple
Gravity
Growl
Growth
Grudge
Guard Split
Guard Swap
Guillotine
Gunk Shot
Gust
Gyro Ball
Hail
Hammer Arm
Happy Hour
Harden
Haze
Head Charge
Head Smash
Headbutt
Headlong Rush
Heal Bell
Heal Block
Heal Order
Heal Pulse
Healing Wish
Heart Stamp
Heart Swap
Heat Crash
Heat Wave
Heavy Slam
Helping Hand
Hex
Hidden Power
High Horsepower
High Jump Kick
Hold Back
Hold Hands
Hone Claws
Horn Attack
Horn Drill
Horn Leech
Howl
Hurricane
Hydro Cannon
Hydro Pump
Hydro Steam
Hyper Beam
Hyper Drill
Hyper Fang
Hyper Voice
Hyperspace Fury
Hyperspace Hole
Hypnosis
Ice Ball
Ice Beam
Ice Burn
Ice Fang
Ice Hammer
Ice Punch
Ice Shard
Ice Spinner
Icicle Crash
Icicle Spear
Icy Wind
Imprison
Incinerate
Infernal Parade
Inferno
Infestation
Ingrain
Instruct
Ion Deluge
Iron Defense
Iron Head
Iron Tail
Ivy Cudgel
Jaw Lock
Jet Punch
Judgment
Jump Kick
Jungle Healing
Karate Chop
Kinesis
King’s Shield
Knock Off
Kowtow Cleave
Lava Plume
Leaf Blade
Leaf Storm
Leaf Tornado
Leafage
Leech Life
Leech Seed
Leer
Lick
Life Dew
Light of Ruin
Light Screen
Liquidation
Lock-On
Lovely Kiss
Low Kick
Low Sweep
Lucky Chant
Lunar Blessing
Lunar Dance
Lunge
Luster Purge
Mach Punch
Magic Coat
Magic Powder
Magic Room
Magical Leaf
Magma Storm
Magnet Bomb
Magnet Rise
Magnetic Flux
Magnitude
Make It Rain
Mat Block
Matcha Gotcha
Mean Look
Meditate
Mega Drain
Mega Kick
Mega Punch
Megahorn
Memento
Metal Burst
Metal Claw
Metal Sound
Meteor Assault
Meteor Beam
Meteor Mash
Metronome
Milk Drink
Mimic
Mind Blown
Mind Reader
Minimize
Miracle Eye
Mirror Coat
Mirror Move
Mirror Shot
Mist
Mist Ball
Misty Explosion
Misty Terrain
Moonblast
Moongeist Beam
Moonlight
Morning Sun
Mortal Spin
Mud Bomb
Mud Shot
Mud Sport
Mud-Slap
Muddy Water
Multi-Attack
Mystical Fire
Nasty Plot
Natural Gift
Nature Power
Nature’s Madness
Needle Arm
Night Daze
Night Shade
Night Slash
Nightmare
No Retreat
Noble Roar
Noxious Torque
Nuzzle
Oblivion Wing
Obstruct
Octazooka
Octolock
Ominous Wind
Order Up
Origin Pulse
Outrage
Overdrive
Overheat
Pain Split
Parabolic Charge
Parting Shot
Pay Day
Payback
Peck
Perish Song
Petal Blizzard
Petal Dance
Phantom Force
Photon Geyser
Pin Missile
Plasma Fists
Play Nice
Play Rough
Pluck
Poison Fang
Poison Gas
Poison Jab
Poison Powder
Poison Sting
Poison Tail
Pollen Puff
Poltergeist
Population Bomb
Pounce
Pound
Powder
Powder Snow
Power Gem
Power Split
Power Swap
Power Trip
Power-Up Punch
Precipice Blades
Present
Prismatic Laser
Protect
Psybeam
Psychic
Psychic Fangs
Psychic Noise
Psychic Terrain
Psycho Boost
Psycho Cut
Psycho Shift
Psyshield Bash
Psyshock
Psystrike
Psywave
Punishment
""".strip().splitlines()
#copied this from AI list of moves given

# Map PokeAPI effect IDs to your internal effect keys
EFFECT_ID_MAP = {
    5:   "burn",   # May burn
    126: "burn",   # Always burns
    6:   "paralysis",  # May paralyze
    68:  "paralysis",  # Always paralyzes
    19:  "lower_def",   # Lowers target's Defense
    11:  "raise_atk",   # Raises user's Attack
    33:  "heal",    # Restores 1/2 HP
    85:  "heal",    # Restores 1/4 HP
}

def get_move_data(move):
    slug = move.strip().lower().replace(" ", "-")
    url  = f"https://pokeapi.co/api/v2/move/{slug}"
    response = requests.get(url)

    if response.status_code != 200:
        return move, None

    data = response.json()

    power    = data["power"]    or 0
    accuracy = data["accuracy"] or 0
    pp       = data["pp"]
    category = data["damage_class"]["name"]
    move_type = data["type"]["name"]

    effect = ""
    effect_id = data.get("effect_entries")

    meta    = data.get("meta") or {}
    ailment = (meta.get("ailment") or {}).get("name", "none")
    stat_changes = data.get("stat_changes", [])
    healing = meta.get("healing", 0)

    if ailment == "burn":
        effect = "burn"
    elif ailment in ("paralysis", "para"):
        effect = "paralysis"
    elif healing and healing > 0:
        effect = "heal"
    elif stat_changes:
        for sc in stat_changes:
            stat  = sc["stat"]["name"]
            change = sc["change"]
            if stat == "defense" and change < 0:
                effect = "lower_def"
                break
            if stat == "attack" and change > 0:
                effect = "raise_atk"
                break

    name = move.strip()
    return name, [power, accuracy, pp, category, move_type, effect]


def build_move_list():
    move_list = {}
    for move in moves:
        name, data = get_move_data(move)
        if data:
            move_list[name] = data
    return move_list