# encoding: utf-8
#   
# web server main app

import tornado.ioloop
import tornado.web
import tornado.options

import functools
import logging
import signal
import time
import boto.sqs
import boto.sns

from tornado.httpserver import HTTPServer


""" Tornado App Configuration

"""

def aws_account():
    aws_access_id = 'AKIAJNDFKACQ6253GVXQ'
    aws_access_key = 'uOvbYfrPeE3hkNIHy9PZrPVNq445nmdPQkl6f33h'

    return aws_access_id, aws_access_key


def get_url_list():

    return [
        
    ]


def get_settings():

    return {
        'cookie_secret': '_&xC#!~-2987UYWq|{RClubCIL}o><?[]axWERFC@',
        'login_url': '/api_v1/login',
        'debug': True
    }


def get_sqs():
    
    aws_access_id, aws_access_key = aws_account()

    conn = boto.sqs.connect_to_region(
        'us-west-2',
        aws_access_key_id=aws_access_id,
        aws_secret_access_key=aws_access_key)
    return conn

def get_sns():

    aws_access_id, aws_access_key = aws_account()

    conn = boto.sns.connect_to_region(
        'us-west-2',
        aws_access_key_id=aws_access_id,
        aws_secret_access_key=aws_access_key)
    return conn

def get_app():

    url_list = get_url_list()
    settings = get_settings()
    sqs = get_sqs()
    sns = get_sns()

    application = tornado.web.Application (
        url_list,
        sqs = sqs,
        sns = sns,
        **settings
    )
    
    return application

def get_ioloop():

    ioloop = tornado.ioloop.IOLoop.instance()
    return ioloop


def stop_server(server):

    logging.info('--- stopping club server ---')
    server.stop()


""" SSL not implemented yet

"""

def get_ssl():

    data_dir = '../'

    return {
                "certfile": os.path.join(data_dir, "server.crt"),
                "keyfile": os.path.join(data_dir, "server.key")
           }


""" Tornado server run loop
    
"""

def main():

    application = get_app()
    tornado.options.parse_command_line()
    server = HTTPServer(application)#, ssl_options=get_ssl())
    server.listen(80)
    ioloop = get_ioloop()
    try:
        ioloop.start()
    except KeyboardInterrupt:
        stop_server(server)

    logging.info('--- club server stopped ---')


if __name__=='__main__':
    main()


