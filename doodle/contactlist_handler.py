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

    	
        email_result = user_table.batch_get(keys=email_list)
    	phone_result = user_table.batch_get(keys=phone_list)

    	add_list = []

    	for user in email_result:
    		if user['UserID'] != '':
    			add_list.append(user['UserID'])

    	for user in phone_result:
    		if user['UserID'] != '':
    			email_id, school_name = user['Email'].split('@')
    			if school_name == email_provider:
    				add_list.append(['UserID'])

    	try:
            current_user = self.user_friend_table.get_item(self.current_userid)
           
        except:
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'invalid userid or friend id'
                })



        for Id_to_add in add_list：
            current_user['FriendList'].list_append_item(Id_to_add)

        current_user.put()
            
        self.write_json({
            'result' : 'ok'
            })