import threading
from . import Settings
from .Sender import CoreSender
from .Postman import CorePostman

#---------------------------------------------------------------------------
# Core Dispatcher Class
#---------------------------------------------------------------------------

class CoreDispatcher(threading.Thread):
    # init method
    def __init__(self, database, cond):
        # initializes the communication sender module
        threading.Thread.__init__(self)
        self.database = database
        self.cond = cond
        self.neighborhood = Settings.NEIGHBORHOOD

    # caller method
    def caller(self, json):
        # send json to neighbors
        for neighbor in self.neighborhood:
            destiny_host = neighbor['IP']
            destiny_port = neighbor['PORT']
            send = CoreSender(json, destiny_host, destiny_port)
            send.start()

    # dispatcher method
    def dispatcher(self):
        # call the postmans in logic sequence
        self.cond.acquire()
        json = self.database.get_json()
        self.cond.release()
        if json != 'NULL':
            if json['TYPE'] == 'REQUEST':
                if self.database.verify_id(json['ID']):
                    postman = CorePostman(self.database, self.cond, json)
                    postman.start()
                    if json['IS_PRIMARY'] == 'YES':
                        json = {
                            'TYPE':'PRE-PREPARE',
                            'ID': json['ID'],
                            'OPERATION': json['OPERATION'],
                            'VALUE': json['VALUE'],
                        }
                        self.caller(json)
                else:
                    self.cond.acquire()
                    self.database.add_json(json)
                    self.cond.release()
            else:
                self.cond.acquire()
                self.database.add_json(json)
                self.cond.release()

    # run method
    def run(self):
        # start the ActiveSender thread
        print('Dispatcher is running...') 
        while(True):
            self.dispatcher()