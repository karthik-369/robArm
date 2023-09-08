import math
import cv2
import numpy as np
from pyfirmata import Arduino, SERVO
from time import sleep
import tkinter as tk
from cvzone.HandTrackingModule import HandDetector
from tkinter import ttk

# Arduino setup
port = 'COM3'
pin_x = 10  # Servo for X-axis
# pin_y = 11  # Servo for Y-axis
pin_z = 12  # Servo for Z-axis

board = Arduino(port)
board.digital[pin_x].mode = SERVO
# board.digital[pin_y].mode = SERVO
board.digital[pin_z].mode = SERVO

# Servo control functions
def set_servo_angle(pin, angle, speed=0.0015):
    board.digital[pin].write(angle)
    sleep(speed)

# Camera and frame setup
wCam, hCam = 1280, 720
frameR = 50
smooth = 2

# Initialize variables
clocx, clocy = 0, 0
plocx, plocy = 0, 0

# Initialize HandDetector
detector = None  # You can initialize this as needed

# Polynomial fit coefficients for distance to servo angle conversion
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2)

# Create tkinter application
app = tk.Tk()
app.title("Servo Control")
app.geometry("400x200")

# Speed control variable
servo_speed = tk.DoubleVar()
servo_speed.set(0.0015)  # Initial speed value

# Function to update servo speed
def update_servo_speed(value):
    global servo_speed
    servo_speed = float(value)
detector = HandDetector(detectionCon=0.8, maxHands=4)
# Slider for speed control
speed_label = ttk.Label(app, text="Rotation Speed:")
speed_label.pack(pady=10)
speed_slider = ttk.Scale(app, from_=0.0001, to=0.0015, variable=servo_speed, orient="horizontal", length=200,
                        command=lambda value: update_servo_speed(value))
speed_slider.pack()

# Function to control servos based on hand tracking (similar to your previous code)
def control_servos():
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        lmList = hands[0]['lmList']
        x, y, w, h = hands[0]['bbox']
        x1, y1, z1 = lmList[5]
        x2, y2, z2 = lmList[17]
        x3, y3, z3 = lmList[9]
        distance = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        A, B, C = coff
        distanceCM = A * distance ** 2 + B * distance + C
        z4 = distanceCM

        # Convert distances to angles for each axis
        angle_x = np.interp(x3, (frameR, wCam - frameR), (0, 180))
        angle_y = np.interp(y3, (frameR, hCam - frameR), (0, 180))
        # angle_z = np.interp(z4, (min(y), max(y)), (0, 180))
        angle_z  = distanceCM
        # Control servo motors with speed control
        set_servo_angle(pin_x, int(angle_x), servo_speed)
        # set_servo_angle(pin_y, int(angle_y), servo_speed)
        set_servo_angle(pin_z, int(angle_z), servo_speed)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    app.after(10, control_servos)

# Start the servo control loop
app.mainloop()
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, wCam)
cap.set(4, hCam)
while(True):
    control_servos()  # Start servo control loop


