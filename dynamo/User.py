

from tornado import gen
from config import *

import hashlib
import time

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
def verify_pwd(username, pwd, dynamo):
    users = dynamo.get_table('users')
    user = users.get_item(
        username=username,
        password=pwd)
    if user:
        return user['uid']
    else:
        return None

@gen.coroutine
def verify_token(token, userid, memcache):
    if userid in memcache and memcache[userid] == token:
        return userid
    return None


def create_token(hashed_userid, memcache):
    m = hashlib.md5()
    m.update(hashed_userid + COOKIE_SECRET + str(time.time()).split(".")[0])
    token = m.hexdigest()
    
    return token
    
