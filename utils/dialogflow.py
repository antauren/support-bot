# https://gist.github.com/grepto/83c723a946a87cead07bbf9befbdd963

import dialogflow_v2 as dialogflow
from google.protobuf.json_format import MessageToDict


def get_intent(project_id: str, display_name: str) -> dict:
    client = dialogflow.IntentsClient()
    parent = client.project_agent_path(project_id)

    intents = client.list_intents(parent, intent_view=dialogflow.enums.IntentView.INTENT_VIEW_FULL)

    for intent in intents:
        if intent.display_name == display_name:
            return MessageToDict(intent, preserving_proto_field_name=True)


def delete_intent(project_id: str, display_name: str):
    client = dialogflow.IntentsClient()

    intent = get_intent(project_id, display_name)
    intent_id = intent['name'].split('/')[-1]

    intent_path = client.intent_path(project_id, intent_id)
    client.delete_intent(intent_path)


def create_intent(project_id: str, display_name: str, phrases: list, messages: list, parameters=None) -> dict:
    client = dialogflow.IntentsClient()
    parent = client.project_agent_path(project_id)

    training_phrases = [wrap_phrase_for_training(phrase) for phrase in phrases]
    training_messages = [wrap_message_for_training(message) for message in messages]

    intent_dict = {
        'display_name': display_name,
        'training_phrases': training_phrases,
        'parameters': parameters,
        'messages': training_messages
    }

    intent = client.create_intent(parent,
                                  intent_dict,
                                  intent_view=dialogflow.enums.IntentView.INTENT_VIEW_FULL)

    return MessageToDict(intent, preserving_proto_field_name=True)


def wrap_phrase_for_training(phrase: str) -> dict:
    return {'parts': [{'text': phrase}],
            'type': 'EXAMPLE'}


def wrap_message_for_training(message: str) -> dict:
    return {'text': {'text': [message]}}
