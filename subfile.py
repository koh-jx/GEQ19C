from telegram import Update
from telegram.ext import CallbackContext


#Dictionary of all user IDs
userdict = {}

def get_userdict():
    return userdict

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
    userdict = {}
    update.message.reply_text(
        "System reset success. /cancel"
    )



# To make an admin function to directly go in userdict and view userdict???