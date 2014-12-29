#encoding: utf-8

import tornado
from .config import *
from tornado import gen
from .base_handler import *

class ClientHandler(BaseHandler):

    @property
    def table(self):
        return self.dynamo.get_table(USER_APNS_SNS_TABLE)


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

    @async_login_required
    @gen.coroutine
    def post(self):
        aws_endpoint_arn = self.add_sns_app_endpoint()
        userid = self.current_user
        attrs = {
            'UserID' : userid, 
            'APNsToken' : self.data['deviceToken'], 
            'SNSToken' : aws_endpoint_arn
            }
        item = self.table.new_item(attrs=attrs)
        item.put()










