import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QSpacerItem, QSizePolicy, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt
import iOSsongSearchGui
import iOSPlaylistSearchGui

class SimpleGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Music Test")
        self.setGeometry(550, 100, 250, 250)

        # Set background color
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#2C2C2C"))  # Dark background color
        self.setPalette(palette)

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a horizontal layout
        layout = QHBoxLayout()

        # Add the logo (if needed)
        # logo_label = QLabel(self)
        # pixmap = QPixmap(r"contact1.png")
        # logo_label.setPixmap(pixmap)
        # logo_label.setAlignment(Qt.AlignCenter)
        # layout.addWidget(logo_label)

        # Spacer to push elements to the center
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Create call by name button
        self.call_by_name_button = QPushButton("Song Search", self)
        self.call_by_name_button.setStyleSheet(self.get_button_css())
        self.call_by_name_button.setFixedSize(150, 50)
        layout.addWidget(self.call_by_name_button, alignment=Qt.AlignCenter)

        # Create call by number button
        self.call_by_number_button = QPushButton("Playlist", self)
        self.call_by_number_button.setStyleSheet(self.get_button_css())
        self.call_by_number_button.setFixedSize(150, 50)
        layout.addWidget(self.call_by_number_button, alignment=Qt.AlignCenter)

        # Spacer to push elements to the center
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Set the layout for the central widget
        central_widget.setLayout(layout)

        # Connect buttons to their functions
        self.call_by_name_button.clicked.connect(self.on_call_by_name_button_click)
        self.call_by_number_button.clicked.connect(self.on_call_by_number_button_click)

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

    def on_call_by_name_button_click(self):
        print("Play by Name of song clicked")
        self.test_gui = iOSsongSearchGui.SimpleGUI()
        self.test_gui.show()

    def on_call_by_number_button_click(self):
        print("play by Playlist clicked")
        self.test_gui = iOSPlaylistSearchGui.SimpleGUI()
        self.test_gui.show()

def main():
    app = QApplication(sys.argv)
    gui = SimpleGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
