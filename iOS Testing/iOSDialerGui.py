# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QSpacerItem, QSizePolicy, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.ios.xcuitest.base import XCUITestOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import iOSAddContact


class SimpleGUI(QMainWindow):
    def get_phone_number(self):
         return self.text_field.text()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Call using Dialer App")
        self.setGeometry(550, 400, 400, 400)

        # Set background color
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#2C2C2C"))  # Dark background color
        self.setPalette(palette)

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout
        layout = QVBoxLayout()

        # Spacer to push the logo downwards
        layout.addSpacerItem(QSpacerItem(50, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add the logo
        logo_label = QLabel(self)
        # Uncomment and set the path to your image file
        pixmap = QPixmap(r"dialer1.png")  # Use raw string for the path
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Spacer to push elements to the center
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Create text field with placeholder
        self.text_field = QLineEdit(self)
        self.text_field.setPlaceholderText("Call by Number")
        self.text_field.setStyleSheet(self.get_text_field_css())
        self.text_field.setFixedSize(350, 70)  # Increased size
        layout.addWidget(self.text_field, alignment=Qt.AlignCenter)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        # Create call button
        self.call_button = QPushButton("Call", self)
        self.call_button.setStyleSheet(self.get_button_css())
        self.call_button.setFixedSize(150, 50)
        button_layout.addWidget(self.call_button, alignment=Qt.AlignCenter)

        # Create save contact button
        self.save_contact_button = QPushButton("Save Contact", self)
        self.save_contact_button.setStyleSheet(self.get_button_css())
        self.save_contact_button.setFixedSize(150, 50)
        button_layout.addWidget(self.save_contact_button, alignment=Qt.AlignCenter)

        layout.addLayout(button_layout)

        # Spacer to push elements to the center
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Set the layout for the central widget
        central_widget.setLayout(layout)

        # Connect buttons to their functions
        self.call_button.clicked.connect(self.on_call_button_click)
        self.save_contact_button.clicked.connect(self.on_save_contact_button_click)

    def get_button_css(self):
        return """
            QPushButton {
                background-color: #E0E0E0; /* Fallback color */
                border: 1px solid #A9A9A9;
                color: #333;
                font-size: 18px;
                border-radius: 25px; /* Rounded corners */
                padding: 10px;
                margin: 10px;
                min-height: 40px;
                background-image: linear-gradient(to bottom, #FFFFFF, #D3D3D3); /* Gradient background */
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2), inset 2px 2px 5px rgba(255, 255, 255, 0.6); /* 3D effect */
                transition: all 0.3s ease; /* Smooth transition */
            }
            QPushButton:hover {
                background-image: linear-gradient(to bottom, #F8F8F8, #A0A0A0);
                border-color: #505050;
                color: #000;
                box-shadow: 6px 6px 15px rgba(0, 0, 0, 0.5), inset 4px 4px 10px rgba(255, 255, 255, 0.8); /* Stronger 3D effect */
                transform: scale(1.1); /* Larger scaling on hover */
            }
            QPushButton:pressed {
                background-image: linear-gradient(to bottom, #D3D3D3, #FFFFFF);
                border-color: #404040;
                box-shadow: inset 2px 2px 5px rgba(0, 0, 0, 0.4); /* Pressed effect */
                transform: scale(0.95); /* Slight shrinking on press */
            }
        """

    def get_text_field_css(self):
        return """
            QLineEdit {
                background-color: #E0E0E0;
                border: 1px solid #A9A9A9;
                color: #333;
                font-size: 18px;
                border-radius: 15px;
                padding: 10px;
                margin: 10px;
                background-image: linear-gradient(to bottom, #FFFFFF, #D3D3D3);
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2), inset 2px 2px 5px rgba(255, 255, 255, 0.6);
                transition: all 0.3s ease;
            }
            QLineEdit:focus {
                border-color: #505050;
                box-shadow: 6px 6px 15px rgba(0, 0, 0, 0.5), inset 4px 4px 10px rgba(255, 255, 255, 0.8);
            }
        """
    

    def on_call_button_click(self):
        phone_number = self.text_field.text()
        print("Call button clicked with text:", phone_number)

        with open("numberinput.txt", "w") as file:
            file.write(phone_number)

        # Initialize Appium driver and perform dialing
        self.make_call(phone_number)
        
    

    def on_save_contact_button_click(self):
        from iOSAddContact import SimpleGUI1
        self.contact_gui = SimpleGUI1(gui=self)
        
        # Show the SimpleGUI1 instance
        self.contact_gui.show()

    def make_call(self, phone_number):
        # Desired capabilities
        desired_capabilities = {
            "platformName": "iOS",
            "appium:udid": "00008110-001974661EF2201E",  # Update with your device UDID
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
        for digit in phone_number:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, digit))
            )
            button.click()

        # Find and click the call button (update the XPath according to the actual UI element)
        makecall = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//XCUIElementTypeButton[@name='ACCEPT']"))
        )
        makecall.click()

        # Quit the driver after the operations
        driver.quit()

def main():
    app = QApplication(sys.argv)
    gui = SimpleGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
