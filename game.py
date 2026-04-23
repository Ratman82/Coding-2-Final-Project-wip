import curses
import pandas as pd

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
    "fire":["grass","bug","ice","steel"],
    "water":["ground","rock","fire",],
    "grass":["ground","rock","water"],
    "electric":["flying","water"],
    "poison":["grass","fairy"],
    "fairy":["dark","dragon","fighting"],
    "dark":["psychic","ghost"],
    "steel":["fairy","ice","rock"],
    "bug":["grass","psychic","dark"],
    "ice":["grass","ground","flying","dragon"],
    "dragon":["dragon"],
    "rock":["flying","fire","bug"],
    "ground":["fire","steel","rock","poison","electric"],
    "psychic":["poison","fighting"],
    "ghost":["ghost","psychic"],
    "flying":["fighting","bug","grass"],
    "fighting":["normal","fighting","rock","steel","ice","dark"],
    "normal":[]
} 
def type_effectiveness(attack_type,target_type):
    if target_type in type_chart.get(attack_type, []):
        return 2.0
    elif attack_type in type_chart.get(target_type, []):
        return 0.5
    else:
        return 1.0
class Move:
    def __init__(self, name, m_type, power, is_special=False):
        self.name = name
        self.type = m_type
        self.power = power
        self.is_special = is_special
   
class Pokemon:
    def __init__(self, name, types, hp, attack, defense, sp_attack, sp_defense, speed, moves):
        self.name=name
        self.types=types if isinstance(types, list) else [types]
        self.hp=hp
        self.attack=attack
        self.defense=defense
        self.sp_attack=sp_attack
        self.sp_defense=sp_defense
        self.speed=speed
        self.moves=moves
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

        