import logging, re
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from telegram.files.inputmedia import InputMediaPhoto
from telegram.files.photosize import PhotoSize

#Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


#GLOBAL VARIABLES
#===========================================================
#Dictionary of all user IDs
userdict = {}

#CONSTANTS
#"Enums" for conversationHandler's Dictionary
ACTION, GETTITLE, GETTEXT, GENERATETEXT, SENDING, POSTTOMANAGE, MANAGEPOST, DELETEPOST, EDITPREVIEW, EDIT, ASKFORPHOTO, EDITPHOTO, EDITPHOTOPOST = range(13)

# #Channel ID to forward messages to, bot must be Admin in the channel
# CHANNELID = -1001475820789
# CHANNELLINKID = 1475820789 #ChannelID without the -100
# #Token for the bot
# TOKEN = '1669722724:AAFzI4ueHRznyydSWylmtSkI4Wm7g2exRMI'

#Test
#Channel ID to forward messages to, bot must be Admin in the channel
CHANNELID = -1001306746114
CHANNELLINKID = 1306746114 #ChannelID without the -100
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
        self.photoid = 0
        self.hasphoto = False
    
    def set_title(self, title):
        self.title = title
    
    def set_text(self, text):
        self.text = text

    def set_id(self, id):
        self.id = id

    def set_hasphoto(self):
        if self.hasphoto:
            self.hasphoto = False
        else:
            self.hasphoto = True

    def set_photoid(self, photoid):
        self.photoid = photoid
        

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
        self.requestedIndex = 0
    
    def addMessage(self, type):
        self.messageList.append(Message(type))

    def listMessages(self):    
        self.clearUnsentMessages()
        text = ""
        for i in range(len(self.messageList)):
            text += (str(i + 1) + ": " + self.messageList[i].title + '\n')
        return text

    def clearUnsentMessages(self):
        i = 0
        while (i < len(self.messageList)):
            if(self.messageList[i].id == 0):
                del self.messageList[i]
                continue
            i += 1
    
    def setRequestedIndex(self, index):
        self.requestedIndex = index
            





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
        """<b>Hello {}!👋</b>
Got hostel essentials to share or donate? Looking for something in particular?

<b>Type 'Make Post' to send a post to the NUSe channel, and 'Manage Posts' to view and edit your current posts!</b>

Send /cancel to cancel your current process at any time UwU
        """.format(name),  reply_markup = reply_markup, parse_mode=ParseMode.HTML)
    
    return ACTION


