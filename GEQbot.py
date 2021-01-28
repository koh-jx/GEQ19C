import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ParseMode
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
#Number of Messages in the Channel
CHANNELMSGID = 1

#CONSTANTS
#"Enums" for conversationHandler's Dictionary
ACTION, GETTITLE, GETTEXT, GENERATETEXT, SENDING, MANAGEMENU = range(6)

#Channel ID to forward messages to, bot must be Admin in the channel
CHANNELID = -1001306746114
#Token for the bot
TOKEN = '1532597200:AAGGlFLs0VEPqnMLdfy7qh5jXFntuSUs8iI'


#CLASS(ES)
#===========================================================
# Classes will be used in global dictionary userdict. To access an individual message's text:
# userdict[userid].messageList[index].text
# update.message.reply_text(userdict[userid].messageList[-1].type)
# update.message.reply_text(userdict[userid].messageList[-1].title)


# Message class contains the title and text of the message, so they can be retrieved from the database.
# Each message also has a type: 1 - Donation/Exchange, 2 - Sharing, 3 - Looking for
# Message has 3 mutators, to change the id, title and text as the user sees fit (For creation and editing purposes)
class Message:
    def __init__(self, type):
        self.id = 0
        self.type = type
        self.title = ""
        self.text = ""
        self.id = 0           #id is 0 if it remains unsent; 1 or more otherwise
    
    def set_title(self, title):
        self.title = title
    
    def set_text(self, text):
        self.text = text

    def set_id(self):
        self.id = CHANNELMSGID
        global CHANNELMSGID
        CHANNELMSGID += 1
        

    def generateMessage(self):
        type = ""
        if (self.type == 1):
            type = "OFFERING"
        elif (self.type == 2):
            type = "UP FOR SHARING"
        elif (self.type == 3):
            type = "LOOKING FOR"
        else:
            type = "???"
        
        title = self.title
        text = self.text
        return '<b>' + type + '</b>\n<b>' + title + '</b>\n' + "====================\n" + text + '\n====================\n'

        
    


# The User class contains the name of the user, as well as a messageList,
# with values of type Message. As the user makes/deletes offers, the messageList will be updated with his/her current messages.
class User:
    def __init__(self, name):
        self.name = name
        self.messageList = []
    
    def addMessage(self, type):
        self.messageList.append(Message(type))

    def listMessages(self):    
        text = ""                                                                                             #TODO
        for i in range(len(self.messageList)):
            text += (str(i + 1) + ": " + self.messageList[i].title + '\n')
        return text





#COMMANDS/CONVERSATION HANDLER
#===========================================================
#MAKE POSTS
# ----------------------------------------------------------
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
Send /cancel to cancel your current process at any time UwU
        """.format(name), reply_markup = reply_markup)
    
    return ACTION

def newpost(update: Update, context: CallbackContext) -> int:
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

    update.message.reply_text("""<b>Input the text of your post</b>.
    An example format:
        <i>Details:
        Looking to exchange for: (If applicable)
        Place for collection: (If applicable)
        etc</i>
<b>NOTE: Your username will be automatically added to the post for people to contact you</b>.
NOTE2: Do NOt use angle brackets (&lt; and &gt;)!""", parse_mode=ParseMode.HTML)             #TODO try-except?
    
    return GENERATETEXT

def generatetext(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    text = update.message.text
    userid = user.id

    #Update text
    userdict[userid].messageList[-1].set_text(text)
    update.message.reply_text("Your post is: ")
    update.message.reply_text(userdict[userid].messageList[-1].generateMessage() + "<b>Post made by @" + user.username + '</b>', parse_mode=ParseMode.HTML)
    update.message.reply_text("Will this be ok? Type 'OK' to confirm, and /text, /title or /type to return to previous selections.")

    return SENDING


def sendToChannel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userid = user.id

    # Send message
    message = userdict[userid].messageList[-1].generateMessage() + "<b>Post made by @" + user.username + '</b>'
    context.bot.send_message(chat_id=CHANNELID, text = message, parse_mode=ParseMode.HTML)

    # Update id
    userdict[userid].messageList[-1].set_id()

    update.message.reply_text("Sent! Thanks for using the channel! <3 Please remember to delete your post once your transaction is complete. Hit /start to return to the main menu.")

    return ConversationHandler.END

    

# MANAGE POSTS
# ----------------------------------------------------------

def manageposts(update: Update, context: CallbackContext) -> int:
    text = userdict[update.message.from_user.id].listMessages()
    update.message.reply_text("List of your submitted posts:\n" + text)

    # Regex is (\d)+, if input is not number, or If length of array less than choice of number, invalid message
    #return MANAGEMENU
    return ConversationHandler.END



# Fallback function: Conversation cancelled at any time with /start
def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(
        'Process cancelled. /start to return to the main menu.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END



# Admin Functions - Use at the main menu to avoid problems/when no one is sending anything
#===========================================================
# Reset system to original settings
def softReset(update: Update, context: CallbackContext) -> None:
    global userdict
    userdict = {}
    update.message.reply_text(
        "System reset success. /cancel"
    )

# To call this whenever we want to send out awareness posts
def checkChannelID(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(CHANNELMSGID)

def addChannelID(update: Update, context: CallbackContext) -> None:
    global CHANNELMSGID
    CHANNELMSGID += 1
    update.message.reply_text("Channel ID is now " + str(CHANNELMSGID) +  '.')


#MAIN
#===========================================================
# Conversation gets your action first (Cancel at any time) [return  ACTION]
#     Make Post? Get the type of your action    [return GETTITLE]
#                     Get the title of your action [return GETTEXT]
#                         Get the text of your action (and images if necessary) [return GETIMAGE]
#                             Generate message, double-confirm
#                                 Post in channel and TODO: save msgid
#     Manage Posts? See list of posts => choose an index to view
        # Display the message: Get type of action
        #     Edit?
        #     Delete
        #     Go back


def main():
    updater = Updater(token = TOKEN, use_context = True)
    dispatcher = updater.dispatcher
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ACTION: [MessageHandler(Filters.regex('Make Post'), newpost), MessageHandler(Filters.regex('Manage Posts'), manageposts)],                                      # TODO FOR MANAGE POSTS
            GETTITLE: [MessageHandler(Filters.text, gettitle)],
            GETTEXT: [MessageHandler(Filters.text, gettext)],
            GENERATETEXT: [MessageHandler(Filters.text, generatetext)],
            SENDING: [MessageHandler(Filters.regex('OK'), sendToChannel), CommandHandler('text', gettext),
                CommandHandler('title', gettitle), CommandHandler('type', newpost)],
            # MANAGEMENU: []
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Admin commands, on the main menu
    dispatcher.add_handler(CommandHandler('geq19csoftreset', softReset))
    dispatcher.add_handler(CommandHandler('checkchannelid', checkChannelID))
    dispatcher.add_handler(CommandHandler('addchannelid', addChannelID))

    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()



# Current bot does not support photos (Uploading photos and forwarding with messages is complex)
# Useful Resources:
# https://core.telegram.org/bots/api#getfile
# https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py
# https://stackoverflow.com/questions/51222907/how-to-send-a-photo-via-python-telegram-bot