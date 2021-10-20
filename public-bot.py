#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

#my imports
import os
import time

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# my functions and variables 
start_time=0

if(os.path.isfile("time_store")): 
    f2= open("time_store","r")
    start_time=f2.read()
    print( " Start time retrieved : "+start_time)
    start_time=float(start_time)
    f2.close()
else:
    pass    

def storetime():
    file1 = open("time_store","w")
    file1.write(str(start_time))
    file1.close()


def time_string(t_secs):
    time = float(t_secs)
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    return("\n   %.2d Days\n   %.2d Hours\n   %.2d Minutes\n   %.2d Seconds" % (day, hour, minutes, seconds))

def start_streak(update,context):
    global start_time
    start_time=time.time()
    context.bot.send_message(chat_id=update.effective_chat.id, text=" Streak started successfully . . .")
    storetime()
    
def stop_streak(update,context):
    global start_time
    if start_time==0:
        context.bot.send_message(chat_id=update.effective_chat.id, text=" Streak has not been started yet .")
        return 
    get_streak(update, context);
    context.bot.send_message(chat_id=update.effective_chat.id, text=" Streak stopped successfully . . .")
    start_time=0
    storetime()
    
def reset_streak(update,context):
    global start_time
    if start_time==0:
        context.bot.send_message(chat_id=update.effective_chat.id, text=" Streak has not been started yet .")
        return 
    get_streak(update, context);
    context.bot.send_message(chat_id=update.effective_chat.id, text=" Streak reset successfully . . .")
    start_time=time.time()
    storetime()

def get_streak(update,context):
    global start_time
    if start_time==0:
        context.bot.send_message(chat_id=update.effective_chat.id, text=" Streak has not been started yet .")
        return 
    streaktime=time.time()-start_time
    print(" Streak in seconds : ",streaktime)
    context.bot.send_message(chat_id=update.effective_chat.id, text="  Streak : "+time_string(streaktime),parse_mode=ParseMode.HTML)
    storetime()


#my functions and variables section ends

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    storetime()    

    

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("streak",get_streak ))
    dp.add_handler(CommandHandler("startstreak",start_streak ))
    dp.add_handler(CommandHandler("stopstreak",stop_streak ))
    dp.add_handler(CommandHandler("resetstreak",reset_streak ))


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


if __name__ == '__main__':
    main()