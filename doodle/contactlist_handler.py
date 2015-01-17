import tornado
from .config import *
from tornado import gen
from .base_handler import *
import re
from .helper import *

class ContactlistHandler(BaseHandler):

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
    	email = client_data['Email']
    	user_emailid, email_provider = email.split('@')
    	contact_list = client_data['contacts']
    	email_list = []
    	phone_list = []

    	for contact in contact_list:
    		if contact['Email'] != '':
    			contact_emailid, contact_emailprovider = contact['Email'].split('@')
    			if contact_emailprovider == email_provider:
    				email_list.append({'Email' : contact_emailprovider})
    		else
    			phone_list.append({'Phone' : contact['Phone']})

    	user_list = current_user['FriendList'].split(';')

    	email_result = user_list.batch_get(keys=email_list)
    	phone_result = user_list.batch_get(keys=phone_list)

    	return_list = []

    	for user in email_result:
    		if user['UserID'] != '':
    			return_list.append({'UserID' : user['UserID']})

    	for user in phone_result:
    		if user['UserID'] != '':
    			email_id, school_name = user['Email'].split('@')
    			if school_name == email_provider:
    				reutrn_list.append({'UserID' : user['UserID']})

    	return return_list
