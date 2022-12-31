import cv2
import pandas as pd

def get_camera():
    global cap
    for i in range(2,9):
        cap = cv2.VideoCapture(i)
        if cap.isOpened() : break

get_camera()
cv2.imshow("jj", cap.read()[1])
cv2.waitKey(10000)

get_camera()

def gray(img):
    ret, result = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 128, 255, cv2.THRESH_OTSU)
    return result

def detect_line(image, ypos, result=False):
    data = image[ypos]
    blacklist = pd.Series([x for x,y in enumerate(data) if y==0])
    while image[ypos][int(blacklist.mean())] != 0 and len(blacklist) > 10:
        blacklist = blacklist[blacklist.quantile(0.1)<blacklist][blacklist<blacklist.quantile(0.9)] 
    try:
        # these cause bugs when no black color is detected
        mean = int(blacklist.mean())
        std = 2*int(blacklist.std())
    except:
        # so we set them to 0 for now
        mean = 0
        std = 0
    if type(result) != bool:
        try:
            cv2.circle(result, (mean, ypos), 8, (0,0,255), thickness=-1)
            cv2.circle(result, (mean-std, ypos), 8, (0,255,0), thickness=-1)
            cv2.circle(result, (mean+std, ypos), 8, (0,255,0), thickness=-1)
        except:
            pass
    return (mean)

def simple(img, ypos, result=False):
    data = pd.Series(img[ypos])
    left_side = 0
    right_side = 0
    if 0 in data:
        check_counter = 0
        while data[check_counter] == 255:
            check_counter += 1
        left_side = check_counter
        while data[check_counter] == 0 and check_counter < 639:
            check_counter += 1
        right_side = check_counter
    cv2.circle(img, (left_side, ypos), 10, (255,255,255), thickness=-1)
    cv2.circle(img, (right_side, ypos), 10, (255,255,255), thickness=-1)
    return int((left_side+right_side)/2)