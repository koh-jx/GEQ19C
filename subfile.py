from telegram import Update
from telegram.ext import CallbackContext
import s3_operations
import pickle

#Dictionary of all user IDs
userdict = {}

def get_userdict():
    return userdict


#To work with s3_operations.py to upload/obtain the pickled files from the S3 server
def save(update: Update, context: CallbackContext) -> None:
    pickle_file()

def read(update: Update, context: CallbackContext) -> None:
    unpickle_file()

def pickle_file():
    with open('userdict.pickle', 'wb') as handle:
        pickle.dump(userdict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    s3_operations.upload_userdict()
    print("Saved")

def unpickle_file():
    global userdict
    s3_operations.read_userdict_from_bucket()
    with open('userdict.pickle', 'rb') as data:
        userdict = pickle.load(data)

    print("Loaded")







#CLASS(ES) User.py and Message.py
#===========================================================
# Classes will be used in global dictionary subfile.get_userdict(). To access an individual message's text:
# subfile.get_userdict()[userid].messageList[index].text
# update.message.reply_text(subfile.get_userdict()[userid].messageList[-1].type)
# update.message.reply_text(subfile.get_userdict()[userid].messageList[-1].title)



# Admin Functions - Use at the main menu to avoid problems/when no one is sending anything
#===========================================================
# Reset system to original settings
def softReset(update: Update, context: CallbackContext) -> None:
    global userdict
    userdict = {}
    update.message.reply_text(
        "System reset success. /start"
    )



# Count functions
countposts = 0
counttransactions = 0

def checkcount(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Post Count: " + str(countposts) + '\nTransaction Count: ' + str(counttransactions) + "\n/cancel or /start"
    )

def resetcount(update: Update, context: CallbackContext) -> None:
    global countposts
    countposts = 0
    global counttransactions
    counttransactions = 0
    update.message.reply_text("Counts Reset. /cancel or /start")