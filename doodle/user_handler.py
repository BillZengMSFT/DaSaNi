#encoding: utf-8

import tornado
import json
import werkzeug
from tornado import gen
from dynamo import User
from .base_handler import BaseHandler
import time
import re
from config import *
from werkzeug.security import generate_password_hash
import hashlib
from .helper import send_email

class UserHandler(BaseHandler):

    @property
    def table(self):
        return self.dynamo.get_table(User_Table)

    @property
    def activate_table(self):
        return self.dynamo.get_table(Activate_Table)

    @gen.coroutine
    def post(self):

        self.input_firewall(self.data)

        # Get email from client and hash it

        password = self.data['password']
        email = self.data['email'].strip()

        m = hashlib.md5()
        m.update(email.encode("utf-8"))
        hashed_userid = m.hexdigest()

        # Check if this email has been registered

        user_exist = self.user_table.has_item(hashed_userid)

        if user_exist is True:

            # tell client and stop processing this request
            self.write_json({
                'status': 0,
                'error': 'Email already in use'
            })
            return


        hashed_password = generate_password_hash(password)
        
        # Build attrs for the new user

        attrs = {
            "UserID"    : hashed_userid,
            "Password"  : hashed_password,
            "Email"     : self.data["email"],
            "Major"     : self.data["major"],
            "School"    : self.data["college"],
            "firstname" : self.data['firstname'],
            "lastname"  : self.data['lastname'],
            "gender"    : self.data['gender']
        }
        
        # Create new user item and upload it to database

        new_user = self.table.new_item(
            hash_key=hashed_userid,
            range_key=None,
            attrs=attrs)

        # Send activate email
        try:
            activate_code = send_email(self.ses,self.data["email"],self.data["first_name"],self.data["last_name"])
        except:
            self.send_error(400)
            return

        activator_attrs = {
            "UserID"    : hashed_userid,
            "Time"      : time.time(),
            "Code"      : activate_code,
            "Attempt"   : 1
        }

        new_user_activator = self.activate_table.new_item(
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
        user_data = self.table.get_item(self.current_user)
        # TODO
        # Check if there is any invalid field in the data

        user_data.update(self.data)
        current_user.data.put()
        self.write_json({'result': 'OK'})


    # get user information
    @async_login_required
    @gen.coroutine
    def get(self):
        userid = self.current_user
        user_data = self.table.get_item(userid)
        # filter output information
        user_data = self.output_firewall(user_data)
        self.write_json({
            'user': user_data
        })


    """
        Take input dict and validate input dict
    """

    def input_firewall(input_dict):
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
            if key not in outside_field_names or len(val) > 20:
                raise tornado.web.HTTPError(400, "Invalid Field: "+key)
            if key == 'phone' and not re.match('/d{3}-/d{3}-/d{4}', val):
                raise tornado.web.HTTPError(400, "Invalid Field: "+key)
            if key == 'email' and not re.match('/s+@/s+.edu', val)
                raise tornado.web.HTTPError(400, "Invalid Field: "+key)

    """
        Take output dict and return filtered dict
    """

    def output_firewall(output_dict):
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










