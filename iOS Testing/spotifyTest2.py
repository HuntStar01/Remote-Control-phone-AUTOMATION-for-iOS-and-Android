from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.ios.xcuitest.base import XCUITestOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from iOSCallTest2 import input_string

def test_song(text):
    # Desired capabilities
    desired_capabilities = {
        "platformName": "iOS",
        "appium:udid": "00008110-001974661EF2201E",
        "appium:automationName": "XCUITest",
        "appium:bundleId": "com.spotify.client"
    }

    # Load capabilities into options
    options = XCUITestOptions()
    options.load_capabilities(desired_capabilities)

    # Appium server URL
    appium_server_url = 'http://localhost:4723'

    # Initialize the driver
    driver = webdriver.Remote(appium_server_url, options=options)

    search_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//XCUIElementTypeButton[@name='tabbar-item-find']"))
    )
    search_button.click()
    search_button.click()


    # Accessing the Search tab
    search_tab = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//XCUIElementTypeSearchField[@name='SearchBarSearch.TextField']"))
    )
    search_tab.send_keys(text)

    search = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//XCUIElementTypeButton[@name='Search']"))
    )
    search.click()


    song_tab = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//XCUIElementTypeOther[@name='search.results']/XCUIElementTypeOther[1]/XCUIElementTypeCollectionView/XCUIElementTypeCell[1]"))
    )
    song_tab.click()