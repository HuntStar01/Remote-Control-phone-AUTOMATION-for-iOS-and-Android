import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.ios.xcuitest.base import XCUITestOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Desired capabilities
def test_call(text):
    desired_capabilities = {
        "platformName": "iOS",
        "appium:udid": "00008110-001974661EF2201E",
        "appium:automationName": "XCUITest",
        "appium:bundleId": "com.apple.MobileAddressBook"
    }

    # Load capabilities into options
    options = XCUITestOptions()
    options.load_capabilities(desired_capabilities)

    # Appium server URL
    appium_server_url = 'http://localhost:4723'

    # Initialize the driver
    driver = webdriver.Remote(appium_server_url, options=options)

    try:
        # Interact with the search field
        search_field = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//XCUIElementTypeSearchField[@name='Search']"))
        )
        search_field.click()
        
        # Send keys to the search field
        
        name = text
        search_field.send_keys(name)

        # Wait for the contact to be clickable and click it
        contact_xpath = f"(//XCUIElementTypeCell[@name='{name}'])/XCUIElementTypeOther[2]"
        contact = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, contact_xpath))
        )
    
        contact.click()
        
        
        # Wait for the call button to be clickable
        call_button_chain = "//XCUIElementTypeCell[@name='mobile']"
        call_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, call_button_chain))
        )
        # Attempt to click the call button
        call_button.click()
        print("Call button clicked successfully.")
        time.sleep(3)
        call_div = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, "//XCUIElementTypeApplication[@name='Phone call']/XCUIElementTypeWindow[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther"))
        )
        if call_div :
            print('call placed')
            call_cut = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, "//XCUIElementTypeButton[@name='End']"))
        )
            call_cut.click()
        # Print debug information
        print(f"Call button location: {call_button.location}")
        print(f"Call button size: {call_button.size}")
        
        
        
    except Exception as e:
        print('')
        
    finally:
        # Ensure to quit the driver session
        driver.quit()
