import subprocess
import cv2
import pytesseract
from pytesseract import Output
import numpy as np
import time
import re
import requests
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys

# Set Tesseract path (adjust as per your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize QApplication instance
app = QApplication(sys.argv)

# Error stack to store errors
error_stack = []

# Function to log errors in the error stack
def log_error(error_message):
    error_stack.append(error_message)

# Function to run adb commands
def run_adb_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip(), True
    except subprocess.CalledProcessError as e:
        log_error(f"Error running command: {' '.join(command)}")
        return e.stdout.strip(), False
    except Exception as e:
        log_error(f"Error running command: {' '.join(command)}")
        return "", False

def turn_on_data_if_off():
    try:
        current_state, success = run_adb_command(['adb', 'shell', 'settings', 'get', 'global', 'mobile_data'])
        if not success:
            return
        if current_state == '0':
            run_adb_command(['adb', 'shell', 'svc', 'data', 'enable'])
            print("Turned on mobile data")
        else:
            print("Mobile data is already on")
    except Exception as e:
        log_error(f"Error turning on mobile data: {e}")

def turn_on_wifi_if_off():
    try:
        current_state, success = run_adb_command(['adb', 'shell', 'dumpsys', 'wifi'])
        if not success:
            return
        if 'Wi-Fi is disabled' in current_state:
            run_adb_command(['adb', 'shell', 'svc', 'wifi', 'enable'])
            print("Turned on Wi-Fi")
        else:
            print("Wi-Fi is already on")
    except Exception as e:
        log_error(f"Error turning on Wi-Fi: {e}")

def check_and_turn_on_data_wifi_if_both_off():
    try:
        data_state, data_success = run_adb_command(['adb', 'shell', 'settings', 'get', 'global', 'mobile_data'])
        wifi_state, wifi_success = run_adb_command(['adb', 'shell', 'dumpsys', 'wifi'])
        
        if not data_success or not wifi_success:
            return
        
        if data_state == '0' and 'Wi-Fi is disabled' in wifi_state:
            turn_on_data_if_off()
            turn_on_wifi_if_off()
        else:
            print("Either mobile data or Wi-Fi is already on.")
    except Exception as e:
        log_error(f"Error checking and turning on data/Wi-Fi: {e}")

# Function to display error stack in a message box
def show_error_popup():
    message_box = QMessageBox()
    message_box.setWindowTitle("Error Details")
    message_box.setText("Errors encountered during execution:")
    message_box.setDetailedText("\n".join(error_stack))
    message_box.exec_()
    

def open_google_maps():
    try:
        run_adb_command(['adb', 'shell', 'am', 'start', '-n', 'com.google.android.apps.maps/com.google.android.maps.MapsActivity'])
    except Exception as e:
        log_error(f"An unexpected error occurred while opening Google Maps: {e}")

def zoom_in(x, y):
    try:
        run_adb_command(['adb', 'shell', 'input', 'tap', str(x), str(y)])
    except Exception as e:
        log_error(f"An unexpected error occurred while zooming in: {e}")

def capture_screen(filename):
    try:
        run_adb_command(['adb', 'shell', 'screencap', '-p', '/sdcard/' + filename])
        run_adb_command(['adb', 'pull', '/sdcard/' + filename, '.'])
        print("Screenshot captured and saved as:", filename)
    except Exception as e:
        log_error(f"An unexpected error occurred while capturing screen: {e}")

