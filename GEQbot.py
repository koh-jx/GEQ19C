import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

#Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


#GLOBAL VARIABLES
#===========================================================
#Dictionary of all user IDs
userdict = {}
#For conversationHandler
MENU = range(1)

#Channel ID to forward messages to, bot must be Admin in the channel
CHANNELID = -1001306746114
#Token for the bot
TOKEN = '1532597200:AAGGlFLs0VEPqnMLdfy7qh5jXFntuSUs8iI'



#CLASS(ES)
#===========================================================
class User:
    def __init__(self, name):
        self.name = name
        self.messageList = {}
    
    def addMessage(self, msgid, title):
        self.messageList[msgid] = title




#COMMANDS/CONVERSATION HANDLER
#===========================================================
#Start Conversation
def start(update, context) -> int:    
    name = update.message.from_user.first_name
    user_id = update.message.from_user.id
    if user_id not in userdict.keys():
        userdict[user_id] = User(name)                                          
    reply_keyboard = [['Share/Donate', 'Look for items', 'Manage Posts']]
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        """Hello {}!
Got hostel essentials to share or donate? Looking for something in particular?
Send /cancel to stop the bot UwU
        """.format(name), reply_markup = reply_markup
    )
    
    return MENU

def looking(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    option = update.message.text
    print(option)
    update.message.reply_text("Looking for items?")

    return ConversationHandler.END

def donating(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    option = update.message.text
    print(option)
    update.message.reply_text("Sharing is Caring")

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(
        'Cancelled. /start to return to the main menu', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END





#MAIN
#===========================================================
def main():
    updater = Updater(token = TOKEN, use_context = True)
    dispatcher = updater.dispatcher
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [MessageHandler(Filters.regex('Look for items'), looking), MessageHandler(Filters.regex('Share/Donate'), donating)],
            # PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
            # LOCATION: [
            #     MessageHandler(Filters.location, location),
            #     CommandHandler('skip', skip_location),
            # ],
            # BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()



if __name__ == '__main__':
    main()













##
##def photo(update: Update, context: CallbackContext) -> int:
##    user = update.message.from_user
##    photo_file = update.message.photo[-1].get_file()
##    photo_file.download('user_photo.jpg')
##    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
##    update.message.reply_text(
##        'Gorgeous! Now, send me your location please, ' 'or send /skip if you don\'t want to.'
##    )
##
##    return LOCATION
##
###photo
##dispatcher.add_handler(MessageHandler(Filters.photo, photo))
