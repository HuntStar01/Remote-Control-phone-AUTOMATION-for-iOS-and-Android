import subprocess
import time
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys

# Error stack to store errors
error_stack = []

def log_error(error_message):
    """Logs errors in the error stack."""
    error_stack.append(error_message)

def adb_shell_command(command):
    """Runs an ADB shell command and returns the result."""
    try:
        result = subprocess.run(['adb', 'shell', command], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            error_message = f"Error: {result.stderr.strip()}"
            log_error(error_message)
            return error_message
    except Exception as e:
        error_message = f"Error: {e}"
        log_error(error_message)
        return error_message

def turn_off_data_if_on():
    """Turns off mobile data if it is on."""
    try:
        current_state = adb_shell_command('settings get global mobile_data')
        if current_state == '1':
            adb_shell_command('svc data disable')
            print("Turned off mobile data")
        else:
            print("Mobile data is already off")
    except Exception as e:
        log_error(f"Error turning off mobile data: {e}")

def turn_off_wifi_if_on():
    """Turns off Wi-Fi if it is on."""
    try:
        current_state = adb_shell_command('dumpsys wifi | grep "Wi-Fi is"')
        if 'enabled' in current_state:
            adb_shell_command('svc wifi disable')
            print("Turned off Wi-Fi")
        else:
            print("Wi-Fi is already off")
    except Exception as e:
        log_error(f"Error turning off Wi-Fi: {e}")

def is_music_playing():
    """Checks if music is currently playing."""
    try:
        output = adb_shell_command('dumpsys media_session')
        for line in output.splitlines():
            if 'state=PlaybackState {' in line and 'state=3' in line:
                return True
        return False
    except Exception as e:
        log_error(f"Error checking music state: {e}")
        return False

def is_speaker_on():
    """Checks if the speaker is on."""
    try:
        output = adb_shell_command('dumpsys audio')
        for line in output.splitlines():
            if 'SCO_STATE_ACTIVE_INTERNAL' in line or 'STREAM_MUSIC' in line:
                return True
        return False
    except Exception as e:
        log_error(f"Error checking speaker state: {e}")
        return False

def push_music_to_device(local_file, device_dir):
    """Pushes a music file to the device."""
    try:
        local_file_unix = local_file.replace("\\", "/")
        device_path = f"{device_dir.rstrip('/')}/{os.path.basename(local_file)}"
        result = subprocess.run(['adb', 'push', local_file_unix, device_path], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Pushed {local_file} to {device_path}")
            return True
        else:
            error_message = f"Error pushing {local_file}: {result.stdout}"
            log_error(error_message)
            return False
    except Exception as e:
        error_message = f"Error: {e}"
        log_error(error_message)
        return False

def play_music(device_path):
    """Plays the specified music file on the device."""
    command = f"am start -a android.intent.action.VIEW -d file://{device_path} -t audio/mp3"
    try:
        result = subprocess.run(['adb', 'shell', command], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Started playing music: {device_path}")
            return True
        else:
            error_message = f"Error playing music: {result.stdout}"
            log_error(error_message)
            return False
    except Exception as e:
        error_message = f"Error: {e}"
        log_error(error_message)
        return False

def pause_music():
    """Pauses the currently playing music."""
    command = "input keyevent 85"
    try:
        result = adb_shell_command(command)
        if "Error" in result:
            log_error(f"Error pausing music: {result}")
            return False
        else:
            print("Music paused")
            return True
    except Exception as e:
        log_error(f"Error pausing music: {e}")
        return False

def get_current_song_metadata():
    """Retrieves the metadata of the current song."""
    try:
        output = adb_shell_command('dumpsys media_session')
        metadata = ""
        for line in output.splitlines():
            if 'description=' in line:
                metadata = line.split('description=')[1].strip()
                break
        return metadata
    except Exception as e:
        log_error(f"Error retrieving song metadata: {e}")
        return ""

def compare_song_metadata(metadata_before, metadata_after):
    """Compares song metadata to determine if they are the same."""
    return metadata_before == metadata_after

def next_song():
    """Skips to the next song."""
    adb_shell_command('input keyevent 87')

def previous_music():
    """Skips to the previous song."""
    adb_shell_command('input keyevent 88')

def sound_result():
    """Checks if music is playing and the speaker is on."""
    return is_music_playing() and is_speaker_on()

def run_full_test(local_file, device_dir):
    """Runs the full test sequence."""
    try:
        # Turn off data and Wi-Fi if they are on
        turn_off_data_if_on()
        turn_off_wifi_if_on()
        
        if not push_music_to_device(local_file, device_dir):
            return False
        
        time.sleep(5)
        
        device_path = f"{device_dir.rstrip('/')}/{os.path.basename(local_file)}"
        if not play_music(device_path):
            return False
        
        time.sleep(10)
        
        metadata_before = get_current_song_metadata()
        print("Current song metadata before:", metadata_before)
        
        if not sound_result():
            log_error("Music is not playing")
            return False

        if not pause_music():
            log_error("Music was not paused")
            return False
        
        time.sleep(3)

        if sound_result():
            return False

        next_song()
        time.sleep(2)
        
        metadata_after = get_current_song_metadata()
        print("Current song metadata after:", metadata_after)

        if compare_song_metadata(metadata_before, metadata_after):
            log_error("Error occured in playing music")
            return False
        
        previous_music()
        time.sleep(2)
        
        metadata_after_prev = get_current_song_metadata()
        print("Current song metadata after previous:", metadata_after_prev)

        if not compare_song_metadata(metadata_after_prev, metadata_before):
            log_error("Current song metadata after previous was same")
            return False
        
        pause_music()

        return True
    
    except Exception as e:
        log_error(f"Error during test: {e}")
        return False

def show_error_popup():
    """Displays error stack in a message box."""
    app = QApplication(sys.argv)
    message_box = QMessageBox()
    message_box.setWindowTitle("Error Details")
    message_box.setText("Errors encountered during execution:")
    message_box.setDetailedText("\n".join(error_stack))
    message_box.exec_()
    

def test_next_previous():
    """Runs the test and handles errors."""
    music_file = r"enchanting_flute.mp3"  # Replace with your local music file path
    device_directory = "/sdcard/Music"

    if run_full_test(music_file, device_directory):
        return True
    else:
        if error_stack:
            show_error_popup()
        return False

if __name__ == "__main__":
    if test_next_previous():
        print("Test completed successfully.")
    else:
        print("Test failed. Check logs for details.")
