from ErrorPrinter import errorFromPrint
from ErrorPrinter import errorPrint
from ErrorPrinter import messagePrint
from ErrorPrinter import ErrorType
from pytube import Playlist
from pytube import YouTube
import os

savePath = "empty"
url = "empty"

userInput = ""
commands = ["set", "vars", "run", "stop", "exit", "clear", "help"]

#Downloading Logic
def toDownload(toDownload):
    os.system(f'python3 videoDownloader.py {savePath} "{toDownload}"')

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
    global savePath, url
    toDonwload = None

    #Checking if the user didn't changed path variable to a working path
    messagePrint("Checking PATH on emptines...")
    if savePath == "empty":
        errorFromPrint(ErrorType.fatal, "run", "'Path' variable is empty. Fill the variable with command: set path = yourPath\tPrint 'help path' for more information ")
        return
    errorPrint(ErrorType.success, "OK")
    
    #Checking if URL is empty
    messagePrint("Checking URL on emptines...")
    if url == "empty":
        errorFromPrint(ErrorType.fatal, "run", "'URL' variable is empty. Fill the variable with command: set url = yoururl\tPrint 'help url' for more information ")
        return
    errorPrint(ErrorType.success, "OK")

    #Checking if URL is a playlist 
    messagePrint("Checking URL on working...")
    try:
        playlist = Playlist(url)
        url = f"{url}\t Videos: {len(playlist.video_urls)}"
        toDonwload = playlist.video_urls
        isPlaylist = True
    except:
        #Checking if URL is a video
        try:
            toDonwload = YouTube(url).watch_url
        except:
            # If both conditions were failed we throw an error
            errorFromPrint(ErrorType.fatal, "run", "the URL link isn't working. Please check the URL.\n")
            return
    errorPrint(ErrorType.success, "OK")
    
    #Starts donwload
    messagePrint("Starting download...")
    toDownload(toDonwload)
    
def commandHelp(options):
    options = options.replace(" ", "") # removing command name and spaces
    
    if len(options) <= 0:
        messagePrint("==========================ABOUT===============================================================================================")
        messagePrint("App for donwloading YouTube videos via y2mate.nu website")
        messagePrint("Author: TDT(TimDevTech) (NeizNayz)")
        print()
        messagePrint("=========================COMANDS==============================================================================================")
        for command in commands:
            printCommandDescription(command)
            messagePrint()
        messagePrint("==============================================================================================================================")
        return

    printCommandDescription(options) 

def printCommandDescription(toExplain):
    match toExplain:
        case "path": 
            messagePrint("'Path' variable stores a path where videos will be stored.\nBefore starting downloading you need to fill it with: set path = yourPath\tWhere yourPath is path to the existing directory where the video will be soterd")
        case "url":
            messagePrint("URL will be inserted into y2mate.nu input field. Make sure that the URL is working (because script doesn't check is the URL working or not, but if URL doesn't work, it can cause some troubles later).\nBefore starting downloading you need to fill it with: set url = yourURL\tWhere yourURL is the url of a video or a playlis on YouTube")
        case "set":
            messagePrint("set variableName = value \t - Will put value in a variable.\n\t\t\t\t\tExample: set url = https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUHcmlja3JvbA%3D%3D")
        case "vars": 
            messagePrint("vars\t\t\t\t - Shows 'user variables' that need to be filled and contents of those variables")
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

def getCommand():
    symbolCount = 1
    command = ''
    for symbol in userInput:

        if symbolCount >= 5:
            break

        if symbol != " ":
            command = command + symbol.lower()
            symbolCount = symbolCount + 1
        
        if symbolCount >= 3:
            for commandName in commands:
                if command == commandName:
                    return command

def checkUserInput():
    command = getCommand()
    options = userInput[len(command):]
    messagePrint("Processing command...")
    match command:
        case "set": commandSet(options)
        case "vars": commandVars()
        case "run": commandRun()
        case "exit": exit()
        case "clear": os.system('cls' if os.name=='nt' else 'clear')
        case "help": commandHelp(options)
        case "stop": errorFromPrint(ErrorType.warning, "checkUserInput()", "Playlist insn't downloading now. Enter 'help stop' for more information")
        case _:
            errorFromPrint(ErrorType.warning, "checkUserInput()", f"Invalid input. Command '{command}' doesn't exist")
    print()

#Program
#print("Hello! Enter help to know how to use the script.")
#while True:
#    print("Enter command: ", end='')
#    userInput = input()
#    checkUserInput()

# Auto insert for testing
userInput = "set url = https://www.youtube.com/watch?v=kRcbYLK3OnQ&list=PLQOaTSbfxUtCrKs0nicOg2npJQYSPGO9r"
checkUserInput()
userInput = "set path = /media/njj/Media/DownloadVideos"
checkUserInput()
userInput = "run"
checkUserInput()

input()