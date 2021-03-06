"""
This is bot to check if contacting user is bot.
User can check if other user is bot or not.
If there is no data then you can request user to get validated
"""

import logging
import json
import time
import threading
from Model import (AddUser, CheckUser, AddQuery)

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
botName = ''

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    isBot = update.effective_user.is_bot
    status = AddUser(update.effective_user, update.effective_chat)

    if status:
        msg = f'Hi {update.effective_user.first_name}'
        msg += '\n'
        if isBot:
            msg += 'You are a bot'
        else:
            msg += 'You are not a bot'

        update.message.reply_text(msg)
    else:
        status = AddQuery(update.effective_user.id, update.effective_chat.id, update.message.text)
        if status:
            update.message.reply_text('Do not query multiple times')

def self_destruct_message(message):
    time.sleep(5)
    message.delete()

def checkin(update, context):
    """Send a message when the command /checkin is issued."""
    isBot = update.effective_user.is_bot
    status = AddUser(update.effective_user, update.effective_chat)

    if status:
        msg = f'Hi {update.effective_user.first_name}'
        msg += '\n'
        if not isBot:
            msg += 'Welcome to group'
        else:
            msg += 'Bots are not allowed to group'

        message = update.message.reply_text(msg+'\nmessage will be deleted in 5 seconds')
        x = threading.Thread(target=self_destruct_message, args=(message,))
        x.start()

    else:
        status = AddQuery(update.effective_user.id, update.effective_chat.id, update.message.text)
        if status:
            update.message.reply_text('Do not query multiple times')

def help(update, context):
    """Send a message when the command /help is issued."""
    msg = '/check <first name>'
    update.message.reply_text(msg)

def check(update, context):
    """Check if requested user is in database and set his status of he is bot or not"""
    message = update.message.text
    status = AddQuery(update.effective_user.id, update.effective_chat.id, message)
    if not status:
        return False

    message = message.replace('/check', '')
    messages = message.split()
    if len(messages) != 1:
        update.message.reply_text('Please use bot wisely.')
        return False

    firstname = messages[0].strip()
    if firstname:
        if  update.effective_chat.id == update.effective_user.id:
            chatID = None
        else:
            chatID = update.effective_chat.id

        status, isBot = CheckUser(firstname, chatID)
        if status:
            if isBot:
                msg = f'{firstname} is a bot'
            else:
                msg = f'{firstname} is not a bot'
        else:
            msg = f'{firstname} never contacted {botName}'
    else:
        msg = '/check <firstname>'
    update.message.reply_text(msg)

def echo(update, context):
    """Echo the user message."""
    message = update.message.text
    status = AddQuery(update.effective_user.id, update.effective_chat.id, message)
    if not status:
        return

    messages = message.split()
    if len(messages) != 1:
        update.message.reply_text('Please use bot wisely.')
        return False

    firstname = messages[0].strip()
    if firstname:
        if  update.effective_chat.id == update.effective_user.id:
            chatID = None
        else:
            chatID = update.effective_chat.id

        status, isBot = CheckUser(firstname, chatID)
        if status:
            if isBot:
                msg = f'{firstname} is a bot'
            else:
                msg = f'{firstname} is not a bot'
        else:
            msg = f'{firstname} never contacted {botName}'
    else:
        msg = '/check <first name>'
    update.message.reply_text(msg)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text('Fatal error please try again.')

def main(token):
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("check", check))
    dp.add_handler(CommandHandler("checkin", checkin))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

def ReadSecrets():
    """Function to read secrets from file"""
    # read file
    with open('secrets.secret', 'r') as secretsFile:
        data = secretsFile.read()

        # parse file
        obj = json.loads(data)

        # show values
        if _DEBUG:
            token = str(obj['TEST_TOKEN'])
        else:
            token = str(obj['TOKEN'])

        global botName
        botName = str(obj['BOT_NAME'])
        return token

_DEBUG = False

if __name__ == '__main__':
    token = ReadSecrets()
    main(token)
