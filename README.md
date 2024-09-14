# 3D_Hand_Control

Control 3D models using hand gestures detected via your webcam. This project translates specific hand gestures into mouse movements and actions, allowing interaction with 3D modeling software or web-based 3D viewers.

Requirements
Python 3.x
OpenCV (opencv-python)
cvzone
PyAutoGUI (pyautogui)
NumPy
Installation
Install the required libraries:

bash
Copy code
pip install opencv-python cvzone pyautogui numpy
Usage
Run the Script:

bash
Copy code
python gesture_control.py
Open Your 3D Application:

Open the 3D modeling software or web-based viewer you want to control.
Ensure it is the active window.
Use Gestures to Control the View:

Orbit (Rotate View): Raise your index finger and move your hand to rotate.
Pan: Raise your index and middle fingers and move your hand to pan.
Zoom: Pinch gesture with thumb and index finger to zoom in or out.
Exit:

Press the ESC key in the camera window to exit the program.
Notes
Ensure good lighting for accurate hand detection.
The webcam window will display your hand with detected landmarks.
Actions executed are printed in the terminal for reference.