def newpost(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Put up item', 'Share item', 'Look for item']]
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("What are you looking to do today? (Put up item, Share item, Look for item)", reply_markup = reply_markup)

    return GETTITLE


def gettype(option):
    if (option == 'Put up item'):
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

    update.message.reply_text("Input the title of your post. (or /cancel)", reply_markup=ReplyKeyboardRemove())

    return GETTEXT


def checkForAngleBrackets(text):
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def gettext(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    title = checkForAngleBrackets(update.message.text)
    userid = user.id

    # Update title
    userdict[userid].messageList[-1].set_title(title)
    update.message.reply_text("Title saved!")

    update.message.reply_text("""<b>Now input the text of your post. (or /cancel)</b>
    Recommended format:
        <i>Details: (Condition etc)
        Looking to exchange for: (If applicable)
        Place for collection: (If applicable)
        Status: (If applicable)
        etc</i>
<b>⚠️Your username will be automatically added to the post for people to contact you.</b>⚠️""", parse_mode=ParseMode.HTML)
    
    return ASKFORPHOTO

def askforphoto(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    text = checkForAngleBrackets(update.message.text)
    userid = user.id
    
    #Update text
    userdict[userid].messageList[-1].set_text(text)

    update.message.reply_text("""<b>Do you want to attach a picture along with the post? </b>
Send a picture, or /skip this step.

<b>⚠️NOTE: This decision is final: Telegram currently does not conversion from photo to text posts. 
(You can still edit the text/photo after submission)</b>⚠️""", parse_mode=ParseMode.HTML)
    return GENERATETEXT


def generatetext(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user 
    userid = user.id
    result = update.message.text       # if its a photo, of type None, if not its "/skip"
    
    #Update Photo IF ANY
    if result == None:
        userdict[userid].messageList[-1].set_hasphoto()
        photoid = context.bot.getFile(update.message.photo[-1].file_id).file_id
        userdict[userid].messageList[-1].set_photoid(photoid)

    text = userdict[userid].messageList[-1].generateMessage() + "<b>Post made by @" + user.username + '</b>'

    update.message.reply_text("Your post is: ")
    if userdict[userid].messageList[-1].hasphoto:
        photoid = userdict[userid].messageList[-1].photoid
        context.bot.send_photo(chat_id = update.effective_chat.id, photo = photoid, caption = text, parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(text, parse_mode=ParseMode.HTML)

    update.message.reply_text("Will this be ok? Type 'OK' (in caps) to confirm, and /text, /title or /type to return to previous selections.")

    return SENDING


def sendToChannel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userid = user.id
    messageDetails = 0

    # Send message
    message = userdict[userid].messageList[-1].generateMessage() + "<b>Post made by @" + user.username + '</b>'

    if userdict[userid].messageList[-1].hasphoto:
        messageDetails = context.bot.send_photo(chat_id = CHANNELID, photo = userdict[userid].messageList[-1].photoid, caption = message, parse_mode=ParseMode.HTML)
    else:
        messageDetails = context.bot.send_message(chat_id=CHANNELID, text = message, parse_mode=ParseMode.HTML)

    # Update id
    userdict[userid].messageList[-1].set_id(messageDetails.message_id)
    
    link = "https://t.me/c/" + str(CHANNELLINKID) + "/" + str(messageDetails.message_id)

    update.message.reply_text("""Sent! Thanks for using the channel! 💖💖💖💖 

<b>View your post here: """ + link + "</b>" + 
        """\n\nPlease remember to update/delete your post once your transaction is complete.
        
Hit /start to return to the main menu.""",  parse_mode=ParseMode.HTML)

    return ConversationHandler.END

    

# MANAGE POSTS
# ----------------------------------------------------------

def manageposts(update: Update, context: CallbackContext) -> int:
    text = userdict[update.message.from_user.id].listMessages()
    userdict[update.message.from_user.id].setRequestedIndex(0)
    if text != "":
        update.message.reply_text("List of your submitted posts:\n" + text, parse_mode=ParseMode.HTML)
        update.message.reply_text("Type the number of the post to manage.", reply_markup=ReplyKeyboardRemove())
        return POSTTOMANAGE
    else:
        update.message.reply_text("You have no posts to manage. Press /start to return to the main menu.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END



def checkpost(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    index = int(re.sub("[^0-9]", "", update.message.text))
    userid = user.id
    userdict[userid].setRequestedIndex(index -1)

    try:
        # Create Message
        message = userdict[userid].messageList[index - 1].generateMessage()

        update.message.reply_text("Your post is: ")
        if userdict[userid].messageList[index - 1].hasphoto:
            photoid = userdict[userid].messageList[index - 1].photoid
            context.bot.send_photo(chat_id = update.effective_chat.id, photo = photoid, caption = message, parse_mode=ParseMode.HTML)
        else:
            update.message.reply_text(message, parse_mode=ParseMode.HTML)
        
        if userdict[userid].messageList[index - 1].hasphoto:
            reply_keyboard = [['Edit', 'Delete', 'Add/Change/Remove Photo', 'Return to posts']]
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            update.message.reply_text("What would you like to do? (Edit, Delete, Add/Change/Remove Photo, Return to posts)", reply_markup = reply_markup)
        else:
            reply_keyboard = [['Edit', 'Delete', 'Return to posts']]
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            update.message.reply_text("What would you like to do? (Edit, Delete, Return to posts)", reply_markup = reply_markup)

        return MANAGEPOST

    except(IndexError):
        update.message.reply_text("Post of that value not found. Type the number again, or /cancel.")
        return POSTTOMANAGE


def getedittext(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("""<b>Input the edited text of your post</b>.
    Here's an example format that you can follow:
        <i>Details: (Condition etc)
        Looking to exchange for: (If applicable)
        Place for collection: (If applicable)
        Status: (If applicable)
        etc</i>
<b>⚠️For consistency purposes, we do not allow the title to be edited.⚠️</b>""", parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    
    return EDITPREVIEW


def generateedittext(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    text = checkForAngleBrackets(update.message.text)
    userid = user.id
    index = userdict[userid].requestedIndex
    
    #Update text
    userdict[userid].messageList[index].set_text(text)

    message = userdict[userid].messageList[index].generateMessage() + "<b>Post made by @" + user.username + '</b>'
    update.message.reply_text("Your post will be changed to: ")

    if userdict[userid].messageList[index].hasphoto:
        photoid = userdict[userid].messageList[index].photoid
        context.bot.send_photo(chat_id = update.effective_chat.id, photo = photoid, caption = message, parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(message, parse_mode=ParseMode.HTML)

    update.message.reply_text("Will this be ok? Type 'OK' (in caps) to confirm, or /cancel.")

    return EDIT


def editInChannel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userid = user.id
    index = userdict[userid].requestedIndex
    msgid = userdict[userid].messageList[index].id
    edited = False

    # Send message
    message = userdict[userid].messageList[index].generateMessage() + "<b>Post made by @" + user.username + '</b>'

    if userdict[userid].messageList[index].hasphoto:
        edited = context.bot.editMessageCaption(chat_id = CHANNELID, message_id = msgid, caption = message, parse_mode=ParseMode.HTML)
    else:
        edited = context.bot.editMessageText(chat_id=CHANNELID, 
            message_id = msgid, 
            text = message, 
            parse_mode=ParseMode.HTML)

    if (edited):

        link = "https://t.me/c/" + str(CHANNELLINKID) + "/" + str(msgid)

        update.message.reply_text("""Edited! Thanks for using the channel! 💖 

<b>View your post here: """ + link + "</b>" + 
        """\n\nPlease remember to update/delete your post once your transaction is complete.

Hit /start to return to the main menu.""", 
        parse_mode=ParseMode.HTML)
    
    else:
        update.message.reply_text("Failed to edit your message. /start to return to the main menu.")

    return ConversationHandler.END



def editphoto(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Send your new photo. (or /cancel)")
    return EDITPHOTO


def generatenewphoto(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user 
    userid = user.id
    result = update.message.text
    index = userdict[userid].requestedIndex
    msgid = userdict[userid].messageList[index].id
    photoid = context.bot.getFile(update.message.photo[-1].file_id).file_id
    userdict[userid].messageList[index].set_photoid(photoid)
    text = userdict[userid].messageList[index].generateMessage() + "<b>Post made by @" + user.username + '</b>'

    update.message.reply_text("Your post is: ")
    if userdict[userid].messageList[index].hasphoto:
        photoid = userdict[userid].messageList[index].photoid
        context.bot.send_photo(chat_id = update.effective_chat.id, photo = photoid, caption = text, parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(text, parse_mode=ParseMode.HTML)

    update.message.reply_text("Will this be ok? Type 'OK' (in caps) to confirm, or /cancel.")
    return EDITPHOTOPOST


def editPhotoInChannel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user 
    userid = user.id
    index = userdict[userid].requestedIndex

    msgid = userdict[userid].messageList[index].id
    photoid = userdict[userid].messageList[index].photoid
    message = userdict[userid].messageList[index].generateMessage() + "<b>Post made by @" + user.username + '</b>'


    result = context.bot.editMessageMedia(chat_id = CHANNELID, message_id = msgid, media = InputMediaPhoto(media = photoid))
    result.photo = [result.photo[-1]]
    edited = context.bot.editMessageCaption(chat_id = CHANNELID, message_id = msgid, caption = message, parse_mode=ParseMode.HTML)
    print(edited)        


    if (edited):
        link = "https://t.me/c/" + str(CHANNELLINKID) + "/" + str(msgid)

        update.message.reply_text("""Edited! Thanks for using the channel! 💖 

<b>View your post here: """ + link + "</b>" + 
        """\n\nPlease remember to update/delete your post once your transaction is complete.

Hit /start to return to the main menu.""", 
        parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text("Failed to edit your message. /start to return to the main menu.")

    return ConversationHandler.END



def deletepostconfirmation(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("""🚨<b>Posts can only be deleted 48 hours within time of submission!</b>
Are you sure you want to delete? Type 'OK' (in caps) or /cancel""", parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    return DELETEPOST


def deletepost(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userid = user.id
    index = userdict[userid].requestedIndex

    deleted = update.message.bot.deleteMessage(chat_id=CHANNELID, message_id=userdict[userid].messageList[index].id)
    if deleted:
        del userdict[userid].messageList[index]
        update.message.reply_text("Post successfully deleted 🙌. /start to return to the main menu")
    else:
        update.message.reply_text("I failed to delete the message. You may prefer to edit the message instead. /start to return to the main menu.")

    return ConversationHandler.END


# Fallback function: Conversation cancelled at any time with /start
#===========================================================
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Process cancelled. /start to return to the main menu.', reply_markup=ReplyKeyboardRemove()
    )
    userdict[update.message.from_user.id].clearUnsentMessages()
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



#MAIN
#===========================================================
# Conversation gets your action first (Cancel at any time) [return  ACTION]
#     Make Post? Get the type of your action    [return GETTITLE]
#                     Get the title of your action [return GETTEXT]
#                         Get the text of your action (and images if necessary) [return GETIMAGE]
#                             Generate message, double-confirm
#                                 Post in channel and save msgid
#     Manage Posts? See list of posts => choose an index to view
        # Display the message: Get type of action
        #     Edit
        #        Change or Remove photo TODO
        #     Delete
        #     Go back


def main():
    updater = Updater(token = TOKEN, use_context = True)
    dispatcher = updater.dispatcher
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ACTION: [MessageHandler(Filters.regex('Make Post'), newpost), MessageHandler(Filters.regex('Manage Posts'), manageposts)],       
            GETTITLE: [MessageHandler(Filters.regex('Put up item'), gettitle), 
                       MessageHandler(Filters.regex('Share item'), gettitle),
                       MessageHandler(Filters.regex('Look for item'), gettitle),
                       MessageHandler(Filters.text, newpost)],
            GETTEXT: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, gettext)],
            ASKFORPHOTO: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, askforphoto)],
            GENERATETEXT: [CommandHandler('skip', generatetext), MessageHandler(Filters.photo, generatetext)],
            SENDING: [MessageHandler(Filters.regex('OK'), sendToChannel), CommandHandler('text', gettext),
                CommandHandler('title', gettitle), CommandHandler('type', newpost)],
            POSTTOMANAGE: [MessageHandler(Filters.regex(r'\d+'), checkpost)],
            MANAGEPOST: [MessageHandler(Filters.regex('Edit'), getedittext), 
                         MessageHandler(Filters.regex('Delete'), deletepostconfirmation),
                         MessageHandler(Filters.regex('Add/Change/Remove Photo'), editphoto),
                         MessageHandler(Filters.regex('Return to posts'), manageposts)],
            DELETEPOST: [MessageHandler(Filters.regex('OK'), deletepost)],
            EDITPREVIEW: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, generateedittext)],
            EDIT: [MessageHandler(Filters.regex('OK'), editInChannel)],
            EDITPHOTO: [CommandHandler('remove', generatenewphoto), MessageHandler(Filters.photo, generatenewphoto)],
            EDITPHOTOPOST: [MessageHandler(Filters.regex('OK'), editPhotoInChannel)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Admin commands, on the main menu
    dispatcher.add_handler(CommandHandler('geq19csoftreset', softReset))

    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()



# Useful Resources:
# https://core.telegram.org/bots/api#getfile
# https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py
# https://stackoverflow.com/questions/51222907/how-to-send-a-photo-via-python-telegram-bot
