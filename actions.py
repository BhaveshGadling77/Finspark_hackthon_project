from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionAskLanguagePreference(Action):
    """Ask user for language preference if not set."""

    def name(self) -> Text:
        return "action_ask_language_preference"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        # Check if language is already set
        current_language = tracker.get_slot("language")
        
        if not current_language:
            dispatcher.utter_message(response="utter_ask_language")
            return []
        
        # Language already set, continue with greeting
        dispatcher.utter_message(response="utter_greet")
        return []


class ActionSetLanguage(Action):
    """Set user's language preference."""

    def name(self) -> Text:
        return "action_set_language"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        # Get language from entities
        language_entities = tracker.latest_message.get('entities', [])
        language = None
        
        # Extract language from entities
        for entity in language_entities:
            if entity.get('entity') == 'language':
                language = entity.get('value')
                break
        
        if language:
            print(f"Language set to: {language}")
            dispatcher.utter_message(response="utter_language_set")
            # Also greet the user after setting language
            dispatcher.utter_message(response="utter_greet")
            return [SlotSet("language", language)]
        
        # If no language entity found, ask again
        dispatcher.utter_message(response="utter_ask_language")
        return []
