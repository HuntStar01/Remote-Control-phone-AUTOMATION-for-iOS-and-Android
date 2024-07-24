import time
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.ios.xcuitest.base import XCUITestOptions
import subprocess
import cv2
import pytesseract
from pytesseract import Output
import numpy as np
import time
import requests
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

def fetch_travel_time(origin, destination):
    
        url = f"http://router.project-osrm.org/route/v1/driving/{origin[1]},{origin[0]};{destination[1]},{destination[0]}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'routes' in data and len(data['routes']) > 0:
                route = data['routes'][0]
                travel_time_seconds = route['duration']
                travel_time_minutes = travel_time_seconds / 60
                travel_time_rounded = round(travel_time_minutes)
                return travel_time_rounded
            else:
                
                return None

def extract_time_to_destination(frame):
    
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresholded_frame = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY_INV)
        custom_config = r'--oem 3 --psm 6'
        ocr_data = pytesseract.image_to_data(thresholded_frame, config=custom_config, output_type=Output.DICT)
      
        for i, text in enumerate(ocr_data['text']):
            
            if 'min' in text.lower():
                time_segments = ocr_data['text'][:i]
                time_segments.reverse()
                for segment in time_segments:
                    if segment.isdigit():
                        time_to_destination = segment 
                        return time_to_destination
        
        return None


def capture_screen():
    
    screenshot_path = 'screenshot.png'
# Run the xcrun command to take a screenshot of the booted iOS simulator
    subprocess.run(['xcrun', 'simctl', 'io', 'booted', 'screenshot', screenshot_path], check=True)
    image = Image.open(screenshot_path)
    frame = np.array(image)
    return frame


def setup():
    desired_capabilities = {
        "platformName": "iOS",
        "appium:platformVersion": "17.5",
        "appium:deviceName": "iPhone 15 Pro Max",
        
        "appium:automationName": "XCUITest",
        "bundleId": "com.apple.Maps",
        "appium:noReset": True,
        "udid":"A5A35118-48ED-452D-A9DC-E40A64A5F9E6"

        }
    options = XCUITestOptions()
    options.load_capabilities(desired_capabilities)
    appium_server_url = 'http://localhost:4723'
    driver = webdriver.Remote(appium_server_url, options=options)
    return driver
driver = setup()
driver.implicitly_wait(10)

# Clicked on text field
search_field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "MapsSearchTextField")
search_field.click()
time.sleep(2)

# Type text as 'bridge' under text field
search_field.send_keys("indore")
time.sleep(2)

# Wait for map to load the location
bridgeport_location = driver.find_element(By.XPATH, "//XCUIElementTypeStaticText[@name='PlaceSummaryTitleLabel' and @label='Indore']")
bridgeport_location.click()
time.sleep(5)

# Click on close icon
close_button = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "ActionRowItemTypeDirections")
close_button.click()

time.sleep(2)
driver.find_element(AppiumBy.ACCESSIBILITY_ID, "delete").click()
time.sleep(2)

driver.find_element(AppiumBy.ACCESSIBILITY_ID, "WaypointSearchField").send_keys("sawer")

time.sleep(2)



time.sleep(2)
driver.find_element(By.XPATH,"//XCUIElementTypeStaticText[@name='PlaceSummaryAccessoryViewImageView-PlaceSummaryTitleLabel-PlaceSummaryLabel'and @label='Sawer, Indore, Madhya Pradesh, India']").click()
time.sleep(2)
driver.find_element(By.XPATH,"(//XCUIElementTypeButton[@name='GoButton'])[1]").click()
time.sleep(2)
driver.quit()
time.sleep(2)


frame = capture_screen()
indore_coordinates = (22.724205,75.6990324)
sanwer_coordinates = (22.969443,75.8168618)


time1=fetch_travel_time(sanwer_coordinates,indore_coordinates)
time2=extract_time_to_destination(frame)

print(time1)
print(time2)
time_minutes = int(time2.split()[0])

travel_time_difference = abs(time1 - time_minutes)
if travel_time_difference <= 10:
    print("Navigation is working fine.")
    



