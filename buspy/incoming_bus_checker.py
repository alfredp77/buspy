import datetime
from buspy.datetime_helpers import now

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

    def check(self, current_time=None):
        arrival_time = self.arrival_getter(self.bus_stop_code, self.service_no)

        current_time = current_time or now()
        when = arrival_time - current_time
        delta = datetime.timedelta(minutes = self.range_minutes)
        if arrival_time >= self.requested_time - delta: 
            return f"Bus {self.service_no} is coming in {int(when.total_seconds()/60)} mins at bus stop {self.bus_stop_code}"

        print(f"Next {self.service_no} is coming in {int(when.total_seconds()/60)} mins at bus stop {self.bus_stop_code}")
        return ""    