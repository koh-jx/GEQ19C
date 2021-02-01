import logging
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

#Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

import Fallback
from globals import (ACTION, GETTITLE, GETTEXT, GENERATETEXT, SENDING, POSTTOMANAGE, 
                    MANAGEPOST, DELETEPOST, EDITPREVIEW, EDIT, ASKFORPHOTO, EDITPHOTO, EDITPHOTOPOST, TOKEN)
import subfile
from Makepost import (
    start,
    newpost,
    gettitle,
    gettext,
    askforphoto,
    generatetext,
    sendToChannel
)
from Managepost import (
    manageposts,
    checkpost,
    getedittext,
    generateedittext,
    editInChannel,
    editphoto,
    generatenewphoto,
    editPhotoInChannel,
    deletepostconfirmation,
    deletepost
)


#CLASS(ES) User.py and Message.py
#===========================================================
# Classes will be used in global dictionary subfile.get_userdict(). To access an individual message's text:
# subfile.get_userdict()[userid].messageList[index].text
# update.message.reply_text(subfile.get_userdict()[userid].messageList[-1].type)
# update.message.reply_text(subfile.get_userdict()[userid].messageList[-1].title)
           

#MAIN
#===========================================================
# Conversation gets your action first (Cancel at any time) [return  ACTION]
#     Make Post? Get the type of your action
#                     Get the title of your action
#                         Get the text of your action (and images if necessary)
#                             Generate message, double-confirm
#                                 Post in channel
#     Manage Posts? See list of posts => choose an index to view
        # Display the message: Get type of action
        #     Edit
        #        Change or Remove photo
        #     Delete
        #        Confirm
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
            GETTEXT: [CommandHandler('cancel', Fallback.cancel), MessageHandler(Filters.text, gettext)],
            ASKFORPHOTO: [CommandHandler('cancel', Fallback.cancel), MessageHandler(Filters.text, askforphoto)],
            GENERATETEXT: [CommandHandler('skip', generatetext), MessageHandler(Filters.photo, generatetext)],
            SENDING: [MessageHandler(Filters.regex('OK'), sendToChannel), CommandHandler('text', gettext),
                CommandHandler('title', gettitle), CommandHandler('type', newpost)],
            POSTTOMANAGE: [MessageHandler(Filters.regex(r'\d+'), checkpost)],
            MANAGEPOST: [MessageHandler(Filters.regex('Edit'), getedittext), 
                         MessageHandler(Filters.regex('Delete'), deletepostconfirmation),
                         MessageHandler(Filters.regex('Change Photo'), editphoto),
                         MessageHandler(Filters.regex('Return to posts'), manageposts)],
            DELETEPOST: [MessageHandler(Filters.regex('OK'), deletepost)],
            EDITPREVIEW: [CommandHandler('cancel', Fallback.cancel), MessageHandler(Filters.text, generateedittext)],
            EDIT: [MessageHandler(Filters.regex('OK'), editInChannel)],
            EDITPHOTO: [MessageHandler(Filters.photo, generatenewphoto)],
            EDITPHOTOPOST: [MessageHandler(Filters.regex('OK'), editPhotoInChannel)]
        },
        fallbacks=[CommandHandler('cancel', Fallback.cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Admin commands, on the main menu
    dispatcher.add_handler(CommandHandler('adminsoftreset', subfile.softReset))

    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()