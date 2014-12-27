#encoding: utf-8

import tornado
from .config import *
from tornado import gen
from .base_handler import *

class ClientHandler(BaseHandler):

	@property
	def table(self):
		return self.dynamo.get_table(USER_APNS_SNS_TABLE)


	def addSNSAppEndpoint(self):
		clientData = self.data
		deviceToken = clientData['deviceToken']
		response = self.sns.create_platform_endpoint(
			AWS_SNS_IOS_APP_ARN,
			deviceToken
			)
		awsEndPointArn = response['CreatePlatformEndpointResponse']['CreatePlatformEndpointResult']['EndpointArn']
		return awsEndPointArn

"""
	Create new sns subcription to App
"""

	@async_login_required
	@gen.coroutine
	def post(self):
		awsEndPointArn = self.addSNSAppEndpoint()
		userID = self.current_user
		attrs = {
			'UserID' : userID, 
			'APNsToken' : self.data['deviceToken'], 
			'SNSToken' : awsEndPointArn
			}
		item = self.table.new_item(attrs=attrs)
		item.put()

"""
    Delete sns subcription to App
"""

	











