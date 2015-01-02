#encoding: utf-8

import tornado
from .config import *
from tornado import gen
from .base_handler import *

class ClientHandler(BaseHandler):

    @property
    def user_apns_sns_table(self):
        return self.dynamo.get_table(USER_APNS_SNS_TABLE)


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
        item = self.user_apns_sns_table.new_item(
            hash_key=self.data['deviceToken'],
            attrs=attrs
        )
        yield gen.maybe_future(item.put())
        self.write_json({
            'result' : 'ok'
            })










