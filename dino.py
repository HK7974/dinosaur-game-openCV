# for https://chrome-dino-game.github.io/
# When God debugs, he doesn't use breakpoints, just divine intervention.

import cv2
import pyautogui
from mss import mss
from cvzone.FPS import FPS
import numpy as np
import cvzone


fpsReader = FPS()
def captureScreenShot(x,y,width,height):
    screenshot = pyautogui.screenshot(region=(x,y,width,height))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot


def captureScreenShotMSS(x,y,width,height):
    with mss() as sct:
        monitor = {"top": y , "left" : x, "width":width, "height":height}
        screen = sct.grab(monitor)
        screenshot = np.array(screen)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        return screenshot

def preProcess(_croppedImage):
    grayImage = cv2.cvtColor(_croppedImage, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("gra",grayImage)
    _ , binaryFrame = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY_INV)
    #cv2.imshow("binar", binaryFrame)
    cannyFrame = cv2.Canny(binaryFrame, 50, 50)
    #cv2.imshow("cann", cannyFrame)
    kernel = np.ones((5,5))
    dilatedFrame = cv2.dilate(cannyFrame, kernel, iterations=2)
    #cv2.imshow("dila", dilatedFrame)

    return dilatedFrame

def doStuff(_conto , _imageConto, jump_distance = 80):
    if _conto:
        leftMostObs = sorted(_conto, key=lambda x : x["bbox"][0])
        # print(leftMostObs[0]["bbox"][0])
        cv2.line(_imageConto, (0,leftMostObs[0]["bbox"][1]+10), (leftMostObs[0]["bbox"][0],leftMostObs[0]["bbox"][1] +10 ), 
                 (100,0,100),5)
        if leftMostObs[0]["bbox"][0] < jump_distance:
            print("Space")
            pyautogui.press('space')



    return _imageConto


def FindCountours(cropImg, preImg):
    imgCont , ContFound = cvzone.findContours(cropImg, preImg, 100 ,filter=None)
    return imgCont, ContFound

while True:
    cap = captureScreenShotMSS(540,150,820,230)  # area of game
    rePo = [140,190,145]
    cropImg = cap[rePo[0]:rePo[1], rePo[2]:] #first parameter is height
    preProcessedImage = preProcess(cropImg)
    ImageContours,ContoursFound = FindCountours(cropImg,preProcessedImage)
    newImageContours = doStuff(ContoursFound,ImageContours)
    cap[rePo[0]:rePo[1],rePo[2]:] = newImageContours
    fps, cap = fpsReader.update(cap)
    cv2.imshow("file",cap)
    cv2.imshow("cropped",cropImg)
    # cv2.imshow("image",ImageContours)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()    