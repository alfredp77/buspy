# to run some ad-hoc python scripts to run the actual thing:

from buspy.datamall_query import RequestSender, ArrivalFetcher
from buspy.incoming_bus_checker import IncomingBusChecker
import datetime
from buspy.datetime_helpers import set_minutes, now
import time


request_sender = RequestSender()
arrival_fetcher = ArrivalFetcher(request_sender)

requested_time = set_minutes(10).after(now())
print(requested_time.isoformat())

checker1 = IncomingBusChecker(67379, 50, requested_time, arrival_fetcher.get_arrival_time, 5)
checker2 = IncomingBusChecker(67379, 372, requested_time, arrival_fetcher.get_arrival_time, 5)

checkers = [checker1, checker2]
waiting = True
while waiting:
    time.sleep(5)
    print(f"{now().isoformat()} Checking if bus is coming ...")
    for checker in checkers:
        message = checker.check()
        if message:
            print(message)
            waiting = False
            break        