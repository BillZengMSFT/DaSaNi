#encoding: utf-8

import hashlib
import time
import re
from .config import ACTIVATOR_EMAILADDRESS
from werkzeug.security import generate_password_hash


def send_email(ses, email, fn, ln):
    code = md5(email+str(time.time()).split(".")[0])
    
    ses.send_email(
        ACTIVATOR_EMAILADDRESS,
        "Activation Email From Carlor",
        "<p>Here is your activate code for Carlor: <strong> "+code[-5:]+"</strong><br><p>Please use it as soon as possible! Thank you!</p><br><br>Carlor",
        [email],
        format = "html"
        )
    return code[-5:]

def md5(s):
    m = hashlib.md5()
    m.update(s.encode("utf-8"))
    return m.hexdigest()

def hash_password(pwd):
    return generate_password_hash(pwd).split(":")[0]

# regex
def list_delete_item(to_remove_reg, list_string):
    # filter out |
    to_remove_reg = to_remove_reg.replace('|','\|')
    # handle empty string
    if list_string == '' or list_string == ';':
        return ';'
    # handle not found 
    print(to_remove_reg,list_string)
    match = re.search(to_remove_reg, list_string)
    if match == None:
        return list_string
    front, rear = list_string.split(match.group())
    if front + rear == '':
        return ';'
    return front + rear

# raw string
def list_append_item(to_append_string, list_string):
    # handle empty string
    if list_string == '' or list_string == ';':
        list_string = ''
    match = re.search(to_append_string, list_string)
    if match != None:
        return list_string
    # automatically append ";"
    list_string += to_append_string + ';'
    return list_string


def option_value(_dict, key):
    if key in _dict:
        return _dict[key]
    return ';'

def client_name_filter(attrs):
    # convert client data names to database names
    name_map = {
        'userid'        : 'UserID',
        'code'          : 'Code',
        'email'         : 'Email',
        'name'          : 'Name',
        'memberlist'    : 'MemberList',
        'capacity'      : 'Capacity',
        'photo'         : 'PhotoID',
        'car_id'        : 'CarID',
        'firstname'     : 'FirstName',
        'lastname'      : 'LastName',
        "gender"        : "Gender",
        "college"       : "College",
        "major"         : "Major",
        "birthday"      : "Birthday",
        "password"      : "Password",
        "phone"         : "Phone",
        "signature"     : "Signature",
        "driver"        : "Driver",
        "license"       : "DriverLicense",
        'start_time'    : 'StartTime',
        'end_time'      : 'EndTime',
        'apn'           : 'APNs',
        'sqs'           : 'SQS',
        'ses'           : 'SES',
        'deviceToken'   : 'APNsToken',
        'event_id'      : 'EventID',
        'chatgroup_id'  : 'ChatgroupID',
        'creator_id'    : 'CreatorID',
        'content'       : 'Content',
        'comment_id'    : 'CommentID',
        'payload'       : 'JsonMessage',
    }
    try:
        new_attrs = {}
        for key, value in attrs.items():
            if key in name_map:
                new_attrs[name_map[key]] = value
            else:
                print("Wrong key in the input attrs. Key: "+key+" Value: "+value)
                continue
        return new_attrs
    except:
        print('attrs is not a dict!')


