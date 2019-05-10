# -*- coding: utf-8 -*-
from typing import Dict, Text, Any, List, Union

from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk import Tracker
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT

class GeneralForm(FormAction):

    def name(self):
        return "general_form"

    @staticmethod
    def required_slots(tracker):
        return ["nombre", "email"]

    def slot_mappings(self):
        return {"nombre": self.from_text(), "email": self.from_text()}

    def submit(self, dispatcher, tracker, domain):
        return []

class RestaurantForm(FormAction):

    def name(self):
        return "restaurant_form"

    @staticmethod
    def required_slots(tracker: Tracker):
        return ["cocina", "nro_personas", "patio_comidas", "preferencias", "feedback"]

    def slot_mappings(self):
        return {
            "cocina": self.from_entity(entity="cocina", not_intent="chitchat"),
            "nro_personas": [
                self.from_entity(
                    entity="nro_personas", intent=["inform", "request_restaurant"]
                ),
                self.from_entity(entity="number"),
            ],
            "patio_comidas": [
                self.from_entity(entity="asiento"),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "preferencias": [
                self.from_intent(intent="deny", value="no hay preferencias"),
                self.from_text(not_intent="affirm"),
            ],
            "feedback": [self.from_entity(entity="feedback"), self.from_text()],
        }

    @staticmethod
    def cocina_db():
        return [
            "caribeña",
            "china",
            "francesa",
            "griega",
            "india",
            "italiana",
            "mexicana"]

    @staticmethod
    def is_int(string: Text):
        try:
            int(string)
            return True
        except ValueError:
            return False

    def validate_cocina(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]):

        if value.lower() in self.cocina_db():
            return value
        else:
            dispatcher.utter_template("utter_wrong_cocina", tracker)
            return None

    def validate_nro_personas(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]):

        if self.is_int(value) and int(value) > 0:
            return value
        else:
            dispatcher.utter_template("utter_wrong_nro_personas", tracker)
            return None

    @staticmethod
    def validate_patio_comidas(
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]):

        if isinstance(value, str):
            if "out" in value:
                return True
            elif "in" in value:
                return False
            else:
                dispatcher.utter_template("utter_wrong_patio_comidas", tracker)
                return None

        else:
            return value

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]):

        dispatcher.utter_template("utter_submit", tracker)
        return []

