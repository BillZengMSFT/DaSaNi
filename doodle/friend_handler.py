#encoding: utf-8

import tornado
from .config import *
from tornado import gen
from .base_handler import *
import re


class FriendHandler(BaseHandler):

    @property 
    def friend_table(self):
        return self.dynamo.get_table(USER_FRIEND_TABLE)

    @property 
    def user_table(self):
        return self.dynamo.get_table(USER_TABLE)

    @async_login_required
    @gen.coroutine
    def post(self):
        client_data = self.data
        if client_data['type'] == 'test':
            self.test_friendship()
        elif client_data['type'] == 'create':
            friend_user_id = client_data['friend']
            current_user = self.friend_table.get_item(self.current_userid)
            friend_user = self.friend_table.get_item(friend_user_id)

            rel_friend = re.search(friend_user_id, current_user['FriendList'])
            if rel_friend == None:
                if current_user['FriendList'] == ';':
                    current_user['FriendList'] = ''
                current_user['FriendList'] += friend_user_id+';'
                current_user.put()

            rel_friend = re.search(self.current_userid, friend_user['FriendList'])
            if rel_friend == None:
                if friend_user['FriendList'] == ';':
                    friend_user['FriendList'] = ''
                friend_user['FriendList'] += self.current_userid+';'
                friend_user.put()
        
        self.write_json({
            "result":"ok"
            })


    @async_login_required
    @gen.coroutine
    def delete(self):
        client_data = self.data
        friend_user_id = client_data['friend']
        current_user = self.friend_table.get_item(self.current_userid)
        friend_user = self.friend_table.get_item(friend_user_id)

        rel_friend = re.search(friend_user_id, current_user['FriendList'])
        if rel_friend != None:
            friends = current_user['FriendList'].split(friend_user_id+';')
            new_friend_list = ''
            for f in friends:
                new_friend_list += f
            if new_friend_list == '':
                new_friend_list = ';'
            current_user['FriendList'] = new_friend_list
            current_user.put()

        rel_friend = re.search(self.current_userid, friend_user['FriendList'])
        if rel_friend != None:
            friends = friend_user['FriendList'].split(self.current_userid+';')
            new_friend_list = ''
            for f in friends:
                new_friend_list += f
            if new_friend_list == '':
                new_friend_list = ';'
            friend_user['FriendList'] = new_friend_list
            friend_user.put()
            self.write_json({
                "result":"ok"
            })
        
        


    @async_login_required
    @gen.coroutine
    def get(self):
        response = []
        current_user = self.friend_table.get_item(self.current_userid)
        friend_list = current_user['FriendList'].split(';')
        for uid in friend_list:
            if uid != "":
                user = self.user_table.get_item(uid)
                cleaned_user = user_object_filter(user)
                response.append(cleaned_user)

        self.write_json({'result' : response})


    @async_login_required
    @gen.coroutine
    def test_friendship(self):
        client_data = self.data
        friend_user_id = client_data['friend']
        current_user = self.friend_table.get_item(self.current_userid)
        rel_friend = re.search(friend_user_id, current_user['FriendList'])
        print(rel_friend)
        if rel_friend == None:
            self.write_json({'result' : 'fail'})
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











