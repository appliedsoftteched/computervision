# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 15:35:52 2021

@author: RPODDAR
"""
# importing OpenCV, time and Pandas library
import cv2, time, pandas
# importing datetime class from datetime library
from datetime import datetime
import time
import numpy as np

class Utility: 

    def getCurrentTimeStamp():       
        ts = time.time()
        return ts
    
    def getElapsedTime(currentTime,previousTime):
        elapsedTime=currentTime-previousTime
        return elapsedTime
    
    def resizeImage(self,img_array,x_pixel,y_pixel):    
        """
        Resizes the Image as per input 
        """ 
        #img_array = cv2.imread(img)
        resized_image = cv2.resize(img_array, (x_pixel, y_pixel))
        return resized_image
    
    def auto_canny(image, sigma=0.33):
    	# compute the median of the single channel pixel intensities
    	v = np.median(image)
    	# apply automatic Canny edge detection using the computed median
    	lower = int(max(0, (1.0 - sigma) * v))
    	upper = int(min(255, (1.0 + sigma) * v))
    	edged = cv2.Canny(image, lower, upper)
    	# return the edged image
    	return edged