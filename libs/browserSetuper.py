from libs.ErrorPrinter import messagePrint
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os

def setupBrowser(_download_folder):
    # Makes a directory for browser
    if not os.path.exists(_download_folder):
        os.mkdir(_download_folder)
        messagePrint("Browser temp directory created")
    else:
        messagePrint("Browser temp directory found")

    # Set up new path
    options = Options()
    options.add_experimental_option("prefs",{
        "download.default_directory": _download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    messagePrint("Browser was setted up")
    return webdriver.Chrome(options=options)