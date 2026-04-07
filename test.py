import curses

RESET = "\033[0m"

TYPE_COLORS = {
    "normal": "\033[37m",  
    "fire": "\033[31m",    
    "water": "\033[34m",   
    "electric": "\033[33m",
    "grass": "\033[32m",   
    "ice": "\033[96m",     
    "fighting": "\033[91m",
    "poison": "\033[35m",  
    "ground": "\033[33m",  
    "flying": "\033[94m",
    "psychic": "\033[95m", 
    "bug": "\033[92m",     
    "rock": "\033[90m",    
    "ghost": "\033[95m",   
    "dragon": "\033[34m",  
    "dark": "\033[90m",    
    "steel": "\033[97m",   
    "fairy": "\033[95m",   
}
def color_text(text, type_name):
    return f"{TYPE_COLORS[type_name]}{text}{RESET}"
print(f"{color_text('Dragon','dragon')}/{color_text('Electric','electric')}")
print(f"{color_text('Water','water')}/{color_text('Fighting','fighting')}")