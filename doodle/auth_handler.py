#encoding: utf-8

import tornado
from .config import *
from tornado import gen
from .base_handler import *
from dynamo import User

class AuthHandler(BaseHandler):

    @property 
    def table(self):
        return self.dynamo.get_table(USER_TOPIC_TABLE)

    @property 
    def sns_table(self):
        self.dynamo.get_table(USER_APNS_SNS_TABLE)

    """
        User Login and re-subscribe users topics
    """
    
    @gen.coroutine
    def post(self):
        client_data = self.data
        userid = yield verify_pwd(
            client_data['email'], 
            client_data['password'],
            self.dynamo
            )

        # verify user logged in
        
        if not userid:
            self.send_error(403)
            return

        # split and subscribe user's topics

        topic_and_subid_string = self.table.get_item(userid)['TopicList']
        topic_and_subid_list = topic_and_subid_string.split(';')
        if not (len(topic_list) == 1 and topic_list[0] == ''):
            endpoint_info = yield self.sns_table.get_item(client_data['apns'])
            endpoint = endpoint_info['APNsToken']
            for topic_and_subid in topic_and_subid_list:
                #   TODO if gets error
                topic_arn = topic_and_subid.split('|')[0]
                yield self.sns.subscribe(topic_arn, "application", endpoint)

        # set user memcache token

        token = User.create_token(userid, self.memcache)
        self.write_json({
            "result" : "OK",
            "token"  : token
            })


    """
        User Logout and un-subrscribe users topics
    """

    @async_login_required
    @gen.coroutine
    def delete(self):
        userid = self.current_user

        if not userid:
            self.send_error(403)
            return

        # split and unsubscribe user's topics

        topic_and_subid_string = self.table.get_item(userid)['TopicList']
        topic_and_subid_list = topic_and_subid_string.split(';')
        if not (len(topic_list) == 1 and topic_list[0] == ''):
            endpoint_info = yield self.sns_table.get_item(client_data['apns'])
            endpoint = endpoint_info['APNsToken']
            for topic_and_subid in topic_and_subid_list:
                #   TODO if gets error
                subid = topic_and_subid.split('|')[1]
                yield self.sns.unsubscribe(subid)
                
        # delete user memcache token

        del self.memcache[userid]
        self.write_json({"result" : "OK"})            









