import tornado
import json
from tornado import gen
from .base_handler import BaseHandler
from config import *



class ActivateHandler(BaseHandler):
    @property
    def table(self):
        return self.dynamo.get_table(User_Table)

    @property
    def activate_table(self):
        return self.dynamo.get_table(Activate_Table)

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
            if activator["code"] == code:
                user_data = self.table.get_item(userid)
                user_data["AccountActive"] = True
                yield gen.maybe_future(user_data.put())
            else:
                self.set_error(403)
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
        try:
            activate_code = send_email(
                self.ses,user_data["Email"],
                user_data["FirstName"],
                user_data["LastName"])
        except:
            self.write_json({
                'result':"ok"
            })
            self.send_error(400)
            return
        # update dynamo

        activator = self.activate_table.get_item(userid)
        activator["code"] = activate_code
        yield gen.maybe_future(activator.put())

        self.write_json({
            'result':"ok"
        })


    @gen.coroutine
    def get(self):
        """
            Retrieve if an account is activated or not

            PAYLOAD:
            {
                userid: USERID
            }
        """
        userid = self.data["userid"]
        user_data = yield gen.maybe_future(self.table.get_item(userid))
        if user_data["AccountActive"] is True:
            self.write_json({
                'result':"ok"
            })
        else:
            self.set_status(403)
            self.write_json({
                'result':"fail"
            })


