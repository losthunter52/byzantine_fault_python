import ast
from . import Settings
from .Sender import CoreSender
from threading import Thread

# ---------------------------------------------------------------------------
# Postman Class
# ---------------------------------------------------------------------------

class CorePostman(Thread):
    # init method
    def __init__(self, database, cond, id, operation, value):
        # initializes the communication receiver module
        Thread.__init__(self)
        self.database = database
        self.cond = cond
        self.operation = operation
        self.value = value
        self.id = id
        self.ip = Settings.SELF_IP
        self.port = Settings.SELF_PORT
        self.neighborhood = Settings.NEIGHBORHOOD
        self.return_messages = []

    # check method
    def check(self):
        # check the return messages
        status = 'OK'
        for message in self.return_messages:
            message = ast.literal_eval(message)
            if message['MESSAGE'] == 'NHA':
                status = 'NHA'
            if status == 'OK':
                self.value = message['VALUE']
        json = {
            'ID': self.id,
            'OPERATION': self.operation,
            'VALUE': self.value,
            'STATUS': status
        }
        self.cond.acquire()
        self.database.add_transaction(json)
        self.cond.release()

    # wait responses method
    def wait_responses(self):
        # wait for neighborhood responses
        while(len(self.return_messages) < len(self.neighborhood)):
            self.cond.acquire()
            json = self.database.get_json()
            self.cond.release()
            if json != 'NULL':
                if json['TYPE'] == 'REPLY':
                    if json['ID'] == self.id:
                        self.return_messages.append(str(json))
                    else:
                        self.cond.acquire()
                        self.database.add_json(json)
                        self.cond.release()
                else:
                    self.cond.acquire()
                    self.database.add_json(json)
                    self.cond.release()
        self.check()

    # send all method
    def send_all(self):
        # send requests for the neighborhood
        for neighbor in self.neighborhood:
            destiny_ip = neighbor['IP']
            destiny_port = neighbor['PORT']
            is_primary = 'NO'
            if neighbor['IS_PRIMARY'] == 'YES':
                is_primary = 'YES'
            json = {
                'TYPE':'REQUEST',
                'ID': self.id,
                'IS_PRIMARY': is_primary,
                'OPERATION': self.operation,
                'VALUE': self.value,
                'CLIENT_IP': self.ip,
                'CLIENT_PORT': self.port
            }
            send = CoreSender(json, destiny_ip, destiny_port)
            send.start()
        self.wait_responses()

    # run method
    def run(self):
        # start the CorePostman thread
        print("Postman Running...")
        self.send_all()