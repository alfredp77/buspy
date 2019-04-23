from flask import Flask, Response, request
import json
from buspy.checker_builder import build_checker
from buspy.bots.explain_arrivals import explain

import datetime
import uuid

# TODO: ideally this dialogflow.py should be in the buspy.bots package

app = Flask(__name__)

@app.route("/", methods = ["POST"])
def main():
    req = request.get_json(silent=True, force=True)
    print(req)
    intent_name = req["queryResult"]["intent"]["displayName"]
    user_storage = get_user_storage(req)

    if intent_name == "GetBusArrivalTimeIntent":
        resp_text = handle_getBusArrivalTimeIntent(req)
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

    return Response(json.dumps(resp), status=200, content_type="application/json")

def get_user_storage(req):
    user_storage = req["originalDetectIntentRequest"]["payload"]["user"].get("userStorage", {})
    if type(user_storage) == str:
        user_storage = json.loads(user_storage)
    return user_storage

def handle_getBusArrivalTimeIntent(req):
    busno = req["queryResult"]["parameters"]["BusNo"]
    busstop = req["queryResult"]["parameters"]["BusStopNo"]
    departuretime_original = req["queryResult"]["outputContexts"][0]["parameters"]["DepartureTime.original"]
    departuretime = req["queryResult"]["parameters"]["DepartureTime"]
    
    checker, resp_text = build_checker(busstop, busno, departuretime, departuretime_original, code_formatter=lambda x:f'<say-as interpret-as="characters">{x}</say-as>')
    if checker:                                    
        result = checker.time_to_be_at_bus_stop()
        resp_text = explain(result)
        if resp_text:
            resp_text = resp_text.replace('<text>','<say-as interpret-as="characters">').replace('</text>','</say-as>')
        else:
            resp_text = "I cannot find bus arrival time near to your departure time. Please try again later"
    return resp_text

app.run(host='0.0.0.0', port=19191, debug=True)