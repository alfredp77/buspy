from flask import Flask, Response, request
import json
from incoming_bus_checker import IncomingBusChecker
from checker_builder import build_checker
from datamall_query import RequestSender, ArrivalFetcher
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
        
        checker, resp_text = build_checker(busstop, busno, departuretime, departuretime_original)
        if checker:            
            mins = checker.timetobeinbusstop()
            if mins:
                resp_text = f"You have to be in bus stop in {mins} minutes"
            else:
                resp_text = "I cannot find bus arrival time near to your departure time. Please try again later"
    else:
        resp_text = "Unable to find a matching intent. Try again."

    resp = {
        "fulfillmentText": resp_text
    }

    return Response(json.dumps(resp), status=200, content_type="application/json")

app.run(host='0.0.0.0', port=5000, debug=True)