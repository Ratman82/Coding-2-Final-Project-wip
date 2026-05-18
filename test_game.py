import pytest
import random
from game import (
    type_effect,
    damage,
    Pokemon,
    Move,
    STATUS_BURN,
    STATUS_PARALYSIS,
    apply_status,
    paralysis_check,
    speed_after_status,
)

def make_pokemon(name, ptype):

    stats = {
        "hp": 100,
        "attack": 100,
        "defense": 100,
        "special-attack": 100,
        "special-defense": 100,
        "speed": 100,
    }

    return Pokemon(
        name=name,
        stats=stats,
        types=[ptype],
        moves=[]
    )
#asked google what needed to be returned

def test_type_effect():

    assert type_effect("fire", ["grass"]) == 2.0
    assert type_effect("water", ["fire"]) == 2.0
    assert type_effect("electric", ["ground"]) == 0.0
    assert type_effect("grass", ["fire"]) == 0.5
    assert type_effect("ghost", ["normal"]) == 0.0

def test_damage():

    attacker = make_pokemon("Charizard", "fire")
    defender = make_pokemon("Venusaur", "grass")

    move = Move(
        name="Flamethrower",
        power=90,
        accuracy=100,
        pp=15,
        category="special",
        mtype="fire"
    )

    dmg = damage(attacker, defender, move)

    assert dmg > 0
    assert isinstance(dmg, int)

def test_zero_damage():

    attacker = make_pokemon("Pikachu", "electric")
    defender = make_pokemon("Squirtle", "water")

    move = Move(
        name="Growl",
        power=0,
        accuracy=100,
        pp=40,
        category="status",
        mtype="normal"
    )
#asked google how I could test 0 dmg moves
    assert damage(attacker, defender, move) == 0

def test_take_damage():

    pokemon = make_pokemon("Blastoise", "water")

    pokemon.take_damage(30)

    assert pokemon.hp == 70
    assert pokemon.fainted is False


def test_fainted():

    pokemon = make_pokemon("Gengar", "ghost")
    pokemon.take_damage(150)

    assert pokemon.hp == 0
    assert pokemon.fainted is True

def test_speed_after_paralysis():

    pokemon = make_pokemon("Alakazam", "psychic")
    pokemon.status = STATUS_PARALYSIS
    assert speed_after_status(pokemon) == 50


def test_speed_normal():

    pokemon = make_pokemon("Jolteon", "electric")
    assert speed_after_status(pokemon) == 100

def test_apply_burn():
    pokemon = make_pokemon("Snorlax", "normal")
    result = apply_status(pokemon, STATUS_BURN)

    assert pokemon.status == STATUS_BURN
    assert "burned" in result.lower()


def test_apply_paralysis():

    pokemon = make_pokemon("Dragonite", "dragon")
    result = apply_status(pokemon, STATUS_PARALYSIS)

    assert pokemon.status == STATUS_PARALYSIS
    assert "paralyzed" in result.lower()


def test_cannot_apply_second_status():

    pokemon = make_pokemon("Machamp", "fighting")
    apply_status(pokemon, STATUS_BURN)
    result = apply_status(pokemon, STATUS_PARALYSIS)

    assert result == f"{pokemon.name} already has a condition!"

def test_paralysis_check_returns_boolean():

    pokemon = make_pokemon("Raichu", "electric")
    pokemon.status = STATUS_PARALYSIS
    result = paralysis_check(pokemon)

    assert result in [True, False]

