#encoding: utf-8

import tornado

from .config import *
from tornado import gen
from .base_handler import *
from boto.dynamodb2.table import Table

class ClientHandler(BaseHandler):


    @property
    def user_apns_sns_table(self):
        return Table('User_APNs_SNS_Table',connection=self.dynamo)


    @gen.coroutine
    def add_sns_app_endpoint(self):
        client_data = self.data
        device_token = client_data['deviceToken']
        response = self.sns.create_platform_endpoint(
            AWS_SNS_IOS_APP_ARN,
            device_token
        )
        aws_endpoint_arn = response['CreatePlatformEndpointResponse']['CreatePlatformEndpointResult']['EndpointArn']
        return aws_endpoint_arn

    """
        Create new sns subcription to App
    """

    @gen.coroutine
    def post(self):
        aws_endpoint_arn = yield self.add_sns_app_endpoint()
        attrs = {
            'APNsToken' : self.data['deviceToken'], 
            'SNSToken'  : aws_endpoint_arn,
            'UserID'    : ';'
            }
        item =  yield gen.maybe_future(self.user_apns_sns_table.put_item(data={
                'APNsToken' : self.data['deviceToken'], 
                'SNSToken'  : aws_endpoint_arn,
                'UserID'    : ';'
            }
        ))
       
        self.write_json({
            'result' : 'ok'
            })






