from colorama import Fore
import colorama
colorama.init(autoreset = True)

logging = False

def log(msg):
    if logging:
        print(Fore.GREEN + msg)

def error(e):
    print(Fore.RED + e)