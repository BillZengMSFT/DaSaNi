#encoding: utf-8

import tornado
import time
import re
from .config import *
from tornado import gen
from .base_handler import *
from .helper import *

class ChatgroupHandler(BaseHandler):

    @property 
    def chatgroup_table(self):
        return self.dynamo.get_table(CHATGROUP_TABLE)

    @property 
    def user_topic_table(self):
        return self.dynamo.get_table(USER_TOPIC_TABLE)

    @property 
    def user_table(self):
        return self.dynamo.get_table(USER_TABLE)

    @property 
    def user_apns_sns_table(self):
        return self.dynamo.get_table(USER_APNS_SNS_TABLE)

    @property 
    def user_inbox_table(self):
        return self.dynamo.get_table(USER_INBOX_TABLE)

    """
        Create a new chatgroup
    """
    
    @async_login_required
    @gen.coroutine
    def post(self):
        client_data = self.data

        event_id = option_value(client_data, 'eventid')

        timestamp = str(time.time()).split('.')[0]

        chatgroup_id = md5(self.current_userid+timestamp)

        # create a new queue for chat
        sqs_response = self.sqs.create_queue(
            chatgroup_id
        )
        sqs_arn = sqs_response._arn()

        # create a new topic for push
        sns_response = self.sns.create_topic(
            chatgroup_id
        )
        sns_arn = sns_response['CreateTopicResponse']['CreateTopicResult']['TopicArn']

        # subscribe to topic 
        user = self.user_apns_sns_table.get_item(self.current_userid)
        subid = self.sns.subscribe(sns_arn, 'application', user['SNSToken'])

        # create a chatgroup in table
        attrs = {
            'ChatgroupID'   : chatgroup_id,
            'EventID'       : event_id,
            'Name'          : client_data['name'],
            'CreatorID'     : self.current_user,
            'MemberList'    : client_data['memberlist'],
            'Capacity'      : client_data['capacity'],
            'PhotoID'       : client_data['photo'],
            'SNS'           : sns_arn,
            'SQS'           : sqs_arn,
            'Timestamp'     : timestamp
        }
        item = self.chatgroup_table.new_item(
            hash_key=chatgroup_id,
            range_key=None,
            attrs=attrs
        )
        item.put()

        # add this subscription to user topic list
        members = memberlist.split(';')
        for member in members:
            self.__add_user_to_topic(member, sns_arn, subid)

        self.write_json({
            'chatgroup_id' : chatgroup_id,
            'sqs' : sqs_arn    
        })

    """
        accept application / accept invitation / leave / update
    """

    @async_login_required
    @gen.coroutine
    def put(self):
        client_data = self.data
        request_type = client_data['type']
        chatgroup_id = client_data['chatgroup_id']

        choice = option_value(client_data, 'choice')
        inbox_id = option_value(client_data, 'inbox_message_id')
        attrs = option_value(client_data, 'attrs')

        if request_type == 'application':
            self.__chatgroup_application(client_data['who_apply'], chatgroup_id, self.current_userid, choice, inbox_message_id)
        elif request_type == 'invitation':
            self.__chatgroup_invitation(client_data['who_invite'], chatgroup_id, self.current_userid, choice, inbox_message_id)
        elif request_type == 'leave':
            self.__chatgroup_leave(client_data['who_leave'], chatgroup_id)
        elif request_type == 'update':
            self.__chatgroup_update(chatgroup_id, client_data['attrs'])

    """
        Create or update user's joined topic list
    """

    def __add_user_to_topic(self, sns_topic, subscription_arn):
        if self.user_topic_table.has_item(member):
            user_topic = self.user_topic_table.get_item(member)
            user_topic['TopicList'] = list_append_item(
                sns_topic+'|'+subscription_arn, 
                user_topic['TopicList']
            )
            user_topic.put()
        else:
            attrs = {
                'UserID'    : member,
                'TopicList' : sns_topic+'|'+subscription_arn+';'
            }
            item = self.user_topic_table.new_item(
                hash_key=member, 
                attrs=attrs
            )
            item.put()

    def __chatgroup_application(self, who_apply, chatgroup_id, who_decide, choice, inbox_message_id):
        if choice == 'accept':
            # update chatgroup member list
            try:
                chatgroup = self.chatgroup_table.get_item(chatgroup_id)
            except:
                self.write_json_with_status(400,{
                    'result' : 'fail',
                    'reason' : 'invalid chatgroup id'
                    })
            if re.search(who_apply, chatgroup['MemberList']) == None:
                chatgroup['MemberList'] = list_append_item(who_apply,chatgroup['MemberList'] )

            sns_topic = chatgroup['SNS']

            # subscribe to sns topic
            try:
                user_apns_sns = self.user_apns_sns_table.get_item(who_apply)
            except:
                self.write_json_with_status(400,{
                    'result' : 'fail',
                    'reason' : 'invalid userid'
                    })
            sns_token = user_apns_sns['SNSToken']
            response = self.sns.subscribe(sns_topic, 'application', sns_token)
            subscription_arn = response['SubscribeResponse']['SubscribeResult']['SubscriptionArn']

            # add user to topic list
            self.__add_user_to_topic(sns_topic, subscription_arn)

            # push info to others
            try:
                who_to_join = self.user_table.get_item(who_apply)
            except:
                self.write_json_with_status(400,{
                    'result' : 'fail',
                    'reason' : 'invalid userid'
                    })
            message = who_to_join['Firstname']+' '+who_to_join['Lastname']+' joined this group :)'
            self.sns.publish(
                topic=sns_topic,
                message=message
            )

        # delete inbox message
        try:
            inbox_message = self.user_inbox_table.get_item(inbox_message_id)
        except:
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'invalid inbox id'
                })
        inbox_message.delete()

        # return chatgroup info
        self.write_json({
            'sqs' : chatgroup['sqs']
        })

    """
        It is same with application, who_invite has no action, 
        but who_decide has same action with who_apply
    """

    def __chatgroup_invitation(self, who_invite, chatgroup_id, who_decide, choice, inbox_message_id):
        self.__chatgroup_application(who_decide, chatgroup_id, who_decide, choice, inbox_message_id)

    def __chatgroup_leave(self, who_leave, chatgroup_id):
        # update chatgroup member list to delete user id
        try:
            chatgroup = self.chatgroup_table.get_item(chatgroup_id)
        except:
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'invalid chatgroup id'
                })
        if re.search(who_leave, chatgroup['MemberList']) != None:
            chatgroup['MemberList'] = list_delete_item(who_leave + ".*?;", chatgroup['MemberList'])
            chatgroup.put()

        sns_topic = chatgroup['SNS']

        # remove user at topic list
        try:
            user_topic = self.user_topic.get_item(member)
        except:
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'invalid userid'
            })
        match = re.search(sns_topic+'.*?;', user_topic['TopicList'])
        if match:
            _, subscription_arn = match.group()[:-1].split('|')
            topics = user_topic['TopicList'].split(atch.group())
            user_topic['TopicList'] = ''
            for topic in topics:
                user_topic['TopicList'] += topic
            user_topic.put()

            # un-subscribe to sns topic
            self.sns.unsubscribe(subscription_arn)

            # push info to others
            try:
                who_to_leave = self.user_table.get_item(who_leave)
            except:
                self.write_json_with_status(400,{
                    'result' : 'fail',
                    'reason' : 'invalid userid'
                    })
            message = who_to_leave['Firstname']+' '+who_to_leave['Lastname']+' leave this group :)'
            self.sns.publish(
                topic=sns_topic,
                message=message
            )

        # return chatgroup info
        self.write_json({'result' : 'OK'})        

    """
        Get specific chatgroup info
    """

    def __chatgroup_update(self,chatgroup_id, attrs):
        self.input_firewall(attrs)
        try:
            chatgroup = self.chatgroup_table.get_item(chatgroup_id)
        except:
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'invalid chatgroup id'
            })
        chatgroup.update(attrs)
        chatgroup.put()
        self.write_json({'result' : 'OK'})


    @async_login_required
    @gen.coroutine
    def get(self, chatgroup_id=''):
        response = {}
        try:
            chatgroup = self.chatgroup_table.get_item(chatgroup_id)
        except:
            self.set_status(400)
            self.write_json({
                "result" : "fail"
            })

        for key, val in chatgroup.itmes():
            if key != 'SNS':
                response[key] = val
        self.write_json(response)

    """
        Delete a chatgroup
            push last message
            Delete sns and sqs
            Delete members topic
            set specific chatgroup sns and sqs ;
    """

    @async_login_required
    @gen.coroutine
    def delete(self):
        client_data = self.data
        chatgroup_id = client_data['chatgroup_id']
        try:
            chatgroup = self.chatgroup_table.get_item(chatgroup_id)
        except:
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'invalid chatgroup id'
                })
        if chatgroup['creator_id'] != self.current_userid:
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'authantication failed'
                })
        sns_arn = chatgroup['SNS']
        if self.data['type'] == 'dismiss':
            message = 'This chatgroup is dismissed by group owner :('
            self.sns.publish(
                topic=sns_arn,
                message=message
            )
            sqs_arn = chatgroup['SQS']
            self.sqs.delete_queue(sqs_arn)
            self.sns.delete_topic(sns_arn)
            chatgroup['SQS'] = ';'
            chatgroup['SNS'] = ';'
            chatgroup.put()
            
            # delete member topic
            member_list = chatgroup['MemberList']
            members = member_list.split(';')

            for member in member_list:
                user_topic = self.user_topic_table.get_item(member)
                user_topic['TopicList'] = list_delete_item(member+'.*?;', user_topic['TopicList'])
                user_topic.put()

        elif client_data['type'] == 'kickout':
            self.__chatgroup_leave(client_data['who_to_kick_out'],client_data['chatgroup_id'])

        self.write_json({'result' : 'OK'})



    """
        Take input dict and validate input dict
    """

    def input_firewall(self,input_dict):

        outside_field_names = [
            'eventid',
            'name',
            'memberlist',
            'capacity',
            'photo'
        ]

        for key, val in input_dict.items():
            if key not in outside_field_names:
                self.set_status(400)
                self.write_json({ 
                    'result':'fail',
                    'reason':'Invalid Field:' + key})
            try:
                int(input_dict['capacity'])
            except:
                self.set_status(400)
                self.write_json({ 
                    'result':'fail',
                    'reason':'Invalid Field: capacity'})

            





    """
        Take output dict and return filtered dict
    """

    def output_firewall(self,output_dict):
        legal_field_names = [
            'ChatgroupID',
            'EventID',
            'Name',
            'CreatorID',
            'MemberList',
            'Capacity',
            'PhotoID',
            'SQS',
            'Timestamp',
            'chatgroup_id',
            'sqs',
            'result',
        ]

        filtered_output = {}
        for key, val in output_dict:
            if key in legal_field_names:
                filtered_output[key] = val

        return filtered_output













