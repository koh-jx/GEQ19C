from telegram import Update
from telegram.ext import CallbackContext

#Dictionary of all user IDs
userdict = {}

def get_userdict():
    return userdict



# Admin Functions - Use at the main menu to avoid problems/when no one is sending anything
#===========================================================
# Reset system to original settings
def softReset(update: Update, context: CallbackContext) -> None:
    userdict = {}
    update.message.reply_text(
        "System reset success. /cancel"
    )