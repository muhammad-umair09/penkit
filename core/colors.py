import sys
from colorama import init, Fore, Style

init(autoreset=True)

class Colors:
    GREEN = Fore.GREEN + Style.BRIGHT
    RED = Fore.RED + Style.BRIGHT
    BLUE = Fore.BLUE + Style.BRIGHT
    YELLOW = Fore.YELLOW + Style.BRIGHT
    CYAN = Fore.CYAN + Style.BRIGHT
    MAGENTA = Fore.MAGENTA + Style.BRIGHT
    WHITE = Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL

    @staticmethod
    def info(msg: str) -> str:
        return f"{Colors.BLUE}[*]{Colors.RESET} {msg}"

    @staticmethod
    def success(msg: str) -> str:
        return f"{Colors.GREEN}[+]{Colors.RESET} {msg}"

    @staticmethod
    def fail(msg: str) -> str:
        return f"{Colors.RED}[-]{Colors.RESET} {msg}"

    @staticmethod
    def warn(msg: str) -> str:
        return f"{Colors.YELLOW}[!]{Colors.RESET} {msg}"