import requests
import json
import datetime

base_url = 'http://datamall2.mytransport.sg/ltaodataservice'
rel_path="../buspy/tokens.json"
with open(rel_path) as f:
    tokens = json.load(f)
headers = {
    "AccountKey": tokens["lta"],
    "accept":"application/json"       
}

def build_full_path(path):
    return f"{base_url}/{path}"

class RequestSender:
    def __init__(self, getter=None):
        self.getter = getter if getter else requests.get

    def send(self, path):
        url = build_full_path(path)
        resp = self.getter(url, headers=headers)
        return resp.json()


class ArrivalFetcher:
    def __init__(self, sender):
        self.sender = sender

    def parse_arrival_data(self, res_json):
        arrival = res_json["Services"][0]["NextBus"]["EstimatedArrival"]
        arrival2 = res_json["Services"][0]["NextBus2"]["EstimatedArrival"]
        arrival3 = res_json["Services"][0]["NextBus3"]["EstimatedArrival"]
        result = []
        for arrival_str in [arrival, arrival2, arrival3]:
            try:
                arrival_time = datetime.datetime.fromisoformat(arrival_str)
                result.append(arrival_time)
            except:
                pass
        return result
        
    def build_arrival_time_path(self, bus_stop_code, service_no):
        return f"/BusArrivalv2?BusStopCode={bus_stop_code}&ServiceNo={service_no}"

    def get_arrival_time(self, bus_stop_code, service_no):    
        path = self.build_arrival_time_path(bus_stop_code, service_no)
        json_response = self.sender.send(path)
        return self.parse_arrival_data(json_response)