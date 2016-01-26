import tornado
from .config import *
from tornado import gen
from .base_handler import *
import re
from boto.dynamodb2.table import Table
from .helper import *

class ContactlistHandler(BaseHandler):

	@property 
    def user_friend_table(self):
        return Table(USER_FRIEND_TABLE, connection=self.dynamo)

    @property 
    def user_table(self):
        return Table(USER_TABLE, connection=self.dynamo)

    @async_login_required
    @gen.coroutine
    def post(self):
    	client_data = self.data
    	email = client_data['Email']
    	user_emailid, email_provider = email.split('@')
    	contact_list = client_data['contacts']
    	email_list = []
    	phone_list = []

        # fetch by ppl's email or phone
    	for contact in contact_list:
    		if contact['Email'] != ';':
    			contact_emailid, contact_emailprovider = contact['Email'].split('@')
                # same school required
    			if contact_emailprovider == email_provider:
    				email_list.append({'Email' : contact_emailprovider})
    		elif contact['Phone'] != ';'
    			phone_list.append({'Phone' : contact['Phone']})

    	# filter out users
        email_result = user_table.scan(Email_in=email_list)
    	phone_result = user_table.scan(Phone_in=phone_list)

    	to_be_friend_list = []

    	for user in email_result:
    		to_be_friend_list.append(user['UserID'])

    	for user in phone_result:
    		email_id, school_name = user['Email'].split('@')
            # same school required
    		if school_name == email_provider:
    			to_be_friend_list.append(user['UserID'])

        # add mutual friends
        current_user = self.user_friend_table.get_item(UserID=self.current_userid)
        for to_be_friend_userid in to_be_friend_list:
            to_be_friend_user = self.user_friend_table.get_item(UserID=to_be_friend_userid)
            # check if the userid duplicates in current user
            rel_friend = re.search(to_be_friend_userid, current_user['FriendList'])
            if rel_friend == None:
                current_user['FriendList'] = list_append_item(to_be_friend_userid, current_user['FriendList'])
            # check if the userid duplicates in friend user
            rel_friend = re.search(self.current_userid, to_be_friend_user['FriendList'])
            if rel_friend == None:
                to_be_friend_user['FriendList'] = list_append_item(self.current_userid, to_be_friend_user['FriendList'])
                to_be_friend_user.save()

        current_user.save()

        self.write_json({
            'result' : 'ok'
        })







