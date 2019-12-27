import logging
from telegram import Bot


class LogsHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)

        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def enamble_bot_logging(token, chat_id, logger):
    bot = Bot(token=token)

    logger.addHandler(LogsHandler(bot, chat_id))
