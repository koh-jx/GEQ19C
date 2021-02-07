from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)
from telegram.ext.conversationhandler import ConversationHandler
import subfile
# Fallback function: Conversation cancelled at any time with /start
#===========================================================



def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Process cancelled. /start to return to the main menu.', reply_markup=ReplyKeyboardRemove()
    )
    user_id = update.message.from_user.id
    if user_id in subfile.get_userdict().keys():
        subfile.get_userdict()[update.message.from_user.id].clearUnsentMessages()
    return ConversationHandler.END