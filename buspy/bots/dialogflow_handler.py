import json
import uuid
from buspy.bots.explain_arrivals import explain
from buspy.checker_builder import build_checker

def get_user_storage(req):
    user_storage = req["originalDetectIntentRequest"]["payload"]["user"].get("userStorage", {})
    if type(user_storage) == str:
        user_storage = json.loads(user_storage)
    return user_storage

def get_user_id(user_storage):
    user_id = user_storage.get("userId")
    if not user_id:
        user_id = str(uuid.uuid4())
        user_storage["userId"] = user_id
    return user_id

def handle_request(req, **kwargs):
    intent_name = req["queryResult"]["intent"]["displayName"]
    user_storage = get_user_storage(req)
    user_id = get_user_id(user_storage)

    intent_handler = kwargs.get(intent_name)
    if intent_handler:
        resp_text = intent_handler(req, user_id)
    else:
        resp_text = "Unable to find a matching intent. Try again."

    resp = {
        "fulfillmentText": f"<speak>{resp_text}</speak>",
        "payload": {
            "google": {
                "userStorage": user_storage
            }
        }
    }

    return resp

def handle_getBusArrivalTimeIntent(req, user_id, checker_factory=build_checker, explainer=explain):
    busno = req["queryResult"]["parameters"]["BusNo"]
    busstop = req["queryResult"]["parameters"]["BusStopNo"]
    departuretime_original = req["queryResult"]["outputContexts"][0]["parameters"]["DepartureTime.original"]
    departuretime = req["queryResult"]["parameters"]["DepartureTime"]
    
    checker, resp_text = checker_factory(busstop, busno, departuretime, departuretime_original)
    if checker:                                    
        result = checker.time_to_be_at_bus_stop()
        resp_text = explainer(result)

    if resp_text:
        resp_text = resp_text.replace('<text>','<say-as interpret-as="characters">').replace('</text>','</say-as>')
    else:
        resp_text = "I cannot find bus arrival time near to your departure time. Please try again later"
    return resp_text