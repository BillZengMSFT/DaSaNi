#encoding: utf-8

import tornado
import config
from tornado import gen
from .base_handler import *

class ClientHandler(BaseHandler):

	def addSNSAppEndpoint(self):
		clientData = self.data
		deviceToken = clientData['deviceToken']
		response = self.sns.create_platform_endpoint(
			config.AWS_SNS_IOS_APP_ARN,
			deviceToken
			)
		tornado.log(response)
		awsEndPointArn = response['CreatePlatformEndpointResponse']['CreatePlatformEndpointResult']['EndpointArn']
		return awsEndPointArn

"""
	Create new sns subcription to App
"""

	@async_login_required
	@gen.coroutine
	def post(self):
		awsEndPointArn = self.addSNSAppEndpoint()
		table = self.dynamo.get_table(config.USER_APNS_SNS_TABLE)
		userID = self.current_user
		attrs = {
			'UserID' : userID, 
			'APNsToken' : self.data['deviceToken'], 
			'SNSToken' : awsEndPointArn
			}
		item = table.new_item(attrs=attrs)
		item.put()



"""
	Delete sns subcription to App
"""
	
	
	












