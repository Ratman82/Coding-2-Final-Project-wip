import requests

pokemon_list = """
Drifblim
Tsareena
Crawdaunt
Arboliva
Tyrantrum
Toucannon
Walrein
Eelektross
Copperajah
Magnezone
Braviary
Avalugg
Yanmega
Dhelmise
Ribombee
Escavalier
Bronzong
Mandibuzz
Toxicroak
Gothitelle
Cherrim
Mudsdale
Bewear
Garganacl
Lurantis
Carracosta
Vanilluxe
Tinkaton
Accelgor
Heliolisk
Dudunsparce
Vikavolt
Brambleghast
Shiftry
Wyrdeer
Cacturne
Porygon-Z
Falinks
Crabominable
Reuniclus
Bellibolt
Kommo-o
Palossand
Chesnaught
Jellicent
Obstagoon
Coalossal
Glimmora
Bombirdier
Hatterene
Cetitan
Revavroom
Maushold
Farigiraf
Clodsire
Kilowattrel
Toedscruel
Veluza
Rabsca
Orthworm
Grafaiai
Flamigo
Dondozo
Baxcalibur
Kingambit
Annihilape
Ceruledge
Armarouge
Iron Hands
Iron Bundle
Iron Thorns
Iron Valiant
Roaring Moon
Slither Wing
Sandy Shocks
Flutter Mane
Glaceon
Leafeon
Noivern
Krookodile
Chandelure
Haxorus
Volcarona
Frosmoth
Dragalge
Malamar
Barbaracle
Aurorus
Goodra
Decidueye
Primarina
Incineroar
Corviknight
Grimmsnarl
Cinderace
Rillaboom
Inteleon
Skeledirge
Meowscarada
Quaquava

""".strip().splitlines()


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