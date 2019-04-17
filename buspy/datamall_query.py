base_url = 'http://datamall2.mytransport.sg/ltaodataservice/'


def get_arrival_time(bus_stop_code):
    url = f"{base_url}BusArrivalv2?BusStopCode="
    return bus_stop_no

def parse_arrival_data(res_json):
    arrival = res_json["Services"][0]["NextBus"]["EstimatedArrival"]
    return arrival