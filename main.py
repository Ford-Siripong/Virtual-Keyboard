from typing import Text
import cv2
import mediapipe as mp
import time
from time import sleep
import handtrack as htm
# import math
# import numpy as np
from pynput.keyboard import Key, Controller
import pyautogui

wcam ,hcam = 1280,720
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
detector = htm.handdetect(detectionCon = 0.8)

KEYS =[ ["!","@","#","$","%","^","&","*","(",")","_","+"],
        ["Q","W","E","R","T","Y","U","I","O","P","{","}","|"],
        ["A","S","D","F","G","H","J","K","L",":","'"],
        ["Z","X","C","V","B","N","M","<",">","?"]]

keys = [["1","2","3","4","5","6","7","8","9","0","-","="],
        ["q","w","e","r","t","y","u","i","o","p","[","]","|"],
        ["a","s","d","f","g","h","j","k","l",";","'"],
        ["z","x","c","v","b","n","m",",",".","/"]]

findtext = ""

keyboard = Controller()


class Button():
    def __init__(self,pos,text,size = [50,48]):
        self.pos = pos
        self.size = size
        self.text = text
    
    def drawAll(img,buttomlist):

        for button in buttomlist:
            x,y = button.pos
            w,h = button.size
            # print(x,y)
            cv2.rectangle(img, button.pos, (x + 50 , y + 48), (255,0,255), cv2.FILLED)
            cv2.putText(img, button.text, (x + 8 , y + 37), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255),2)
            cv2.rectangle(img, (50, 50), (130, 98), (255,0,255), cv2.FILLED)
            cv2.rectangle(img, (50, 110), (130,158), (255,0,255), cv2.FILLED)
            cv2.rectangle(img, (50, 170), (130,218), (255,0,255), cv2.FILLED)
            cv2.rectangle(img, (50, 230), (130,278), (255,0,255), cv2.FILLED)
            cv2.putText(img, "Esc", ( 60 , 92 ), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),3)
            cv2.putText(img, "Tab", ( 60 , 150 ), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),2)
            cv2.putText(img, "Shift", ( 50 , 210 ), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),2)
            cv2.putText(img, "Exit", ( 60 , 270 ), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),3)
            # cv2.rectangle(img, (990, 50), (1040, 98), (0,0,0), cv2.FILLED)
            cv2.rectangle(img, (920, 170), (1040, 218), (255,0,255), cv2.FILLED)
            cv2.rectangle(img, (850, 230), (1040, 278), (255,0,255), cv2.FILLED)
            cv2.putText(img, "Enter", ( 935 , 210 ), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),2)
            cv2.putText(img, "Backspace", ( 860 , 270 ), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),2)


        return img

    # def drawtext(self,img):
        

        # return img


# buttomlist = []
# # mybuttom = Button([100*x + 50 ,100],"Q")

# for i in range(len(keys)):
#     for j, key in enumerate(keys[i]):
#         buttomlist.append(Button([70*j + 150 ,60*i + 50], key))
#         # print(70*j + 150)

def keybutton():
    buttomlist = []
    for i in range(len(keys)):
        if caps == 0:
            for j, key in enumerate(keys[i]):
                buttomlist.append(Button([70*j + 150 ,60*i + 50], key))
        else:
             for j, key in enumerate(KEYS[i]):
                buttomlist.append(Button([70*j + 150 ,60*i + 50], key))
    return buttomlist


