from enum import Enum
from colorama import Fore

class ErrorType(Enum):
    message = 0
    success = 1
    warning = 2
    fatal = 3

#Prints errors success/warning/fatal

def messagePrint(message):
    print(Fore.CYAN + message + Fore.WHITE)

def errorPrint(errorType, message):
    match errorType:
        case ErrorType.message:
            print(Fore.CYAN + message + Fore.WHITE)
        case ErrorType.success:
            print(Fore.GREEN + message + Fore.WHITE)
        case ErrorType.warning:
            print(Fore.YELLOW + message  + Fore.WHITE)
        case ErrorType.fatal:
            print(Fore.RED + message + Fore.WHITE)
        case _:
            print(Fore.RED + message + Fore.WHITE)

def errorFromPrint(errorType, errorFrom, message):
    match errorType:
        case ErrorType.message:
            print(Fore.CYAN + f"Message from: '{errorFrom}': {message}" + Fore.WHITE)
        case ErrorType.success:
            print(Fore.GREEN + f"Success from: '{errorFrom}': {message}" + Fore.WHITE)
        case ErrorType.warning:
            print(Fore.YELLOW + f"Warining from: '{errorFrom}': {message}" + Fore.WHITE)
        case ErrorType.fatal:
            print(Fore.RED + f"Error from: '{errorFrom}': {message}" + Fore.WHITE)
        case _:
            print(Fore.RED + f"Error from: 'errorPrinter()': Error type: '{errorType}' doesn't exist!" + Fore.WHITE)
