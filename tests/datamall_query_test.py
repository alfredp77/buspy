import unittest
import buspy.datamall_query as query
import json

class DataMallQueryTests(unittest.TestCase):
    def test_should_be_able_to_parse_arrival_time(self):
        with open("./tests/responses/bus_arrival.json") as f:
            data = json.load(f)
        arrival = query.parse_arrival_data(data)
        self.assertEqual("2019-04-17T13:37:43+08:00", arrival)
        

if __name__ == '__main__':
    unittest.main()