#encoding: utf-8

from tornado import gen
from doodle import config

import hashlib
import time
from doodle import config
from doodle import helper
# User Model

"""

    UserID         = str        Indexed
    FirstName      = str
    LastName       = str
    Birthday       = str    =>  unix timestamp
    Email          = str        Indexed
    Password       = str
    Phone          = str        foramt:1aaabbbcccc!important
    School         = str        Indexed
    Major          = str        Indexed
    Gender         = Number   male => true  Indexed
    Signature      = str
    Driver         = bool       Indexed
    EmailActive    = bool
    PhoneActive    = bool
    AccountActive  = bool
    DriverLicense  = str
    CarID          = str        None
    PhotoID        = str        None

"""


@gen.coroutine
def verify_pwd(email, pwd, dynamo):
    user_table = Table('User_Table',connection=dynamo)
    user_data_exist = user_table.has_item(Email=helper.md5(email))
    if user_data_exist:
        user_data = user_table.get_item(Email=helper.md5(email))
    else:
        return None
    if user_data["Password"] == helper.hash_password(pwd):
        return user_data['UserID']
    else:
        return None

@gen.coroutine
def verify_token(token, userid, memcache):
    try:
        if userid in memcache and memcache[userid] == token:
            return userid
        return None
    except:
        return None


def create_token(hashed_userid, memcache):
    token = helper.md5(hashed_userid + config.COOKIE_SECRET + str(time.time()).split(".")[0])
    memcache[hashed_userid] = token
    return token
    



