from libs.browserSetuper import setupBrowser
from libs.donwloadLogic import downloadVideo
from libs.ErrorPrinter import errorFromPrint
from libs.ErrorPrinter import messagePrint
from libs.ErrorPrinter import errorPrint
from libs.ErrorPrinter import ErrorType
from pytube import Playlist
from pytube import YouTube
from time import sleep
import os

parentFolder = None
download_folder = None
downloadFrom = 0
downloadTo = 1
driver = None
urls = None
videosInList = 0
currentVideoIndex = 0

def checkNumber(number):
        if len(number) > 0:
            try:
                number = int(number)
                if number < 0:
                    return -1 #number is less than zero
            except:
                return -1 #number is invalid
        else:
            number = -2 #number is empty

        return number 

def getFromToIndexes(links):
    global videosInList

    print("Playlist prep")
    errorPrint(ErrorType.warning, "Do you want to set from where to where to download? ")
    errorPrint(ErrorType.fatal,"If you don't:\t\tJust press enter")
    errorPrint(ErrorType.success,"If you do:\t\tEnter: fromNumber:toNumber")
    messagePrint("Example: 10:15\t\tWill download from -the video 10- to -the video 15 included-")
    messagePrint("Example: 10:\t\tWill download from -the video 10- to -the end of the playlist-")
    messagePrint("Example: :15\t\tWill download from -the start of the playlist- -to the video 15 included-")

    while True:
        print("input: ", end="")
        userInput = input().replace(" ", "")

        if len(userInput) != 0:
            devider = userInput.find(":")
            if devider == -1:
                errorPrint(ErrorType.warning, "Devider ':' wasn't find.")
                continue

            downloadFrom = checkNumber(userInput[:devider])
            if downloadFrom == -1:
                errorPrint(ErrorType.warning, "Invalind 'fromNumber'. 'fromNumber' should be only a number or nothing. Example: '34' or ''.")
                continue

            downloadTo = checkNumber(userInput[devider+1:])
            if downloadTo == -1:
                print(userInput[devider+1:]);
                errorPrint(ErrorType.warning, "Invalind 'toNumber'. 'toNumber' should be only a number or nothing. Example: '34' or ''.")
                continue

            if downloadFrom == -2:  #If user entered: ':10' then it means download from 0 to 10
                downloadFrom = 0

            if downloadTo == -2:    #If user entered: '10:' then it means download from 10 to the end of a playlist
                downloadTo = videosInList
            
            messagePrint(f"fromNumber: '{downloadFrom}', toNumber: '{downloadTo}'")

            if downloadFrom > downloadTo:
                errorPrint(ErrorType.warning, "fromNumber cannot be more than toNumber")
                continue

            videosInList = len(links)

            if downloadFrom > videosInList or downloadTo > videosInList:
                errorPrint(ErrorType.warning, f"fromNumber and toNumber cannot be more than num of videos. Videos in playlist: {videosInList}")
                continue

            if downloadFrom == 0 and downloadTo == 0:
                return [0, videosInList]
                
            if downloadFrom > 0:
                downloadFrom-=1

        else:
            downloadFrom = 0
            downloadTo = len(links)

        return [downloadFrom, downloadTo]
def isPathAndURLEmpty(savePath, url):
    #Checking if the user didn't changed path variable to a working path
    messagePrint("Checking PATH on emptines...")
    if savePath == "empty":
        errorFromPrint(ErrorType.fatal, "run", "'Path' variable is empty. Fill the variable with command: set path = yourPath\tPrint 'help path' for more information ")
        return True
    errorPrint(ErrorType.success, "OK")
    
    #Checking if URL is empty
    messagePrint("Checking URL on emptines...")
    if url == "empty":
        errorFromPrint(ErrorType.fatal, "run", "'URL' variable is empty. Fill the variable with command: set url = yoururl\tPrint 'help url' for more information ")
        return True
    errorPrint(ErrorType.success, "OK")

    return False

def downloaderSetup(_savePath):
    global parentFolder, download_folder, downloadFrom, downloadTo, videosInList
    
    parentFolder = _savePath
    download_folder = os.path.join(_savePath, f'browser_temp_folder')
    videosInList = len(urls)

    print("=========================")
    print(videosInList)

    if videosInList > 1:
        fromTo = getFromToIndexes(urls)
        downloadFrom = int(fromTo[0])
        downloadTo = int(fromTo[1])

    print(downloadFrom)
    print(downloadTo)
    print("=========================")
def startDownloading(_savePath, _url):
    global urls, driver, downloadFrom, downloadTo

    if isPathAndURLEmpty(_savePath, _url): return
     
    messagePrint("Checking URL on working...")
    messagePrint("\tIs a playlist?")

    try: #Checking if URL is a playlist
        playlist = Playlist(_url)
        urls = playlist.video_urls
        errorPrint(ErrorType.success, "\tYES")

    except: #Checking if URL is a video
        errorPrint(ErrorType.fatal, "\tNO")
        messagePrint("\tIs a video?")
        
        try:
            urls = YouTube(_url).watch_url
            errorPrint(ErrorType.success, "\tYES")
        except:
            # If both conditions were failed we throw an error
            errorPrint(ErrorType.fatal, "\tNO")
            errorFromPrint(ErrorType.fatal, "run", "the URL link isn't working. Please check the URL.\n")
            return
    errorPrint(ErrorType.success, "OK")
    
    messagePrint("Donwloading...")

    #Setuping
    downloaderSetup(_savePath)
    driver = setupBrowser(download_folder)
    driver.get("https://y2mate.nu/en-1oJK/")

    for i in range(downloadFrom, downloadTo):
        downloadVideo(driver, urls[i], download_folder, parentFolder, videosInList, i)
        sleep(2)

    errorPrint(ErrorType.success, "Done!")


    #https://gamma.123tokyo.xyz/get.php/7/e4/fbYknr-HPYE.mp3?cid=MmEwMTo0Zjk6YzAxMjo2ZGJiOjoxfE5BfEZJ&h=yBe4f11qyYiYcbooDuGdwA&s=1738796382&n=lvalues%20and%20rvalues%20in%20C%2B%2B&uT=R&uN=Y29kZWJ1c3RlcnM%3D&s=3&v=fbYknr-HPYE&f=mp4&_=0.13476051159350333