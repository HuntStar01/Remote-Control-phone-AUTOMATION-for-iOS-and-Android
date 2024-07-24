import re
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QMessageBox,
                             QInputDialog, QVBoxLayout, QDialog, QFormLayout, QLineEdit,
                             QTextEdit, QDialogButtonBox)
from PyQt5.QtGui import QPixmap, QLinearGradient, QColor, QPalette
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QDate
import subprocess
import automated_nav
import call
import map_navigation_test
import music_test
import json
import os

class FeedbackDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Feedback Form")
        self.setGeometry(100, 100, 400, 300)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        self.feedback_input = QTextEdit()

        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Feedback:", self.feedback_input)

        layout.addLayout(form_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

        self.setLayout(layout)

    def accept(self):
        username = self.username_input.text()
        feedback = self.feedback_input.toPlainText()

        if not username or not feedback:
            QMessageBox.warning(self, "Input Error", "Please enter both username and feedback.")
            return

        feedback_data = {
            "username": username,
            "feedback": feedback,
            "date": QDate.currentDate().toString(Qt.ISODate)
        }

        feedback_dir = "feedback"
        os.makedirs(feedback_dir, exist_ok=True)

        feedback_file = os.path.join(feedback_dir, f"{username}.json")

        with open(feedback_file, 'w') as f:
            json.dump(feedback_data, f, indent=4)

        QMessageBox.information(self, "Success", "Feedback submitted successfully!")
        super().accept()

class HoverButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(200, 40)
        self.set_default_style()

    def set_default_style(self):
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #8e44ad;
                border: 2px solid #512e5f;
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #9b59b6;
                border-radius: 10px;
            }
            QPushButton:pressed {
                background-color: #6c3483;
                border-radius: 10px;
            }
            """
        )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phone Automation Testing")
        self.setGeometry(100, 100, 600, 700)  # Increased height to accommodate new button
        self.scrcpy_process = None  # Store reference to the scrcpy process
        self.remote_control_process = None  # Store reference to the remote control process

        self.initUI()

    def initUI(self):
        # Set background gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(51, 51, 51))  # Darker gray
        gradient.setColorAt(1.0, QColor(102, 102, 102))  # Lighter gray

        palette = self.palette()  # Get the current palette
        palette.setBrush(QPalette.Window, gradient)  # Set background brush to gradient
        self.setPalette(palette)  # Apply the modified palette to the main window

        # Heading image
        heading_label = QLabel(self)
        heading_label.setGeometry(250, 20, 100, 120)  # Centered heading
        heading_pixmap = QPixmap("heading.png")
        heading_label.setPixmap(heading_pixmap)
        heading_label.setScaledContents(True)

        # Calculate central x-coordinate for buttons
        button_x = (self.width() - 200) // 2
        button_y_start = 150
        button_y_offset = 50

        # Buttons
        self.start_button = HoverButton("Start Mirror", self)
        self.start_button.setGeometry(button_x, button_y_start, 200, 40)
        self.start_button.clicked.connect(self.start_screen_mirroring)

        self.test_button = HoverButton("Test Screen Mirroring", self)
        self.test_button.setGeometry(button_x, button_y_start + button_y_offset, 200, 40)
        self.test_button.clicked.connect(self.test_screen_mirror)

        self.test_button_music = HoverButton("Test Music", self)
        self.test_button_music.setGeometry(button_x, button_y_start + 2 * button_y_offset, 200, 40)
        self.test_button_music.clicked.connect(self.music_check)

        self.test_call_button = HoverButton("Test Call", self)
        self.test_call_button.setGeometry(button_x, button_y_start + 3 * button_y_offset, 200, 40)
        self.test_call_button.clicked.connect(self.test_call)

        self.test_nav = HoverButton("Test Navigation", self)
        self.test_nav.setGeometry(button_x, button_y_start + 4 * button_y_offset, 200, 40)
        self.test_nav.clicked.connect(self.test_navigation)

        self.auto_test_button = HoverButton("Auto Test", self)
        self.auto_test_button.setGeometry(button_x, button_y_start + 5 * button_y_offset, 200, 40)
        self.auto_test_button.clicked.connect(self.auto_test)

        self.retest_button = HoverButton("Retest", self)
        self.retest_button.setGeometry(button_x, button_y_start + 6 * button_y_offset, 200, 40)
        self.retest_button.clicked.connect(self.reset_tests)

        # New button for remote control
        self.remote_control_button = HoverButton("Remote Control", self)
        self.remote_control_button.setGeometry(button_x, button_y_start + 7 * button_y_offset, 200, 40)
        self.remote_control_button.clicked.connect(self.execute_remote_control)

        # Feedback button
        self.feedback_button = HoverButton("Feedback", self)
        self.feedback_button.setGeometry(button_x, button_y_start + 8 * button_y_offset, 200, 40)
        self.feedback_button.clicked.connect(self.open_feedback_dialog)

    def start_screen_mirroring(self):
        try:
            self.scrcpy_process = subprocess.Popen(["scrcpy-win64-v2.1\\scrcpy-win64-v2.1\\scrcpy.exe"])
            self.update_button_state(self.start_button, "Mirroring Started", False, "green")
        except FileNotFoundError as e:
            QMessageBox.critical(self, "Error", f"Scrcpy not found! {e}")

    def test_screen_mirror(self):
        try:
            result = self.verify_screen()
            self.handle_test_result(self.test_button, result)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def verify_screen(self):
        return automated_nav.verify_navigation()

    def test_call(self):
        try:
            phone_number, ok = QInputDialog.getText(self, 'Phone Number Input', 'Enter the phone number to receive call (including country code):')

            if ok:
                pattern = re.compile(r'^\+91\d{10}$')
                if not pattern.match(phone_number):
                    QMessageBox.warning(self, "Invalid Input", "Please enter a valid phone number with country code +91 followed by 10 digits.")
                    return

                result = self.verify_call(phone_number)
                self.handle_test_result(self.test_call_button, result)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def verify_call(self, phone_number):
        return call.verify(phone_number)

    def test_navigation(self):
        try:
            result = self.verify_navigation()
            self.handle_test_result(self.test_nav, result)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def verify_navigation(self):
        return map_navigation_test.compare()

    def music_check(self):
        try:
            result = self.music_check1()
            self.handle_test_result(self.test_button_music, result)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def music_check1(self):
        return music_test.test_next_previous()

    def auto_test(self):
        try:
            self.start_screen_mirroring()
            self.test_screen_mirror()
            self.test_call()
            self.test_navigation()
            self.music_check()
            QMessageBox.information(self, "Auto Test", "All tests completed.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def handle_test_result(self, button, result):
        if result:
            self.update_button_state(button, "Test Passed", False, "green")
        else:
            self.update_button_state(button, "Test Failed", False, "red")
            self.animate_button_upwards(button)
            QMessageBox.warning(self, "Test Result", "Test Failed")

    def update_button_state(self, button, text, enabled, color):
        button.setText(text)
        button.setStyleSheet(f"background-color: {color}; border-radius: 10px;")
        button.setEnabled(enabled)

    def animate_button_upwards(self, button):
        anim = QPropertyAnimation(button, b"pos")
        anim.setDuration(100)
        anim.setStartValue(button.pos())
        anim.setEndValue(button.pos() + QPoint(0, -50))
        anim.start()
    
    def reset_tests(self):
        self.update_button_state(self.start_button, "Start Mirror", True, "#8e44ad")
        self.reset_button_state(self.test_button, "Test Screen Mirroring")
        self.reset_button_state(self.test_button_music, "Test Music")
        self.reset_button_state(self.test_call_button, "Test Call")
        self.reset_button_state(self.test_nav, "Test Navigation")

    def reset_button_state(self, button, text):
        button.setText(text)
        button.set_default_style()
        button.setEnabled(True)

    def execute_remote_control(self):
        try:
            self.remote_control_process = subprocess.Popen(["python", "Remote_Control.py"])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not execute Remote_Control.py! {e}")

    def open_feedback_dialog(self):
        dialog = FeedbackDialog(self)
        if dialog.exec() == QDialog.Accepted:
            QMessageBox.information(self, "Feedback", "Thank you for your feedback!")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirm Exit', 'Are you sure you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Terminate scrcpy process if running
            if self.scrcpy_process:
                self.scrcpy_process.terminate()
            
            # Terminate remote control process if running
            if self.remote_control_process:
                self.remote_control_process.terminate()
            
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
