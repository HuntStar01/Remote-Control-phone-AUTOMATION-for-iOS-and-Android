import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.ios.xcuitest.base import XCUITestOptions

def setup():
    desired_capabilities = {
        "platformName": "iOS",
        "appium:platformVersion": "17.5",
        "appium:deviceName": "iPhone 15 Pro Max",
        "appium:app": "/Users/vaibhavisrivastava/Desktop/MusicApp/build/Release-iphonesimulator/MusicApp.app",
        "appium:automationName": "XCUITest",
        "appium:noReset": True
        }
    options = XCUITestOptions()
    options.load_capabilities(desired_capabilities)
    appium_server_url = 'http://localhost:4723'
    driver = webdriver.Remote(appium_server_url, options=options)
    return driver
    
def test_music_app(driver):

    play_check = False
    next_check = False
    prev_check = False

    play_button = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "play")
    next_button = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "next")
    prev_button = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "prev")

    # Wait for the app to load
    time.sleep(10)
    
    # Next Button Call
    if next_button :
        next_button.click()
        next_check = True

    time.sleep(5)

    # Previous Button Call
    if prev_button :
        prev_button.click()
        prev_check = True

    time.sleep(5)

    # Pause Music Call
    if play_button :
        play_button.click()
        play_check = True

    if play_check and next_check and prev_check :
        return True
    else:
        return False

def teardown(driver):
    driver.quit()

if __name__ == "__main__":
    driver = setup()
    try :
        if test_music_app(driver) :    
            print("Jai Shree Ram")
        else:
            print("Mulla Madarchod")
    finally:
        teardown(driver)



