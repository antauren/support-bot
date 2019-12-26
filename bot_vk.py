import os
import random

from dotenv import load_dotenv

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType

from utils.dialogflow import detect_intent_text
from utils.bot_logger import make_bot_logger


def start_bot(token, project_id, logger, language_code='ru'):
    vk_session = VkApi(token=token)
    vk_session_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():

        if not (event.type == VkEventType.MESSAGE_NEW and event.to_me):
            continue

        try:
            response = detect_intent_text(project_id=project_id,
                                          session_id=event.user_id,
                                          text=event.text,
                                          language_code=language_code
                                          )
        except Exception as error:
            logger.exception(error)
            continue

        if response['is_fallback']:
            continue

        try:
            vk_session_api.messages.send(user_id=event.user_id,
                                         message=response['answer'],
                                         random_id=random.randint(1, 1000)
                                         )
        except Exception as error:
            logger.exception(error)
            continue


if __name__ == '__main__':
    load_dotenv()

    bot_logger = make_bot_logger(token=os.environ['TG_BOT_TOKEN'],
                                 chat_id=os.environ['TG_LOG_CHAT_ID']
                                 )

    start_bot(token=os.environ['VK_GROUP_TOKEN'],
              project_id=os.environ['DIALOGFLOW_PROJECT_ID'],
              logger=bot_logger
              )
