import unittest
import buspy.datamall_query as query
from buspy.datamall_query import RequestSender
from buspy.datamall_query import ArrivalFetcher
import json
from unittest.mock import MagicMock
import datetime
from buspy.datetime_helpers import set_minutes
import requests

def load_arrival_test_data():
    with open("./tests/responses/bus_arrival.json") as f:
        return json.load(f)

class RequestSenderTests(unittest.TestCase):
    def test_send_request_should_return_json(self):  
        data = load_arrival_test_data()      
        mock_response = MagicMock()
        mock_response.json.return_value=data
        mock_get_method = MagicMock(return_value=mock_response)
        request_sender = RequestSender(mock_get_method)

        request_path = "rest/api/path"
        result = request_sender.send(request_path)

        self.assertEqual(data, result)
        mock_get_method.assert_called_once_with(query.build_full_path(request_path), headers=query.headers)


class ArrivalFetcherTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._data = load_arrival_test_data()
    
    def setUp(self):
        self.mock_sender = MagicMock()
        self.fetcher = ArrivalFetcher(self.mock_sender)
    
    def test_should_be_able_to_parse_arrival_time(self):        
        arrival = self.fetcher.parse_arrival_data(self._data)
        self.assertEqual(datetime.datetime.fromisoformat("2019-04-17T13:37:43+08:00"), arrival)

    def test_get_arrival_time(self):
        self.mock_sender.send.return_value = self._data
        
        result = self.fetcher.get_arrival_time(67379, 372)
        
        self.assertEqual(datetime.datetime.fromisoformat("2019-04-17T13:37:43+08:00"), result)
        self.mock_sender.send.assert_called_once_with(self.fetcher.build_arrival_time_path(67379, 372))


if __name__ == '__main__':
    unittest.main()