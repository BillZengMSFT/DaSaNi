#encoding: utf-8

import tornado
import json
from tornado import gen
from .base_handler import BaseHandler
from .config import *
from .helper import *


class ActivateHandler(BaseHandler):
    @property
    def table(self):
        return self.dynamo.get_table(USER_TABLE)

    @property
    def activate_table(self):
        return self.dynamo.get_table(ACTIVATE_TABLE)

    @gen.coroutine
    def post(self):
        """
            Get activate code from clients and activate their accounts if a valid code is presented

            PAYLOAD:
            {
                userid: USERID
                code : ACTIVATECODE ## EX: "5DE3C"
            }
        """
        code = self.data["code"]
        userid = self.data["userid"]
        code_is_real =  self.activate_table.has_item(userid)
        if code_is_real:
            activator = yield gen.maybe_future(self.activate_table.get_item(userid))
            if activator["Code"] == code:
                user_data = self.table.get_item(userid)
                user_data["AccountActive"] = True
                yield gen.maybe_future(user_data.put())
                yield gen.maybe_future(activator.delete())
                self.write_json({
                    "result":"success"
                    })
            else:
                self.send_error(403)
                return


    @gen.coroutine
    def put(self):
        """
            Request to send a new activate email

            PAYLOAD:
            {
                userid: USERID
            }
        """
        userid = self.data["userid"]
        user_data = yield gen.maybe_future(self.table.get_item(userid))
        activator = self.activate_table.get_item(userid)
        
        activator["Attempt"] = activator["Attempt"] + 1
        if activator["Attempt"] > 3:
            self.write_json({
                'result':"fail: Too many attempts recorded"
            })
            return
        try:
            activate_code = send_email(
                self.ses,
                user_data["Email"],
                user_data["Firstname"],
                user_data["Lastname"])
        except:
            self.write_json({
                'result':"fail: Email not sent"
            })
            return
        # update dynamo

        activator["Code"] = activate_code

        yield gen.maybe_future(activator.put())

        self.write_json({
            'result':"ok"
        })


    @gen.coroutine
    def get(self, userid):
        """
            Retrieve if an account is activated or not
        """
        user_data = yield gen.maybe_future(self.table.get_item(userid))
        if user_data["AccountActive"] == True:
            self.write_json({
                'result':"ok"
            })
        else:
            self.set_status(403)
            self.write_json({
                'result':"fail"
            })


