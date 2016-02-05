class messageManager(object):
    def __init__(self):
        self.__fifo__={'base':[]}

    def append(self, content, fifo='base'):
        try:
            self.__fifo__[fifo].append(content)
        except KeyError:
            self.__fifo__[fifo]=[content]

    def pop(self, fifo='base'):
        if fifo not in self.__fifo__.keys():
            raise Exception('FIFO "%s" does not exist' % fifo)
        else:
            return self.__fifo__[fifo].pop(0)
        
    def dump(self, fifo='__ALL__'):
        if fifo not in self.__fifo__.keys():
            raise Exception('FIFO "%s" does not exist' % fifo)
        elif fifo == '__ALL__':
            return self.__fifo__
        else:
            return self.__fifo__[fifo]

    def log_warning(self, message):
        print message
