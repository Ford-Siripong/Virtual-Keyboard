import cv2
import time
import mediapipe as mp
import numpy as np
import math

from pyautogui import RIGHT

class handdetect():
    def __init__(self,mode = False,maxHands = 2,model = 1, detectionCon = 0.5,trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.model = model
        self.detectionCon = detectionCon
        self.trackCon = trackCon        
        
        self.mphand = mp.solutions.hands
        self.hands = self.mphand.Hands(self.mode, self.maxHands, self.model, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

        self.tipid = [4,8,12,16,20]

    def findHands(self,img,draw = True, fliptype = True, drawmark = True, drawpoint = True, drawscale = True, Typehand = True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        h, w ,c = img.shape
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handtype,handlms in zip(self.results.multi_handedness,self.results.multi_hand_landmarks):
                myhand = {}
                xlist =[]
                ylist = []
                handlmlist = []
                idhand = []

                if fliptype:
                    if handtype.classification[0].label =="Right":
                        myhand["type"] = "Left"
                    else:
                        myhand["type"] = "Right"
                else:myhand["type"] = handtype.classification[0].label
                allHands.append(myhand)


                for id, lm in enumerate(handlms.landmark):
                    #print(id,lm)
                    
                    cx,cy = int(lm.x*w),int(lm.y*h)
                    #print(h,w)
                    xlist.append(cx)
                    ylist.append(cy)
                    handlmlist.append([cx,cy])
                    idhand.append(id)
                    if drawpoint:
                    # cv2.circle(img,(cx,cy),5,(255,255,0),cv2.FILLED)
                        if myhand["type"] == "Right":
                            if id == 8:
                                cv2.circle(img,(cx,cy),5,(255,255,0),cv2.FILLED)
                        else:
                            if id == 8:
                                cv2.circle(img, (cx,cy), 5, (168,192,224), cv2.FILLED)
                    
                    

                xmin, xmax = min(xlist), max(xlist)
                ymin, ymax = min(ylist), max(ylist)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                
                myhand["lmlist"] = handlmlist
                myhand["id"] = idhand
                myhand["bbox"] = bbox

                # if id == 4 and lm.z*(-100) > 8 and lm.z*(-100) < 10: #id finger enable in z direction
                
                if drawscale:
                    cv2.rectangle(img,(bbox[0] - 20, bbox[1] - 20), (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20), (0,255,0), 2)
                
                if Typehand:
                    cv2.putText(img, myhand["type"],(bbox[0] - 30, bbox[1] - 30),cv2.FONT_HERSHEY_PLAIN,2,(255, 0, 255),2)

                if drawmark:
                    self.mpDraw.draw_landmarks(img, handlms, self.mphand.HAND_CONNECTIONS)
                    cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20), (bbox[0] + bbox[2] + 20, bbox[1]+ bbox[3] + 20), (120,154,165), 2)
        if draw:
            return allHands, img
        else:
            return allHands

    def fingersup(self, myhand):
        fingers = []
        myhandtype = myhand["type"]
        lmlist = myhand["lmlist"]
        if self.results.multi_hand_landmarks:
            
            if myhandtype == "Right":
                if lmlist[self.tipid[0]][0] > lmlist[self.tipid[0]-2][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if lmlist[self.tipid[0]][0] < lmlist[self.tipid[0]-2][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)


            for id in range(1,5):
                if lmlist[self.tipid[id]][1] < lmlist[self.tipid[id]-2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        # print(fingers)
        return fingers


    def findDistance(self,p1,p2, img = None, draw = True):
        x1, y1 = p1
        x2, y2 = p2
        cx,cy = (x1+x2)//2 , (y1+y2)//2
        length = math.hypot(x2-x1,y2-y1)
        info = (x1,y1,x2,y2,cx,cy)
        if img is not None:
            if draw :
                cv2.circle(img, (x1,y1),15,(255,0,255),cv2.FILLED)
                cv2.circle(img, (x2,y2),15,(255,0,255),cv2.FILLED)
                cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
                cv2.circle(img, (cx,cy),15,(0,0,255),cv2.FILLED)
            return length,info,img
        else:
            return length,info



def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handdetect()

    while True:
        success, img = cap.read()
        hand, img = detector.findHands(img, drawmark=False)
        # print(hand)
        if hand:
            # print(lmlist[4])
            hand1 = hand[0]
            lmlist1 = hand1["lmlist"]
            handtype1 = hand1["type"]
            finger1 = detector.fingersup(hand1)

            length , info , img = detector.findDistance(lmlist1[4],lmlist1[12],img)

            if len(hand) == 2:
                hand2 = hand[1]
                lmlist2 = hand2["lmlist"]
                handtype2 = hand2["type"]
                finger2 = detector.fingersup(hand2)
                
                length , info , img = detector.findDistance(lmlist2[4],lmlist2[12],img)


        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(img,str(int(fps)),(10,60),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

        cv2.imshow("image",img)
        cv2.waitKey(1)



if __name__ == "__main__":
    main()