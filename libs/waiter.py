from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import time
import os

# If these logics end successfully they will return True, otherwise will return False
def waitingPageReady(_driver):
    try:
        WebDriverWait(_driver, 10).until(
            lambda driver:
                driver.execute_script("return document.readyState")
        )
        return True
    except TimeoutException:
        return False

# Waiting until the video will be converted
def waitingVideoConverting(_driver):
    try:
        button = WebDriverWait(_driver, 600).until(
            EC.any_of(
                EC.presence_of_element_located((By.XPATH, "//button[text()='Download']")),
                EC.presence_of_element_located((By.XPATH, "//button[text()='Back']"))))
        
        if button == None or button.text == "Back":
            return False

    except TimeoutException:
        return False

# Waiting until the video will be downloaded. If the video was downloaded it'll return True. Otherwise if it catches timeout than it'll return False
def waitingVideoDownload(_download_folder):
    start_time = time.time()
    file_path = ""
    while time.time() - start_time < 3600:
        files = os.listdir(_download_folder)
        if files:
            file_path = os.path.join(_download_folder, files[0])

        if file_path.endswith(".mp4"):
            break
        
        sleep(1)