import os
import json
from dotenv import load_dotenv

from tqdm import tqdm

from utils.dialogflow import create_intent, get_intent, delete_intent


def load_json(path) -> dict:
    with open(path, encoding='utf-8') as fd:
        return json.load(fd)


if __name__ == '__main__':

    load_dotenv()

    project_id = os.environ['DF_PROJECT_ID']
    path = os.environ['INTENTS_DATA_PATH']

    intents_data = load_json(path)

    for display_name, intent_dict in tqdm(intents_data.items(), desc='training'):

        intent = get_intent(project_id, display_name)
        if intent:
            delete_intent(project_id, display_name)

        create_intent(project_id,
                      display_name,
                      phrases=intent_dict['questions'],
                      messages=[intent_dict['answer']],
                      parameters=[]
                      )
