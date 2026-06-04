START MIRROR is a comprehensive tool for remote control and screen projection of Android and iOS mobile devices to PCs, facilitating automated testing of key functionalities such as screen mirroring, music playback, calls, and map navigation.

1.Key Features
a.Screen Mirroring

Utilizes Screen copy to initialize mirroring.
Navigation on mirrored screens using PyQtGui.
Compares direct and mirrored screenshots with metrics like Mean Squared Error, Peak Signal-to-Noise Ratio, and histogram comparison.

b.Music Test

Pushes local files to the device and verifies playback with ADB.
Supports actions like pausing, skipping, and metadata comparison.

c.Call Test

Prompts for receiver's number, checks network status, and initiates calls using ADB.
Verifies call status using the Twilio API.

d.Map Navigation Test

Automates Google Maps (Android) and Apple Maps (iOS) for navigation accuracy.
Uses Tesseract OCR and OSRM API to verify travel times.

e.Automated Testing

Auto Test button runs all tests sequentially, logging results.
Retest button refreshes script execution without restarting.

f.Remote Control

Manages Android device functions from the PC, including battery, volume, Wi-Fi, Bluetooth, data connectivity, and app access.

g.Feedback Collection

User feedback is collected and stored in JSON format.

h.Error Handling

Comprehensive error handling with logs and GUI alerts.

**System Requirements**
Android: USB/WiFi connection, ADB enabled.
iOS: USB/WiFi connection, Xcode, AirServer.
General: Python, PyQtGui, Appium, Tesseract OCR, OpenCV.
Getting Started
Setup Environment: Install necessary dependencies and tools.
Connect Device: Ensure device connection via USB or WiFi.
Run Tests: Use the GUI to select and run specific or automated tests.
View Results: Analyze results and provide feedback.

** Android **
<img width="1920" height="1080" alt="353136156-3a9ac446-ab8e-4b3f-8243-e186da3f3501" src="https://github.com/user-attachments/assets/dfce6bf5-2447-4209-b363-ce47257feb2b" />
<img width="1920" height="1080" alt="353136297-f7d55f20-5fc9-4322-921a-986006a9706e" src="https://github.com/user-attachments/assets/e17f0e48-0262-4979-8682-14e9ba8fe59b" />
** IOS **
<img width="1202" height="540" alt="353139625-b92cfbe0-74b7-460a-a5eb-63a7193393d8" src="https://github.com/user-attachments/assets/a5e352ee-233c-4a6d-bf1c-2b2e90e54429" />
<img width="1202" height="540" alt="353139583-16632857-4164-4a87-a98a-c59ac4cc1f91" src="https://github.com/user-attachments/assets/4acd815c-f836-4ab5-b7c0-8ffa42cda7d7" />



++Contributing++
Contributions are welcome! Please fork the repository and submit a pull request with your improvements.
