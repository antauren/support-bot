import os

from dotenv import dotenv_values

from bot_vk import start_bot

if __name__ == '__main__':
    dotenv_dict = dotenv_values()

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = dotenv_dict['GOOGLE_APPLICATION_CREDENTIALS']

    start_bot(
        token=dotenv_dict['VK_GROUP_TOKEN'],
        project_id=dotenv_dict['PROJECT_ID']
    )
