#encoding: utf-8

import tornado
import time
import re
from .config import *
from tornado import gen
from .base_handler import *
from .helper import *
from boto.dynamodb2.table import Table

class PhoneHandler(BaseHandler):
    @property 
    def user_table(self):
        return Table('User_Table',connection=self.dynamo)

    @async_login_required
    @gen.coroutine
    def post(self):
        """
        PAYLOAD:
        {
            "phone":"a serious phone number,format:1aaabbbcccc"
        }
        """
        client_data = self.data
        # check if the number is registered by another user
        is_occupied = len([u for u in self.user_table.scan({'Phone':EQ(client_data['phone']),'PhoneActive':EQ(1)})])
        if is_occupied:
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'this phone number has been used'
                })

        userid = self.current_userid
        sns_arn = config.AWS_SNS_MESSAGE_ARN
        # should we check phone number format validity here?
        try:
            self.sns_east.subscribe(sns_arn,"sms",client_data['phone'])
            self.write_json_with_status(200,{
                'result' : 'ok'
                })
        except:
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'unable to subscribe, maybe wrong number provided'
                })

    @async_login_required
    @gen.coroutine 
    def get(self):
        """
        check if current user has subscribed to message topic
        """
        user = self.user_table.get_item(UserID=self.current_userid)
        try:
            user_phone_number = user['Phone']
        except:
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'please update your phone number before verifying it'
                })
        all_sub = self.sns_east.get_all_subscriptions_by_topic(config.AWS_SNS_MESSAGE_ARN)

        try:
            for sub in all_sub['ListSubscriptionsByTopicResponse']['ListSubscriptionsByTopicResult']['Subscriptions']:
                if sub['Endpoint'] == user_phone_number and sub['SubscriptionArn'] != 'PendingConfirmation':
                    # update user infomation
                    user['PhoneActive'] = True
                    user.partial_save()

                    # send message back to client
                    self.write_json_with_status(200,{
                        'result' : 'ok'
                    })
        except:
            self.write_json_with_status(500,{
                'result' : 'fail',
                'reason' : 'AWS does not return a valid dictionary',
                }


        # number not found
        self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'number not subscribed'
            })
