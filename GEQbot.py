import logging

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

#For Webhook
import os

#For auto-saving userdict
from thread2 import autoThread

#Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

import Fallback
from globals import (ACTION, GETTITLE, GETTEXT, GENERATETEXT, SENDING, POSTTOMANAGE, 
                    MANAGEPOST, DELETEPOST, EDITPREVIEW, EDIT, ASKFORPHOTO, EDITPHOTO, EDITPHOTOPOST, CHANGESTATUS,
                    DELETEPOSTCONFIRM, FEEDBACK, TOKEN)
import subfile
from Makepost import (
    start,
    newpost,
    gettitle,
    gettext,
    askforphoto,
    generatetext,
    sendToChannel,
    about,
    feedback,
    postfeedback
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
    PORT = int(os.environ.get('PORT', 5000))
    updater = Updater(token = TOKEN, use_context = True)
    dispatcher = updater.dispatcher

    thread2 = autoThread()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ACTION: [MessageHandler(Filters.regex('Make Post 📬'), newpost), 
                    MessageHandler(Filters.regex('Manage Posts 💼'), manageposts),
                    MessageHandler(Filters.regex('Help/About ❓'), about),
                    MessageHandler(Filters.regex('Give Feedback/Contact Us 📣'), feedback)],   

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
                           MessageHandler(Filters.regex('Withdraw Post ❌'), updatestatus)],
            FEEDBACK: [CommandHandler('cancel', Fallback.cancel), 
                       MessageHandler(Filters.text, postfeedback)]
        },
        fallbacks=[CommandHandler('cancel', Fallback.cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Admin commands
    dispatcher.add_handler(CommandHandler('softreset', subfile.softReset))
    dispatcher.add_handler(CommandHandler('save', subfile.save))
    dispatcher.add_handler(CommandHandler('read', subfile.read))
    dispatcher.add_handler(CommandHandler('checkcount', subfile.checkcount))
    dispatcher.add_handler(CommandHandler('resetcount', subfile.resetcount))

    subfile.unpickle_file()
    thread2.start()

    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://stormy-bayou-05179.herokuapp.com/' + TOKEN)
    updater.idle()



if __name__ == '__main__':
    main()