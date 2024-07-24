import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt
import subprocess
import iOSCallTestButtonGui
import iOSMusicTestButtonGui

class SimpleGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("iOS Testing")
        self.setGeometry(100, 100, 400, 400)

        # Set background color
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#2C2C2C"))  # Dark background color
        self.setPalette(palette)

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout
        layout = QVBoxLayout()

        # Add the logo
        logo_label = QLabel(self)
        pixmap = QPixmap("apple.png")  # Use forward slashes for the path
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Spacer to push buttons to the center
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Create buttons and add them to the layout
        self.button1 = QPushButton("Appium", self)
        self.button2 = QPushButton("Music Test", self)
        self.button3 = QPushButton("Navigation Test", self)
        self.button5 = QPushButton("iOS Call Test", self)
        self.button4 = QPushButton("Screen Mirroring", self)


        # Style the buttons
        self.button1.setStyleSheet(self.get_button_css())
        self.button2.setStyleSheet(self.get_button_css())
        self.button3.setStyleSheet(self.get_button_css())
        self.button5.setStyleSheet(self.get_button_css())
        self.button4.setStyleSheet(self.get_button_css())
        

        # Set button sizes
        self.button1.setFixedSize(200, 50)
        self.button2.setFixedSize(200, 50)
        self.button3.setFixedSize(200, 50)
        self.button5.setFixedSize(200, 50)
        self.button4.setFixedSize(200, 50)
        

        # Add buttons to the layout
        layout.addWidget(self.button1, alignment=Qt.AlignCenter)
        layout.addWidget(self.button2, alignment=Qt.AlignCenter)
        layout.addWidget(self.button3, alignment=Qt.AlignCenter)
        layout.addWidget(self.button5, alignment=Qt.AlignCenter)
        layout.addWidget(self.button4, alignment=Qt.AlignCenter)
        

        # Spacer to push buttons to the center
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Set the layout for the central widget
        central_widget.setLayout(layout)

        # Connect buttons to their respective functions
        self.button1.clicked.connect(self.on_button1_click)
        self.button2.clicked.connect(self.on_button2_click)
        self.button3.clicked.connect(self.on_button3_click)
        self.button5.clicked.connect(self.on_button5_click)
        self.button4.clicked.connect(self.on_button4_click)
        

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

    def on_button1_click(self):
        print("Running Script 1...")
        subprocess.run(["appium"])  # Replace with the path to your script

    def on_button2_click(self):
        print("Running Script 2...")
        self.test_gui = iOSMusicTestButtonGui.SimpleGUI()
        self.test_gui.show()

    def on_button3_click(self):
        print("Running Script 3...")
        subprocess.run(["python3", "iOSMapTest.py"])  # Replace with the path to your script

    def on_button5_click(self):
        print("call test running..")
        self.test_gui = iOSCallTestButtonGui.SimpleGUI()
        self.test_gui.show()
        
        # subprocess.run(["python3", "iOSCallTest.py"])

    def on_button4_click(self):
        print("Running Script 4...")
        subprocess.run(["open", "/Applications/AirServer.app"])


def main():
    app = QApplication(sys.argv)
    gui = SimpleGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
