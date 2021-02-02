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
                    MANAGEPOST, DELETEPOST, EDITPREVIEW, EDIT, ASKFORPHOTO, EDITPHOTO, EDITPHOTOPOST, CHANGESTATUS,
                    DELETEPOSTCONFIRM, TOKEN)
import subfile
from Makepost import (
    start,
    newpost,
    gettitle,
    gettext,
    askforphoto,
    generatetext,
    sendToChannel,
    about
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
    deletepost,
    statuschange,
    updatestatus,
    deletepostreason
)

def main():
    updater = Updater(token = TOKEN, use_context = True)
    dispatcher = updater.dispatcher
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ACTION: [MessageHandler(Filters.regex('Make Post 📬'), newpost), 
                    MessageHandler(Filters.regex('Manage Posts 💼'), manageposts),
                    MessageHandler(Filters.regex('Help/About ❓'), about)],   

            GETTITLE: [CommandHandler('cancel', Fallback.cancel), 
                       MessageHandler(Filters.regex('Put up item ✉️'), gettitle), 
                       MessageHandler(Filters.regex('Share item 🤝'), gettitle),
                       MessageHandler(Filters.regex('Look for item 👀'), gettitle),
                       MessageHandler(Filters.text, newpost)],

            GETTEXT: [CommandHandler('cancel', Fallback.cancel), 
                      MessageHandler(Filters.text, gettext)],

            ASKFORPHOTO: [CommandHandler('cancel', Fallback.cancel), 
                          MessageHandler(Filters.text, askforphoto)],
                          
            GENERATETEXT: [CommandHandler('skip', generatetext), 
                          MessageHandler(Filters.photo, generatetext)],

            SENDING: [MessageHandler(Filters.regex('OK'), sendToChannel), 
                     CommandHandler('text', gettext),
                     CommandHandler('title', gettitle), 
                     CommandHandler('type', newpost)],

            POSTTOMANAGE: [MessageHandler(Filters.regex(r'\d+'), checkpost)],

            MANAGEPOST: [MessageHandler(Filters.regex('Edit 📝'), getedittext), 
                         MessageHandler(Filters.regex('Delete 🛑'), deletepostreason),
                         MessageHandler(Filters.regex('Change Photo 🖼️'), editphoto),
                         MessageHandler(Filters.regex('Change Status ✔️❌'), statuschange),
                         MessageHandler(Filters.regex('Return to posts 🔙'), manageposts)],

            DELETEPOSTCONFIRM: [CommandHandler('cancel', Fallback.cancel), 
                          MessageHandler(Filters.text, deletepostconfirmation)],

            DELETEPOST: [MessageHandler(Filters.regex('OK'), deletepost)],

            EDITPREVIEW: [CommandHandler('cancel', Fallback.cancel), 
                         MessageHandler(Filters.text, generateedittext)],

            EDIT: [MessageHandler(Filters.regex('OK'), editInChannel)],

            EDITPHOTO: [MessageHandler(Filters.photo, generatenewphoto)],

            EDITPHOTOPOST: [MessageHandler(Filters.regex('OK'), editPhotoInChannel)],
            
            CHANGESTATUS: [MessageHandler(Filters.regex('Return to post 🔙'), checkpost),
                           MessageHandler(Filters.regex('My item is taken ✔️'), updatestatus),
                           MessageHandler(Filters.regex('It is currently loaned ✔️'), updatestatus),
                           MessageHandler(Filters.regex('I found my item ✔️'), updatestatus),
                           MessageHandler(Filters.regex('Put the post back up'), updatestatus),
                           MessageHandler(Filters.regex('The item has been returned ✔️'), updatestatus),
                           MessageHandler(Filters.regex('Withdraw Post ❌'), updatestatus)]
        },
        fallbacks=[CommandHandler('cancel', Fallback.cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Admin commands
    dispatcher.add_handler(CommandHandler('adminsoftreset', subfile.softReset))

    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()