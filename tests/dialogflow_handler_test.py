import unittest
import json
import copy
from buspy.bots.dialogflow_handler import *

req = {
            "queryResult": {
                "intent" : {
                    "displayName" : ""
                }
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