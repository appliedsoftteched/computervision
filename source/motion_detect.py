# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 09:18:30 2021

@author: AppliedSoftTech

"""
import sys
from appconfig import appcfg
import cv2
#sys.path.insert(0, appcfg.DETECT.CORE_PACKAGES)
sys.path.insert(0, './utils')
from aws_util import AwsUtil
from twilio_util import TwilioUtil
from utility import Utility
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import time
import boto3
from botocore.exceptions import NoCredentialsError

class CamVisionDNN:
    #Output image folder. All output images are place into this folder    
    output_loc = './output'
    
    executor = None
    
    #Initial Image Frame. This is needed to check the change in frame during video analytics.
    initialFrame = None
    
    #This is to show the message that movement has been detected
    movementFrame='movement.png'
    
    #This is to show the message that movement has not been detected
    nomovementFrame='nomovement.png'
    
    #Reference for utility class
    utility = Utility()

    #Reference for AWS Utility class
    aws = AwsUtil()
    
    #Reference for AWS Utility class
    twilioUtil = TwilioUtil()
    
    #This is for parallel operation. Once the moevement is detected, the respnsibility to 
    #send the mesage to user over SMS is given to a thread
    executor=None
    
    #Slider Configuration
    lightthreshhold='./input/lightthreshhold.png'
    
    #Threshhold value for detecting light bulb brigtness
    lightDetectionThreshHold=180


    #Last sent message time
    lastSentMessageTime=None
    
    #Access key for AWS Service
    ACCESS_KEY = None
    #Secret Key for AWS
    SECRET_KEY = None

    #Twilio Account Id
    TWILIO_ACCT_ID=None
    
    #Twilio Auth Token
    TWILIO_ATUH_TOKEN=None

    def initApp(self):
        self.ACCESS_KEY= appcfg.DETECT.AWS_ACCESS_KEY
        self.SECRET_KEY=appcfg.DETECT.AWS_SECRET_KEY
        self.TWILIO_ACCT_ID=appcfg.DETECT.TWILIO_ACCT_ID
        self.TWILIO_ATUH_TOKEN=appcfg.DETECT.TWILIO_ATUH_TOKEN
    
    def uploadToAws(self,local_file, bucket, s3_file):
          print('uploadToAws')
          s3 = boto3.client('s3', aws_access_key_id=self.ACCESS_KEY,aws_secret_access_key=self.SECRET_KEY)
          
          try:
              #local_file = 'nomovement.png'
              print('uploadToAws with file as '+local_file)
              s3.upload_file(local_file, bucket, s3_file)
              print("Upload Successful")
              return True
          except FileNotFoundError:
              print("The file was not found")
              return False
          except NoCredentialsError:
              print("Credentials not available")
              return False
    
    """
    This is to do paralleloperations. When a movement of Lights On is detected then 
    message is being sent to user mobile number using AWS Cloud Service and Twilio 
    Service
    """    
    def doParallelTask(self,current_frame,isLightsTurnedOn):
        print('Going for Sending the message')
        messageTobeSent='Movement Detected at '+str(time.time())
        #print(messageTobeSent)

        milliseconds = int(round(time.time() * 1000))
        #print(milliseconds )

        fileName = str(milliseconds)+'.jpg'
        #print(fileName)
        fileWithPath = './output'+'/'+fileName
        
        sendMessage=False
        gapBetweenMessage = 60000
        if self.lastSentMessageTime is None:
            print('First Time')
        else:
            lapsedTime=(milliseconds)-(self.lastSentMessageTime)
            #print('Lapsed Time ',lapsedTime)
        #print('Lapse ',)
        if self.lastSentMessageTime is None:
            self.lastSentMessageTime=    milliseconds
            sendMessage=True
        else:
            if milliseconds-self.lastSentMessageTime>gapBetweenMessage:
                #print('Parallel Task GAP MORE')
                self.lastSentMessageTime=    milliseconds
                sendMessage=True
            else:
                #print('Parallel Task GAP LESS')
                sendMessage=False
        if sendMessage==True:        
            #print('Parallel Task Started for countNo ',milliseconds)
            cv2.imwrite('./output/' + "/%#05d.jpg" % (milliseconds), current_frame)        
            if isLightsTurnedOn==True:
                messageTobeSent='Lights has been turned on at '+time.time()            
            #self.aws.hasIt()    
            try:
                uploaded = self.uploadToAws(fileWithPath, 'compvision', str(milliseconds)+'.jpg')  
            except:
                print('Error uploading image')
                
            try:
                if appcfg.DETECT.SEND_SMS == True:
                    #https://compvision.s3.amazonaws.com/1627649929798.jpg
                    snappedImageUrl=appcfg.DETECT.S3_BASE_URL+str(milliseconds)+'.jpg'
                    messageTobeSent=messageTobeSent+'. File url is '+snappedImageUrl
                    print(messageTobeSent)
                    self.twilioUtil.sendSMS(messageTobeSent,appcfg.DETECT.SMS_FROM_NO, appcfg.DETECT.SMS_TO_NO,self.TWILIO_ACCT_ID,self.TWILIO_ATUH_TOKEN)  
                
            except:
                print('Error Sending SMS from this file')
        
  
    #This to take inputs for threshhold value beyond which a lights on event can be detected
    def on_change(self,val):
        print(val)
        self.lightDetectionThreshHold=val

    """
    This will detect if change in the background is due to Lights Turned on. To detect a lights on, threshhold is 
    applied to check if there are any contours detected after threshhold is applied. The threshhold is applied using the value taken as input from
    users.lightDetectionThreshHold is taken as input from user. This will help to tune the threshhold after which
    you can detect Lights on
    """
    def checkIfLightStarted(self,diffImage):
        _, threshLight = cv2.threshold(diffImage, self.lightDetectionThreshHold, 255, cv2.THRESH_BINARY)

        cv2.namedWindow("THRESHLIGHT");
        cv2.moveWindow("THRESHLIGHT", 0, 300);
        threshLight = cv2.resize(threshLight,(380,240))                

        cv2.imshow('THRESHLIGHT ',threshLight)
        
        contours, _ = cv2.findContours(
          threshLight, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        isLightsOn=False
        
        for contour in contours:
            if cv2.contourArea(contour) > 5000:
                isLightsOn=True
                (x, y, w, h) = cv2.boundingRect(contour)
                print(cv2.contourArea(contour))
                cv2.rectangle(threshLight, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(threshLight, "L", (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 0, 0), 3)
        return isLightsOn        

    def detectMovement_v2(self,current_frame, initialFrame1,count):
        self.movementFrameArray = cv2.imread(self.movementFrame)    
        self.nomovementFrameArray = cv2.imread(self.nomovementFrame)
        
        isMovementDetected=False
        diff = cv2.absdiff(current_frame, initialFrame1)
        
        cv2.namedWindow("Difference");
        cv2.moveWindow("Difference", 400, 0);
        diff = cv2.resize(diff,(380,240))                

        cv2.imshow('Difference ',diff) 
        
        _, thresh = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)
        
        dilated = cv2.dilate(thresh, None, iterations=3)
        
        contours, _ = cv2.findContours(
            dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
        for contour in contours:
            count=count+1
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 50000:
                if isMovementDetected==True:
                    isMovementDetected=True
                else :
                    isMovementDetected=False
                
                x2,y2,w2,h2 = 0,20,275,95
                # Draw black background rectangle
                cv2.rectangle(current_frame, (x2, x2), (x2 + w2, y2 + h2), (0,0,0), -1)
                # Add text
                cv2.putText(current_frame, "No Movement", (x2 + int(w2/10),y2 + int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
            else:
                
                isMovementDetected=True
                x1,y1,w1,h1 = 0,20,275,95
                
                # Draw black background rectangle
                cv2.rectangle(current_frame, (x1, x1), (x1 + w1, y1 + h1), (0,0,0), -1)
                
                # Add text
                cv2.putText(current_frame, "Movement Detected", (x1 + int(w1/10),y1 + int(h1/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

                cv2.rectangle(current_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        ###############MOVEMENT DETECTED 
        if isMovementDetected==True:
            
            isLightsON = self.checkIfLightStarted(diff)
            if isLightsON==True:
                print('MOTION DETECT DUE TO LIGHT')   
                future = self.executor.submit(self.doParallelTask,current_frame,True)
            else:
                print('Moton detected')
                future = self.executor.submit(self.doParallelTask,current_frame,False)
            #cv2.imshow('STATUS',self.movementFrameArray)
        else :
            #cv2.imshow('STATUS',self.nomovementFrameArray)
            isLightsON = self.checkIfLightStarted(diff)
            if isLightsON==True:
                print('MOTION DETECT DUE TO LIGHT')   
                future = self.executor.submit(self.doParallelTask,current_frame,True)
            else:
                print('NO MOTION')   
            
    def convertToHSV(self,img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = ((img_hsv > np.array([0, 0, 230])).astype(np.float32) + (img_hsv > np.array([0, 0, 230])).astype(np.float32) * (-0.5) + 0.5)
        img_partly_darken = cv2.cvtColor(mask * img_hsv, cv2.COLOR_HSV2BGR)
        cv2.imshow('HSV',cv2.cvtColor(img_partly_darken, cv2.COLOR_BGR2RGB))
        
        
    def liveCameAnalysis_v2(self):
        rtsp = appcfg.DETECT.CAM_RTSP
        
        if appcfg.DETECT.INPUTVIDEO_SOURCE=='CAM':
            #Use this if you want to use integrated camera
            #vid = cv2.VideoCapture(0)    
            
            vid = cv2.VideoCapture(rtsp)    
        else:
            vid = cv2.VideoCapture(appcfg.DETECT.VIDEO_IN)

        firstFrame = None
        count=0;
        priviousFrame=None
        cv2.imshow("Input", cv2.imread(self.lightthreshhold)) 
        cv2.createTrackbar('slider', 'Input', 100, 255, self.on_change)
        cv2.setTrackbarPos('slider','Input',180)
        while True:
            return_value, frame= vid.read()
            #frame=self.utility.resizeImage(frameOrg,320,320)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            cv2.imshow('HSVIMAGE',gray)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            #gray = cv2.bilateralFilter(gray,9,75,75)
            if firstFrame is None:
                firstFrame = gray
                priviousFrame = firstFrame
            count=count+1
            
            if appcfg.DETECT.DETECT_MOTION==True:
                #gray = cv2.Canny(gray, 10, 200)
                #self.convertToHSV(frame)
                self.detectMovement_v2(gray, firstFrame, count)
                #frame = self.utility.auto_canny(gray)
                            
            cv2.namedWindow("InputFrame");
            cv2.moveWindow("InputFrame", 0, 0);
            frame = cv2.resize(frame,(380,240))                
            cv2.imshow("InputFrame", frame)            
            
            priviousFrame = frame
            if cv2.waitKey(1) & 0xFF == ord('q'): break
            
        cv2.destroyAllWindows()

    
    
    
    """
    This method is only for testing purppse
    """
    
    def testParallel(self):
        milliseconds = 1627638990692
        
    
        fileName = str(milliseconds)+'.jpg'
        
        fileWithPath = self.output_loc+'/'+fileName
        print(fileWithPath)    
        
        messageTobeSent='Testing messaeg from here'
        self.twilioUtil.sendSMS(messageTobeSent,'+15109747406', '+919890678703',self.TWILIO_ACCT_ID,self.TWILIO_ATUH_TOKEN)  

    
if __name__ == "__main__":
    camvision = CamVisionDNN()
    camvision.initApp()
    #This is for sending out the Image over SMS whenever the movement is detected
    camvision.executor = ThreadPoolExecutor(max_workers=3)
    camvision.liveCameAnalysis_v2()
