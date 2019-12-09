import os
import logging

from dotenv import dotenv_values
from functools import partial

from bot_tg import start_bot, get_answer, error

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
    p_error = partial(error,
                      logger=logger,
                      chat_id=dotenv_dict['TELEGRAM_CHAT_ID']
                      )

    start_bot(token=dotenv_dict['TELEGRAM_TOKEN'],
              message_handler=p_get_answer,
              error_handler=p_error
              )
