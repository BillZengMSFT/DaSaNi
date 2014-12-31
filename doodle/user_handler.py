#encoding: utf-8

import tornado
import json
import werkzeug
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
    def activate_table(self):
        return self.dynamo.get_table(USER_ACTIVATE_TABLE)

    @property
    def topic_table(self):
        return self.dynamo.get_table(USER_TOPIC_TABLE)

    @property
    def friend_table(self):
        return self.dynamo.get_table(USER_FRIEND_TABLE)

    @property
    def user_event_table(self):
        return self.dynamo.get_table(USER_EVENT_TABLE)

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
            self.write_json({
                'status': 0,
                'error': 'Email already in use'
            })
            return


        hashed_password = hash_password(password)
        
        # Build attrs for the new user

        attrs = {
            "Password"      : hashed_password,
            "Email"         : self.data["email"],
            "Major"         : self.data["major"],
            "School"        : self.data["college"],
            "FirstName"     : self.data['firstname'],
            "LastName"      : self.data['lastname'],
            "Gender"        : self.data['gender'],
            "AccountActive" : False,
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
            self.set_status(400)
            return

        activator_attrs = {
            "Time"      : str(time.time()).split(".")[0],
            "Code"      : activate_code,
            "Attempt"   : 1
        }
        
        new_user_activator = self.activate_table.new_item(
            hash_key=hashed_userid,
            range_key=None,
            attrs=activator_attrs
            )

        new_user_topic_list= self.topic_table.new_item(
            hash_key=hashed_userid,
            range_key=None,
            attrs={"TopicList" : ";"}
            )

        new_user_friend_list= self.friend_table.new_item(
            hash_key=hashed_userid,
            range_key=None,
            attrs={"FriendList" : ";"}
            )

        new_user_event_list = self.user_event_table.new_item(
            hash_key=hashed_userid,
            range_key=None,
            attrs={"EventList" : ";"}
            )

        # Upload new user information and activator to AWS
        yield gen.maybe_future(new_user.put())
        yield gen.maybe_future(new_user_activator.put())
        yield gen.maybe_future(new_user_topic_list.put())
        yield gen.maybe_future(new_user_friend_list.put())
        yield gen.maybe_future(new_user_event_list.put())
        # Only send userid back to the client

        self.write_json({
            'userid': hashed_userid,
        })


    # update a user information
    @async_login_required
    @gen.coroutine
    def put(self):
        self.input_firewall(self.data)
        user_data = self.user_table.get_item(self.current_userid)
        # TODO
        # Check if there is any invalid field in the data

        user_data.update(self.data)
        current_user.data.put()
        self.write_json({'result': 'OK'})


    # get user information
    @async_login_required
    @gen.coroutine
    def get(self):
        userid = self.current_userid
        user_data = self.user_table.get_item(userid)
        # filter output information
        user_data = self.output_firewall(user_data)
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
            
            if key == "email" and len(val)>50:
                self.set_status(400)
                self.write_json({ "result":"fail : Invalid Field: "+key})
            if key not in outside_field_names or (key != "email" and key != "gender" and len(val)> 20):
                self.set_status(400)
                self.write_json({ "result":"fail : Invalid Field: "+key})
            if key == 'phone' and not re.match('\d{3}-\d{3}-\d{4}', val):
                self.set_status(400)
                self.write_json({ "result":"fail : Invalid Field: "+key})
            if key == 'email' and not re.match(r'[a-zA-Z0-9]+@[a-z]+\.edu', val):
                self.set_status(400)
                self.write_json({ "result":"fail : Invalid Field: "+key})





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










