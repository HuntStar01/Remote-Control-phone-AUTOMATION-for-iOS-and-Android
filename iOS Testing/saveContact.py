from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.ios.xcuitest.base import XCUITestOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 

# Desired capabilities
def save_con(text1,text2,text3,num):
    desired_capabilities = {
        "platformName": "iOS",
        "appium:udid": "00008110-001974661EF2201E",
        "appium:automationName": "XCUITest",
        "appium:bundleId": "conquerors.iOSContact"
    }

    # Load capabilities into options
    options = XCUITestOptions()
    options.load_capabilities(desired_capabilities)

    # Appium server URL
    appium_server_url = 'http://localhost:4723'

    # Initialize the driver
    driver = webdriver.Remote(appium_server_url, options=options)
    
    #variable
    name = text1
    familyname = text2
    emailInput = text3
    number = num

    first_name= WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//XCUIElementTypeTextField[@name='firstname']"))
        )
    first_name.click()

    # Send keys to the text field

    first_name.send_keys(name)
    if familyname :
        family_name= WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//XCUIElementTypeTextField[@value='Family Name']"))
            )
        family_name.send_keys(familyname)
    if emailInput:
        email= WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//XCUIElementTypeTextField[@value='Email']"))
            )
        email.send_keys(emailInput)


    phone_num= WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//XCUIElementTypeTextField[@name='phonenum']"))
        )

    phone_num.send_keys(number)

    add_Contact= WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//XCUIElementTypeButton[@name='addcontact']"))
        )
    add_Contact.click()

    # Quit the driver after the operations
    driver.quit()
