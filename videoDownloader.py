from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from time import sleep
import sys
import os
import time

def renameAndMoveVideo():
    files = os.listdir(download_folder)
    if len(files) < 0:
        return
    new_file_name = files[0].replace(".crdownload", ".mp4")

    #Adding video number if videos in list more than 1
    if videosInList > 1:
        new_file_name = f"{currentVideoIndex + 1}# {new_file_name}"

    old_file_path = os.path.join(download_folder, files[0])
    new_file_path = os.path.join(parentFolder, new_file_name)
    os.rename(old_file_path, new_file_path)

# If these logics end successfully they will return True, otherwise will return False
def waitingPageAnswer():
    try:
        WebDriverWait(driver, 10).until(
            lambda driver:
                driver.execute_script("return document.readyState")
        )
        return True
    except TimeoutException:
        return False

# Waiting until the video will be converted
def waitingFileConverting():
    try:
        button_Text = WebDriverWait(driver, 600).until(
            lambda driver:
            "Download" if driver.find_element(By.XPATH, '//button[text()="Download"]') else
                 "Back" if driver.find_element(By.CSS_SELECTOR, '//button[text()="Back"]') else None)
        return button_Text == "Download"
    except TimeoutException:
        return False

# Waiting until the video will be downloaded. If the video was downloaded it'll return True. Otherwise if it catches timeout than it'll return False
def waitingVideoDownload():
    start_time = time.time()
    file_path = ""
    while time.time() - start_time < 3600:
        files = os.listdir(download_folder)
        if files:
            file_path = os.path.join(download_folder, files[0])

        if not file_path.endswith(".crdownload"):
            break
        
        time.sleep(1)

    renameAndMoveVideo()


# Sending URL to y2mate and begins convertion
def beginConvertion(link):
    try:
        input = driver.find_element(By.ID, "video")
        format = driver.find_element(By.ID, "format")
        submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        input.send_keys(link)
        format.click()
        submit.click()
        return True
    except:
        return False

def downloadingPreparation(link):
    #Waiting until the y2mate page will be loaded
    if waitingPageAnswer() == False:
        return False
    print("y2mate page is downloaded!")
    sleep(4)
    
    #Sending URL to y2mate and begins convertion
    if beginConvertion(link) == False:
        return False
    print("Convertion begin!")
    sleep(4)

    #Waiting until the video will be converted to downlod
    if waitingFileConverting() == False:
        driver.find_element(By.XPATH, '//button[text()="Back"]').click()
        return False
    print("Convertion completed!")
    
    #Pressing 'Download' button to start downloading
    print("Pressing 'Download' button...")
    driver.find_element(By.XPATH, '//button[text()="Download"]').click()
    sleep(4)

    #Waiting until the Ad page will be loaded
    if waitingPageAnswer() == False:
        return False
    print("Ad page is downloaded!")
    sleep(4)

    #Closes the Ad tab
    tabs = driver.window_handles
    if len(tabs) > 1:
        driver.switch_to.window(tabs[1])
        driver.close()
        driver.switch_to.window(tabs[0])
    return True

# Will be in loop untill it starts downloading a video. If the download failse or something, next link will be selected
def downloadVideo(link):
    while True:
        # If any step before donwloading will be failed then those operations will be repeated
        if downloadingPreparation(link) == False:
            driver.refresh()
            continue
        print("Preparations complete")

        sleep(2)

        # Waiting until the video will download or the waiting time will hit timeout
        print("Waiting for the video to donwload...")
        waitingVideoDownload()
        print("Video downloaded. Preparing for the next link")

        sleep(2)

        # Tries to find 'Next' button and presses it. Otherwise it will refresh the page
        try:
            buttonNext = driver.find_element(By.XPATH, "//button[@type='submit'] and text()='Next'")
            buttonNext.click
        except:
            driver.refresh()
        print("Preparation for the next link complete!")

        sleep(2)

        return

# Preparations     
args = sys.argv
parentFolder = f'{args[1]}'
download_folder = os.path.join(args[1], f'browser_temp_folder')
links = args[2].split(",")

videosInList = len(links)
currentVideoIndex = 0

print("Variables were prepared")

# Makes a directory for browser
if not os.path.exists(download_folder):
    if len(links) > 1:
        os.mkdir(download_folder)
        print("Browser temp directory created")
else:
    print("Browser temp directory found")

# Set up new path
options = Options()
options.add_experimental_option("prefs",{
    "download.default_directory": download_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
driver = webdriver.Chrome(options=options)
print("Browser was setted up")

# Open browser
driver.get("https://y2mate.nu/en-1oJK/")
print("Browser was launched")

sleep(2)

print(f"Videos to download: {len(links)}")

print("Downloading...")
# Logic
for i in range(videosInList):
    currentVideoIndex = i
    downloadVideo(links[i])
    print("Next link")
    sleep(2)

print("Done!!!")