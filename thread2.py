import threading
import time
from subfile import pickle_file

INTERVAL = 300  #5 minutes

class autoThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            time.sleep(INTERVAL)
            pickle_file()
            print("Userdict uploaded automatically.")
            
            