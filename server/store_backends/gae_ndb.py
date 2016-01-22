from google.appengine.ext import ndb

class Message(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    data = ndb.StringProperty(indexed=False)

class MESSAGES(object):
    def __init__(self):
        self.name = 'FIFO_0'
        self.key = ndb.Key('FIFO', 'FIFO_0')
        self.query = Message.query(ancestor=self.key).order(Message.date)

    def append(self, content):
        m = Message(parent=self.key)
        m.data=json.dumps(content)
        m.put()
    
    def pop(self):
        m=self.query.fetch(1)
        print m[0].key.delete()
        
        return map(lambda x: {'timestamp': str(x.date), 'data': json.loads(x.data)}, 
            m)
        
        
    def get(self):
        return map(lambda x: {'timestamp': str(x.date), 'data': json.loads(x.data)}, 
                   self.query.fetch())
