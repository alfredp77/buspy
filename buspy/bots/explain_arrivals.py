
def explain(arrival_result, message_code=0):
    if arrival_result.within_range:
        if message_code == 0:
            return f"Bus <text>{arrival_result.service_no}</text> will arrive at bus stop <text>{arrival_result.bus_stop_code}</text> in {arrival_result.within_range} minutes time"
        return f"You have to be at bus stop <text>{arrival_result.bus_stop_code}</text> in {arrival_result.within_range} minutes to catch bus <text>{arrival_result.service_no}</text>"

    if arrival_result.outside_range:
        if arrival_result.after_requested:
            return f"The next <text>{arrival_result.service_no}</text> will come in {arrival_result.outside_range} minutes time, and the one after that will come in {arrival_result.after_requested} minutes time, that's after your requested time"
        else:
            return f"The closest available <text>{arrival_result.service_no}</text> for your requested time will come in {arrival_result.outside_range} minutes time"

    
    if arrival_result.after_requested:
        return f"The only available <text>{arrival_result.service_no}</text> will come after your requested time, {arrival_result.after_requested} minutes from now"

    return None