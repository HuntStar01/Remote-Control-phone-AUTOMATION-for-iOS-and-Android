# Example usage
input_string = "7985662592"

if __name__ == "__main__":

    from appium import webdriver
    from appium.webdriver.common.appiumby import AppiumBy
    from appium.options.ios.xcuitest.base import XCUITestOptions
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # Desired capabilities
    desired_capabilities = {
        "platformName": "iOS",
        "appium:udid": "00008110-001974661EF2201E",
        "appium:automationName": "XCUITest",
        "appium:bundleId": "com.apple.mobilephone"
    }

    # Load capabilities into options
    options = XCUITestOptions()
    options.load_capabilities(desired_capabilities)

    # Appium server URL
    appium_server_url = 'http://localhost:4723'

    # Initialize the driver
    driver = webdriver.Remote(appium_server_url, options=options)


    # Loop through each digit and click the corresponding button on the dialer
    for it in input_string:
        # Find the button by accessibility ID (usually, the digits themselves are the accessibility IDs)
        button = WebDriverWait(driver, 0.1).until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, it))
        )
        button.click()

    makecall= WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//XCUIElementTypeButton[@name='ACCEPT']"))
        )
    makecall.click()
    # Quit the driver after the operations
    driver.quit()
