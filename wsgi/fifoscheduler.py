import threading
import time

class Scheduler(object):
    def __init__(self, MESSAGES):
        self.MESSAGES=MESSAGES
        self.t = threading.Thread(name='daemon', target=self.run)
        self.t.setDaemon(True)
        self.t.start()

    def log(self, text):
        self.MESSAGES.append(text, 'log')

    def run(self):
        while True:
            self.log('Still alive at %s' % time.time())
            time.sleep(5)
            
