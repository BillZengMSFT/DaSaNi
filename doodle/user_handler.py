#encoding: utf-8

import tornado
import json
from tornado import gen
from dynamo import User
from .base_handler import *
import time
import re
from .config import *
import hashlib
from .helper import *

class UserHandler(BaseHandler):

    @property
    def user_table(self):
        return self.dynamo.get_table(USER_TABLE)

    @property
    def user_activate_table(self):
        return self.dynamo.get_table(USER_ACTIVATE_TABLE)

    @gen.coroutine
    def post(self):

        self.input_firewall(self.data)

        # Get email from client and hash it

        password = self.data['password']
        email = self.data['email'].strip()

        hashed_userid = md5(email)

        # Check if this email has been registered
               
        user_exist = yield gen.maybe_future(self.user_table.has_item(hashed_userid))

        if user_exist == True:

            # tell client and stop processing this request
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'email already used'
                })

            return

        hashed_password = hash_password(password)
        
        # Build attrs for the new user

        attrs = {
            "Email"         : self.data["email"],
            "FirstName"     : self.data['firstname'],
            "LastName"      : self.data['lastname'],
            "AccountActive" : False,
            "Password"      : hashed_password,
        }
        # Create new user item and upload it to database
        new_user = self.user_table.new_item(
            hash_key=hashed_userid,
            range_key=None,
            attrs=attrs
            )
        # Send activate email
        try:
            activate_code = yield gen.maybe_future(
                send_email(
                    self.ses,
                    self.data["email"],
                    self.data["firstname"],
                    self.data["lastname"]
                )
            )
        except:
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'failed to send email'
            })

        activator_attrs = {
            "Timestamp" : str(time.time()).split(".")[0],
            "Code"      : activate_code,
            "Attempt"   : 1
        }
        
        new_user_activator = self.user_activate_table.new_item(
            hash_key=hashed_userid,
            range_key=None,
            attrs=activator_attrs
            )

        # Upload new user information and activator to AWS
        yield gen.maybe_future(new_user.put())
        yield gen.maybe_future(new_user_activator.put())
        # Only send userid back to the client

        self.write_json({
            'userid': hashed_userid,
        })


    # update a user information
    @async_login_required
    @gen.coroutine
    def put(self):
        self.input_firewall(self.data)
        user = self.user_table.get_item(self.current_userid)
        try:
            # if we are updating password, hash it
            if self.data['password']:
                self.data['password'] = hash_password(self.data['password'])
        except:
            pass
        for key, value in self.data.items():
            if not self.data[key]:
                self.data[key] = ';'
        user.update(client_name_filter(self.data))
        user.put()
        self.write_json({'result': 'OK'})


    # get user information
    @async_login_required
    @gen.coroutine
    def get(self):
        userid = self.current_userid
        user = self.user_table.get_item(userid)
        # filter output information
        user_data = self.output_firewall(user)
        self.write_json({
            'user': user_data
        })


    """
        Take input dict and validate input dict
    """

    def input_firewall(self,input_dict):

        outside_field_names = [
            'firstname',
            'lastname',
            'gender',
            'college',
            'major',
            'email',
            'birthday',
            'password',
            'phone',
            'signature',
            'driver',
            'license'
        ]

        for key, val in input_dict.items():
            
            if key == 'email' and len(val) > 50:
                self.set_status(400)
                self.write_json({ 
                    'result':'fail',
                    'reason':'Invalid Field:' + key})
            if key not in outside_field_names or (key != "email" and key != "gender" and len(val) > 30):
                self.set_status(400)
                self.write_json({ 
                    'result':'fail',
                    'reason':'Invalid Field:' + key})
            if key == 'phone' and not re.match('\d{3}-\d{3}-\d{4}', val):
                self.set_status(400)
                self.write_json({ 
                    'result':'fail',
                    'reason':'Invalid Field:' + key})
            if key == 'email' and not re.match(r'[a-zA-Z0-9]+@[a-z]+\.edu', val):
                self.set_status(400)
                self.write_json({ 
                    'result':'fail',
                    'reason':'Invalid Field:' + key})





    """
        Take output dict and return filtered dict
    """

    def output_firewall(self,output_dict):
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
            'DriverLicense',
            'CarID',
            'PhotoID'
        ]

        filtered_output = {}
        for key, val in output_dict:
            if key in legal_field_names:
                filtered_output[key] = val

        return filtered_output










