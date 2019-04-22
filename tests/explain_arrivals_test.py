import unittest
from buspy.bots.explain_arrivals import explain
from buspy.incoming_bus_checker import ArrivalResult

class ExplainArrivalsTests(unittest.TestCase):
    def test_bus_is_coming_soon(self):
        arrival = ArrivalResult(12345, 111, 0)
        message = explain(arrival)
        self.assertEqual("Bus <text>111</text> is arriving at bus stop <text>12345</text>", message)

    def test_bus_is_coming_soon_and_next_bus_available(self):
        arrival = ArrivalResult(12345, 111, 0, after_requested=5)
        message = explain(arrival)
        self.assertEqual("Bus <text>111</text> is arriving at bus stop <text>12345</text>, and the next one will arrive in 5 minutes", message)


    def test_when_within_range_is_available(self):
        arrival = ArrivalResult(12345, 111, 7)
        expected_results = [
            "Bus <text>111</text> will arrive at bus stop <text>12345</text> in 7 minutes time",
            "You have to be at bus stop <text>12345</text> in 7 minutes to catch bus <text>111</text>"
        ]        
        for index in range(0, len(expected_results)):
            with self.subTest(i=index):
                message = explain(arrival, index)
                self.assertEqual(expected_results[index], message)

    def test_when_only_after_requested_is_available(self):
        arrival = ArrivalResult(12345, 111, None, after_requested=12)
        message = explain(arrival)
        self.assertEqual("The only available <text>111</text> will come after your requested time, 12 minutes from now", message)

    def test_when_only_outside_range_is_available(self):
        arrival = ArrivalResult(12345, 111, None, outside_range=3)
        message = explain(arrival)
        self.assertEqual("The closest available <text>111</text> for your requested time will come in 3 minutes time", message)

    def test_when_only_outside_range_and_after_requested_are_available(self):
        arrival = ArrivalResult(12345, 111, None, outside_range=2, after_requested=16)
        message = explain(arrival)
        self.assertEqual("The next <text>111</text> will come in 2 minutes time, and the one after that will come in 16 minutes time, that's after your requested time", message)