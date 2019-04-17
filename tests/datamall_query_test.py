import unittest
import buspy.datamall_query as query

class DataMallQueryTests(unittest.TestCase):
    def test_should_get_something(self):
        self.assertEqual('blah', query.get_arrival_time('blah'))

    def test_should_get_another_one(self):
        self.assertEqual('abc', query.get_arrival_time('abc'))


if __name__ == '__main__':
    unittest.main()