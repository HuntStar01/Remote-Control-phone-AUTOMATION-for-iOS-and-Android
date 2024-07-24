import sys
import subprocess
import time
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QInputDialog, QHBoxLayout)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QTimer

# Function to execute ADB command
def execute_adb_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True, encoding='utf-8')
        if result.returncode != 0:
            print(f"Error executing command '{command}': {result.stderr}")
            return None
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e}")
        return None
    except UnicodeDecodeError as uderr:
        print(f"Error decoding command output: {uderr}")
        return None
    except Exception as ex:
        print(f"Unexpected error executing command '{command}': {ex}")
        return None

# Function to find package name of an app
def find_package_name(app_name):
    try:
        package_command = f'adb shell pm list packages -f'
        package_result = execute_adb_command(package_command)
        if package_result:
            lines = package_result.splitlines()
            package_name = None
            for line in lines:
                if app_name.lower() in line.lower():  # Case insensitive search
                    package_name = line.split('=')[-1].strip()
                    break
            if not package_name:
                print(f"Package '{app_name}' not found in package list.")
            return package_name
        else:
            print("No packages found.")
            return None
    except Exception as e:
        print(f"Error finding package name: {e}")
        return None

class RemoteControlGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Remote Control for Phone')
        self.setGeometry(1300, 100, 400, 600)
        self.setWindowIcon(QIcon(""))  # Set an icon for the window if available

        # Layout
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Heading
        heading_label = QLabel('Remote Control for Phone', self)
        heading_label.setFont(QFont('Arial', 18, QFont.Bold))
        heading_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(heading_label)

        # Labels for Battery Level and Device Name
        self.battery_label = QLabel('', self)
        self.battery_label.setFont(QFont('Arial', 12))
        self.battery_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.battery_label)

        self.device_name_label = QLabel('', self)
        self.device_name_label.setFont(QFont('Arial', 12))
        self.device_name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.device_name_label)

        # Small Buttons Layout
        small_buttons_layout = QHBoxLayout()
        small_buttons_layout.setSpacing(15)

        def create_circular_button(text, color, function):
            button = QPushButton(text, self)
            button.setFont(QFont('Arial', 12))
            button.setFixedSize(60, 60)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 30px;
                }}
                QPushButton:pressed {{
                    background-color: darken({color}, 20%);
                }}
            """)
            button.clicked.connect(function)
            return button

        # Adding small buttons to layout
        small_buttons_layout.addWidget(create_circular_button('Vol +', '#607D8B', self.volume_up))
        small_buttons_layout.addWidget(create_circular_button('Vol -', '#607D8B', self.volume_down))
        small_buttons_layout.addWidget(create_circular_button('WiFi', '#2196F3', self.wifi))
        small_buttons_layout.addWidget(create_circular_button('BT', '#9C27B0', self.bluetooth))
        small_buttons_layout.addWidget(create_circular_button('Data', '#4CAF50', self.mobile_data))

        layout.addLayout(small_buttons_layout)

        # Main Buttons Layout
        main_buttons_layout = QVBoxLayout()
        main_buttons_layout.setSpacing(15)
        main_buttons_layout.setAlignment(Qt.AlignCenter)  # Center align the buttons

        def create_rounded_button(text, color, function):
            button = QPushButton(text, self)
            button.setFont(QFont('Arial', 12))
            button.setFixedSize(200, 50)  # Adjust size for rectangular with rounded edges
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 10px;  # Adjusted for rounded edges
                }}
                QPushButton:pressed {{
                    background-color: darken({color}, 20%);
                }}
            """)
            button.clicked.connect(function)
            return button

        
        main_buttons_layout.addWidget(create_rounded_button('Call', '#4CAF50', self.make_call))
        main_buttons_layout.addWidget(create_rounded_button('Message', '#4CAF50', self.send_message))
        main_buttons_layout.addWidget(create_rounded_button('Chrome', '#2196F3', self.open_chrome))
        main_buttons_layout.addWidget(create_rounded_button('YouTube', '#FF0000', self.open_youtube))
        main_buttons_layout.addWidget(create_rounded_button('Photos', '#FF9800', self.open_photos))
        main_buttons_layout.addWidget(create_rounded_button('Lock Device', '#F44336', self.lock_device))

        layout.addLayout(main_buttons_layout)

        # Input for custom command
        self.command_input = QLineEdit(self)
        self.command_input.setFont(QFont('Arial', 12))
        self.command_input.setPlaceholderText("Enter app name to open...")
        layout.addWidget(self.command_input)

        # Button: Execute Custom Command
        btn_execute_command = QPushButton('Execute', self)
        btn_execute_command.setFont(QFont('Arial', 14))
        btn_execute_command.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:pressed {
                background-color: darken(#9C27B0, 20%);
            }
        """)
        btn_execute_command.clicked.connect(self.execute_custom_command)
        layout.addWidget(btn_execute_command)

        layout.addStretch()
        self.setLayout(layout)

        # Start a timer to update battery status, level, and device info every 5 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_battery_and_device_info)
        self.timer.start(5000)  # Update every 5 seconds

        self.update_battery_and_device_info()  # Initial update

        self.show()

    def update_battery_and_device_info(self):
        # Update battery level and status
        battery_command = ['adb', 'shell', 'dumpsys', 'battery']
        battery_result = execute_adb_command(battery_command)
        if battery_result:
            battery_level = self.extract_battery_level(battery_result)
            self.battery_label.setText(f'Battery {battery_level}')
        else:
            self.battery_label.setText('Failed to retrieve battery status.')

        # Update device name
        device_info_command = ['adb', 'shell', 'getprop', 'ro.product.model']
        device_info_result = execute_adb_command(device_info_command)
        if device_info_result:
            self.device_name_label.setText(f'Device Name: {device_info_result}')
        else:
            self.device_name_label.setText('Failed to retrieve device name.')

    def extract_battery_level(self, battery_output):
        lines = battery_output.splitlines()
        for line in lines:
            if 'level:' in line.lower():
                return line.strip()

    def make_call(self):
        if not self.is_phone_ready():
            QMessageBox.warning(self, 'Error', 'Phone is in airplane mode or no SIM card detected.')
            return

        phone_number, ok = QInputDialog.getText(self, 'Make Call', 'Enter phone number (with country code +91):')
        if ok and phone_number:
            if self.is_valid_phone_number(phone_number):
                command = ['adb', 'shell', 'am', 'start', '-a', 'android.intent.action.CALL', '-d', f'tel:{phone_number}']
                result = self.execute_adb_command(command)
                if result:
                    QMessageBox.information(self, 'Command Result', f"Call initiated to {phone_number}.")
                else:
                    QMessageBox.warning(self, 'Error', f"Failed to make call to {phone_number}.")
            else:
                QMessageBox.warning(self, 'Error', 'Invalid phone number. Ensure it includes country code +91 and is 10 digits long after the country code.')

    def send_message(self):
        if not self.is_phone_ready():
            QMessageBox.warning(self, 'Error', 'Phone is in airplane mode or no SIM card detected.')
            return

        phone_number, ok = QInputDialog.getText(self, 'Send Message', 'Enter phone number:')
        if ok and phone_number:
            message_content, ok = QInputDialog.getText(self, 'Send Message', 'Enter message:')
            if ok and message_content:
                command = [
                    'adb', 'shell', 'am', 'start', '-a', 'android.intent.action.SENDTO',
                    '-d', f'sms:{phone_number}', '--es', 'sms_body', message_content
                ]
                result = self.execute_adb_command(command)
                if result:
                    time.sleep(2)  # Give time for the message app to open and populate the message
                    # Simulate ENTER key press to send the message
                    send_command = ['adb', 'shell', 'input', 'keyevent', '66']  # Keycode 66 is the ENTER key
                    send_result = self.execute_adb_command(send_command)
                    if send_result:
                        QMessageBox.information(self, 'Command Result', f"Message sent to {phone_number}.")
                    else:
                        QMessageBox.warning(self, 'Error', f"Failed to send message to {phone_number}.")
                else:
                    QMessageBox.warning(self, 'Error', f"Failed to open messaging app for {phone_number}.")

    def is_phone_ready(self):
        # Check if phone is in airplane mode or no SIM card
        try:
            # Check if airplane mode is enabled
            airplane_mode_command = ['adb', 'shell', 'settings', 'get', 'global', 'airplane_mode_on']
            airplane_mode_result = self.execute_adb_command(airplane_mode_command).strip()
            if airplane_mode_result == '1':
                return False

            # Check SIM card status
            sim_status_command = ['adb', 'shell', 'service', 'call', 'iphonesubinfo', '1']
            sim_status_result = self.execute_adb_command(sim_status_command)
            if "error" in sim_status_result.lower():
                return False

            return True

        except Exception as e:
            print(f"Exception occurred: {e}")
            return False

    def execute_adb_command(self, command):
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error executing command {command}: {e}")
            return None

    def is_valid_phone_number(self, phone_number):
        # Validate phone number format (dummy validation for example)
        if phone_number.startswith('+91') and len(phone_number) == 13 and phone_number[3:].isdigit():
            return True
        return False

    def open_chrome(self):
        command = ['adb', 'shell', 'am', 'start', '-n', 'com.android.chrome/com.google.android.apps.chrome.Main']
        result = execute_adb_command(command)
        if result:
            QMessageBox.information(self, 'Command Result', "Chrome opened successfully.")
        else:
            QMessageBox.warning(self, 'Error', "Failed to open Chrome.")

    def open_youtube(self):
        command = ['adb', 'shell', 'am', 'start', '-n', 'com.google.android.youtube/com.google.android.youtube.HomeActivity']
        result = execute_adb_command(command)
        if result:
            QMessageBox.information(self, 'Command Result', "YouTube opened successfully.")
        else:
            QMessageBox.warning(self, 'Error', "Failed to open YouTube.")

    def open_photos(self):
        command = ['adb', 'shell', 'am', 'start', '-n', 'com.google.android.apps.photos/com.google.android.apps.photos.home.HomeActivity']
        result = execute_adb_command(command)
        if result:
            QMessageBox.information(self, 'Command Result', "Photos opened successfully.")
        else:
            QMessageBox.warning(self, 'Error', "Failed to open Photos.")

    def execute_custom_command(self):
        app_name = self.command_input.text()
        if app_name:
            package_name = find_package_name(app_name)
            if package_name:
                # Modify the command to use the main activity
                command = f'adb shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1'
                result = execute_adb_command(command)
                if result:
                    QMessageBox.information(self, 'Command Result', f"{app_name.capitalize()} opened successfully.")
                else:
                    QMessageBox.warning(self, 'Error', f"Failed to open {app_name}.")
            else:
                QMessageBox.warning(self, 'Error', f"Package for {app_name} not found.")

    def lock_device(self):
        command = ['adb', 'shell', 'input', 'keyevent', '26']  # Keycode for POWER (lock device)
        result = execute_adb_command(command)
        if result is not None:
            QMessageBox.information(self, 'Command Result', "Device locked successfully.")
        else:
            QMessageBox.warning(self, 'Error', "Failed to lock the device.")

    def volume_up(self):
        command = ['adb', 'shell', 'input', 'keyevent', '24']  # Keycode for Volume Up
        result = execute_adb_command(command)
        if result is None:
            QMessageBox.warning(self, 'Error', "Failed to increase volume.")

    def volume_down(self):
        command = ['adb', 'shell', 'input', 'keyevent', '25']  # Keycode for Volume Down
        result = execute_adb_command(command)
        if result is None:
            QMessageBox.warning(self, 'Error', "Failed to decrease volume.")

    def get_airplane_mode_status(self):
        command_check_status = ['adb', 'shell', 'settings', 'get', 'global', 'airplane_mode_on']
        status = execute_adb_command(command_check_status)
        if status == '1':
            return 'enabled'
        elif status == '0':
            return 'disabled'
        else:
            return None

    def airplane_mode(self):
        # Step 1: Get current Airplane Mode status
        current_status = self.get_airplane_mode_status()
        if current_status is None:
            QMessageBox.warning(self, 'Error', "Failed to get Airplane Mode status.")
            return

        # Step 2: Open Airplane Mode Settings
        command_open_settings = ['adb', 'shell', 'am', 'start', '-a', 'android.settings.AIRPLANE_MODE_SETTINGS']
        result_open_settings = execute_adb_command(command_open_settings)
        if result_open_settings is None:
            QMessageBox.warning(self, 'Error', "Failed to open Airplane Mode settings.")
            return

        # Give it time to open
        time.sleep(2)

        # Step 3: Tap the first row (Airplane Mode toggle)
        command_tap_airplane_mode = ['adb', 'shell', 'input', 'tap', '540', '300']  # Adjust coordinates as necessary
        result_tap_airplane_mode = execute_adb_command(command_tap_airplane_mode)

        if result_tap_airplane_mode is None:
            QMessageBox.warning(self, 'Error', "Failed to toggle Airplane mode.")
            return

        # Give it time to apply the change
        time.sleep(2)

        # Step 4: Get new Airplane Mode status
        new_status = self.get_airplane_mode_status()
        if new_status is None:
            QMessageBox.warning(self, 'Error', "Failed to get new Airplane Mode status.")
        else:
            QMessageBox.information(self, 'Command Result', f"Airplane mode {new_status}.")

    def mobile_data(self):
        # Check current mobile data state
        current_state = execute_adb_command(['adb', 'shell', 'settings', 'get', 'global', 'mobile_data'])
        if current_state and '1' in current_state:
            # Disable mobile data
            command = ['adb', 'shell', 'svc', 'data', 'disable']
            state = "disabled"
        else:
            # Enable mobile data
            command = ['adb', 'shell', 'svc', 'data', 'enable']
            state = "enabled"

        result = execute_adb_command(command)
        if result is not None:
            QMessageBox.information(self, 'Command Result', f"Mobile data {state}.")
        else:
            QMessageBox.warning(self, 'Error', f"Failed to {state} mobile data.")

    def wifi(self):
        current_state = execute_adb_command(['adb', 'shell', 'dumpsys', 'wifi | grep "Wi-Fi is"'])
        if current_state and 'enabled' in current_state:
            command = ['adb', 'shell', 'svc', 'wifi', 'disable']
            state = "disabled"
        else:
            command = ['adb', 'shell', 'svc', 'wifi', 'enable']
            state = "enabled"

        result = execute_adb_command(command)
        if result is not None:
            QMessageBox.information(self, 'Command Result', f"WiFi {state}.")
        else:
            QMessageBox.warning(self, 'Error', f"Failed to {state} WiFi.")

    def bluetooth(self):
        # Check current Bluetooth status
        check_bluetooth_command = ['adb', 'shell', 'settings', 'get', 'global', 'bluetooth_on']
        status_result = execute_adb_command(check_bluetooth_command)

        if status_result is not None:
            if status_result == '1':
                # Disable Bluetooth
                toggle_bluetooth_command = ['adb', 'shell', 'svc', 'bluetooth', 'disable']
                result = execute_adb_command(toggle_bluetooth_command)
                if result:
                    QMessageBox.information(self, 'Command Result', "Bluetooth disabled.")
                else:
                    QMessageBox.warning(self, 'Error', "Failed to disable Bluetooth.")
            elif status_result == '0':
                # Enable Bluetooth
                toggle_bluetooth_command = ['adb', 'shell', 'svc', 'bluetooth', 'enable']
                result = execute_adb_command(toggle_bluetooth_command)
                if result:
                    QMessageBox.information(self, 'Command Result', "Bluetooth enabled.")
                else:
                    QMessageBox.warning(self, 'Error', "Failed to enable Bluetooth.")
            else:
                QMessageBox.warning(self, 'Error', "Unknown Bluetooth status.")
        else:
            QMessageBox.warning(self, 'Error', "Failed to check Bluetooth status.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RemoteControlGUI()
    sys.exit(app.exec_())
