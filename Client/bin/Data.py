# ---------------------------------------------------------------------------
# Database Class
# ---------------------------------------------------------------------------

class Database:
    # init method
    def __init__(self):
        # initializes the database struct
        self.list = []
        self.transactions = []
        self.balance = '0'

    # add transaction method
    def add_transaction(self, json):
        # modify the balance with a transaction json
        self.transactions.append(json)
        if json['STATUS'] == 'OK':
            self.balance = int(json['VALUE'])
    
    # print transaction method
    def print_transactions(self):
        # print stratum of transaction list and the current balance
        self.transactions = sorted(self.transactions, key=lambda k: k['ID']) 
        print('')
        balance = '0'
        for transaction in self.transactions:
            if 'TYPE' in transaction:
                if transaction['OPERATION'] == 'DEBIT':
                    print('ID[' + str(transaction['ID']) + ']                                             -' + str(transaction['VALUE']))
                else: 
                    print('ID[' + str(transaction['ID']) + ']                                              ' + str(transaction['VALUE']))
            else:
                if transaction['STATUS'] == 'NHA':
                    print('')
                    print('**************** OPERATION  CANCELED! ****************')
                    print('')
                    print('                                         BALANCE:  ' + balance)
                    print('')
                else:
                    balance = str(transaction['VALUE'])
                    print('')
                    print('                                         BALANCE:  ' + balance)
                    print('')
        print('                                 CURRENT BALANCE:  ' + str(self.balance))
        print('')

    # add_json method
    def add_json(self, json):
        # add a json to the database
        self.list.append(json)

    # add_request method
    def add_request(self, json):
        self.transactions.append(json)

    # get json method
    def get_json(self):
        # return a json object and remove him from list
        if len(self.list) > 0:
            aux = self.list[0]
            self.list.pop(0)
            return aux
        else:
            return 'NULL'