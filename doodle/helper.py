#encoding: utf-8

import hashlib
import time
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