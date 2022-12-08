# ---------------------------------------------------------------------------
# Database Class
# ---------------------------------------------------------------------------

class Database:
    # init method
    def __init__(self):
        # initializes the database struct
        self.list = []
        self.current_balance = 0
        self.id = 1

    # add json method
    def add_json(self, json):
        # add a json to the database
        self.list.append(json)

    # add transaction method
    def add_transaction(self, json):
        # modify the balance with a transaction json
        if json['OPERATION'] == 'CREDIT':
            self.current_balance = self.current_balance + int(json['VALUE'])
        if json['OPERATION'] == 'DEBIT':
            self.current_balance = self.current_balance - int(json['VALUE'])

    # balance method
    def balance(self):
        # return the current balance
        return self.current_balance

    # set balance method
    def set_balance(self, value):
        # modify the current balance
        self.current_balance = int(value)

    # add id method
    def add_id(self):
        # add 1 to current id
        self.id += 1

    # verify id method
    def verify_id(self, id):
        # verify the current id (logic clock)
        if id <= self.id:
            return True
        else:
            return False

    # get method
    def get_json(self):
        # return a json object and remove him from queue
        if len(self.list) > 0:
            aux = self.list[0]
            self.list.pop(0)
            return aux
        else:
            return 'NULL'