from bin.Data import Database
from bin.Dispatcher import CoreDispatcher
from bin.Receptor import Receptor
import threading

# ---------------------------------------------------------------------------
# Main Class
# ---------------------------------------------------------------------------

# main method
def Main():
    # responsible for starting and ending the node
    data = Database()
    threads = []
    cond = threading.Condition()

    # init threads
    receptor = Receptor(data, cond)
    threads.append(receptor)
    receptor.start()
    dispatcher = CoreDispatcher(data, cond)
    threads.append(dispatcher)
    dispatcher.start()

    # join threads
    for thread in threads:
        thread.join()


# program launcher
if __name__ == '__main__':
    Main()