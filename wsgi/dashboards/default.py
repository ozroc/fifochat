import json

def generate_dashboard(data):
    response = '''<html>
<body>
Wellcome to FifoChat!
<pre>
<code>
%s
</code>
</pre>
</body>
</html>''' % json.dumps(data, indent=4)
    return response
