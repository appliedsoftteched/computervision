# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 18:38:31 2021

@author: RPODDAR
"""

from twilio.rest import Client

class TwilioUtil:
    
    def sendSMS(self,message,fromNum,toNum,account_sid,auth_token):
        # Your Account SID from twilio.com/console
        # Your Auth Token from twilio.com/console
        print('SENDING SMS ')
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            to=toNum, 
            from_=fromNum,
            body=message)
        
        print(message.sid)

if __name__ == "__main__":
    utilSS = TwilioUtil()
    #uploaded = utilSS.sendSMS('+15109747406', '+919890678703')    
