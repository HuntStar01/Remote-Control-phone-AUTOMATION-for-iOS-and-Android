import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QSpacerItem, QSizePolicy, QLineEdit
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt
from spotifyTest import test_music

class SimpleGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Paying Song by Name")
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


        # Spacer to push elements to the center
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Add the logo
        logo_label = QLabel(self)
        # Uncomment and set the path to your image file
        pixmap = QPixmap(r"playlistLogo1.png")  # Use raw string for the path
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Spacer to push elements to the center
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Create text field with placeholder
        self.text_field = QLineEdit(self)
        self.text_field.setPlaceholderText("Playlist Number")
        self.text_field.setStyleSheet(self.get_text_field_css())
        self.text_field.setFixedSize(350, 70)  # Increased size
        layout.addWidget(self.text_field, alignment=Qt.AlignCenter)

        # Create text field with placeholder
        self.text_field1= QLineEdit(self)
        self.text_field1.setPlaceholderText("Song Number")
        self.text_field1.setStyleSheet(self.get_text_field_css())
        self.text_field1.setFixedSize(350, 70)  # Increased size
        layout.addWidget(self.text_field1, alignment=Qt.AlignCenter)

        # Create call button
        self.call_button = QPushButton("Play", self)
        self.call_button.setStyleSheet(self.get_button_css())
        self.call_button.setFixedSize(100, 60)
        layout.addWidget(self.call_button, alignment=Qt.AlignCenter)

        # Spacer to push elements to the center
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Set the layout for the central widget
        central_widget.setLayout(layout)

        # Connect button to its function
        self.call_button.clicked.connect(self.on_call_button_click)

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
        playlistNo =self.text_field.text()
        songNo=self.text_field1.text()
        test_music(playlistNo,songNo)


def main():
    app = QApplication(sys.argv)
    gui = SimpleGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
