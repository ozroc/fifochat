class messageManager(object):
    def __init__(self):
        self.__fifo__=[]

    def append(self, content):
        self.__fifo__.append(content)
    
    def pop(self):
        return self.__fifo__.pop(0)
        
    def get(self):
        return self.__fifo__
