import os
import pymongo

class messageManager(object):
    def __init__(self):
        self.__client = pymongo.MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL']) 
        self.__db = self.__client.fifo

    def append(self, content):
        self.__db.fifo.insert_one({ 'fifo': 'base', 'payload': content})
        
    def pop(self):
        return self.__db.fifo.find_one_and_delete(
            {'fifo': 'base'},
            sort=[('_id', pymongo.ASCENDING)]
            )['payload']
        
    def get(self):
        return map(lambda x: x['payload'], self.__db.fifo.find({'fifo':'base'}))
