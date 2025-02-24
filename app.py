from libs.ErrorPrinter import errorFromPrint
from libs.ErrorPrinter import messagePrint
from libs.ErrorPrinter import errorPrint
from libs.ErrorPrinter import ErrorType
from donwloader import startDownloading
import os

savePath = "empty"
url = "empty"

userInput = ""
commands = ["set", "vars", "run", "stop", "exit", "clear", "help", "path", "url"]

#Commands
def commandSet(options):
    global savePath, url
    options = options.replace(" ", "")
    deviderIndex = options.find("=")
    variableName = options[:deviderIndex]
    value = options[deviderIndex + 1:]

    if len(value) <= 0:
        errorFromPrint(ErrorType.warning, "set", f"Invalid value. Value cannot be empty. Your value: '{value}'")

    match variableName:
        case "path":
            if os.path.exists(value):
                savePath = value
                errorFromPrint(ErrorType.success, "set", f"'path' value was changed on '{savePath}'")
            else:
                errorFromPrint(ErrorType.warning, "set", f"Path '{value}' doesn't exist. Path must contain only existing path")
        
        case "url":
            url = value
            errorFromPrint(ErrorType.success, "set", f"'url' value was changed on '{url}'")

        case _:
            errorFromPrint(ErrorType.warning, "set", f"Invalid value. Value '{variableName}' doesn't exist")
def commandVars():
    errorPrint(ErrorType.message, f"Path: '{savePath}'")
    errorPrint(ErrorType.message, f"URL: '{url}'")
def commandRun():
    startDownloading(savePath, url)
def commandHelp(options):
    options = options.replace(" ", "") # removing command name and spaces
    
    if len(options) <= 0:
        messagePrint("==ABOUT========================================================================================================================")
        messagePrint("App for donwloading YouTube videos via y2mate.nu website")
        messagePrint("Author: TDT(TimDevTech) (NeizNayz)")
        print()
        messagePrint("==COMANDS======================================================================================================================")
        for command in commands:
            printCommandDescription(command)
            messagePrint()

        messagePrint("==VARIABLES====================================================================================================================")
        messagePrint("Variables can be changed via 'variableName = value'\nExample: url = https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUHcmlja3JvbA%3D%3D \nIt will set https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUHcmlja3JvbA%3D%3D value in url variable")
        messagePrint("Variables available: path, url")
        messagePrint("To see what which variable for, enter: help variableName")
        messagePrint("To see what variables contain, enter: vars")
        commandVars()
        print()
        return

    printCommandDescription(options) 
def printCommandDescription(toExplain):
    match toExplain:
        case "path": 
            messagePrint("Variable 'Path' variable stores a path where videos will be stored.\nBefore starting downloading you need to fill it with: set path = yourPath\tWhere yourPath is path to the existing directory where the video will be soterd")
        case "url":
            messagePrint("Variable 'URL' will be inserted into y2mate.nu input field. Make sure that the URL is working (because script doesn't check is the URL working or not, but if URL doesn't work, it can cause some troubles later).\nBefore starting downloading you need to fill it with: set url = yourURL\tWhere yourURL is the url of a video or a playlis on YouTube")
        case "vars": 
            messagePrint("vars\t\t\t\t - Shows 'user variables' that need to be filled")
        case "run": 
            messagePrint("run\t\t\t\t - Starts downloading and will use info from 'user variables'")
        case "stop":
            messagePrint("stop\t\t\t\t - Stops downloading immediatly. Works only when you downloading a playlist")
        case "exit":
            messagePrint("exit\t\t\t\t - Closes this script")
        case "clear":
            messagePrint("clear\t\t\t\t - Clears the console")
        case "help": 
            messagePrint("help optionName\t\t\t - Shows information how to work with a command or a variable.\n\t\t\t\t\tExample: help set\tWill show how to use 'set' command\n\t\t\t\t\tExample: help path\tWill explain how to use path variable\n\t\t\t\t\tExmaple: help\t will show all about the script and commands list")
        case _:
            errorFromPrint(ErrorType.warning, "help/printCommandDescription()", f"Command {toExplain} doesn't exist. Print 'help' for more information")

#User input handling
def findCommand():
    global userInput
    command = userInput.strip().split(" ")[0].lower()
    if command in commands:
        return command
    else:
        return None
def checkUserInput():
    if len(userInput) <= 0:
        return

    command = findCommand()
    if command is None:
        errorFromPrint(ErrorType.warning, "checkUserInput()", f"Invalid command 'userInput'. Enter 'help' to see available commands.")
        return

    options = userInput[len(command):].strip()

    match command:
        case "vars": commandVars()
        case "run": commandRun()
        case "exit": exit()
        case "clear": os.system('cls' if os.name=='nt' else 'clear')
        case "help": commandHelp(options)
        case "stop": errorFromPrint(ErrorType.warning, "checkUserInput()", "Playlist insn't downloading now. Enter 'help stop' for more information")
        case _:
            commandSet(userInput)
    print()

#Program
messagePrint("Hello! Enter help to know how to use the script.")

# Auto insert for testing or downloading huge playlist. TO USE autoinsert UNCOMMENT and change (if you want next) next lines:
userInput = "url = https://www.youtube.com/watch?v=18c3MTX0PK0&list=PLlrATfBNZ98dudnM48yfGUldqGD0S4FFb"
checkUserInput()
userInput = "path = I:\Tutorials\C++"
checkUserInput()
userInput = "run"
checkUserInput()

while True:
    print("command: ", end='')
    userInput = input()
    checkUserInput()