while True:
    success, img = cap.read()
    hand, img = detector.findHands(img, drawmark=False, drawscale=False)
    breakprogram = 0
    caps = 0
    buttomlist = keybutton()
    img = Button.drawAll(img,buttomlist)
    
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(1200,700),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    # img = mybuttom.drawtext(img)
    if hand :
        hands = hand[0]
        lmlist = hands["lmlist"]
        # id = hands["id"]

        hand1 = hand[0]
        lmlist1 = hand1["lmlist"]
        handtype1 = hand1["type"]
        finger1 = detector.fingersup(hand1)

        # length1 , info , img = detector.findDistance(lmlist1[4], lmlist1[12], img, draw=False)

        for button in buttomlist:
                x,y = button.pos
                w,h = button.size
                # print(lmlist[8])
                # print(y)
                # print(x)
                length1,_,_ = detector.findDistance(lmlist1[4],lmlist1[12],img, draw=False)

                if x < lmlist1[8][0] < x + w and y < lmlist1[8][1] < y+h:

                    cv2.rectangle(img, button.pos, (x + w, y + h), (0,255,0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 10 , y + 30), cv2.FONT_HERSHEY_PLAIN, 3,( 255,255,255),3)
                    if length1< 33 :
                        keyboard.press(button.text)
                        # cv2.rectangle(img, button.pos, (x + w, y + h), (0,0,0), cv2.FILLED)
                        # cv2.putText(img, button.text, (x + 15 , y + 70), cv2.FONT_HERSHEY_PLAIN, 5,( 255,255,255),3)
                        findtext += button.text
                        sleep(0.15)

                if 920 < lmlist1[8][0] < 1040 and 170 < lmlist1[8][1] < 218:
                    cv2.rectangle(img, (920, 170), (1040, 218), (0,255,0), cv2.FILLED)
                    cv2.putText(img, "Enter", ( 935 , 205 ), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),2)
                    if length1 < 33:
                        keyboard.press(Key.enter)

                if 850 < lmlist1[8][0] < 1040 and 230 < lmlist1[8][1] < 278:
                    cv2.rectangle(img, (850, 230), (1040, 278), (0,255,0), cv2.FILLED)
                    cv2.putText(img, "backspace", ( 860 , 265 ), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),2)
                    if length1 < 33:
                        keyboard.press(Key.backspace)
                        # sleep(0.05)
                        # findtext = findtext.replace(button.text,'')
                    
                if 50 < lmlist1[8][0] < 130:
                    if 50 < lmlist1[8][1] < 98:
                        cv2.rectangle(img, (50, 50), (130, 98), (0,255,0), cv2.FILLED)
                        cv2.putText(img, "Esc", ( 60 , 92 ), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),3)
                        if length1 < 33:
                            keyboard.press(Key.esc)

                    elif 110 < lmlist1[8][1] < 158:
                        cv2.rectangle(img, (50, 110), (130,158), (0,255,0), cv2.FILLED)
                        cv2.putText(img, "Tab", ( 60 , 150 ), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),2)
                        if length1 < 33:
                            keyboard.tap(Key.space)
                            # keyboard.tab(Key.space)

                    elif 170 < lmlist1[8][1] < 218:
                        cv2.rectangle(img, (50, 170), (130,218), (0,255,0), cv2.FILLED)
                        cv2.putText(img, "Shift", ( 50 , 210 ), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),2)
                        if length1 < 33:
                            keyboard.tap(Key.caps_lock)
                            # keyboard.pressed(Key.shift)
                            # keyboard.press(button.text)
                            # keyboard.release(button.text.upper())
                            # findtext += button.text.upper()

                    elif 230 < lmlist1[8][1] < 278:
                        cv2.rectangle(img, (50, 230), (130,278), (0,255,0), cv2.FILLED)
                        cv2.putText(img, "Exit", ( 60 , 270 ), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),3)
                        if length1 < 33:
                            breakprogram = "123456789"

        if len(hand) == 2:
            hand2 = hand[1]
            lmlist2 = hand2["lmlist"]
            handtype2 = hand2["type"]
            finger2 = detector.fingersup(hand2)

            # length2 , info , img = detector.findDistance(lmlist2[4], lmlist2[12], img, draw=False)
        
            for button in buttomlist:
                x,y = button.pos
                w,h = button.size
                # print(lmlist[8])
                # print(y)
                # print(x)
                length2,_,_ = detector.findDistance(lmlist2[4],lmlist2[12],img, draw=False)

                if x < lmlist2[8][0] < x + w and y < lmlist2[8][1] < y+h:

                    cv2.rectangle(img, button.pos, (x + w, y + h), (0,255,0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 10 , y + 30), cv2.FONT_HERSHEY_PLAIN, 3,( 255,255,255),3)
                    if length2 < 33 :
                        keyboard.press(button.text)
                        # cv2.rectangle(img, button.pos, (x + w, y + h), (0,0,0), cv2.FILLED)
                        # cv2.putText(img, button.text, (x + 15 , y + 70), cv2.FONT_HERSHEY_PLAIN, 5,( 255,255,255),3)
                        findtext += button.text
                        sleep(0.15)

                if 920 < lmlist2[8][0] < 1040 and 170 < lmlist2[8][1] < 218:
                    cv2.rectangle(img, (920, 170), (1040, 218), (0,255,0), cv2.FILLED)
                    cv2.putText(img, "Enter", ( 935 , 205 ), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),2)
                    if length2 < 33:
                        keyboard.press(Key.enter)

                if 850 < lmlist2[8][0] < 1040 and 230 < lmlist2[8][1] < 278:
                    cv2.rectangle(img, (850, 230), (1040, 278), (0,255,0), cv2.FILLED)
                    cv2.putText(img, "Backspace", ( 860 , 265 ), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),2)
                    if length2 < 33:
                        keyboard.press(Key.backspace)
                        sleep(0.05)
                        # findtext = findtext.replace(button.text,'')

                if 50 < lmlist2[8][0] < 130:
                    if 50 < lmlist2[8][1] < 98:
                        cv2.rectangle(img, (50, 50), (130, 98), (0,255,0), cv2.FILLED)
                        cv2.putText(img, "Esc", ( 60 , 92 ), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),3)
                        if length2 < 33:
                            keyboard.press(Key.esc)

                    elif 110 < lmlist2[8][1] < 158:
                        cv2.rectangle(img, (50, 110), (130,158), (0,255,0), cv2.FILLED)
                        cv2.putText(img, "Tab", ( 60 , 150 ), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),2)
                        if length2 < 33:
                            pyautogui.press("tab")
                            # keyboard.tab('\t')

                    elif 170 < lmlist2[8][1] < 218:
                        cv2.rectangle(img, (50, 170), (130,218), (0,255,0), cv2.FILLED)
                        cv2.putText(img, "Shift", ( 50 , 210 ), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),2)
                        if length2 < 33:
                            keyboard.tap(Key.caps_lock)

                    elif 230 < lmlist2[8][1] < 278:
                        cv2.rectangle(img, (50, 230), (130,278), (0,255,0), cv2.FILLED)
                        cv2.putText(img, "Exit", ( 60 , 270 ), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),3)
                        if length2 < 33:
                            breakprogram = "123456789"
                    
                    # print(l)
                

    # cv2.rectangle(img, (50,350), (700, 450), (175,0,175), cv2.FILLED)
    # cv2.putText(img, findtext, (60 , 430), cv2.FONT_HERSHEY_PLAIN, 4,( 198,214,36),5)
                
    # if len(lmlist) !=0:
    #     # print(lmlist[4],lmlist[8])

    #     fingers = detector.fingersup()
    #     print(fingers)
    # print(caps)
    cv2.imshow("image",img)
    cv2.waitKey(1)
    if breakprogram == "123456789":
        break