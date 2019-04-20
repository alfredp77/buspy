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

    def setup_checker(self, requested, range, *arrivals):
        arrival_getter = MagicMock(return_value=list(arrivals))
        return IncomingBusChecker(67379, 372, requested, arrival_getter, range)
     
    def test_time_at_bus_stop_should_return_no_more_when_only_one_arrival_is_available(self):
        requested = set_minutes(10).after(self.now)
        arrival1 = set_minutes(4).after(self.now)

        checker = self.setup_checker(requested, 10, arrival1)
        result = checker.time_to_be_at_bus_stop(self.now)

        self.assertEqual(True, result.no_more)

    def test_time_at_bus_stop_should_return_all_possible_times(self):
        requested = set_minutes(15).after(self.now)
        arrival1 = set_minutes(3).after(self.now)
        arrival2 = set_minutes(7).after(self.now)
        arrival3 = set_minutes(17).after(self.now)
        
        checker = self.setup_checker(requested, 10, arrival1, arrival2, arrival3)
        result = checker.time_to_be_at_bus_stop(self.now)

        self.assertEqual(7, result.within_range)
        self.assertEqual(3, result.outside_range)
        self.assertEqual(17, result.after_requested)

    def test_time_at_bus_stop_should_return_the_closest_one_to_requested_time(self):
        requested = set_minutes(15).after(self.now)
        arrival1 = set_minutes(6).after(self.now)
        arrival2 = set_minutes(11).after(self.now)

        checker = self.setup_checker(requested, 10, arrival1, arrival2)
        result = checker.time_to_be_at_bus_stop(self.now)

        self.assertEqual(11, result.within_range)
        self.assertIsNone(result.outside_range)
        self.assertIsNone(result.after_requested)

    def test_time_at_bus_stop_should_consider_earliest_after_requested_time(self):
        requested = set_minutes(15).after(self.now)
        arrival1 = set_minutes(16).after(self.now)
        arrival2 = set_minutes(18).after(self.now)

        checker = self.setup_checker(requested, 10, arrival1, arrival2)
        result = checker.time_to_be_at_bus_stop(self.now)

        self.assertIsNone(result.within_range)
        self.assertIsNone(result.outside_range)
        self.assertEqual(16, result.after_requested)

    def test_time_at_bus_stop_should_take_outside_range_time_closest_to_requested_time(self):
        requested = set_minutes(15).after(self.now)
        arrival1 = set_minutes(2).after(self.now)
        arrival2 = set_minutes(4).after(self.now)

        checker = self.setup_checker(requested, 10, arrival1, arrival2)
        result = checker.time_to_be_at_bus_stop(self.now)

        self.assertIsNone(result.within_range)
        self.assertEqual(4, result.outside_range)
        self.assertIsNone(result.after_requested)


if __name__ == '__main__':
    unittest.main()