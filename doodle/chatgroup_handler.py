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

    @property 
    def user_table(self):
        return self.dynamo.get_table(USER_TABLE)

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

        members = memberlist.split(';')
        for member in members:
            self.__add_user_to_topic(member)

    """
        accept application / accept invitation / leave  
    """

    @async_login_required
    @gen.coroutine
    def put(self):
        client_data = self.data
        request_type = client_data['type']
        choice = client_data['choice']
        chatgroup_id = client_data['chatgroup_id']
        inbox_id = client_data['inbox_id']
        if request_type == 'application':
            self.__chatgroup_application(client_data['who_apply'], chatgroup_id, self.current_user, choice, inbox_id)
        elif request_type == 'invitation':
            self.__chatgroup_invitation(client_data['who_invite'], chatgroup_id, self.current_user, choice, inbox_id)
        elif request_type == 'leave':
            self.__chatgroup_leave(self.current_user, chatgroup_id, choice, inbox_id)

    """
        Create or update user's joined topic list
    """

    def __add_user_to_topic(self, member):
        if self.user_topic_table.has_item(member):
                user_topic = self.user_topic.get_item(member)
                user_topic['TopicList'] += sns_arn+';'
                user_topic.put()
            else:
                attrs = {
                    'UserID'    : member,
                    'TopicList' : sns_arn+';'
                }
                item = self.user_topic_table.new_item(
                    hash_key=member, 
                    attrs=attrs
                )
                item.put()

    def __chatgroup_application(self, who_apply, chatgroup_id, who_decide, choice, inbox_id):
        if choice == 'accept':
            # update chatgroup member list
            chatgroup = self.table.get_item(chatgroup_id)
            chatgroup['MemberList'].append(who_apply+';')

            # push info to others
            who_to_join = self.user_table.get_item(who_apply)
            message = who_to_join['Firstname']+' '+who_to_join['Lastname']+' joined this group :)'
            sns_topic = chatgroup['SNS']
            self.sns.publish(
                topic=sns_topic,
                message=message
            )

            # subscribe to sns topic
            

            # add user to topic list
            self.__add_user_to_topic(who_apply)

        # update inbox status

        # return chatgroup info


    def __chatgroup_invitation(self, who_invite, chatgroup_id, who_decide, choice, inbox_id):


    def __chatgroup_leave(self, who_leave, chatgroup_id, choice, inbox_id):










