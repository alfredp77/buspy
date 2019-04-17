import requests
import json

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

print(get_arrival_time(67379, 372))
