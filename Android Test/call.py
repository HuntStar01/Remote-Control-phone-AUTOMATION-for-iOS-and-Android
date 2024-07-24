from twilio.rest import Client
import time
import subprocess
import logging
from googlesearch import search
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys

error_stack = []
app = QApplication(sys.argv)  # Create QApplication instance

def log_error(error_message):
    error_stack.append(error_message)
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

def check_network_connectivity():
    try:
        output = subprocess.check_output(['adb', 'shell', 'ping', '-c', '1', '8.8.8.8'])
        output_str = output.decode('utf-8')
        return "1 packets transmitted, 1 packets received" in output_str
    except subprocess.CalledProcessError as e:

        return False
    except FileNotFoundError as e:
        log_error("Error: ADB or ping command not found.")
        return False
    except Exception as e:
        log_error(f"An unexpected error occurred while checking network connectivity: {str(e)}")
        return False

def check_airplane_mode():
    try:
        output = subprocess.check_output(['adb', 'shell', 'settings', 'get', 'global', 'airplane_mode_on'])
        return int(output.strip()) == 1
    except subprocess.CalledProcessError as e:
        log_error("Failed to check airplane mode status.")
        return False
    except FileNotFoundError as e:
        log_error("Error: ADB is not installed on your computer. Please install the Android SDK Platform-tools.")
        return False
    except Exception as e:
        log_error(f"An unexpected error occurred while checking airplane mode: {str(e)}")
        return False

def check_call_functionality():
    try:
        if check_network_connectivity() or check_airplane_mode():
            return False
        subprocess.run(['adb', 'shell', 'am', 'start', '-a', 'android.intent.action.CALL', '-d', 'tel:7985662792'])
        print("Test call made.")
        return True
    except FileNotFoundError as e:
        log_error("Error: ADB tool not found. Please make sure you have Android Debug Bridge (adb) installed.")
        return False
    except subprocess.CalledProcessError as e:
        log_error("Failed to make the test call. Check if your device is connected and if ADB has necessary permissions.")
        return False
    except Exception as e:
        log_error(f"An unexpected error occurred while making a test call: {str(e)}")
        return False

def check_call_status():
    try:
        output = subprocess.check_output(['adb', 'shell', 'dumpsys', 'telephony.registry'], text=True)
        call_state = None
        for line in output.splitlines():
            if 'mCallState' in line:
                call_state = line.strip().split('=')[1].strip()
                break
        return call_state
    except subprocess.CalledProcessError as e:
        log_error("Failed to check call status. Please make sure your device is connected and ADB is properly set up.")
        return None
    except FileNotFoundError as e:
        log_error("Error: ADB is not installed on your computer. Please install the Android SDK Platform-tools.")
        return None
    except Exception as e:
        log_error(f"An unexpected error occurred while checking call status: {str(e)}")
        return None

def answer_call():
    try:
        subprocess.run(['adb', 'shell', 'input', 'keyevent', 'KEYCODE_CALL'])
        print("Call answered.")
    except subprocess.CalledProcessError as e:
        log_error("Failed to answer the call.")
    except FileNotFoundError as e:
        log_error("Error: ADB is not installed on your computer. Please install the Android SDK Platform-tools.")
    except Exception as e:
        log_error(f"An unexpected error occurred while answering the call: {str(e)}")

def end_call():
    try:
        if check_network_connectivity() or check_airplane_mode():
            return False
        subprocess.run(['adb', 'shell', 'input', 'keyevent', 'KEYCODE_ENDCALL'], check=True)
        logging.info("Call ended successfully.")
        return True
    except subprocess.CalledProcessError as e:
        log_error("Failed to end the call. Please make sure your device is connected and ADB is properly set up.")
        return False
    except FileNotFoundError as e:
        log_error("Error: ADB is not installed on your computer. Please install the Android SDK Platform-tools.")
        return False
    except Exception as e:
        log_error(f"An unexpected error occurred while ending the call: {str(e)}")
        return False

def make_and_end_call(to_number=None):
    try:
        if not to_number:
            to_number = input("Enter the phone number to call (including country code): ").strip()

        account_sid = '# add your credentials'
        auth_token = '# add your credentials'
        client = Client(account_sid, auth_token)
        call = client.calls.create(
            url='http://demo.twilio.com/docs/voice.xml',
            to=to_number,
            from_='+16068067837'
        )
        print(f"Call {call.sid} has been made.")
        print("Waiting for the call to be received...")
        time.sleep(10)
        call_state = check_call_status()
        if call_state == '1':
            print("Call received.")
            print("Answering the call...")
            answer_call()
            time.sleep(10)
            print("Ending the call...")
            end_call()
            print("Call ended.")
            return True
        else:
            logging.info("Call was not received.")
            return False
    except Exception as e:
        log_error(f"An unexpected error occurred while making and ending the call: {str(e)}")
        return False

def show_error_popup():
    message_box = QMessageBox()
    message_box.setWindowTitle("Error Details")
    message_box.setText("Errors encountered during execution:")
    message_box.setDetailedText("\n".join(error_stack))
    message_box.exec_()

def verify(phone_number=None):
    try:
        if (check_and_turn_on_data_wifi_if_both_off()):
            time.sleep(3)
        call_successful = check_call_functionality()
        time.sleep(5)
        print("Ending call...")
        end_call()
        if not call_successful:
            log_error("Failed to initiate test call , Check your Network Connectivity")
            return False
        
        if make_and_end_call(phone_number):
            time.sleep(5)
            return True
        else:
            return False
    except Exception as e:
        log_error(f"An unexpected error occurred during verification: {str(e)}")
        return False
    finally:
        if error_stack:
            show_error_popup()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if verify(sys.argv[1]):
            print("Verification completed successfully.")
        else:
            print("Verification failed. Check logs for details.")
    else:
        print("Please provide a phone number to verify.")
