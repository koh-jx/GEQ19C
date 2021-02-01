from User import User
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
    index = int(re.sub("[^0-9]", "", update.message.text))
    userid = user.id
    subfile.get_userdict()[userid].setRequestedIndex(index -1)

    try:
        # Create Message
        message = subfile.get_userdict()[userid].messageList[index - 1].generateMessage()

        update.message.reply_text("Your post is: ")
        if subfile.get_userdict()[userid].messageList[index - 1].hasphoto:
            photoid = subfile.get_userdict()[userid].messageList[index - 1].photoid
            context.bot.send_photo(chat_id = update.effective_chat.id, photo = photoid, caption = message, parse_mode=ParseMode.HTML)
        else:
            update.message.reply_text(message, parse_mode=ParseMode.HTML)
        
        if subfile.get_userdict()[userid].messageList[index - 1].hasphoto:
            reply_keyboard = [['Edit', 'Delete', 'Change Photo', 'Return to posts']]
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            update.message.reply_text("What would you like to do? (Edit, Delete, Change Photo, Return to posts)", reply_markup = reply_markup)
        else:
            reply_keyboard = [['Edit', 'Delete', 'Return to posts']]
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            update.message.reply_text("What would you like to do? (Edit, Delete, Return to posts)", reply_markup = reply_markup)

        return globals.MANAGEPOST

    except(IndexError):
        update.message.reply_text("Post of that value not found. Type the number again, or /cancel.")
        return globals.POSTTOMANAGE


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

    message = subfile.get_userdict()[userid].messageList[index].generateMessage() + "<b>Post made by @" + user.username + '</b>'
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
    message = subfile.get_userdict()[userid].messageList[index].generateMessage() + "<b>Post made by @" + user.username + '</b>'

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
        """\n\nPlease remember to update/delete your post once your transaction is complete.

Hit /start to return to the main menu.""", 
        parse_mode=ParseMode.HTML)
    
    else:
        update.message.reply_text("Failed to edit your message. /start to return to the main menu.")

    return ConversationHandler.END



def editphoto(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Send your new photo. (or /cancel)")
    return globals.EDITPHOTO


def generatenewphoto(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user 
    userid = user.id
    index = subfile.get_userdict()[userid].requestedIndex
    photoid = context.bot.getFile(update.message.photo[-1].file_id).file_id
    subfile.get_userdict()[userid].messageList[index].set_photoid(photoid)
    text = subfile.get_userdict()[userid].messageList[index].generateMessage() + "<b>Post made by @" + user.username + '</b>'

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
    message = subfile.get_userdict()[userid].messageList[index].generateMessage() + "<b>Post made by @" + user.username + '</b>'


    result = context.bot.editMessageMedia(chat_id = globals.CHANNELID, message_id = msgid, media = InputMediaPhoto(media = photoid))
    result.photo = [result.photo[-1]]
    edited = context.bot.editMessageCaption(chat_id = globals.CHANNELID, message_id = msgid, caption = message, parse_mode=ParseMode.HTML)
    print(edited)        


    if (edited):
        link = "https://t.me/c/" + str(globals.CHANNELLINKID) + "/" + str(msgid)

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
    return globals.DELETEPOST


def deletepost(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userid = user.id
    index = subfile.get_userdict()[userid].requestedIndex

    deleted = update.message.bot.deleteMessage(chat_id=globals.CHANNELID, message_id=subfile.get_userdict()[userid].messageList[index].id)
    if deleted:
        del subfile.get_userdict()[userid].messageList[index]
        update.message.reply_text("Post successfully deleted 🙌. /start to return to the main menu")
    else:
        update.message.reply_text("I failed to delete the message. You may prefer to edit the message instead. /start to return to the main menu.")

    return ConversationHandler.END