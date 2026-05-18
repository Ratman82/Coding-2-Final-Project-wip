import requests

pokemon_list = """
Garchomp
Blastoise
Corviknight
Tyranitar
Dragapult
Lucario
Volcarona
Toxapex
Metagross
Meowscarada
Salamence
Excadrill
Togekiss
Rotom-Wash
Ferrothorn
Dragonite
Kingambit
Skeledirge
Greninja
Scizor
Hydreigon
Gholdengo
Azumarill
Baxcalibur
Clefable
Infernape
Great Tusk
Annihilape
Blaziken
Hatterene
Mimikyu
Gliscor
Ting-Lu
Iron Valiant
Swampert
Umbreon
Weavile
Kommo-o
Ceruledge
Goodra
Talonflame
Milotic
Snorlax
Gallade
Breloom
Pelipper
Hippowdon
Clodsire
Alakazam
Sylveon
Noivern
Conkeldurr
Krookodile
Chandelure
Magnezone
Slowking
Dondozo
Primarina
Arcanine
Aegislash
Porygon-Z
Mamoswine
Bronzong
Reuniclus
Skarmory
Gyarados
Amoonguss
Staraptor
Tinkaton
Roserade
Bisharp
Haxorus
Empoleon
Sableye
Gastrodon
Ribombee
Mandibuzz
Grimmsnarl
Electivire
Scrafty
Feraligatr
Nidoking
Quaquaval
Espathra
Jolteon
Tyrantrum
Donphan
Luxray
Bellibolt
Cinderace
Decidueye
Obstagoon
Venusaur
Zoroark
Toxtricity
Avalugg
Gardevoir
Darmanitan
Slaking
Flygon
Steelix
Cetitan
Heracross
Maushold
Dudunsparce
Rillaboom
Coalossal
Pawmot
Ursaluna
Wyrdeer
Samurott
Overqwil
Kleavor
Basculegion
Lilligant
Arboliva
Toedscruel
Farigiraf
Revavroom
Orthworm
Bombirdier
Veluza
Brambleghast
Lokix
Rabsca
Flamigo
Kilowattrel
Mabosstiff
Grafaiai
Dachsbun
Garganacl
Armarouge
Braviary
Electrode
Tentacruel
Cloyster
Machamp
Vaporeon
Espeon
Leafeon
Glaceon
Flareon
Raichu
Ninetales
Sandslash
Victreebel
Exeggutor
Starmie
Lapras
Omastar
Kabutops
Aerodactyl
Meganium
Typhlosion
Crobat
Ampharos
Bellossom
Politoed
Quagsire
Forretress
Granbull
Houndoom
Kingdra
Hitmontop
Blissey
Sceptile
Ludicolo
Shiftry
Hariyama
Aggron
Altaria
Zangoose
Banette
Absol
Walrein
Torterra
Rampardos
Bastiodon
Vespiquen
Floatzel
Drifblim
Lopunny
Honchkrow
Skuntank
Spiritomb
Toxicroak
Abomasnow
Yanmega
Probopass
Dusknoir
Froslass
Stoutland
Gigalith
Seismitoad
Scolipede
Whimsicott
Crustle
Sigilyph
Carracosta
Archeops
Garbodor
Cinccino
Gothitelle
Jellicent
Galvantula
Eelektross
Beheeyem
Beartic
Mienshao
Golurk
Bouffalant
Durant
Chesnaught
Delphox
Pyroar
Florges
Pangoro
Barbaracle
Dragalge
Clawitzer
Hawlucha
Dedenne
Carbink
Trevenant
Gourgeist
Noivern
Incineroar
Vikavolt
Tsareena
Golisopod
Palossand
Turtonator
Dracovish
Appletun
Sandaconda
Copperajah
Frosmoth
Indeedee
Morpeko
Falinks
Eiscue
Arctozolt
Iron Hands
Iron Bundle
Iron Moth
Iron Thorns
Iron Treads
Roaring Moon
Flutter Mane
Slither Wing
Sandy Shocks
Brute Bonnet
Walking Wake
Raging Bolt
Gouging Fire
Iron Crown
Iron Boulder
Archaludon
Hydrapple
Ogerpon
Bloodmoon Ursaluna
Pecharunt
Tauros
Muk
Weezing
Slowbro
Persian
Dugtrio
Dodrio
Seaking
Jynx
Pinsir
Tauros-Paldea
Xatu
Azumarill
Sudowoodo
Jumpluff
Sunflora
Steelix
Mantine
Donphan
Smeargle
Mightyena
Swellow
Exploud
Medicham
Manectric
Sharpedo
Camerupt
Seviper
Glalie
Bibarel
Pachirisu
Purugly
Lumineon
Watchog
Leavanny
Amoonguss
Accelgor
Heatmor
""".strip().splitlines()
# Copied this list of pokemon from AI list aswell

def get_pokemon_data(pokemon):
    pokemon = pokemon.strip().lower()

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    response = requests.get(url)

    if response.status_code != 200:
        return pokemon, None

    data = response.json()

    name = data["name"]
    id_ = data["id"]
    height = data["height"]
    weight = data["weight"]
    base_experience = data["base_experience"]

    types = [t["type"]["name"] for t in data["types"]]
    abilities = [a["ability"]["name"] for a in data["abilities"]]

    stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}

    return name, {
        "id": id_,
        "height": height,
        "weight": weight,
        "base_experience": base_experience,
        "types": types,
        "abilities": abilities,
        "stats": stats
    }


def build_pokemon_list():
    result = {}

    for pokemon in pokemon_list:
        name, data = get_pokemon_data(pokemon)
        if data:
            result[name] = data

    return result