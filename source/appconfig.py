"""
This is for application level configuration

"""

from easydict import EasyDict as edict
__APP_CONFIG                           = edict()
# Import this as from appconfig import appcfg

appcfg                           = __APP_CONFIG
    
__APP_CONFIG.DETECT                         = edict()
__APP_CONFIG.DETECT.PROCESSED_IMAGE_OUT     = '.output'
__APP_CONFIG.DETECT.VIDEO_IN     = './input/India - 8698.mp4'
__APP_CONFIG.DETECT.CORE_PACKAGES = '../compvision/utils'
__APP_CONFIG.DETECT.SHOW_OBJECT_COUNT = True
__APP_CONFIG.DETECT.SAVE_PEOPLE_ROI = True
__APP_CONFIG.DETECT.DETECT_MOTION = True
__APP_CONFIG.DETECT.INPUTVIDEO_SOURCE='CAM'
__APP_CONFIG.DETECT.CAM_RTSP='rtsp://192.168.1.3:8080/h264_pcm.sdp'
__APP_CONFIG.DETECT.SEND_SMS = False
__APP_CONFIG.DETECT.SMS_FROM_NO = '+15109747406'
__APP_CONFIG.DETECT.SMS_TO_NO = '+919890678703'
__APP_CONFIG.DETECT.S3_BASE_URL = 'https://compvision.s3.amazonaws.com/'

#Place your AWS KEYS HERE
__APP_CONFIG.DETECT.AWS_ACCESS_KEY='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
__APP_CONFIG.DETECT.AWS_SECRET_KEY='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

#Place your TWILIO KEYS HERE
__APP_CONFIG.DETECT.TWILIO_ACCT_ID='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
__APP_CONFIG.DETECT.TWILIO_ATUH_TOKEN='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'





#__APP_CONFIG.TRAIN                     = edict()