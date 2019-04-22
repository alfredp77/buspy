import datetime
from buspy.datetime_helpers import now, diff_in_minutes

class ArrivalResult:
    def __init__(self, bus_stop_code, service_no, within_range, outside_range=None, 
                after_requested=None,
                no_more=None,
                outside_range_may_be_acceptable=False):
        self.bus_stop_code = bus_stop_code
        self.service_no = service_no
        self.within_range = within_range
        self.outside_range = outside_range
        self.after_requested = after_requested
        self.no_more = no_more
        self.outside_range_may_be_acceptable = outside_range_may_be_acceptable

    def is_blank(self):
        return not self.within_range and not self.outside_range and not self.after_requested

class IncomingBusChecker:
    def __init__(self, bus_stop_code, service_no, requested_time, 
                arrival_getter,
                range_minutes=10, owner_id=None):
        self.bus_stop_code = bus_stop_code
        self.service_no = service_no
        self.requested_time = requested_time
        self.range_minutes = range_minutes
        self.arrival_getter = arrival_getter
        self.owner_id = owner_id

    def expired(self, current_time=None):
        current_time = current_time or now()
        return self.requested_time < current_time

    def time_to_be_at_bus_stop(self, current_time=None):
        print("Getting bus arrivals...")
        arrival_times = self.arrival_getter(self.bus_stop_code, self.service_no)

        # TODO: must check first bus and last bus on the bus stop

        arrival_within_range = None
        arrival_after_requested = None
        arrival_outside_range = None
        mins_within_range = None
        mins_after_requested = None
        mins_outside_range = None
        current_time = current_time or now()

        for arrival in arrival_times:            
            min = diff_in_minutes(arrival, self.requested_time)
            if min < self.range_minutes:
                if min >= 0:
                    if not arrival_within_range or arrival > arrival_within_range:
                        arrival_within_range = arrival
                        mins_within_range = diff_in_minutes(current_time, arrival)
                else:
                    if not arrival_after_requested or arrival < arrival_after_requested:
                        arrival_after_requested = arrival
                        mins_after_requested = diff_in_minutes(current_time, arrival)
            else:
                arrival_outside_range = arrival
                mins_outside_range = diff_in_minutes(current_time, arrival)

        print("arrival_within_range : ", arrival_within_range)
        print("arrival_after_requested : ", arrival_after_requested)
        print("arrival_outside_range : ", arrival_outside_range)       

        return ArrivalResult(
            self.bus_stop_code,
            self.service_no,
            mins_within_range, 
            mins_outside_range, 
            mins_after_requested,
            no_more=len(arrival_times)<=1,
            outside_range_may_be_acceptable=arrival_outside_range and diff_in_minutes(arrival_outside_range, self.requested_time)<self.range_minutes+5)