import sys
import time
from colorama import Fore, Style, init

init(autoreset=True)

ascii_tag = """
 ██▓     ▒█████   ▄▄▄▄    ▒█████  ▄▄▄█████▓ ▒█████   ███▄ ▄███▓▓██   ██▓
▓██▒    ▒██▒  ██▒▓█████▄ ▒██▒  ██▒▓  ██▒ ▓▒▒██▒  ██▒▓██▒▀█▀ ██▒ ▒██  ██▒
▒██░    ▒██░  ██▒▒██▒ ▄██▒██░  ██▒▒ ▓██░ ▒░▒██░  ██▒▓██    ▓██░  ▒██ ██░
▒██░    ▒██   ██░▒██░█▀  ▒██   ██░░ ▓██▓ ░ ▒██   ██░▒██    ▒██   ░ ▐██▓░
░██████▒░ ████▓▒░░▓█  ▀█▓░ ████▓▒░  ▒██▒ ░ ░ ████▓▒░▒██▒   ░██▒  ░ ██▒▓░
░ ▒░▓  ░░ ▒░▒░▒░ ░▒▓███▀▒░ ▒░▒░▒░   ▒ ░░   ░ ▒░▒░▒░ ░ ▒░   ░  ░   ██▒▒▒ 
░ ░ ▒  ░  ░ ▒ ▒░ ▒░▒   ░   ░ ▒ ▒░     ░      ░ ▒ ▒░ ░  ░      ░ ▓██ ░▒░ 
  ░ ░   ░ ░ ░ ▒   ░    ░ ░ ░ ░ ▒    ░      ░ ░ ░ ▒  ░      ░    ▒ ▒ ░░  
    ░  ░    ░ ░   ░          ░ ░               ░ ░         ░    ░ ░     
                       ░                                        ░ ░     
"""

def typewriter(text, color=Fore.MAGENTA, delay=0.0001):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    print(Style.RESET_ALL)

typewriter(ascii_tag)

