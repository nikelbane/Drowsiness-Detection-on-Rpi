import cv2
import os, time, threading, io
from tensorflow.keras.models import load_model
import numpy as np
from pygame import mixer
import imutils
import RPi.GPIO as GPIO
from imutils.video import WebcamVideoStream
import pynmea2, serial

def getgpsdata(ser):
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

    while True:
        line = sio.readline()
        if line[0:6] == "$GPGGA":
            newmsg = pynmea2.parse(line)
            lat=newmsg.latitude
            lng=newmsg.longitude
            gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
            print(gps)
            time.sleep(1.0)

def dist(TRIG,ECHO):
    while(True):
       GPIO.output(TRIG, True)
       time.sleep(0.00001)
       GPIO.output(TRIG, False)

       while GPIO.input(ECHO)==0:
          pulse_start = time.time()

       while GPIO.input(ECHO)==1:
          pulse_end = time.time()

       pulse_duration = pulse_end - pulse_start

       distance = pulse_duration * 17150

       distance = round(distance+1.15, 2)
  
       if distance<=20:
          print ("ALERT: Collision distance:",distance,"cm")
          
       time.sleep(0.5)

def drowsinessDetection(lpred, rpred, score):
    while(True):
        frame = cap.read()
        frame = imutils.resize(frame, width=300)
        height,width = frame.shape[:2] 

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        # faces = face.detectMultiScale(gray,minNeighbors=5,scaleFactor=1.1,minSize=(25,25))
        left_eye = leye.detectMultiScale(gray)
        right_eye =  reye.detectMultiScale(gray)

        cv2.rectangle(frame, (0,height-50) , (200,height) , (0,0,0) , thickness=cv2.FILLED )

        for (x,y,w,h) in right_eye:
            r_eye=frame[y:y+h,x:x+w]
            r_eye = cv2.cvtColor(r_eye,cv2.COLOR_BGR2GRAY)
            r_eye = cv2.resize(r_eye,(24,24))
            r_eye= r_eye/255
            r_eye=  r_eye.reshape(24,24,-1)
            r_eye = np.expand_dims(r_eye,axis=0)
            rpred = model.predict_classes(r_eye)
            if(rpred[0]==1):
                lbl='Open' 
            if(rpred[0]==0):
                lbl='Closed'
            break

        for (x,y,w,h) in left_eye:
            l_eye=frame[y:y+h,x:x+w]
            l_eye = cv2.cvtColor(l_eye,cv2.COLOR_BGR2GRAY)  
            l_eye = cv2.resize(l_eye,(24,24))
            l_eye= l_eye/255
            l_eye=l_eye.reshape(24,24,-1)
            l_eye = np.expand_dims(l_eye,axis=0)
            lpred = model.predict_classes(l_eye)
            if(lpred[0]==1):
                lbl='Open'   
            if(lpred[0]==0):
                lbl='Closed'
            break

        if(rpred[0]==0 and lpred[0]==0):
            score=score+1
            cv2.putText(frame,"Closed",(10,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
        else:
            score=score-1
            cv2.putText(frame,"Open",(10,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
    
        
        if(score<0):
            score=0   
        cv2.putText(frame,'Score:'+str(score),(100,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
        if(score>2):
            try:
                sound.play()
                #GPIO.output(8, GPIO.HIGH)
                #time.sleep(3) 
                #GPIO.output(8, GPIO.LOW) 
                #time.sleep(1)
            except: 
                pass
            cv2.rectangle(frame,(0,0),(width,height),(0,0,255),cv2.BORDER_DEFAULT) 
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
if __name__=="__main__":
    
    GPIO.setmode(GPIO.BOARD)

    TRIG = 16
    ECHO = 18
    LED = 8
    i=0

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    # GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

    GPIO.output(TRIG, False)
    print ("Calibrating.....")
    time.sleep(2)
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=2)

    mixer.init()
    sound = mixer.Sound('/home/pi/Desktop/Major-1/alarm.wav')

    # load haar cascade files for face and eyes
    face = cv2.CascadeClassifier('/home/pi/Desktop/Major-1/haar cascade files/haarcascade_frontalface_alt.xml')
    leye = cv2.CascadeClassifier('/home/pi/Desktop/Major-1/haar cascade files/haarcascade_lefteye_2splits.xml')
    reye = cv2.CascadeClassifier('/home/pi/Desktop/Major-1/haar cascade files/haarcascade_righteye_2splits.xml')
    
    # label classification for eyes open or close
    lbl=['Close','Open']

    # load pretrained model on dataset
    model = load_model('/home/pi/Desktop/Major-1/models/cnnCat2.h5')
    path = os.getcwd()
    cap = WebcamVideoStream(src=0).start()
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    score=0

    rpred=[99]
    lpred=[99]
    t1 = threading.Thread(target=dist, args=(TRIG,ECHO))
    t1.start()
    t2 = threading.Thread(target=getgpsdata, args=(ser,))
    t2.start()
    drowsinessDetection(lpred, rpred, score)
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
    
    