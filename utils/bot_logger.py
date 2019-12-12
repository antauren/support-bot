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


def make_bot_logger(token, chat_id):
    bot = Bot(token=token)

    logger = logging.getLogger('Bot-logger')
    logger.setLevel(logging.INFO)

    logger.addHandler(LogsHandler(bot, chat_id))

    return logger
