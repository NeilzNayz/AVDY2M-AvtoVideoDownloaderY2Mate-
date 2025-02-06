from selenium.webdriver.common.by import By
from libs.waiter import waitingVideoConverting
from libs.waiter import waitingVideoDownload
from libs.waiter import waitingPageReady
from libs.ErrorPrinter import messagePrint
from time import sleep
import os

def renameAndMoveVideo(_download_folder, _parentFolder, _videosInList, _currentVideoIndex):

    files = os.listdir(_download_folder)

    if len(files) <= 0: return

    new_file_name = files[0].replace(".crdownload", ".mp4")

    #Adding video number if videos in list more than 1
    if _videosInList > 1:
        new_file_name = f"{_currentVideoIndex + 1}# {new_file_name}"

    old_file_path = os.path.join(_download_folder, files[0])
    new_file_path = os.path.join(_parentFolder, new_file_name)
    os.rename(old_file_path, new_file_path)

def beginConvertion(_dirver, link):
    try:
        input = _dirver.find_element(By.ID, "video")
        format = _dirver.find_element(By.ID, "format")
        submit = _dirver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        input.send_keys(link)
        format.click()
        submit.click()
        return True
    except:
        return False

def downloadingPreparation(_driver, _link):
    #Waiting until the y2mate page will be loaded
    if waitingPageReady(_driver) == False:
        return False
    messagePrint("y2mate page is downloaded!")
    
    sleep(1)
    #Sending URL to y2mate and begins convertion
    if beginConvertion(_driver, _link) == False:
        return False
    messagePrint("Convertion begin!")

    #Waiting until the video will be converted to download
    if waitingVideoConverting(_driver) == False:
        return False
    messagePrint("Convertion completed!")

    sleep(2)

    #Pressing 'Download' button to start downloading
    messagePrint("Pressing 'Download' button...")
    _driver.find_element(By.XPATH, '//button[text()="Download"]').click()

    #Waiting until the Ad page will be loaded
    if waitingPageReady(_driver) == False:
        return False
    messagePrint("Ad page is downloaded!")
    
    sleep(4)

    #Closes the Ad tab
    tabs = _driver.window_handles
    if len(tabs) > 1:
        _driver.switch_to.window(tabs[1])
        _driver.close()
        _driver.switch_to.window(tabs[0])
    return True

# Will be in loop untill it starts downloading a video. If the download failse or something, next link will be selected
def downloadVideo(_driver, _link, _download_folder, _parentFolder, videosInList, currentVideoIndex):
    while True:

        # If any step before donwloading will be failed then those operations will be repeated
        if downloadingPreparation(_driver, _link) == False:
            _driver.refresh()
            continue

        messagePrint("Preparations completed")
        messagePrint("Waiting for the video to donwload...")

        # Waiting until the video will download or the waiting time will hit timeout
        waitingVideoDownload(_download_folder)
        renameAndMoveVideo(_download_folder, _parentFolder, videosInList, currentVideoIndex)

        sleep(1)
        messagePrint("Preparing for the next link")

        # Tries to find 'Next' button and presses it. Otherwise it will refresh the page
        try:
            buttonNext = _driver.find_element(By.XPATH, "//button[@type='submit'] and text()='Next'")
            buttonNext.click
        except:
            _driver.refresh()

        messagePrint("Preparation for the next link complete!")

        return