import math
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

from pyfirmata import Arduino, SERVO, util
from time import sleep


port = 'COM3'
pin_x = 10
pin_y = 11
# pin_z = 12

board = Arduino(port)
board.digital[pin_x].mode = SERVO
board.digital[pin_y].mode = SERVO
# board.digital[pin_z].mode = SERVO

def set_servo_angle(pin, angle, speed):
    board.digital[pin].write(angle)
    sleep(speed)


wCam, hCam = 1280, 720
frameR = 50
smooth = 2
# 0

clocx, clocy = 0, 0
plocx, plocy = 0, 0
speed = 0.0015

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, wCam)
cap.set(4, hCam)


detector = HandDetector(detectionCon=0.8, maxHands=4)


x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2)

while True:
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


        angle_x = np.interp(x3, (frameR, wCam - frameR), (0, 180))
        angle_y = np.interp(y3, (frameR, hCam - frameR), (0, 180))
        # angle_z = np.interp(z4, (min(y), max(y)), (0, 180))
        # angle_z = distanceCM

        set_servo_angle(pin_x, int(angle_x), speed)
        set_servo_angle(pin_y, int(angle_y), speed)
        # set_servo_angle(pin_z, int(angle_z), speed)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
