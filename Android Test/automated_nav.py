import subprocess
import time
import pyautogui
import cv2
import numpy as np
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys

# Error stack to store errors
error_stack = []

def log_error(error_message):
    """Logs errors in the error stack."""
    error_stack.append(error_message)


# Function for image comparison
def capture_screen():
    try:
        # Capture screen using adb command
        process = subprocess.Popen(['adb', 'exec-out', 'screencap', '-p'], stdout=subprocess.PIPE)
        output, _ = process.communicate()

        # Convert output to numpy array
        np_array = np.frombuffer(output, dtype=np.uint8)

        # Decode image
        return cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    except Exception as e:
        log_error(f"Error capturing screen: {e}")
        return None

# Function to capture the phone screen directly
def capture_direct_screen(filename):
    try:
        # Capture screen using adb shell screencap command
        subprocess.run(['adb', 'shell', 'screencap', f'/sdcard/{filename}'])
        # Pull the screenshot from the device
        subprocess.run(['adb', 'pull', f'/sdcard/{filename}', 'direct_screenshots'])
    except Exception as e:
        log_error(f"Error pulling direct screenshot: {e}")

def compare_images(img1, img2):
    try:
        # Convert images to grayscale
        gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Compute Mean Squared Error (MSE)
        mse = np.mean((gray_img1 - gray_img2) ** 2)

        # Compute Peak Signal-to-Noise Ratio (PSNR)
        psnr = cv2.PSNR(gray_img1, gray_img2)

        # Compute Histogram Comparison
        hist_img1 = cv2.calcHist([gray_img1], [0], None, [256], [0, 256])
        hist_img2 = cv2.calcHist([gray_img2], [0], None, [256], [0, 256])
        hist_corr = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_CORREL)

        return mse, psnr, hist_corr
    except Exception as e:
        log_error(f"Error comparing images: {e}")
        return None, None, None

# Function to check if images match
def check_images_match(img1, img2):
    try:
        # Compare images using multiple metrics
        mse, psnr, hist_corr = compare_images(img1, img2)

        # Define thresholds for each metric
        mse_threshold = 100
        psnr_threshold = 30
        hist_corr_threshold = 0.95

        # Check if all metrics meet their thresholds
        if mse < mse_threshold and psnr > psnr_threshold and hist_corr > hist_corr_threshold:
            return True
        else:
            return False
    except Exception as e:
        log_error(f"Error checking images match: {e}")
        return False

# Function to perform navigation actions and observe mirrored screen
def verify_navigation():
    try:
        os.makedirs("direct_screenshots", exist_ok=True)
        os.makedirs("mirrored_screenshots", exist_ok=True)


        # Wait for scrcpy to initialize (adjust delay as needed)
        

        # Perform navigation actions on the phone
        print("Performing navigation actions on your phone...")

        # Wait for animation to complete (adjust delay as needed)
        time.sleep(1)

        # Swipe down to access notification panel
        pyautogui.moveTo(1000, 150)  # Move mouse to middle of the screen
        pyautogui.dragTo(1000, 900, duration=0.7)
        time.sleep(1)

        capture_direct_screen("screenshot_before.png")

        # Capture the screen from mirror before scrolling down
        mirrored_screenshot_before = capture_screen()
        if mirrored_screenshot_before is None:
            log_error("Cannot capture Screenshot")
            return False

        cv2.imwrite("mirrored_screenshots/screenshot_mirrored_before.png", mirrored_screenshot_before)

        # Allow time for navigation actions to be performed (adjust delay as needed)

        # Close the notification panel
        pyautogui.moveTo(1000, 800)  # Move mouse to middle of the screen
        pyautogui.dragTo(1000, 100, duration=0.7)
        

        capture_direct_screen("screenshot_after_down.png")

        # Capture the screen from mirror after scrolling down
        mirrored_screenshot_after_down = capture_screen()
        if mirrored_screenshot_after_down is None:
            log_error("Cannot capture Screenshot")
            return False

        cv2.imwrite("mirrored_screenshots/screenshot_mirrored_after_down.png", mirrored_screenshot_after_down)

        

        # Open app drawer
        pyautogui.moveTo(1000, 800)  # Move mouse to middle of the screen
        pyautogui.dragTo(1000, 200, duration=0.8)  # Increased swipe distance
        time.sleep(1)

        capture_direct_screen("screenshot_after_up.png")

        # Capture the screen from mirror after scrolling up
        mirrored_screenshot_after_up = capture_screen()
        if mirrored_screenshot_after_up is None:
            log_error("Cannot capture Screenshot")
            return False

        cv2.imwrite("mirrored_screenshots/screenshot_mirrored_after_up.png", mirrored_screenshot_after_up)

        # Close app drawer
        pyautogui.moveTo(1000, 200)  # Move mouse to middle of the screen
        pyautogui.dragTo(1000, 2200, duration=0.7)  # Increased swipe distance
        

        # Navigate right to left
        pyautogui.moveTo(1100, 500)  # Move mouse to middle of the screen
        pyautogui.dragTo(800, 500, duration=0.7)
    

        capture_direct_screen("screenshot_after_left.png")

        # Capture the screen from mirror after scrolling up
        mirrored_screenshot_after_left = capture_screen()
        if mirrored_screenshot_after_left is None:
            log_error("Cannot capture Screenshot")
            return False

        cv2.imwrite("mirrored_screenshots/screenshot_mirrored_after_left.png", mirrored_screenshot_after_left)

        # Navigate left to right
        pyautogui.moveTo(800, 500)  # Move mouse to middle of the screen
        pyautogui.dragTo(1100, 500, duration=0.7)

        # Compare screenshots
        direct_screenshot_before = cv2.imread("direct_screenshots/screenshot_before.png")
        mirrored_screenshot_before = cv2.imread("mirrored_screenshots/screenshot_mirrored_before.png")

        direct_screenshot_after_down = cv2.imread("direct_screenshots/screenshot_after_down.png")
        mirrored_screenshot_after_down = cv2.imread("mirrored_screenshots/screenshot_mirrored_after_down.png")

        direct_screenshot_after_up = cv2.imread("direct_screenshots/screenshot_after_up.png")
        mirrored_screenshot_after_up = cv2.imread("mirrored_screenshots/screenshot_mirrored_after_up.png")
        
        # Compare screenshots
        if check_images_match(direct_screenshot_before, mirrored_screenshot_before) and \
            check_images_match(direct_screenshot_after_down, mirrored_screenshot_after_down) and \
            check_images_match(direct_screenshot_after_up, mirrored_screenshot_after_up):
            if check_images_match(direct_screenshot_before, direct_screenshot_after_down) or \
            check_images_match(direct_screenshot_after_down, direct_screenshot_before):
                log_error("Images are same for before swipe and after swipe")
                return False
            else:
                return True
        else:
            log_error("Mirrored and Direct screenshot are same")
            return False
    except Exception as e:
        log_error(f"Error in verify_navigation: {e}")
        return False

def show_error_popup():
    """Displays error stack in a message box."""
    app = QApplication(sys.argv)
    message_box = QMessageBox()
    message_box.setWindowTitle("Error Details")
    message_box.setText("Errors encountered during execution:")
    message_box.setDetailedText("\n".join(error_stack))
    message_box.exec_()

# Main function
def main():
    # Perform navigation verification
    if verify_navigation():
        return True
    else:
        if error_stack:
            show_error_popup()
        return False

if __name__ == "__main__":
    main()
