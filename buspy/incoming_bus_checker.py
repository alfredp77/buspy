import datetime
from datetime_helpers import now

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

    def check(self, current_time=None):
        arrival_times = self.arrival_getter(self.bus_stop_code, self.service_no)

        arrival_time = arrival_times[0]
        current_time = current_time or now()
        when = arrival_time - current_time
        delta = datetime.timedelta(minutes = self.range_minutes)
        if arrival_time >= self.requested_time - delta: 
            arrival_str = str(int(when.total_seconds()/60))
            return self.build_message([arrival_str])

        return None

    def timetobeinbusstop(self, current_time=None):
        arrival_times = self.arrival_getter(self.bus_stop_code, self.service_no)

        selected_arrival = None
        for arrival in arrival_times:            
            min = int((self.requested_time - arrival).total_seconds()/60)
            print(arrival, min)
            if min >= 2 and min < self.range_minutes + 2:
                if not selected_arrival or arrival > selected_arrival:
                    selected_arrival = arrival

        if selected_arrival:
            current_time = current_time or now()
            return int((selected_arrival - current_time).total_seconds()/60 - 2)

        return None

    def build_message(self, arrivals):
        return f"Bus {self.service_no} is coming in {', '.join(arrivals)} mins at bus stop {self.bus_stop_code}"

    def firstcheck(self, current_time=None):
        current_time = current_time or now() 

        if (self.requested_time - current_time).total_seconds() < self.range_minutes * 60:
            arrivals = self.arrival_getter(self.bus_stop_code, self.service_no)
            mins = [str(int((arrival - current_time).total_seconds()/60)) for arrival in arrivals]
            return self.build_message(mins)

        return None