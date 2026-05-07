import curses
import random
import os
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder

from pokemon import build_pokemon_list
from moves import build_move_list

RESET = "\033[0m"

TYPE_COLORS = {
    "normal": "\033[97m",
    "fire": "\033[38;5;196m",
    "water": "\033[34m",
    "electric": "\033[1;33m",
    "grass": "\033[32m",
    "ice": "\033[96m",
    "fighting": "\033[2;31m",
    "poison": "\033[38;5;129m",
    "ground": "\033[33m",
    "flying": "\033[94m",
    "psychic": "\033[38;2;160;0;200m",
    "bug": "\033[38;5;190m",
    "rock": "\033[38;5;52m",
    "ghost": "\033[38;2;128;0;128m" ,
    "dragon": "\033[2;34m",
    "dark": "\033[2;30m",
    "steel": "\033[38;5;250m",
    "fairy": "\033[1;95m",
}
def color_text(text, type_name):
    return f"{TYPE_COLORS[type_name]}{text}{RESET}"

type_chart = {
    "normal": {
        "rock": 0.5, "ghost": 0.0, "steel": 0.5
    },
    "fire": {
        "grass": 2.0, "ice": 2.0, "bug": 2.0, "steel": 2.0,
        "fire": 0.5, "water": 0.5, "rock": 0.5, "dragon": 0.5
    },
    "water": {
        "fire": 2.0, "ground": 2.0, "rock": 2.0,
        "water": 0.5, "grass": 0.5, "dragon": 0.5
    },
    "electric": {
        "water": 2.0, "flying": 2.0,
        "electric": 0.5, "grass": 0.5, "dragon": 0.5,
        "ground": 0.0
    },
    "grass": {
        "water": 2.0, "ground": 2.0, "rock": 2.0,
        "fire": 0.5, "grass": 0.5, "poison": 0.5,
        "flying": 0.5, "bug": 0.5, "dragon": 0.5, "steel": 0.5
    },
    "ice": {
        "grass": 2.0, "ground": 2.0, "flying": 2.0, "dragon": 2.0,
        "fire": 0.5, "water": 0.5, "ice": 0.5, "steel": 0.5
    },
    "fighting": {
        "normal": 2.0, "ice": 2.0, "rock": 2.0, "dark": 2.0, "steel": 2.0,
        "poison": 0.5, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "fairy": 0.5,
        "ghost": 0.0
    },
    "poison": {
        "grass": 2.0, "fairy": 2.0,
        "poison": 0.5, "ground": 0.5, "rock": 0.5, "ghost": 0.5,
        "steel": 0.0
    },
    "ground": {
        "fire": 2.0, "electric": 2.0, "poison": 2.0, "rock": 2.0, "steel": 2.0,
        "grass": 0.5, "bug": 0.5,
        "flying": 0.0
    },
    "flying": {
        "grass": 2.0, "fighting": 2.0, "bug": 2.0,
        "electric": 0.5, "rock": 0.5, "steel": 0.5
    },
    "psychic": {
        "fighting": 2.0, "poison": 2.0,
        "psychic": 0.5, "steel": 0.5,
        "dark": 0.0
    },
    "bug": {
        "grass": 2.0, "psychic": 2.0, "dark": 2.0,
        "fire": 0.5, "fighting": 0.5, "poison": 0.5,
        "flying": 0.5, "ghost": 0.5, "steel": 0.5, "fairy": 0.5
    },
    "rock": {
        "fire": 2.0, "ice": 2.0, "flying": 2.0, "bug": 2.0,
        "fighting": 0.5, "ground": 0.5, "steel": 0.5
    },
    "ghost": {
        "ghost": 2.0, "psychic": 2.0,
        "dark": 0.5,
        "normal": 0.0
    },
    "dragon": {
        "dragon": 2.0,
        "steel": 0.5,
        "fairy": 0.0
    },
    "dark": {
        "psychic": 2.0, "ghost": 2.0,
        "fighting": 0.5, "dark": 0.5, "fairy": 0.5
    },
    "steel": {
        "ice": 2.0, "rock": 2.0, "fairy": 2.0,
        "fire": 0.5, "water": 0.5, "electric": 0.5, "steel": 0.5
    },
    "fairy": {
        "fighting": 2.0, "dragon": 2.0, "dark": 2.0,
        "fire": 0.5, "poison": 0.5, "steel": 0.5
    }
}

move_list = build_move_list()

def type_effectiveness(attack_type, target_types):
    multiplier = 1.0
    
    for t in target_types:
        multiplier *= type_chart.get(attack_type, {}).get(t, 1.0)
    
    return multiplier

STAGE_MULTIPLIERS = {
    -6: 2/8,
    -5: 2/7,
    -4: 2/6,
    -3: 2/5,
    -2: 2/4,
    -1: 2/3,
     0: 2/2,
     1: 3/2,
     2: 4/2,
     3: 5/2,
     4: 6/2,
     5: 7/2,
     6: 8/2,
}

class Move:
    def __init__(self, name, m_type, power, accuracy, pp, category, effect=None):
        self.name = name
        self.type = m_type
        self.power = power
        self.accuracy = accuracy
        self.pp = pp
        self.category = category
        self.effect = effect
   
class Pokemon:
    def __init__(self, name, hp, attack, defense, sp_attack, sp_defense, speed, types, moves):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sp_attack = sp_attack
        self.sp_defense = sp_defense
        self.speed = speed
        self.types = types
        self.moves = moves
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

        