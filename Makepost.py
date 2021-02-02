from User import User
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ParseMode
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)
import subfile
import globals


#MAKE POSTS
# ----------------------------------------------------------
#Start Conversation
def start(update, context) -> int:    
    name = update.message.from_user.first_name
    user_id = update.message.from_user.id

    # Create user if not found in dictionary
    if user_id not in subfile.get_userdict().keys():
        subfile.get_userdict()[user_id] = User(name)

    reply_keyboard = [['Make Post 📬'], ['Manage Posts 💼'], ['Help/About ❓', 'Give Feedback/Contact Us 📣']]
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        """<b>Hello {}!👋</b>
Got hostel essentials to share or donate? Looking for something in particular?

<b>Type 'Make Post' to send a post to the NUSe channel, and 'Manage Posts' to view and edit your current posts!</b>

Send /cancel to cancel your current process at any time UwU
        """.format(name),  reply_markup = reply_markup, parse_mode=ParseMode.HTML)
    
    return globals.ACTION


def newpost(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Put up item ✉️'], ['Share item 🤝'], ['Look for item 👀']]
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("What are you looking to do today? (Put up item, Share item, Look for item)", reply_markup = reply_markup)

    return globals.GETTITLE


def gettype(option):
    if (option == 'Put up item ✉️'):
        return 1
    elif (option == 'Share item 🤝'):
        return 2
    elif (option == 'Look for item 👀'):
        return 3
    else:
        return 0


def gettitle(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    option = update.message.text
    userid = user.id
    type = gettype(option)


    # Create Message
    subfile.get_userdict()[userid].addMessage(type)

    update.message.reply_text("Input the title of your post. (or /cancel)", reply_markup=ReplyKeyboardRemove())

    return globals.GETTEXT


def checkForAngleBrackets(text):
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def gettext(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    title = checkForAngleBrackets(update.message.text)
    userid = user.id

    # Update title
    subfile.get_userdict()[userid].messageList[-1].set_title(title)
    update.message.reply_text("Title saved!")

    update.message.reply_text("""<b>Now input the text of your post. (or /cancel)</b>
    Recommended format:
        <i>Details: (Condition etc)
        Looking to exchange for: (If applicable)
        Place for collection: (If applicable)
        Status: (If applicable)
        etc</i>
<b>⚠️Your username will be automatically added to the post for people to contact you.</b>⚠️""", parse_mode=ParseMode.HTML)
    
    return globals.ASKFORPHOTO

def askforphoto(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    text = checkForAngleBrackets(update.message.text)
    userid = user.id
    
    #Update text
    subfile.get_userdict()[userid].messageList[-1].set_text(text)

    update.message.reply_text("""<b>Do you want to attach a picture along with the post? </b>
Send a picture, or /skip this step.

<b>⚠️NOTE: This decision is final: Telegram currently does not conversion from photo to text posts. 
(You can still edit the text/photo after submission)</b>⚠️""", parse_mode=ParseMode.HTML)
    return globals.GENERATETEXT


def generatetext(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user 
    userid = user.id
    result = update.message.text       # if its a photo, of type None, if not its "/skip"
    
    #Update Photo IF ANY
    if result == None:
        subfile.get_userdict()[userid].messageList[-1].set_hasphoto()
        photoid = context.bot.getFile(update.message.photo[-1].file_id).file_id
        subfile.get_userdict()[userid].messageList[-1].set_photoid(photoid)

    text = subfile.get_userdict()[userid].messageList[-1].generateMessage(user.username)

    update.message.reply_text("Your post is: ")
    if subfile.get_userdict()[userid].messageList[-1].hasphoto:
        photoid = subfile.get_userdict()[userid].messageList[-1].photoid
        context.bot.send_photo(chat_id = update.effective_chat.id, photo = photoid, caption = text, parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(text, parse_mode=ParseMode.HTML)

    update.message.reply_text("Will this be ok? Type 'OK' (in caps) to confirm, and /text, /title or /type to return to previous selections.")

    return globals.SENDING


def sendToChannel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userid = user.id
    messageDetails = 0

    # Send message
    message = subfile.get_userdict()[userid].messageList[-1].generateMessage(user.username)

    if subfile.get_userdict()[userid].messageList[-1].hasphoto:
        messageDetails = context.bot.send_photo(chat_id = globals.CHANNELID, photo = subfile.get_userdict()[userid].messageList[-1].photoid, caption = message, parse_mode=ParseMode.HTML)
    else:
        messageDetails = context.bot.send_message(chat_id=globals.CHANNELID, text = message, parse_mode=ParseMode.HTML)

    # Update id
    subfile.get_userdict()[userid].messageList[-1].set_id(messageDetails.message_id)
    
    link = "https://t.me/c/" + str(globals.CHANNELLINKID) + "/" + str(messageDetails.message_id)

    update.message.reply_text("""Sent! Thanks for using the channel! 💖💖💖💖 

<b>View your post here: """ + link + "</b>" + 
        """\n\n<b>Please remember to update your post using Manage Posts once your transaction is complete. </b>
        
Hit /start to return to the main menu.""",  parse_mode=ParseMode.HTML)

    return ConversationHandler.END


def about(update, context) -> int:    
    update.message.reply_text(
        """<b>Welcome to NUSeBot!</b>
View the NUSe channel here: "LINK"

<b>About Us</b>
NUSe is part of a GEQ1917 Project to reduce waste generated by residences in NUS.

<b>How do I use the bot?</b>
Start by going to <b>'Make Post'</b> to create a post for your channel.
The bot will walk you through all the steps needed to create your post!

You can then view, edit and change the status of your post in <b>'Manage Posts'</b>.
Once your transaction is done, you should <b>update the status</b> of your post in  <b>'Manage Posts'</b> so people know that your post has expired.

<b>Feedback</b>
If you have any questions/feedback, found bugs, or <b>wish to participate in our focus group discussion during Week 8</b>, 
do drop us a message using by accessing <b>Give Feedback 📣</b> in the main menu! 

/start to return to the main menu.
        """, parse_mode=ParseMode.HTML)
    
    return ConversationHandler.END 




def feedback(update, context) -> int:    
    update.message.reply_text("""Type any feedback/bugs/concerns/questions etcccc here! :D 
(or /cancel) 

You may include your Telegram ID to help us seek clarifications if necessary.

<i>Speaking of feedback...</i>
<b>We are looking for people to participate in a focus group discussion about our app (and its objectives) around Sem 2 Week 8!!

If you're free, do come down and join us to help us with our project. :)

Do drop us a message here should you be willing to participate, thank you very much!!!!!!!!!!!
(Refreshments would be provided). </b>
        """, parse_mode=ParseMode.HTML)
    
    return globals.FEEDBACK

def postfeedback(update, context) -> int:    
    feedback = update.message.text

    context.bot.send_message(chat_id=globals.ADMINCHANNELID, text = "FEEDBACK BY @" + update.message.from_user.username + ": \n"  + feedback)
    
    update.message.reply_text("""Thank you for your feedback/concerns!
You may return to the main menu using /start.
        """, parse_mode=ParseMode.HTML)
    
    return ConversationHandler.END
