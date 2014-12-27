#encoding: utf-8

import tornado
from .config import *
from tornado import gen
from .base_handler import *
from tornado.log import logging
from logging import debug as log

class ClientHandler(BaseHandler):

    def addSNSAppEndpoint(self):
        try:
            clientData = self.data
            deviceToken = clientData['deviceToken']
            response = self.sns.create_platform_endpoint(
            AWS_SNS_IOS_APP_ARN,
            deviceToken+"1"
            )
        except:
            return
        

    """
    Create new sns subcription to App
    """

    #@async_login_required
    @gen.coroutine
    def post(self):
        awsEndPointArn = self.addSNSAppEndpoint()
        table = self.dynamo.get_table(USER_APNS_SNS_TABLE)
        userID = self.current_user
        attrs = {
            'UserID' : "lz2",#userID, 
            'APNsToken' : self.data['deviceToken'], 
            'SNSToken' : awsEndPointArn
            }
        item = table.new_item(attrs=attrs)
        item.put()



"""
    Delete sns subcription to App
"""
    
    
    












