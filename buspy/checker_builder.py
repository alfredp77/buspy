import json
import datetime
from incoming_bus_checker import IncomingBusChecker
from datamall_query import RequestSender, ArrivalFetcher
from datetime_helpers import gettime, now

request_sender = RequestSender()
arrival_fetcher = ArrivalFetcher(request_sender)

rel_path2="../buspy/data/bus_stops.json"
with open(rel_path2) as f:
    bus_stops = json.load(f)   

rel_path3="../buspy/data/bus_routes.json"
with open(rel_path3) as f:
    bus_routes = json.load(f)   

def build_checker(bus_stop_code,  service_no, requested_time_str, original_request_time_str, owner_id=None, code_formatter=None):
    formatted_bus_stop_code = (code_formatter and code_formatter(bus_stop_code)) or bus_stop_code
    formatted_service_no = (code_formatter and code_formatter(service_no)) or service_no
    if bus_stop_code not in bus_stops:
        return (None, f"I couldn't find your bus stop {formatted_bus_stop_code}. Please try again.")

    if f"{service_no}_{bus_stop_code}" not in bus_routes:
        return (None, f"I couldn't find your bus {formatted_service_no} at your bus stop {formatted_bus_stop_code}. Please try again.")
              
    try:
        requested_time = datetime.datetime.fromisoformat(requested_time_str)
    except:
        requested_time = None

    if not requested_time:
        return (None, f"I don't understand your time {requested_time_str}. Please try again.")

    if requested_time < now():
        return (None, f"Your time {original_request_time_str} is in the past. Please try again.")
  
    return (IncomingBusChecker(bus_stop_code, service_no, requested_time, arrival_fetcher.get_arrival_time, owner_id=owner_id), None)