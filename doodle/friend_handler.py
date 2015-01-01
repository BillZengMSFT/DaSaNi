#encoding: utf-8

import tornado
from .config import *
from tornado import gen
from .base_handler import *
import re
from .helper import *


class FriendHandler(BaseHandler):

    @property 
    def user_friend_table(self):
        return self.dynamo.get_table(USER_FRIEND_TABLE)

    @property 
    def user_table(self):
        return self.dynamo.get_table(USER_TABLE)

    @async_login_required
    @gen.coroutine
    def post(self):
        client_data = self.data
        
        # route to different functionality

        # test if friend

        if client_data['type'] == 'test':
            self.__test_friendship()

        # create a friendship

        elif client_data['type'] == 'create':
            friend_user_id = client_data['friend']
            try:
                current_user = self.user_friend_table.get_item(self.current_userid)
                friend_user = self.user_friend_table.get_item(friend_user_id)
            except:
                self.set_status(400)
                self.write_json({
                    'result' : 'fail',
                    'reason' : 'invalid userid or friend id'
                    })

            rel_friend = re.search(friend_user_id, current_user['FriendList'])
            if rel_friend == None:
                current_user['FriendList'] = list_append_item(friend_user_id, current_user['FriendList'])
                current_user.put()

            rel_friend = re.search(self.current_userid, friend_user['FriendList'])
            if rel_friend == None:
                friend_user['FriendList'] =list_append_item(self.current_userid, friend_user['FriendList'])
                friend_user.put()

            self.write_json({
                'result':'ok'
            })


    @async_login_required
    @gen.coroutine
    def delete(self):
        client_data = self.data
        friend_user_id = client_data['friend']

        try:
            current_user = self.user_friend_table.get_item(self.current_userid)
            friend_user = self.user_friend_table.get_item(friend_user_id)
        except:
            self.set_status(400)
            self.write_json({
                'result' : 'fail',
                'reason' : 'invalid userid or friend id'
                })

        rel_friend = re.search(friend_user_id, current_user['FriendList'])
        if rel_friend != None:
            friends = current_user['FriendList'].split(friend_user_id+';')
            current_user['FriendList'] = list_remove_item(
                friend_user_id + '.*?;',
                current_user['FriendList']
                )
            current_user.put()

        rel_friend = re.search(self.current_userid, friend_user['FriendList'])
        if rel_friend != None:
            friend_user['FriendList'] = list_remove_item(
                self.current_userid + '.*?;',
                friend_user['FriendList']
                )
            friend_user.put()

        self.write_json({
            'result':'ok'
        })
        
        


    @async_login_required
    @gen.coroutine
    def get(self):
        response = []
        
        try:
            current_user = self.user_friend_table.get_item(self.current_userid)
        except:
            self.set_status(400)
            self.write_json({
                'result' : 'fail',
                'reason' : 'invalid userid'
                })

        friend_list = current_user['FriendList'].split(';')

        for uid in friend_list:
            if uid != '':

                try:
                    user = self.user_table.get_item(uid)
                except:
                    # save me san francisco
                    friend_user['FriendList'] = list_remove_item(
                        uid + '.*?;',
                        friend_user['FriendList']
                    )

                cleaned_user = user_object_filter(user)
                response.append(cleaned_user)

        self.write_json({'result' : response})


    @gen.coroutine
    def __test_friendship(self):
        client_data = self.data
        friend_user_id = client_data['friend']
        
        try:
            current_user = self.user_friend_table.get_item(self.current_userid)
        except:
            self.set_status(400)
            self.write_json({
                'result' : 'fail',
                'reason' : 'invalid userid'
                })

        rel_friend = re.search(friend_user_id, current_user['FriendList'])
        if rel_friend == None:
            self.set_status(400)
            self.write_json({
                'result' : 'fail',
                'reason' : 'invalid friend userid'
                })
        else:
            self.write_json({'result' : 'ok'})


def user_object_filter(Object):
    legal_field_names = [
            'FirstName',
            'LastName',
            'Birthday',
            'Email',
            'Phone',
            'School',
            'Major',
            'Gender',
            'Signature',
            'Driver',
            'CarID',
            'PhotoID'
        ]
    cleaned_user = {}
    for key, val in Object.items():
        if key in legal_field_names:
            cleaned_user[key] = val
    return cleaned_user











