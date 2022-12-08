import socket, threading

#---------------------------------------------------------------------------
# Core Sender Class
#---------------------------------------------------------------------------

class CoreSender(threading.Thread):
    # init method
    def __init__(self, object, DESTINY_HOST, DESTINY_PORT):
        # initializes the communication sender module
        threading.Thread.__init__(self)
        self.object = str(object)
        self.DESTINY_HOST = DESTINY_HOST
        self.DESTINY_PORT = DESTINY_PORT

    # send method
    def send(self):
        # sends stored information to a pre-defined destination
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.DESTINY_HOST, self.DESTINY_PORT))
            sock.sendall(bytes(self.object,encoding="utf-8"))
        finally:
            sock.close()
        
    # run method
    def run(self):
        # start the ActiveSender thread
        self.send()