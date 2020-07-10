"""
This is bot to check if contacting user is bot.
User can check if other user is bot or not.
If there is no data then you can request user to get validated
"""

import logging
import json
from Model import (AddUser, CheckUser)

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
    status = AddUser(update.effective_user.username, isBot)
    if status:
        msg = f'Hi {update.effective_user.username}'
        msg += '\n'
        if isBot:
            msg += 'You are a bot'
        else:
            msg += 'You are not a bot'

        update.message.reply_text(msg)
    else:
        update.message.reply_text('Do not query multiple times')

def help(update, context):
    """Send a message when the command /help is issued."""
    msg = '/check <username>'
    update.message.reply_text(msg)

def check(update, context):
    """Check if requested user is in database and set his status of he is bot or not"""
    message = update.message.text
    message = message.replace('/check', '')
    messages = message.split()
    if messages != 1:
        update.message.reply_text('Please use bot wisely.')

    username = messages[0].strip()
    if username:
        status, isBot = CheckUser(username)
        if status:
            if isBot:
                msg = f'{username} is not a bot'
            else:
                msg = f'{username} is a bot'
        else:
            msg = f'{username} never contacted {botName}'
    else:
        msg = '/check <username>'
    update.message.reply_text(msg)

def echo(update, context):
    """Echo the user message."""
    message = update.message.text
    messages = message.split()
    if len(messages) != 1:
        update.message.reply_text('Please use bot wisely.')

    username = messages[0].strip()
    if username:
        status, isBot = CheckUser(username)
        if status:
            if isBot:
                msg = f'{username} is a bot'
            else:
                msg = f'{username} is not a bot'
        else:
            msg = f'{username} never contacted {botName}'
    else:
        msg = '/check <username>'
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

_DEBUG = True

if __name__ == '__main__':
    token = ReadSecrets()
    main(token)
