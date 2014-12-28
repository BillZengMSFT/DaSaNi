#encoding: utf-8

import tornado
from .config import *
from tornado import gen
from .base_handler import *
import re


class FriendHanlder(BaseHandler):

    @property 
    def table(self):
        return self.dynamo.get_table(USER_FRIEND_TABLE)

    @property 
    def user_table(self):
        return self.dynamo.get_table(USER_TABLE)

    @async_login_required
    @gen.coroutine
    def post(self):
        client_data = self.data
        current_user_id = self.current_user
        friend_user_id = client_data['friend']
        current_user = self.table.get_item(current_user_id)
        friend_user = self.table.get_item(friend_user_id)

        rel_friend = re.search(friend_user_id, current_user['FriendList'])
        if rel_friend == None:
            current_user['FriendList'] += friend_user_id+';'

        rel_friend = re.search(current_user_id, friend_user['FriendList'])
        if rel_friend == None:
            friend_user['FriendList'] += current_user_id+';'

        current_user.put()
        friend_user.put()


    @async_login_required
    @gen.coroutine
    def delete(self):
        client_data = self.data
        friend_user_id = client_data['friend']
        current_user = self.table.get_item(current_user_id)
        friend_user = self.table.get_item(friend_user_id)

        rel_friend = re.search(friend_user_id, current_user['FriendList'])
        if rel_friend != None:
            friends = current_user['FriendList'].split(friend_user_id+';')
            new_friend_list = ''
            for f in friends:
                new_friend_list += f
            current_user['FriendList'] = new_friend_list

        rel_friend = re.search(current_user_id, friend_user['FriendList'])
        if rel_friend != None:
            friends = friend_user['FriendList'].split(current_user_id+';')
            new_friend_list = ''
            for f in friends:
                new_friend_list += f
            friend_user['FriendList'] = new_friend_list

        current_user.put()
        friend_user.put()

    @async_login_required
    @gen.coroutine
    def get(self):
        response = []
        current_user = self.table.get_item(current_user_id)
        friend_list = current_user['FriendList'].split(";")

        for uid in friend_list:
            user = self.user_table.get_item(uid)
            cleaned_user = user_object_filter(user)
            response.append(cleaned_user)

        self.write_json(response)



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











