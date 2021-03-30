import threading
import time
from subfile import pickle_file

# Saves the data onto the S3 server once every 12 hours
INTERVAL = 43200  # 43200 seconds = 12 Hours

class autoThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            time.sleep(INTERVAL)
            pickle_file()
            print("Userdict uploaded automatically.")
            
            