import unittest
from buspy.datetime_helpers import gettime, now

class GetTimeTests(unittest.TestCase):
    def setUp(self):
        self.now = now()

    def test_replace_hour_and_minute_correctly(self):
        result = gettime("11:07", self.now)
        self.assertEqual(11, result.hour)
        self.assertEqual(7, result.minute)
        self.assertEqual(0, result.second)
        self.assertEqual(0, result.microsecond)

    def test_invalid_time(self):
        result = gettime("90:15", self.now)
        self.assertIsNone(result)