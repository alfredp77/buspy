import unittest
from unittest.mock import MagicMock
import json
import copy
from buspy.bots.dialogflow_handler import *

req = {
            "queryResult": {
                "intent" : {
                    "displayName" : ""
                },
                "parameters": {
                    "BusNo": "",
                    "BusStopNo": "",
                    "DepartureTime": None
                },
                "outputContexts": [
                    {
                        "parameters" : {
                            "DepartureTime.original": ""
                        }
                    }
                ]
            },
            "originalDetectIntentRequest" : {
                "payload": {
                    "user": {
                        "userStorage": ""
                    }
                }
            }
}

class GetUserStorageTests(unittest.TestCase):
    def setUp(self):
        self.req = copy.deepcopy(req)

    def test_returns_blank_dictionary_when_user_storage_does_not_exist(self):
        self.req["originalDetectIntentRequest"]["payload"]["user"].pop("userStorage")
        self.assertEqual({}, get_user_storage(self.req))

    def test_returns_existing_dictionary_when_user_storage_exists(self):
        d = { "userId": "abc" }
        self.req["originalDetectIntentRequest"]["payload"]["user"]["userStorage"] = d
        self.assertEqual(d, get_user_storage(self.req))

    def test_returns_json_when_user_storage_is_string(self):
        d = { "userId": "abc"}
        json_string = json.dumps(d)
        self.req["originalDetectIntentRequest"]["payload"]["user"]["userStorage"] = json_string
        self.assertEqual(d, get_user_storage(self.req))

class GetUserIdTests(unittest.TestCase):
    def test_returns_new_user_id_when_user_storage_is_empty(self):
        storage = {}
        user_id = get_user_id(storage)
        self.assertIsNotNone(user_id)
        self.assertGreater(len(user_id), 0)
        self.assertEqual(user_id, storage.get("userId"))

    def test_returns_existing_user_id_when_user_storage_has_it(self):
        storage = {"userId":"blah"}
        user_id = get_user_id(storage)
        self.assertEqual("blah", user_id)
        self.assertEqual("blah", storage.get("userId"))

class HandleRequestTests(unittest.TestCase):
    def setUp(self):
        self.intent_name = "TestIntent"
        self.user_storage = { "userId": "abc" }
        self.req = copy.deepcopy(req)
        self.req["queryResult"]["intent"]["displayName"] = self.intent_name
        self.req["originalDetectIntentRequest"]["payload"]["user"]["userStorage"] = self.user_storage

    def build_expected_result(self, text, storage):
        return (text, storage)

    def test_returns_unable_to_find_intent_when_no_intent_handler_found(self):
        text, storage = handle_request(self.req, response_builder=self.build_expected_result, blah=lambda x: "test")
        self.assertEqual("Unable to find a matching intent. Try again.", text)
        self.assertEqual(storage, self.user_storage)

    def test_returns_text_from_specified_intent(self):
        self.passed_req = None
        self.passed_user_id = None

        def intent_handler(req_arg, user_id_arg):
            self.passed_req = req_arg
            self.passed_user_id = user_id_arg
            return "from intent handler"

        text, storage = handle_request(self.req, response_builder=self.build_expected_result, TestIntent=intent_handler)
        self.assertEqual("from intent handler", text)
        self.assertEqual(self.user_storage, storage)
        self.assertEqual(self.req, self.passed_req)
        self.assertEqual(self.user_storage["userId"], self.passed_user_id)


class HandleGetBusArrivalTimeIntentTests(unittest.TestCase):
    def setUp(self):
        self.checker = MagicMock()
        self.req = copy.deepcopy(req)
        self.busstop = '12345'
        self.busno = '333'
        self.departuretime = '2019-04-19T09:00:00+08:00'
        self.departuretime_original = '9am'

        parameters = self.req["queryResult"]["parameters"]
        parameters["BusNo"] = self.busno
        parameters["BusStopNo"] = self.busstop
        self.req["queryResult"]["outputContexts"][0]["parameters"]["DepartureTime.original"] = self.departuretime_original
        parameters["DepartureTime"] = self.departuretime

    def create_checker_factory(self, checker, text=None):
        return MagicMock(return_value=(checker, text))
    
    def create_explainer(self, result):
        return MagicMock(return_value=result)

    def test_should_return_text_from_checker(self):
        checker_factory = self.create_checker_factory(self.checker)
        self.checker.time_to_be_at_bus_stop = MagicMock(return_value="response")
        explainer = self.create_explainer('response explained')

        resp_text = handle_getBusArrivalTimeIntent(self.req, 'blah', checker_factory, explainer)

        self.assertEqual('response explained', resp_text)
        checker_factory.assert_called_once_with(self.busstop, self.busno, self.departuretime, self.departuretime_original)
        explainer.assert_called_once_with('response')

    def test_should_return_text_from_checker_factory_when_checker_is_none(self):
        checker_factory = self.create_checker_factory(checker=None, text="hello")
        
        resp_text = handle_getBusArrivalTimeIntent(self.req, 'blah', checker_factory, None)

        self.assertEqual('hello', resp_text)

    def assert_unable_to_find_arrival(self, text):
        self.assertEqual('I cannot find bus arrival time near to your departure time. Please try again later', text)

    def test_should_return_unable_to_find_when_text_from_checker_factory_is_none(self):
        checker_factory = self.create_checker_factory(checker=None, text=None)
        
        resp_text = handle_getBusArrivalTimeIntent(self.req, 'blah', checker_factory, None)

        self.assert_unable_to_find_arrival(resp_text)

    def test_should_return_unable_to_find_when_explainer_returns_blank_text(self):
        checker_factory = self.create_checker_factory(self.checker)
        self.checker.time_to_be_at_bus_stop = MagicMock(return_value="response")
        explainer = self.create_explainer(None)

        resp_text = handle_getBusArrivalTimeIntent(self.req, 'blah', checker_factory, explainer)

        self.assert_unable_to_find_arrival(resp_text)
        checker_factory.assert_called_once_with(self.busstop, self.busno, self.departuretime, self.departuretime_original)
        explainer.assert_called_once_with('response')

    def test_should_replace_text_tags(self):
        checker_factory = self.create_checker_factory(self.checker)
        self.checker.time_to_be_at_bus_stop = MagicMock(return_value="response")
        explainer = self.create_explainer('response <text>explained</text>')

        resp_text = handle_getBusArrivalTimeIntent(self.req, 'blah', checker_factory, explainer)

        self.assertEqual('response <say-as interpret-as="characters">explained</say-as>', resp_text)

