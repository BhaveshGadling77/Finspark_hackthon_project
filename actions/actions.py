# # actions.py
# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.events import SlotSet
# import re

# class ActionAskLanguagePreference(Action):
#     """Ask user for language preference if not set (sends buttons programmatically)."""

#     def name(self) -> Text:
#         return "action_ask_language_preference"

#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any]
#     ) -> List[Dict[Text, Any]]:

#         current_language = tracker.get_slot("language")

#         if not current_language:
#             text = (
#                 "Please choose your preferred language / "
#                 "कृपया अपनी भाषा चुनें / कृपया तुमची भाषा निवडा / "
#                 "దయచేసి మీ భాషను ఎంచుకోండి / ದಯವಿಟ್ಟು ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ:"
#             )

#             buttons = [
#                 {"title": "English", "payload": '/set_language{"language":"en"}'},
#                 {"title": "हिंदी", "payload": '/set_language{"language":"hi"}'},
#                 {"title": "मराठी", "payload": '/set_language{"language":"mr"}'},
#                 {"title": "తెలుగు", "payload": '/set_language{"language":"te"}'},
#                 {"title": "ಕನ್ನಡ", "payload": '/set_language{"language":"kn"}'},
#             ]

#             dispatcher.utter_message(text=text, buttons=buttons)
#             return []

#         dispatcher.utter_message(response="utter_greet")
#         return []


# # class ActionAskLanguagePreference(Action):
# #     """Ask user for language preference if not set (sends only text, no buttons)."""

# #     def name(self) -> Text:
# #         return "action_ask_language_preference"

# #     def run(
# #         self,
# #         dispatcher: CollectingDispatcher,
# #         tracker: Tracker,
# #         domain: Dict[Text, Any]
# #     ) -> List[Dict[Text, Any]]:

# #         current_language = tracker.get_slot("language")

# #         if not current_language:
# #             text = (
# #                 "Please choose your preferred language / "
# #                 "कृपया अपनी भाषा चुनें / कृपया तुमची भाषा निवडा / "
# #                 "దయచేసి మీ భాషను ఎంచుకోండి / ದಯವಿಟ್ಟು ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ:"
# #             )
# #             dispatcher.utter_message(text=text)
# #             return []

# #         dispatcher.utter_message(response="utter_greet")
# #         return []


# class ActionSetLanguage(Action):
#     """Set user's language preference. Accepts entity OR parses payload text from button click."""

#     def name(self) -> Text:
#         return "action_set_language"

#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any]
#     ) -> List[Dict[Text, Any]]:

#         # 1) Try entity extraction first
#         language = None
#         for entity in tracker.latest_message.get("entities", []):
#             if entity.get("entity") == "language":
#                 language = entity.get("value")
#                 break

#         # 2) If no entity, parse button payload text
#         if not language:
#             text = tracker.latest_message.get("text") or ""
#             # pattern matches: /set_language{"language":"en"}
#             m = re.search(r'/set_language\{\s*["\']?language["\']?\s*:\s*["\'](?P<lang>[a-z]{2})["\']\s*\}', text)
#             if m:
#                 language = m.group("lang")
#             else:
#                 # fallback for alternative payload style like /set_language_en
#                 m2 = re.search(r'/set_language[_\-](?P<lang>[a-z]{2})', text)
#                 if m2:
#                     language = m2.group("lang")

#         if language:
#             print(f"Language set to: {language}")
#             dispatcher.utter_message(response="utter_language_set")
#             dispatcher.utter_message(response="utter_greet")
#             return [SlotSet("language", language)]

#         dispatcher.utter_message(response="utter_ask_language")
#         return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re


class ActionAskLanguagePreference(Action):
    """Ask user for language preference if not set (sends only text, no buttons)."""

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
            dispatcher.utter_message(text=text)
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


class ActionGreet(Action):
    """Custom greeting action that considers language preference."""

    def name(self) -> Text:
        return "action_greet"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        current_language = tracker.get_slot("language")
        
        if current_language:
            # Language is set, send appropriate greeting
            dispatcher.utter_message(response="utter_greet")
        else:
            # No language set, ask for preference first
            dispatcher.utter_message(response="utter_ask_language")
        
        return []


class ActionProvideHelp(Action):
    """Provide help information based on user's language preference."""

    def name(self) -> Text:
        return "action_provide_help"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        current_language = tracker.get_slot("language")
        
        # Help messages in different languages
        help_messages = {
            "en": "I can help you with:\n• Account opening\n• Balance enquiry\n• ATM services\n• Internet banking\n• Mobile banking\n• Customer support",
            "hi": "मैं इनमें आपकी मदद कर सकता हूँ:\n• खाता खोलना\n• बैलेंस पूछताछ\n• एटीएम सेवाएं\n• इंटरनेट बैंकिंग\n• मोबाइल बैंकिंग\n• ग्राहक सहायता",
            "mr": "मी यामध्ये तुमची मदत करू शकतो:\n• खाते उघडणे\n• शिल्लक चौकशी\n• एटीएम सेवा\n• इंटरनेट बँकिंग\n• मोबाइल बँकिंग\n• ग्राहक सेवा",
            "te": "నేను వీటిలో మీకు సహాయం చేయగలను:\n• ఖాతా తెరవడం\n• బ్యాలెన్స్ విచారణ\n• ATM సేవలు\n• ఇంటర్నెట్ బ్యాంకింగ్\n• మొబైల్ బ్యాంకింగ్\n• కస్టమర్ మద్దతు",
            "kn": "ನಾನು ಇವುಗಳಲ್ಲಿ ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಲ್ಲೆ:\n• ಖಾತೆ ತೆರೆಯುವಿಕೆ\n• ಬ್ಯಾಲೆನ್ಸ್ ವಿಚಾರಣೆ\n• ATM ಸೇವೆಗಳು\n• ಇಂಟರ್ನೆಟ್ ಬ್ಯಾಂಕಿಂಗ್\n• ಮೊಬೈಲ್ ಬ್ಯಾಂಕಿಂಗ್\n• ಗ್ರಾಹಕ ಸಹಾಯ"
        }
        
        message = help_messages.get(current_language or "en", help_messages["en"])
        dispatcher.utter_message(text=message)
        
        return []