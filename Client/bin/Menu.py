import os, threading, random
from .Postman import CorePostman
from . import Settings

#---------------------------------------------------------------------------
# Control Painel Class
#---------------------------------------------------------------------------

class ControlPainel(threading.Thread):
    # init method
    def __init__(self, database, cond):
        # initializes the control painel module
        threading.Thread.__init__(self)
        self.database = database
        self.cond = cond
        self.id = 0
        self.stress_lvl = Settings.STRESS_LVL

    # menu method
    def menu(self):
        # control the program
        running = True
        while running == True:
            os.system('cls')
            print("------------------------------------------------------")
            print('         - Bizzantine Fault Tolerance Client -        ')
            print("------------------------------------------------------")
            print('1 - Credit Value')
            print('2 - Debit Value')
            print('3 - Show Extract')
            print('0 - Exit')
            print("------------------------------------------------------")
            option = input('Type a option: ')

            if option == '1':
                self.credit()

            if option == '2':
                self.debit()

            if option == '3':
                self.print()

            if option == '666':
                self.stress_test()

            if option == '0':
                os.system('cls')
                running = False
                print("Bye Bye - By losthunter52")

    # credit method
    def credit(self):
        # send a credit request
        os.system('cls')
        operation = 'CREDIT'
        value = input('Type a value to credit: ')
        os.system('cls')
        print('loading..')
        try:
            value = int(value)
            self.id += 1
            json = {
                'TYPE':'REQUEST',
                'ID': self.id,
                'OPERATION': operation,
                'VALUE': value,
            }
            self.database.add_request(json)
            postman = CorePostman(self.database, self.cond, self.id, operation, value)
            postman.start()
        except:
            pass

    # debit method
    def debit(self):
        # send a debit request
        os.system('cls')
        operation = 'DEBIT'
        value = input('Type a value to debit: ')
        os.system('cls')
        print('loading..')
        try:
            value = int(value)
            self.id += 1
            json = {
                'TYPE':'REQUEST',
                'ID': self.id,
                'OPERATION': operation,
                'VALUE': value,
            }
            self.database.add_request(json)
            postman = CorePostman(self.database, self.cond, self.id, operation, value)
            postman.start()
        except:
            pass

     # stress test method (SECRET)
    def stress_test(self):
        # send X random requests of transactions
        os.system('cls')
        print('loading..')
        operation = 'NULL'
        for x in range (self.stress_lvl):
            op = random.randint(0, 1)
            if op == 1:
                operation = 'DEBIT'
            else:
                operation = 'CREDIT'
            value = random.randint(1,50)
            value = int(value)
            self.id += 1
            json = {
                    'TYPE':'REQUEST',
                    'ID': self.id,
                    'OPERATION': operation,
                    'VALUE': value,
            }
            self.database.add_request(json)
            postman = CorePostman(self.database, self.cond, self.id, operation, value)
            postman.start()

    # print method
    def print(self):
        # print the stratum of transactions
        os.system('cls')
        print("------------------------------------------------------")
        print("                       STRATUM:                       ")
        print("------------------------------------------------------")
        self.cond.acquire()
        self.database.print_transactions()
        self.cond.release()
        print("------------------------------------------------------")
        input("              Press ENTER to continue...              ")

    # run method
    def run(self):
        # start the menu thread
        self.menu()