from enum import Enum
from colorama import Fore
from pytube import Playlist
from pytube import YouTube
from math import ceil
from multiprocessing import Process
import os

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

#Downloading Logic
def downloadVideo(toDownload, browser_index = 0, lastVideoIndex = -1):
    os.system(f'python3 videoDownloader.py {str(browser_index)} {savePath} "{toDownload}" {lastVideoIndex}')

def downloadPlaylist(URLs):
    videosCount = len(URLs)
    toOpenCount = 4 #getStep(videosCount)
    openedCount = 0
    linksPerBrowser = ceil(videosCount / toOpenCount)
    linksAdded = 0
    browserLinks = []
    browserTitles = []

    print("Downloading a playlist")

    for i in range(videosCount):
        browserLinks.append(URLs[i])
        linksAdded += 1

        if(linksAdded == linksPerBrowser or i >= videosCount - 1):
            print("Opening browser")
            print(f"Videos num: {len(browserLinks)}")
            openedCount += 1
            linksAsString = ",".join(browserLinks)
            Process(target=downloadVideo, args=(linksAsString, openedCount, i)).start()
            browserLinks.clear()
            browserTitles.clear()
            linksAdded = 0
    
    errorPrinter(ErrorType.success, "downloadPlaylist()", "Downloading was started. You can use console now, to do something else")

#Commands
def commandSet(options):
    global savePath, url
    options = options.replace(" ", "")
    deviderIndex = options.find("=")
    variableName = options[:deviderIndex]
    value = options[deviderIndex + 1:]

    if len(value) <= 0:
        errorPrinter(ErrorType.warning, "set", f"Invalid value. Value cannot be empty. Your value: '{value}'")

    match variableName:
        case "path":
            if os.path.exists(value):
                savePath = value
                errorPrinter(ErrorType.success, "set", f"'path' value was changed on '{savePath}'")
            else:
                errorPrinter(ErrorType.warning, "set", f"Path '{value}' doesn't exist. Path must contain only existing path")
        
        case "url":
            url = value
            errorPrinter(ErrorType.success, "set", f"'url' value was changed on '{url}'")

        case _:
            errorPrinter(ErrorType.warning, "set", f"Invalid value. Value '{variableName}' doesn't exist")

def commandVars():
    print(f"Path: '{savePath}'")
    print(f"URL: '{url}'")

def commandRun():
    global savePath, url
    toDonwload = None
    isPlaylist = False

    #Checking if the user didn't changed path variable to a working path
    print("Checking PATH on emptines...")
    if savePath == "empty":
        errorPrinter(ErrorType.fatal, "run", "'Path' variable is empty. Fill the variable with command: set path = yourPath\tPrint 'help path' for more information ")
        return
    print("OK")
    
    #Checking if URL is empty
    print("Checking URL on emptines...")
    if url == "empty":
        errorPrinter(ErrorType.fatal, "run", "'URL' variable is empty. Fill the variable with command: set url = yoururl\tPrint 'help url' for more information ")
        return
    print("OK")

    #Checking if URL is a playlist 
    print("Checking URL on working...")
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
            errorPrinter(ErrorType.fatal, "run", "the URL link isn't working. Please check the URL.\n")
            return
    print("OK")
    

    #Starts donwload
    print("Starting download...")
    if isPlaylist: 
        print("Downloading a playlist...")
        downloadPlaylist(toDonwload)
    else:
        print("Downloading a video...")
        downloadVideo(toDonwload)
    
def commandHelp(options):
    options = options.replace(" ", "") # removing command name and spaces
    
    if len(options) <= 0:
        print("==========================ABOUT===============================================================================================")
        print("App for donwloading YouTube videos via y2mate.nu website")
        print("Author: TDT(TimDevTech) (NeizNayz)")
        print()
        print("=========================COMANDS==============================================================================================")
        for command in commands:
            printCommandDescription(command)
            print()
        print("==============================================================================================================================")
        return

    printCommandDescription(options) 

def printCommandDescription(toExplain):
    match toExplain:
        case "path": 
            print("'Path' variable stores a path where videos will be stored.\nBefore starting downloading you need to fill it with: set path = yourPath\tWhere yourPath is path to the existing directory where the video will be soterd")
        case "url":
            print("URL will be inserted into y2mate.nu input field. Make sure that the URL is working (because script doesn't check is the URL working or not, but if URL doesn't work, it can cause some troubles later).\nBefore starting downloading you need to fill it with: set url = yourURL\tWhere yourURL is the url of a video or a playlis on YouTube")
        case "set":
            print("set variableName = value \t - Will put value in a variable.\n\t\t\t\t\tExample: set url = https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUHcmlja3JvbA%3D%3D")
        case "vars": 
            print("vars\t\t\t\t - Shows 'user variables' that need to be filled and contents of those variables")
        case "run": 
            print("run\t\t\t\t - Starts downloading and will use info from 'user variables'")
        case "stop":
            print("stop\t\t\t\t - Stops downloading immediatly. Works only when you downloading a playlist")
        case "exit":
            print("exit\t\t\t\t - Closes this script")
        case "clear":
            print("clear\t\t\t\t - Clears the console")
        case "help": 
            print("help optionName\t\t\t - Shows information how to work with a command or a variable.\n\t\t\t\t\tExample: help set\tWill show how to use 'set' command\n\t\t\t\t\tExample: help path\tWill explain how to use path variable\n\t\t\t\t\tExmaple: help\t will show all about the script and commands list")
        case _:
            errorPrinter(ErrorType.warning, "help/printCommandDescription()", f"Command {toExplain} doesn't exist. Print 'help' for more information")

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
    print("Processing command...")
    match command:
        case "set": commandSet(options)
        case "vars": commandVars()
        case "run": commandRun()
        case "exit": exit()
        case "clear": os.system('cls' if os.name=='nt' else 'clear')
        case "help": commandHelp(options)
        case "stop": errorPrinter(ErrorType.warning, "checkUserInput()", "Playlist insn't downloading now. Enter 'help stop' for more information")
        case _:
            errorPrinter(ErrorType.warning, "checkUserInput()", f"Invalid input. Command '{command}' doesn't exist")
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