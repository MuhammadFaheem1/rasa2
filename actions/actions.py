# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"


from codecs import utf_32_encode
from encodings import utf_8
from typing import Any, Text, Dict, List

import rasa.core.tracker_store
from rasa.shared.core.trackers import DialogueStateTracker, Restarted
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime
from datetime import datetime

class ActionSaveConversation(Action):
    
    def name(self) -> Text:
        return "action_save_conversation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        conversation=tracker.events
        print(conversation)
        import os
        if not os.path.isfile('chats.csv'):
            with open('chats.csv','w', encoding="utf-8") as file:
                file.write("intent,user_input,entity_name,entity_value,action,bot_reply\n")
        chat_data='\n'
        for i in conversation:

            if i['event'] == 'user':
                chat_data+= '\n' + i['parse_data']['intent']['name']+','+i['text']
                print('user: {}'.format(i['text']))
                if len(i['parse_data']['entities']) > 0:
                    chat_data+= i['parse_data']['entities'][0]['entity']+','+i['parse_data']['entities'][0]['value']+'__'
                    print('extra data:', i['parse_data']['entities'][0]['entity'], '=', i['parse_data']['entities'][0]['value'])
                else:
                    chat_data+="__"
            elif i['event'] == 'bot':
                print('Bot: {}'.format(i['text']))
                try:
                    chat_data+= '-->' + i['metadata']['utter_action']
                except KeyError:
                    pass
        else:
            with open('chats.csv','a', encoding="utf-8") as file:
                file.write(dt_string)
                file.write(chat_data)
        return []

class ActionRestarted(Action):

    def name(self):
        return "action_restart"

    def run(self, dispatcher, tracker, domain):
        return [Restarted()]