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
commands = ["set", "vars", "run", "stop", "exit", "clear", "help", "path", "url"]

def checkNumber(number):
        if len(number) > 0:
            try:
                number = int(number)
                if number < 0:
                    return -1
            except:
                return -1
        else:
            number = 0

        return number 

#Downloading Logic
def toDownloadFunc(toDownload, downloadFrom = 0, downloadTo = 0):
    os.system(f'python3 videoDownloader.py {savePath} "{toDownload}" {downloadFrom} {downloadTo}')

def downloadPlaylist(toDownload):
    print("Playlist prep")
    errorPrint(ErrorType.warning, "Do you want to set from where to where to download? ")
    errorPrint(ErrorType.fatal,"If you don't:\t\tJust press enter")
    errorPrint(ErrorType.success,"If you do:\t\tEnter: fromNumber:toNumber")
    messagePrint("Example: 10:15\t\tWill download from -the video 10- to -the video 15 included-")
    messagePrint("Example: 10:\t\tWill download from -the video 10- to -the end of the playlist-")
    messagePrint("Example: :15\t\tWill download from -the start of the playlist- -to the video 15 included-")

    while True:
        print("input: ", end="")
        userInput = input()

        devider = userInput.find(":")

        if devider == -1:
            errorPrint(ErrorType.warning, "Devider ':' wasn't find.")
            continue

        fromNumber = checkNumber(userInput[:devider])
        if fromNumber == -1:
            errorPrint(ErrorType.warning, "Invalind 'fromNumber'. 'fromNumber' should be only a number or nothing. Example: '34' or ''.")
            continue

        toNumber = checkNumber(userInput[devider+1:])
        if toNumber == -1:
            errorPrint(ErrorType.warning, "Invalind 'toNumber'. 'toNumber' should be only a number or nothing. Example: '34' or ''.")
            continue
        
        messagePrint(f"fromNumber: '{fromNumber}', toNumber: '{toNumber}'")

        if fromNumber > toNumber:
            errorPrint(ErrorType.warning, "fromNumber cannot be more than toNumber")
            continue

        videosCount = len(toDownload)
        if fromNumber > videosCount or toNumber > videosCount:
            errorPrint(ErrorType.warning, f"fromNumber and toNumber cannot be more than num of videos. Videos in playlist: {videosCount}")
            continue

        if fromNumber == 0 and toNumber == 0:
            messagePrint("Are you serious? Both are zero! You could just press 'Enter' >_<")
            messagePrint("Enter 'y' if you are seious.")
            userAnwer = input("").lower()
            if userAnwer == "y":
                print()
                messagePrint("Please don't do this again! I don't like it. Q_Q")
                messagePrint("Just press enter next time. if you want to download full playlist")
                messagePrint("Press 'Enter' to continue")
                input()
            else:
                return
        
        if fromNumber > 0:
            fromNumber-=1

        toDownloadFunc(toDownload, fromNumber, toNumber + 1)
        return
    
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
    isPlaylist = False
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

    print(f"Is a playlisth: {isPlaylist}")

    if isPlaylist:
        downloadPlaylist(toDonwload)
    else:
        toDownloadFunc(toDonwload)
    
    errorPrint(ErrorType.success, "Downloading complete")
    
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
def getCommand():
    global userInput
    command = userInput.strip().split(" ")[0].lower()
    if command in commands:
        return command
    else:
        return None

def checkUserInput():
    if len(userInput) <= 0:
        return

    command = getCommand()
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

userInput = "url = https://www.youtube.com/watch?v=62Vjm0UGfv8&list=PLepq44cq4JdyaMy-U1xQQLwWgD63MzTR3"
checkUserInput()
userInput = "path = /media/njj/Media/DownloadVideos"
checkUserInput()
userInput = "run"
checkUserInput()

while True:
    print("Enter command: ", end='')
    userInput = input()
    checkUserInput()

# Auto insert for testing