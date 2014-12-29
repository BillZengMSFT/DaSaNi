#encoding: utf-8

import tornado
import time
from .config import *
from tornado import gen
from .base_handler import *
from .helper import *

class ChatgroupHandler(BaseHandler):

    @property 
    def table(self):
        return self.dynamo.get_table(CHATGROUP_TABLE)

    @proerty 
    def user_topic_table(self):
        return self.dynamo.get_table(USER_TOPIC_TABLE)

    """
        Create a new chatgroup
    """
    
    @async_login_required
    @gen.coroutine
    def post(self):
        client_data = self.data
        event_id = ''
        if client_data.has_key('EventID'):
            event_id = client_data['EventID']
        timestamp = str(time.time()).split('.')[0]
        chatgroup_id = md5(self.current_user+timestamp)
        sqs_response = self.sqs.create_queue(
            chatgroup_id
        )
        sqs_arn = sqs_response._arn()
        sns_response = self.sns.create_topic(
            chatgroup_id
        )
        sns_arn = sns_response['CreateTopicResponse']['CreateTopicResult']['TopicArn']

        attrs = {
            'ChatgroupID'   : chatgroup_id,
            'EventID'       : event_id
            'Name'          : client_data['name']
            'CreatorID'     : self.current_user,
            'MemberList'    : client_data['memberlist'],
            'Capacity'      : client_data['capacity'],
            'PhotoID'       : client_data['photo'],
            'SNS'           : sns_arn,
            'SQS'           : sqs_arn,
            'Timestamp'     : timestamp
        }
        item = self.table.new_item(attrs=attrs)
        item.put()

        if self.user_topic_table.has_item(self.current_user):
            user_topic = self.user_topic.get_item(self.current_user)
            user_topic['TopicList'] += sns_arn+';'
            user_topic.put()
        else:
            attrs = {
                'UserID'    : self.current_user,
                'TopicList' : sns_arn+';'
            }
            item = self.user_topic_table.new_item(
                hash_key=self.current_user, 
                attrs=attrs
            )
            item.put()

    """
        accept application / accept invitation / leave  
    """

    @async_login_required
    @gen.coroutine
    def put(self):
        pass






