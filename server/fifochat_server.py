"""`main` is the top level module for your Flask application."""

from flask import Flask
from flask import request
import time, json
app = Flask(__name__)

from store_backends.memory import messageManager

MESSAGES = messageManager()

@app.route('/')
def hello():
    return '''<html>
<body>
<pre>
<code>
%s
</code>
</pre>
</body>
</html>''' % json.dumps(map( lambda x: json.loads(x), MESSAGES.get()), indent=4)

@app.route('/MESSAGES')
def messages():
    return json.dumps(MESSAGES.get(), indent=4)

@app.route('/fifo', methods=['GET', 'POST'])
def fifo():
    if request.method == 'POST':
        try:
            message = {'timestamp':time.time(), 'data': json.loads(request.data)}
            MESSAGES.append(message)
            return json.dumps(message)
        except Exception, e:
            return json.dumps(str(e))
    else:
        if len(MESSAGES.get()) > 0:
            return json.dumps(MESSAGES.pop())
        else:
            return json.dumps(None)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404

@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
