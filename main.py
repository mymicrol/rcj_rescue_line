import image
import cv2
from time import sleep

cap = cv2.VideoCapture(2)

if not cap.isOpened():
    print("No camera found")
    exit()

while True:
    ret, frame = cap.read()
    gray = image.gray(frame)
    centers = []
    for i in range(350,471,30):
        centers.append(image.detect_line(gray, i,gray))
    for i,j in enumerate(range(350, 441, 30)):
        cv2.line(gray,(centers[i],j), (centers[i+1],j+30), (255,255,255),thickness=3)
    cv2.imshow("display", gray)
    cv2.waitKey(30)