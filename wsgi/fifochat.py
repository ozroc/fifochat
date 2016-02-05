#!/usr/bin/env python
import tornado.web
import tornado.options
from tornado.ioloop import IOLoop
from tornado import gen
import json
import time
import traceback
import sys

try:
    from store_backends.mongo import messageManager
    MESSAGES = messageManager()
except:
    print('Unable to load mongoDB backend storage, defaulting to in-memory')
    from store_backends.memory import messageManager
    MESSAGES = messageManager()


import dashboards.bokeh_simple as dashboard
import dashboards.default as base_dashboard

def capture_exceptions(f):
    '''
    A decorator to capture exceptions and send information in a json.
    '''
    def wrapper(*args):
        try:
            f(*args)
        except Exception as e:
            response=json.dumps({
                    'Exception': str(e),
                    'traceback': traceback.format_exc(sys.exc_info()).splitlines()
                    }, indent=4)
            args[0].write(response)
            args[0].set_header("Content-Type", "application/json")
    return wrapper


class MainHandler(tornado.web.RequestHandler):
    @capture_exceptions
    def get(self):
        self.write(base_dashboard.generate_dashboard(MESSAGES.dump()))
        self.set_header("Content-Type", "text/html")


class FifoHandler(tornado.web.RequestHandler):

    @capture_exceptions
    @gen.coroutine
    def get(self, *args):
        uri=[ y for y in self.request.uri.split('/') if y != '']
        if uri[-1].upper() == 'POP':
            response = json.dumps(MESSAGES.pop(uri[1]), indent=4)
            self.write(response)
            self.set_header("Content-Type", "application/json")
        else:
            response = dashboard.generate_dashboard(MESSAGES.dump(uri[1]))
            self.write(response)
            self.set_header("Content-Type", "text/html")

    @capture_exceptions
    @gen.coroutine
    def post(self, *args):
        uri=[ y for y in self.request.uri.split('/') if y != '']
        message = {'timestamp':time.time(), 'data': json.loads(self.request.body)}
        response = json.dumps(message, indent=4)
        MESSAGES.append(message, uri[1])
        self.write(response)
        self.set_header("Content-Type", "application/json")




# Put here yours handlers.

handlers = [(r'/', MainHandler),
            (r'/fifo/(.*)', FifoHandler),]
