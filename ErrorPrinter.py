from enum import Enum
from colorama import Fore

class ErrorType(Enum):
    success = 1
    warning = 2
    fatal = 3

savePath = "empty"
url = "empty"

userInput = ""
commands = ["set", "vars", "run", "stop", "exit", "clear", "help"]

#Prints errors success/warning/fatal
def errorPrinter(errorType, errorFrom, message):
    match errorType:
        case ErrorType.success:
            print(Fore.GREEN + f"Message from: '{errorFrom}': {message}" + Fore.WHITE)
        case ErrorType.warning:
            print(Fore.YELLOW + f"Warining from: '{errorFrom}': {message}" + Fore.WHITE)
        case ErrorType.fatal:
            print(Fore.RED + f"Error from: '{errorFrom}': {message}" + Fore.WHITE)
        case _:
            print(Fore.RED + f"Error from: 'errorPrinter()': Error type: '{errorType}' doesn't exist!" + Fore.WHITE)
