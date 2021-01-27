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
ACTION, GETTITLE, GETTEXT = range(3)

#Channel ID to forward messages to, bot must be Admin in the channel
CHANNELID = -1001306746114
#Token for the bot
TOKEN = '1532597200:AAGGlFLs0VEPqnMLdfy7qh5jXFntuSUs8iI'



#CLASS(ES)
#===========================================================
# Classes will be used in global dictionary userdict. To access an individual message's text:
# userdict[userid].messageList[index].text


# Message class contains the title and text of the message, so they can be retrieved from the database.
# Each message also has a type: 1 - Donation/Exchange, 2 - Sharing, 3 - Looking for
# Message has 2 mutators, to change the title and text as the user sees fit (For creation and editing purposes)
class Message:
    def __init__(self, type):
        self.id = 0
        self.type = type
        self.title = ""
        self.text = ""
    
    def set_title(self, title):
        self.title = title
    
    def set_text(self, text):
        self.text = text


# The User class contains the name of the user, as well as a messageList,
# with values of type Message. As the user makes/deletes offers, the messageList will be updated with his/her current messages.
class User:
    def __init__(self, name):
        self.name = name
        self.messageList = []
    
    def addMessage(self, type):
        self.messageList.append(Message(type))




#COMMANDS/CONVERSATION HANDLER
#===========================================================
#Start Conversation
def start(update, context) -> int:    
    name = update.message.from_user.first_name
    user_id = update.message.from_user.id

    # Create user if not found in dictionary
    if user_id not in userdict.keys():
        userdict[user_id] = User(name)

    reply_keyboard = [['Make Post', 'Manage Posts']]
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        """Hello {}!
Got hostel essentials to share or donate? Looking for something in particular?
Send /cancel to stop the bot UwU
        """.format(name), reply_markup = reply_markup)
    
    return ACTION

def newpost(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    option = update.message.text

    print(user.first_name + " chose " + option)
    reply_keyboard = [['Put on offer', 'Share item', 'Look for item']]
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("What are you looking to do today?", reply_markup = reply_markup)

    return GETTITLE

def gettype(option):
    if (option == 'Put on offer'):
        return 1
    elif (option == 'Share item'):
        return 2
    elif (option == 'Look for item'):
        return 3
    else:
        return 0

def gettitle(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    option = update.message.text
    userid = user.id
    type = gettype(option)

    # Create Message
    userdict[userid].addMessage(type)

    update.message.reply_text("Input the title of your post.")

    return GETTEXT

def gettext(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    title = update.message.text
    userid = user.id

    # Update title
    userdict[userid].messageList[-1].set_title(title)

    update.message.reply_text("Input the text of your post.")

    #TESTING: TO CREATE A METHOD IN MESSAGE THAT COMPILES EVERYTHING AND RETURNS ONE SHOT
    update.message.reply_text(userdict[userid].messageList[-1].type)
    update.message.reply_text(userdict[userid].messageList[-1].title)


    return ConversationHandler.END

#Fallback function: Conversation cancelled at any time with /start
def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(
        'Cancelled. /start to return to the main menu', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END





#MAIN
#===========================================================
# Conversation gets your action first (Cancel at any time) [return  ACTION]
#     Make Post? Get the type of your action    [return GETTITLE]
#                     Get the title of your action [return GETTEXT]
#                         Get the text of your action (and images if necessary) [return GETIMAGE]
#                             Generate message, double-confirm
#                                 Post in channel
#     Manage Posts  .......


def main():
    updater = Updater(token = TOKEN, use_context = True)
    dispatcher = updater.dispatcher
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ACTION: [MessageHandler(Filters.regex('Make Post'), newpost)],     # TO DO FOR MANAGE POSTS
            GETTITLE: [MessageHandler(Filters.text, gettitle)],
            GETTEXT: [MessageHandler(Filters.text, gettext)],
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
