import requests
import json
import datetime

base_url = 'http://datamall2.mytransport.sg/ltaodataservice/'
rel_path="../buspy/tokens.json"
with open(rel_path) as f:
    data = json.load(f)

def parse_arrival_data(res_json):
    arrival = res_json["Services"][0]["NextBus"]["EstimatedArrival"]
    return arrival

def get_arrival_time(bus_stop_code, service_no):    
    headers = {
        "AccountKey": data["lta"],
        "accept":"application/json"       
    }

    url = f"{base_url}BusArrivalv2?BusStopCode={bus_stop_code}&ServiceNo={service_no}"
    resp = requests.get(url , headers= headers )
    return parse_arrival_data(resp.json())

def check_bus_coming(bus_stop_code, service_no, requested_time_str):
    arrival_time = datetime.datetime.fromisoformat(get_arrival_time(bus_stop_code, service_no))
    requested_time = datetime.datetime.fromisoformat(requested_time_str)

    delta = datetime.timedelta(minutes = 10)
    if arrival_time < requested_time + delta and arrival_time >= requested_time - delta: 
        return "Bus is coming soon"

    return ""