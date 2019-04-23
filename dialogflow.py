from flask import Flask, Response, request
import json
from buspy.bots.dialogflow_handler import handle_request, handle_getBusArrivalTimeIntent

app = Flask(__name__)

@app.route("/", methods = ["POST"])
def main():
    req = request.get_json(silent=True, force=True)
    resp = handle_request(req, GetBusArrivalTimeIntent=handle_getBusArrivalTimeIntent)
    return Response(json.dumps(resp), status=200, content_type="application/json")


app.run(host='0.0.0.0', port=19191, debug=True)