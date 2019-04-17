import unittest
import buspy.datamall_query as query
import json
from unittest.mock import MagicMock
import datetime

class DataMallQueryTests(unittest.TestCase):
    def test_should_be_able_to_parse_arrival_time(self):
        with open("./tests/responses/bus_arrival.json") as f:
            data = json.load(f)
        arrival = query.parse_arrival_data(data)
        self.assertEqual("2019-04-17T13:37:43+08:00", arrival)
        
    def test_magicmock(self):
        query.get_arrival_time = MagicMock(return_value="a mock")
        self.assertEqual("a mock", query.get_arrival_time(67379,372))

    def test_returns_no_bus_coming_when_bus_is_still_far(self):
        requested_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
        arrival_time = datetime.datetime.now() - datetime.timedelta(minutes=12)
        query.get_arrival_time = MagicMock(return_value=arrival_time.isoformat())
        result = query.check_bus_coming(67379, 372, requested_time.isoformat)
        self.assertEqual("", result)

    # def test_returns_bus_is_coming_when_its_within_10_mins(self):
    #     query.get_arrival_time = MagicMock(return_value="2019-04-17T13:37:43+08:00")
    #     result = query.check_bus_coming(67379, 372, "some time string")
    #     self.assertEqual("Bus is coming soon", result)
if __name__ == '__main__':
    unittest.main()