# actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re

class ActionAskLanguagePreference(Action):
    """Ask user for language preference if not set (sends buttons programmatically)."""

    def name(self) -> Text:
        return "action_ask_language_preference"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        current_language = tracker.get_slot("language")

        if not current_language:
            text = (
                "Please choose your preferred language / "
                "कृपया अपनी भाषा चुनें / कृपया तुमची भाषा निवडा / "
                "దయచేసి మీ భాషను ఎంచుకోండి / ದಯವಿಟ್ಟು ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ:"
            )

            buttons = [
                {"title": "English", "payload": '/set_language{"language":"en"}'},
                {"title": "हिंदी", "payload": '/set_language{"language":"hi"}'},
                {"title": "मराठी", "payload": '/set_language{"language":"mr"}'},
                {"title": "తెలుగు", "payload": '/set_language{"language":"te"}'},
                {"title": "ಕನ್ನಡ", "payload": '/set_language{"language":"kn"}'},
            ]

            dispatcher.utter_message(text=text, buttons=buttons)
            return []

        dispatcher.utter_message(response="utter_greet")
        return []


class ActionSetLanguage(Action):
    """Set user's language preference. Accepts entity OR parses payload text from button click."""

    def name(self) -> Text:
        return "action_set_language"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # 1) Try entity extraction first
        language = None
        for entity in tracker.latest_message.get("entities", []):
            if entity.get("entity") == "language":
                language = entity.get("value")
                break

        # 2) If no entity, parse button payload text
        if not language:
            text = tracker.latest_message.get("text") or ""
            # pattern matches: /set_language{"language":"en"}
            m = re.search(r'/set_language\{\s*["\']?language["\']?\s*:\s*["\'](?P<lang>[a-z]{2})["\']\s*\}', text)
            if m:
                language = m.group("lang")
            else:
                # fallback for alternative payload style like /set_language_en
                m2 = re.search(r'/set_language[_\-](?P<lang>[a-z]{2})', text)
                if m2:
                    language = m2.group("lang")

        if language:
            print(f"Language set to: {language}")
            dispatcher.utter_message(response="utter_language_set")
            dispatcher.utter_message(response="utter_greet")
            return [SlotSet("language", language)]

        dispatcher.utter_message(response="utter_ask_language")
        return []
