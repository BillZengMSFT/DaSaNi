#encoding: utf-8
import uuid
import tornado
import boto.dynamodb
from tornado import gen
from .base_handler import BaseHandler

	@gen.coroutine
	def addEndpoint(self):
		deviceToken = self.data['deviceToken']
		response = self.sns.create_platform_endpoint(
			AWS_SNS_IOS_APP_ARN,
			deviceToken
			)
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
		awsEndpointArn = self.addEndpoint
		DB = getDynamoDB()
		table = DB.get_table('User_APNs_SNS_Table')
		userID = uuid.uuid1();
		attrs = {'UserID' : userID, 'SNSToken' : self.data['deviceToken'], 'awsEndpointArn' : awsEndpointArn}
		item = table.new_item(attrs=attrs)
		