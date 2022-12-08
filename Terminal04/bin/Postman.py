from . import Settings
from .Sender import CoreSender
from threading import Thread
import time
import random

# ---------------------------------------------------------------------------
# Postman Class
# ---------------------------------------------------------------------------

class CorePostman(Thread):
    # init method
    def __init__(self, database, cond, json):
        # initializes the communication receiver module
        Thread.__init__(self)
        self.database = database
        self.cond = cond
        self.id = json['ID']
        self.is_bizzantine = Settings.IS_BIZZANTINE
        self.operation = json['OPERATION']
        self.value = json['VALUE']
        self.is_primary = json['IS_PRIMARY']
        self.return_messages = []
        self.commit_messages = []
        self.neighborhood = Settings.NEIGHBORHOOD
        self.client_ip = json['CLIENT_IP']
        self.client_port = json['CLIENT_PORT']
        self.message = 'OK'
        self.running = True
        self.old_value = 0

    # reply method
    def reply(self):
        # reply to client the transaction response
        while(len(self.commit_messages) != len(self.neighborhood)):
            self.cond.acquire()
            json = self.database.get_json()
            self.cond.release()
            if json != 'NULL':
                if json['TYPE'] == 'COMMIT' and json['ID'] == self.id:
                    self.commit_messages.append(json)
                else:
                    self.cond.acquire()
                    self.database.add_json(json)
                    self.cond.release()
        for message in self.commit_messages:
            if message['MESSAGE'] == 'NHA':
                self.message = 'NHA'
        if self.message == 'NHA':
            self.database.set_balance(self.old_value)
        json = {
            'TYPE': 'REPLY',
            'ID' : self.id,
            'OPERATION': self.operation,
            'VALUE': self.database.balance(),
            'MESSAGE': self.message,
        }
        destiny_ip = self.client_ip
        destiny_port = self.client_port
        send = CoreSender(json, destiny_ip, destiny_port)
        send.start()
        self.cond.acquire()
        self.database.add_id()
        self.cond.release()
        self.running = False
    
    # commit method
    def commit(self):
        # commit in terminals the transaction status
        while(len(self.return_messages) != len(self.neighborhood)):
            self.cond.acquire()
            json = self.database.get_json()
            self.cond.release()
            if json != 'NULL':
                if json['TYPE'] == 'PREPARE' and json['ID'] == self.id:
                    self.return_messages.append(json)
                else:
                    self.cond.acquire()
                    self.database.add_json(json)
                    self.cond.release()
        for message in self.return_messages:
            if message['OPERATION'] != self.operation or message['VALUE'] != self.value:
                self.message = 'NHA'
        json = {
            'TYPE':'COMMIT',
            'ID': self.id,
            'MESSAGE': self.message
        }
        for neighbor in self.neighborhood:
            destiny_ip = neighbor['IP']
            destiny_host = neighbor['PORT']
            sender = CoreSender(json, destiny_ip, destiny_host)
            sender.start()
        self.reply()

    # prepare method
    def prepare(self, json):
        # prepare terminals to a transaction conversation
        json = {
            'TYPE': 'PREPARE',
            'ID': self.id,
            'OPERATION': self.operation,
            'VALUE': self.value,
        }
        for neighbor in self.neighborhood:
            destiny_ip = neighbor['IP']
            destiny_host = neighbor['PORT']
            sender = CoreSender(json, destiny_ip, destiny_host)
            sender.start()
        self.commit()

    # postman method
    def postman(self):
        # pre prepare the terminal to a transaction conversation
        self.cond.acquire()
        json = self.database.get_json()
        self.cond.release()
        if json != 'NULL':
            if json['TYPE'] == 'PRE-PREPARE' and json['ID'] == self.id:
                self.old_value = self.database.balance()
                self.database.add_transaction(json)
                self.value = self.database.balance()
                self.prepare(json)
            else:
                self.cond.acquire()
                self.database.add_json(json)
                self.cond.release()
            

    # run method
    def run(self):
        # start the CorePostman thread
        print("Transaction[" + str(self.id) + "] Running...")
        if self.is_bizzantine:
            fault = random.randint(0,1)
            if fault == 0:
                print('---------------------------------------------')
                print('')
                print('-------- !!!  BIZZANTINE  FAULT  !!! --------')
                print('')
                print('---------------------------------------------')
                if self.operation == 'CREDIT':
                    self.operation = 'DEBIT'
                elif self.operation == 'DEBIT':
                    self.operation = 'CREDIT'
        while(self.running):
            self.postman()
        print("Transaction[" + str(self.id) + "] Ending...")