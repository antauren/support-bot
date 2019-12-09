import os
import random

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType

from utils.dialogflow import detect_intent_text
from dotenv import dotenv_values, load_dotenv


def start_bot(token, project_id, language_code='ru'):
    vk_session = VkApi(token=token)
    vk_session_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():

        if not (event.type == VkEventType.MESSAGE_NEW and event.to_me):
            continue

        response = detect_intent_text(project_id=project_id,
                                      session_id=event.user_id,
                                      text=event.text,
                                      language_code=language_code
                                      )

        if response['display_name'] == 'Default Fallback Intent':
            continue

        vk_session_api.messages.send(user_id=event.user_id,
                                     message=response['answer'],
                                     random_id=random.randint(1, 1000)
                                     )


if __name__ == '__main__':
    dotenv_dict = dotenv_values()
    load_dotenv()

    start_bot(
        token=os.environ['VK_GROUP_TOKEN'],
        project_id=os.environ['PROJECT_ID']
    )
