#!/usr/bin/env python
import tornado.web
import json
import time
import traceback
import sys

from store_backends.memory import messageManager

MESSAGES = messageManager()


def capture_exceptions(f):
    '''
    A decorator to capture exceptions and send information in a json.
    '''
    def wrapper(self, *args):
        try:
            f(self, *args)
        except Exception as e:
            response=json.dumps({
                    'Exception': str(e),
                    'traceback': traceback.format_exc(sys.exc_info()).splitlines()
                    }, indent=4)
            self.write(response)
            self.set_header("Content-Type", "application/json")
    return wrapper


class MainHandler(tornado.web.RequestHandler):

     @capture_exceptions
     def get(self):
          response = '''<html>
<body>
Wellcome to FifoChat!
<pre>
<code>
%s
</code>
</pre>
</body>
</html>''' % json.dumps(MESSAGES.get(), indent=4)
          self.write(response)
          self.set_header("Content-Type", "text/html")


class FifoHandler(tornado.web.RequestHandler):

     @capture_exceptions
     def get(self):
         if len(MESSAGES.get()) > 0:
             response = json.dumps(MESSAGES.pop(), indent=4)
         else:
             response = json.dumps(None, indent=4)
         self.write(response)
         self.set_header("Content-Type", "application/json")

     @capture_exceptions
     def post(self):
         message = {'timestamp':time.time(), 'data': json.loads(self.request.body)}
         MESSAGES.append(message)
         response = json.dumps(message, indent=4)
         self.write(response)
         self.set_header("Content-Type", "application/json")
               



# Put here yours handlers.

handlers = [(r'/', MainHandler),
            (r'/fifo', FifoHandler),]
