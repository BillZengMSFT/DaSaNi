#encoding: utf-8

from tornado import gen
from doodle import config

import hashlib
import time
from doodle import config

# User Model

"""

    UserID         = str        Indexed
    FirstName      = str
    LastName       = str
    Birthday       = str    =>  unix timestamp
    Email          = str        Indexed
    Password       = str
    Phone          = str
    School         = str        Indexed
    Major          = str        Indexed
    Gender         = Binary   male => true  Indexed
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
    user_table = dynamo.get_table(USER_TABLE)
    user_data = user_table.get_item(md5(email))
    if user_data["Password"] == pwd:
        return user_data['UserID']
    else:
        return None

@gen.coroutine
def verify_token(token, userid, memcache):
    if userid in memcache and memcache[userid] == token:
        return userid
    return None


def create_token(hashed_userid, memcache):
    token = md5(hashed_userid + COOKIE_SECRET + str(time.time()).split(".")[0])
    memcache[hashed_userid] = token
    return token
    