def compare_images(image1, image2):
    try:
        img1 = cv2.imread(image1, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(image2, cv2.IMREAD_GRAYSCALE)
        difference = cv2.subtract(img1, img2)
        result = cv2.countNonZero(difference) > 0
        return result
    except Exception as e:
        log_error(f"Error comparing images: {e}")
        return False

def check_zoom_in_changes():
    try:
        check_and_turn_on_data_wifi_if_both_off()
        
        x_coordinate = 500
        y_coordinate = 1200

        open_google_maps()
        time.sleep(5)

        capture_screen('before_zoom_in.png')

        zoom_in(x_coordinate, y_coordinate)
        zoom_in(x_coordinate, y_coordinate)

        time.sleep(5)

        capture_screen('after_zoom_in.png')

        is_different = compare_images('before_zoom_in.png', 'after_zoom_in.png')

        print("Is different:", is_different)

        if is_different:
            print("Images are different. There was a change after zooming in.")
        else:
            print("Images are the same. No change after zooming in.")
            log_error("Images are the same. No change after zooming in.")
            return False

        return is_different

    except Exception as e:
        log_error(f"Error checking zoom in changes: {e}")
        return False

def capture_screenn():
    try:
        process = subprocess.Popen(['adb', 'exec-out', 'screencap', '-p'], stdout=subprocess.PIPE)
        screen_data = process.stdout.read()
        nparr = np.frombuffer(screen_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return frame
    except Exception as e:
        log_error(f"Error capturing screen using exec-out: {e}")
        return None

def extract_time_to_destination(frame):
    try:
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
                        time_to_destination = segment + ' min'
                        return time_to_destination
        
        return None
    except Exception as e:
        log_error(f"Error extracting time to destination: {e}")
        return None

def fetch_travel_time(origin, destination):
    try:
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
                log_error("No route found.")
                return None
        else:
            log_error(f"Failed to fetch travel time: {response.text}")
            return None
    except Exception as e:
        log_error(f"Error fetching travel time: {e}")
        return None

def close_google_maps():
    try:
        run_adb_command(['adb', 'shell', 'input', 'keyevent', 'KEYCODE_BACK'])
    except Exception as e:
        log_error(f"Error closing Google Maps: {e}")

def open_google_maps_with_directions(origin, destination):
    try:
        origin = origin.replace(' ', '%20')
        destination = destination.replace(' ', '%20')
        url = f"google.navigation:q={destination}&origin={origin}&mode=d"
        command = [
            'adb', 'shell', 'am', 'start', '-a', 'android.intent.action.VIEW',
            '-d', url
        ]
        run_adb_command(command)
    except Exception as e:
        log_error(f"Error opening Google Maps with directions: {e}")

def main():
    try:
        city_coordinates = (26.20936905105623, 78.19044021340072)
        chetakpuri_coordinates = (26.201202685712474, 78.17280093756635)
        origin = "City Center, Gwalior"
        destination = "Chetakpuri, Gwalior"
        
        open_google_maps_with_directions(origin, destination)
        time.sleep(14)
        
        screen_frame = capture_screenn()
        if screen_frame is None:
            return False
        
        time_from_image = extract_time_to_destination(screen_frame)
        print('Time to reach destination from image:', time_from_image)
        
        time.sleep(2)
        
        travel_time = fetch_travel_time(city_coordinates, chetakpuri_coordinates)
        if travel_time is None:
            return False
        if travel_time:
            print("Time to reach destination from API:", travel_time , ' min')
            if time_from_image:
                time_from_image_minutes = int(time_from_image.split()[0])  # Extract minutes from the time_from_image
                travel_time_difference = abs(travel_time - time_from_image_minutes)
                if travel_time_difference <= 10:
                    print("Navigation is working fine.")
                    close_google_maps()
                    return True
                else:
                    print("Navigation might not be working as expected.")
                    log_error("Navigation might not be working as expected.")
                    close_google_maps()
                    return False
            else:
                print("No time information found from the image.")
                log_error("No time information found from the image.")
                close_google_maps()
                return False
    
    except Exception as e:
        log_error(f"Error in main function: {e}")
        return False

def compare():
    if check_zoom_in_changes() and main():
        return True
    else:
        if error_stack:
            show_error_popup()
        return False

if __name__ == "__main__":
    if compare():
        print("Comparison completed successfully.")
    else:
        print("Comparison failed. Check logs for details.")
