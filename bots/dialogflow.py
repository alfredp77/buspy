from flask import Flask, Response, request
import json
from buspy.incoming_bus_checker import IncomingBusChecker
from buspy.checker_builder import build_checker
from buspy.datamall_query import RequestSender, ArrivalFetcher
from bots.explain_arrivals import explain

import datetime

request_sender = RequestSender()
arrival_fetcher = ArrivalFetcher(request_sender)

app = Flask(__name__)

@app.route("/", methods = ["POST"])
def main():
    
    req = request.get_json(silent=True, force=True)
    print(req)
    intent_name = req["queryResult"]["intent"]["displayName"]

    if intent_name == "GetBusArrivalTimeIntent":
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
    else:
        resp_text = "Unable to find a matching intent. Try again."

    resp = {
        "fulfillmentText": f"<speak>{resp_text}</speak>"
    }

    return Response(json.dumps(resp), status=200, content_type="application/json")

app.run(host='0.0.0.0', port=5000, debug=True)