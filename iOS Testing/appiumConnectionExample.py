from appium import webdriver
from appium.options.ios.xcuitest.base import XCUITestOptions
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