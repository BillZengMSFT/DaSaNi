#encoding: utf-8

import tornado
from .config import *
from tornado import gen
from .base_handler import *
from dynamo import User

class AuthHandler(BaseHandler):

    @property 
    def user_topic_table(self):
        return self.dynamo.get_table(USER_TOPIC_TABLE)

    @property 
    def user_apns_sns_table(self):
        return self.dynamo.get_table(USER_APNS_SNS_TABLE)

    '''
        User Login and re-subscribe users topics
    '''
    
    @gen.coroutine
    def post(self):
        client_data = self.data
        userid = yield User.verify_pwd(
            client_data['email'], 
            client_data['password'],
            self.dynamo
            )
        
        # verify user logged in
        
        if not userid:
            self.write_json_with_status(403,{
                'result' : 'fail',
                'reason' : 'authantication failed'
                })
            return

        # log out other devices
        if userid in self.memcache:
            yield self.user_logout(userid)

        # split and subscribe user's topics

        if self.user_topic_table.has_item(userid):
            
            topic_and_subid = self.user_topic_table.get_item(userid)
            topic_and_subid_string = topic_and_subid['TopicList']
            
            topic_and_subid_list = topic_and_subid_string.split(';')
            topic_and_subid_list = topic_and_subid_string.split(';')

            if not (len(topic_and_subid_list) == 2 and topic_and_subid_list[0] == ''):
                new_topic_list = ';'
                endpoint_info = yield gen.maybe_future(self.user_apns_sns_table.get_item(client_data['apns']))
                endpoint = endpoint_info['APNsToken']
                
                for topic_and_subid in topic_and_subid_list:
                    topic_arn = topic_and_subid.split('|')[0]
                    # optimistic continue
                    try:
                        new_subid = yield gen.maybe_future(self.sns.subscribe(topic_arn, 'application', endpoint))
                        # replace old subscription id 
                        new_topic_list = list_append_item(
                            topic_arn+'|'+new_subid, 
                            new_topic_list
                        )
                    except Exception as e:
                        print(e)
                        continue
                
                topic_and_subid['TopicList'] = new_topic_list

        # set user memcache token

        token = User.create_token(userid, self.memcache)

        self.write_json({
            'result' : 'OK',
            'token'  : token
        })


    '''
        User Logout and un-subrscribe users topics
    '''

    @async_login_required
    @gen.coroutine
    def delete(self):
        yield self.user_logout(self.current_userid)
        self.write_json({'result' : 'OK'})            



    @gen.coroutine
    def user_logout(self, userid):

        if not userid:
            self.write_json_with_status(403,{
                'result' : 'fail',
                'reason' : 'authantication failed'
                })
            return

        if self.user_topic_table.has_item(userid):
            
            # split and unsubscribe user's topics
            
            topic_and_subid = self.user_topic_table.get_item(userid)
            topic_and_subid_string = topic_and_subid['TopicList']
            topic_and_subid_list = topic_and_subid_string.split(';')

            if not (len(topic_and_subid_list) == 2 and topic_and_subid_list[0] == ''):
                endpoint_info =  self.user_apns_sns_table.get_item(client_data['apns'])
                endpoint = endpoint_info['APNsToken']
                
                for topic_and_subid in topic_and_subid_list:
                    #   TODO if gets error
                    subid = topic_and_subid.split('|')[1]
                    # optimistic continue
                    try:
                        self.sns.unsubscribe(subid)
                    except Exception as e:
                        print(e)
                        continue
        
        # delete user memcache token

        del self.memcache[userid]




