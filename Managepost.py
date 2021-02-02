# from User import User
import re
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ParseMode
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)
from telegram.files.inputmedia import InputMediaPhoto

import globals
import subfile
from Makepost import checkForAngleBrackets

# MANAGE POSTS
# ----------------------------------------------------------

def manageposts(update: Update, context: CallbackContext) -> int:
    text = subfile.get_userdict()[update.message.from_user.id].listMessages()
    subfile.get_userdict()[update.message.from_user.id].setRequestedIndex(0)
    if text != "":
        update.message.reply_text("List of your submitted posts:\n" + text, parse_mode=ParseMode.HTML)
        update.message.reply_text("Type the number of the post to manage. (or /cancel)", reply_markup=ReplyKeyboardRemove())
        return globals.POSTTOMANAGE
    else:
        update.message.reply_text("You have no posts to manage. Press /start to return to the main menu.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END



def checkpost(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    
    userid = user.id
    input = update.message.text
    index = 0
    
    if input != 'Return to post 🔙':
        index = int(re.sub("[^0-9]", "", input)) - 1
        subfile.get_userdict()[userid].setRequestedIndex(index)
    else:
        index = subfile.get_userdict()[userid].requestedIndex

    try:
        # Create Message
        message = subfile.get_userdict()[userid].messageList[index].generateMessage(user.username)

        update.message.reply_text("Your post is: ")
        if subfile.get_userdict()[userid].messageList[index].hasphoto:
            photoid = subfile.get_userdict()[userid].messageList[index].photoid
            context.bot.send_photo(chat_id = update.effective_chat.id, photo = photoid, caption = message, parse_mode=ParseMode.HTML)
        else:
            update.message.reply_text(message, parse_mode=ParseMode.HTML)
        
        if subfile.get_userdict()[userid].messageList[index].hasphoto:
            reply_keyboard = [['Edit 📝'], ['Change Photo 🖼️'], ['Change Status ✔️❌'], ['Delete 🛑'], ['Return to posts 🔙']]
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            update.message.reply_text("What would you like to do? (Edit, Delete, Change Photo, Return to posts)", reply_markup = reply_markup)
        else:
            reply_keyboard = [['Edit 📝'], ['Delete 🛑'], ['Change Status ✔️❌'], ['Return to posts 🔙']]
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            update.message.reply_text("What would you like to do? (Edit, Delete, Return to posts)", reply_markup = reply_markup)

        return globals.MANAGEPOST

    except(IndexError):
        update.message.reply_text("Post of that value not found. Type the number again, or /cancel.")
        return globals.POSTTOMANAGE


#EDIT POST TEXT
#========================================================================

def getedittext(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("""<b>Input the edited text of your post</b>.
    Here's an example format that you can follow:
        <i>Details: (Condition etc)
        Looking to exchange for: (If applicable)
        Place for collection: (If applicable)
        Status: (If applicable)
        etc</i>
<b>⚠️For consistency purposes, we do not allow the title to be edited.⚠️</b>""", parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    
    return globals.EDITPREVIEW


def generateedittext(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    text = checkForAngleBrackets(update.message.text)
    userid = user.id
    index = subfile.get_userdict()[userid].requestedIndex
    
    #Update text
    subfile.get_userdict()[userid].messageList[index].set_text(text)

    message = subfile.get_userdict()[userid].messageList[index].generateMessage(user.username)
    update.message.reply_text("Your post will be changed to: ")

    if subfile.get_userdict()[userid].messageList[index].hasphoto:
        photoid = subfile.get_userdict()[userid].messageList[index].photoid
        context.bot.send_photo(chat_id = update.effective_chat.id, photo = photoid, caption = message, parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(message, parse_mode=ParseMode.HTML)

    update.message.reply_text("Will this be ok? Type 'OK' (in caps) to confirm, or /cancel.")

    return globals.EDIT


def editInChannel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userid = user.id
    index = subfile.get_userdict()[userid].requestedIndex
    msgid = subfile.get_userdict()[userid].messageList[index].id
    edited = False

    # Send message
    message = subfile.get_userdict()[userid].messageList[index].generateMessage(user.username)

    if subfile.get_userdict()[userid].messageList[index].hasphoto:
        edited = context.bot.editMessageCaption(chat_id = globals.CHANNELID, message_id = msgid, caption = message, parse_mode=ParseMode.HTML)
    else:
        edited = context.bot.editMessageText(chat_id=globals.CHANNELID, 
            message_id = msgid, 
            text = message, 
            parse_mode=ParseMode.HTML)

    if (edited):

        link = "https://t.me/c/" + str(globals.CHANNELLINKID) + "/" + str(msgid)

        update.message.reply_text("""Edited! Thanks for using the channel! 💖 

<b>View your post here: """ + link + "</b>" + 
        """\n\n<b>Please remember to update your post once your transaction is complete.</b>

Hit /start to return to the main menu.""", 
        parse_mode=ParseMode.HTML)
    
    else:
        update.message.reply_text("Failed to edit your message. /start to return to the main menu.")

    return ConversationHandler.END




# PHOTO FUNCTIONALITY
#========================================================================

def editphoto(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Send your new photo. (or /cancel)")
    return globals.EDITPHOTO


def generatenewphoto(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user 
    userid = user.id
    index = subfile.get_userdict()[userid].requestedIndex
    photoid = context.bot.getFile(update.message.photo[-1].file_id).file_id
    subfile.get_userdict()[userid].messageList[index].set_photoid(photoid)
    text = subfile.get_userdict()[userid].messageList[index].generateMessage(user.username) 

    update.message.reply_text("Your post is: ")
    if subfile.get_userdict()[userid].messageList[index].hasphoto:
        photoid = subfile.get_userdict()[userid].messageList[index].photoid
        context.bot.send_photo(chat_id = update.effective_chat.id, photo = photoid, caption = text, parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(text, parse_mode=ParseMode.HTML)

    update.message.reply_text("Will this be ok? Type 'OK' (in caps) to confirm, or /cancel.")
    return globals.EDITPHOTOPOST


def editPhotoInChannel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user 
    userid = user.id
    index = subfile.get_userdict()[userid].requestedIndex

    msgid = subfile.get_userdict()[userid].messageList[index].id
    photoid = subfile.get_userdict()[userid].messageList[index].photoid
    message = subfile.get_userdict()[userid].messageList[index].generateMessage(user.username)


    result = context.bot.editMessageMedia(chat_id = globals.CHANNELID, message_id = msgid, media = InputMediaPhoto(media = photoid))
    result.photo = [result.photo[-1]]
    edited = context.bot.editMessageCaption(chat_id = globals.CHANNELID, message_id = msgid, caption = message, parse_mode=ParseMode.HTML)

    if (edited):
        link = "https://t.me/c/" + str(globals.CHANNELLINKID) + "/" + str(msgid)

        update.message.reply_text("""Edited! Thanks for using the channel! 💖 

<b>View your post here: """ + link + "</b>" + 
        """\n\n<b>Please remember to update the status of  your post once your transaction is complete.</b>

Hit /start to return to the main menu.""", 
        parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text("Failed to edit your message. /start to return to the main menu.")

    return ConversationHandler.END



#DELETE PHOTO
#=========================================================================


def deletepostreason(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("""NOTE!! 🚨<b>Telegram only allows the deletion of posts 48 hours within its time of submission!</b>

<b>Completed transactions should have their status marked as completed instead of being deleted.</b> 

Please briefly state your reason for deletion. This will be recorded to help us better improve our channel :) (Or /cancel)""", 
    reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
    return globals.DELETEPOSTCONFIRM


def deletepostconfirmation(update: Update, context: CallbackContext) -> int:

    # Send reason for deletion to me (or a dedicated channel)
    reason = update.message.text
    context.bot.send_message(chat_id=globals.ADMINCHANNELID, text = "DELETION BY @" + update.message.from_user.username + ": "  + reason)

    update.message.reply_text("""ARE YOU SURE YOU WANT TO DELETE? 
    
Type 'OK' (in caps) or /cancel""")
    return globals.DELETEPOST


def deletepost(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userid = user.id
    index = subfile.get_userdict()[userid].requestedIndex

    deleted = update.message.bot.deleteMessage(chat_id=globals.CHANNELID, message_id=subfile.get_userdict()[userid].messageList[index].id)
    if deleted:
        text = subfile.get_userdict()[userid].messageList[index].generateMessage(user.username)
        context.bot.send_message(chat_id=globals.ADMINCHANNELID, text = "DELETION TEXT BY @" + update.message.from_user.username + ": \n"  + text)
        del subfile.get_userdict()[userid].messageList[index]
        update.message.reply_text("Post successfully deleted 🙌. /start to return to the main menu")
    else:
        update.message.reply_text("I failed to delete the message. The post was likely made more than 48 hours ago. You may prefer to edit the message instead. /start to return to the main menu.")

    return ConversationHandler.END




# STATUS CHANGE
#=================================================================================


def statuschange(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userid = user.id
    index = subfile.get_userdict()[userid].requestedIndex
    status = subfile.get_userdict()[userid].messageList[index].getstatus()
    type = subfile.get_userdict()[userid].messageList[index].type
    reply_keyboard = []

    if status == "[Available]":
        if type == 1:
            reply_keyboard = [['My item is taken ✔️'], ['Withdraw Post ❌'], ['Return to post 🔙']]
        elif type == 2:
            reply_keyboard = [['It is currently loaned ✔️'], ['Withdraw Post ❌'], ['Return to post 🔙']]
    elif status == "[Pending]":
        reply_keyboard = [['I found my item ✔️'], ['Withdraw Post ❌'], ['Return to post 🔙']]
    elif status == "[Completed]":
        reply_keyboard = [['Put the post back up'], ['Return to post 🔙']]
    elif status == "[On Loan]":
        reply_keyboard = [['The item has been returned ✔️'], ['Return to post 🔙']]
    elif status == "[Post Redacted]":
        reply_keyboard = [['Return to post 🔙']]
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text("You have withdrawn this post. You cannot change its status. You may make a new post.", reply_markup = reply_markup)
        return globals.CHANGESTATUS

    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("Change the status of your post.", reply_markup = reply_markup)
    
    return globals.CHANGESTATUS



def updatestatus(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userid = user.id
    index = subfile.get_userdict()[userid].requestedIndex
    target = subfile.get_userdict()[userid].messageList[index]
    msgid = target.id
    action = update.message.text

    if action == 'My item is taken ✔️' or action == 'It is currently loaned ✔️' or action == 'I found my item ✔️':
        target.changestatus(1)
    elif action == 'Put the post back up' or action == 'The item has been returned ✔️':
        target.changestatus(0)
    elif action == 'Withdraw Post ❌':
        target.changestatus(2)

    message = target.generateMessage(user.username)

    link = "https://t.me/c/" + str(globals.CHANNELLINKID) + "/" + str(msgid)
    
    if subfile.get_userdict()[userid].messageList[index].hasphoto:
        context.bot.editMessageCaption(chat_id = globals.CHANNELID, message_id = msgid, caption = message, parse_mode=ParseMode.HTML)
    else:
        context.bot.editMessageText(chat_id=globals.CHANNELID, 
            message_id = msgid, 
            text = message, 
            parse_mode=ParseMode.HTML
            ) 
            

    context.bot.send_message(chat_id=globals.ADMINCHANNELID, text = "STATUS UPDATE BY @" + user.username + ": "  + message + "\n" + action, parse_mode=ParseMode.HTML)

    reply_keyboard = [['Return to post 🔙']]
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("""Status updated! 💖 

<b>View your post here: """ + link + """</b>
""", 
        parse_mode=ParseMode.HTML, reply_markup = reply_markup)

    return globals.CHANGESTATUS