import unittest
import json
from buspy.bots.dialogflow_handler import *

class GetUserStorageTests(unittest.TestCase):
    def setUp(self):
        self.req = {
            "originalDetectIntentRequest" : {
                "payload": {
                    "user": {
                        "userStorage": ""
                    }
                }
            }
        }

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