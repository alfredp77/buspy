import unittest
from unittest.mock import MagicMock
import datetime
from buspy.datetime_helpers import set_minutes, now
from buspy.incoming_bus_checker import IncomingBusChecker

class IncomingBusCheckerTests(unittest.TestCase):
    def setUp(self):
        self.now = now()

    def setup_arrival(self, arrival):
        return MagicMock(return_value=arrival)

    def test_check_returns_blank_when_next_bus_before_earliest_range(self):
        requested = set_minutes(30).after(self.now)
        arrival = set_minutes(16).before(requested)
        arrival_getter = self.setup_arrival(arrival)

        checker = IncomingBusChecker(67379, 372, requested, arrival_getter, 15)
        self.assertEqual("", checker.check(self.now))

    def test_check_returns_incoming_when_next_bus_after_latest_range(self):
        requested = set_minutes(30).after(self.now)
        arrival = set_minutes(16).after(requested)
        arrival_getter = self.setup_arrival(arrival)

        checker = IncomingBusChecker(67379, 372, requested, arrival_getter, 15)
        self.assertEqual('Bus 372 is coming in 46 mins at bus stop 67379', checker.check(self.now))

    def test_check_returns_incoming_when_next_bus_is_in_range_before_requested_time(self):
        requested = set_minutes(30).after(self.now)
        arrival = set_minutes(7).before(requested)
        arrival_getter = self.setup_arrival(arrival)

        checker = IncomingBusChecker(67379, 372, requested, arrival_getter, 15)
        self.assertEqual('Bus 372 is coming in 23 mins at bus stop 67379', checker.check(self.now))

    def test_check_returns_incoming_when_next_bus_is_after_requested_time(self):
        requested = set_minutes(30).after(self.now)
        arrival = set_minutes(3).after(requested)
        arrival_getter = self.setup_arrival(arrival)

        checker = IncomingBusChecker(67379, 372, requested, arrival_getter, 15)
        self.assertEqual('Bus 372 is coming in 33 mins at bus stop 67379', checker.check(self.now))

if __name__ == '__main__':
    unittest.main()