''''
Author: George Mtombeni
LinkedIn: https://www.linkedin.com/in/george-mtombeni-04948b211/
GitHub: https://github.com/24861723
Description: This script uses the cvzone library to detect hand gestures and control the mouse cursor.

Usage: 
1. Run the script.
2. Show your hand in front of the camera.
3. Use the following gestures to control the mouse:
    - Orbit: One finger up (index finger) - Left mouse drag
    - Pan: Two fingers up (index and middle fingers) - Right mouse drag
    - Zoom: Pinching motion (thumb and index finger close together) - Scroll up/down
    
Press ESC to exit the program.

Note: Make sure to install the required libraries before running the script.

Script tested on fetchcfd.com
'''

import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import numpy as np

def main():
    # Initialize camera
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1, detectionCon=0.8)

    # Get screen size
    screen_width, screen_height = pyautogui.size()
    # Get camera image size
    cam_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cam_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Variables to keep track of previous finger positions
    prev_x, prev_y = None, None
    prev_distance = None
    gesture_mode = None

    smoothening = 2  # Smoothing factor for mouse movement

    while True:
        success, img = cap.read()
        if not success:
            break
        # Flip the image horizontally for natural (mirror) viewing
        img = cv2.flip(img, 1)
        # Detect hands and get the image with drawn landmarks
        hands, img = detector.findHands(img)

        if hands:
            hand = hands[0]
            lmList = hand['lmList']  # List of 21 Landmark points

            fingers = detector.fingersUp(hand)  # List of which fingers are up

            # Determine gestures based on fingers up
            # Orbit: One finger up (index finger)
            if fingers == [0, 1, 0, 0, 0]:
                gesture_mode = 'orbit'
                x, y = lmList[8][0], lmList[8][1]  # Index finger tip

                # Map coordinates to screen size
                screen_x = np.interp(x, [0, cam_width], [0, screen_width])
                screen_y = np.interp(y, [0, cam_height], [0, screen_height])

                if prev_x is not None and prev_y is not None:
                    dx = screen_x - prev_x
                    dy = screen_y - prev_y

                    # Apply smoothing
                    dx = dx / smoothening
                    dy = dy / smoothening

                    # Move the mouse relative to previous position
                    pyautogui.moveRel(dx, dy)
                    
                    # Hold down left mouse button if not already
                    if not pyautogui.mouseDown(button='left'):
                        pyautogui.mouseDown(button='left')
                    print("Orbit: Left mouse drag")
                prev_x, prev_y = screen_x, screen_y

            # Pan: Two fingers up (index and middle fingers)
            elif fingers == [0, 1, 1, 0, 0]:
                gesture_mode = 'pan'
                x, y = lmList[8][0], lmList[8][1]  # Index finger tip

                # Map coordinates to screen size
                screen_x = np.interp(x, [0, cam_width], [0, screen_width])
                screen_y = np.interp(y, [0, cam_height], [0, screen_height])

                if prev_x is not None and prev_y is not None:
                    dx = screen_x - prev_x
                    dy = screen_y - prev_y

                    # Apply smoothing
                    dx = dx / smoothening
                    dy = dy / smoothening

                    # Move the mouse relative to previous position
                    pyautogui.moveRel(dx, dy)
                    # Hold down right mouse button if not already
                    pyautogui.mouseDown(button='right')
                    print("Pan: Right mouse drag")
                prev_x, prev_y = screen_x, screen_y

            # Zoom: Pinching motion (thumb and index finger close together)
            elif fingers == [1, 1, 0, 0, 0]:
                gesture_mode = 'zoom'
                # Measure distance between thumb tip and index finger tip
                x1, y1 = lmList[4][0], lmList[4][1]  # Thumb tip
                x2, y2 = lmList[8][0], lmList[8][1]  # Index finger tip
                distance = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5

                if prev_distance is not None:
                    delta = distance - prev_distance
                    # delta can be positive or negative
                    scroll_amount = int(delta * 0.5)  # Adjust scroll sensitivity
                    if scroll_amount != 0:
                        pyautogui.scroll(scroll_amount)
                        if scroll_amount > 0:
                            print("Zoom in: Scrolling up")
                        else:
                            print("Zoom out: Scrolling down")
                prev_distance = distance
            else:
                # No valid gesture detected
                if gesture_mode == 'orbit':
                    pyautogui.mouseUp(button='left')
                elif gesture_mode == 'pan':
                    pyautogui.mouseUp(button='right')
                gesture_mode = None
                prev_x, prev_y = None, None
                prev_distance = None

        else:
            # No hands detected
            if gesture_mode == 'orbit':
                pyautogui.mouseUp(button='left')
            elif gesture_mode == 'pan':
                pyautogui.mouseUp(button='right')
            gesture_mode = None
            prev_x, prev_y = None, None
            prev_distance = None

        # Display the image
        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == 27:
            break  # Press ESC to exit

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
