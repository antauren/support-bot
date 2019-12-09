import os
import logging

from functools import partial
from dotenv import dotenv_values

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from utils.dialogflow import detect_intent_text


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    '''Send a message when the command /start is issued.'''
    update.message.reply_text('Здравствуйте')


def help(bot, update):
    '''Send a message when the command /help is issued.'''
    update.message.reply_text('Help!')


def error(bot, update, error, logger):
    '''Log Errors caused by Updates.'''
    logger.warning('Update "%s" caused error "%s"', update, error)


def get_answer(bot, update, project_id, language_code):
    response = detect_intent_text(project_id=project_id,
                                  session_id=update.message.chat_id,
                                  text=update.message.text,
                                  language_code=language_code)

    update.message.reply_text(response['answer'])


def start_bot(token, message_handler, error_handler):
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(MessageHandler(Filters.text, message_handler))

    # log all errors
    dp.add_error_handler(error_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    dotenv_dict = dotenv_values()

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = dotenv_dict['GOOGLE_APPLICATION_CREDENTIALS']

    p_get_answer = partial(get_answer,
                           project_id=dotenv_dict['PROJECT_ID'],
                           language_code='ru'
                           )

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO
                        )
    logger = logging.getLogger(__name__)
    p_error = partial(error, logger=logger)

    start_bot(token=dotenv_dict['TELEGRAM_TOKEN'],
              message_handler=p_get_answer,
              error_handler=p_error)
