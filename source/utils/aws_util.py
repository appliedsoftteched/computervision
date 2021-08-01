# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 17:28:45 2021

@author: RPODDAR
"""

import sys
import numpy as  np
#from appconfig import appcfg
import cv2
import time
from numpy import asarray
import boto3
from botocore.exceptions import NoCredentialsError



class AwsUtil:
    
  

    def hasIt():
        print('Yes it is in aws')
    
    def uploadToAws(self,local_file, bucket, s3_file,ACCESS_KEY,SECRET_KEY):
        print('uploadToAws')
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
        
        try:
            local_file = 'D:/knowledgebase/ml_ext/git/Computer_Vision/rm_after_try/output/'+s3_file
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


    
    
if __name__ == "__main__":
    utilSS = AwsUtil()
    uploaded = utilSS.uploadToAws('../output/1627649929798.jpg', 'compvision', '1627649929798.jpg','AKIAXKDGAKHAE2Y3BQNK','47DwH9BsG/7XfJqpP+cT+iHTXsra7DnjGoNIrvaB')    
