#encoding: utf-8
import uuid
import tornado
import boto.dynamodb
from tornado import gen
from .base_handler import BaseHandler



class ClientHandler(BaseHandler):

	def post(self):
		self.addEndpoint()
		return

	@gen.coroutine
	def addEndpoint(self):
		clientData = self.data
		deviceToken = clientData['deviceToken']
		awsIosAppArn = 'arn:aws:sns:us-west-2:878165105740:app/APNS_SANDBOX/CarlorDev'
		response = self.sns.create_platform_endpoint(
			awsIosAppArn,
			deviceToken
			)
		tornado.log(response)
		awsEndPointArn = response['CreatePlatformEndpointResponse']['CreatePlatformEndpointResult']['EndpointArn']
		return awsEndPointArn

	def getDynamoDB():
		conn = boto.dynamodb.connect_to_region(
			'us-west-2',
        	aws_access_key_id='AKIAJNDFKACQ6253GVXQ',
        	aws_secret_access_key='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')
		return conn

	@gen.coroutine
	def storeUser(self):
		awsEndPointArn = self.addEndpoint
		DB = getDynamoDB()
		table = DB.get_table('User_APNs_SNS_Table')
		userID = uuid.uuid1();
		attrs = {'UserID' : userID, 'SNSToken' : self.data['deviceToken'], 'awsEndPointArn' : awsEndPointArn}
		item = table.new_item(attrs=attrs)
		
