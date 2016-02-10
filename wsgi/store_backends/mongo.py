import os
import pymongo



class messageManager(object):
    def __init__(self):
        self.__client = pymongo.MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL']) 
        self.__db = self.__client.fifo
        try:
            self.__db.drop_collection('log')
        except:
            pass
        self.__db.create_collection('log', capped=True, size=500000, max=5000)
    def append(self, content, fifo='base'):
        self.__db[fifo].insert_one({ 'fifo': fifo, 'payload': content})
        
    def pop(self, fifo='base'):
        return self.__db[fifo].find_one_and_delete(
            {'fifo': fifo},
            sort=[('_id', pymongo.ASCENDING)]
            )['payload']
        
    def dump(self, fifo='__ALL__'):
        if fifo is not '__ALL__':
            return map(lambda x: x['payload'], self.__db[fifo].find({}))
        else:
            return map(
                lambda x: {
                    x: map(
                        lambda y: y.get('payload',y), 
                        self.__db[x].find().sort('_id',-1).limit(5)
                        )
                    },
                self.__db.collection_names()[1:]
                )
