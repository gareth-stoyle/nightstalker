import unittest
from src.fitbit import *
# Left out API call related unittests, 
# found those easier to test as written.

class TestFitbit(unittest.TestCase):
    def test_is_valid_date(self):
        self.assertTrue(is_valid_date('2023-12-09'))
        self.assertTrue(is_valid_date('2023-01-01'))
        self.assertTrue(is_valid_date('2020-12-09'))
        self.assertFalse(is_valid_date(1234))
        self.assertFalse(is_valid_date(True))
        self.assertFalse(is_valid_date(False))
        self.assertFalse(is_valid_date('2019-12-09'))
        self.assertFalse(is_valid_date('2100-12-09'))
        self.assertFalse(is_valid_date('2129-01-01'))
        self.assertFalse(is_valid_date('2129-01-01'))
        self.assertFalse(is_valid_date('23-01-01'))
        self.assertFalse(is_valid_date('10-10-23'))
        self.assertFalse(is_valid_date('2023-23-10'))

    def test_time_range_spans_multidays(self):
        self.assertTrue(time_range_spans_multidays(['23:05', '08:04']))
        self.assertTrue(time_range_spans_multidays(['16:00', '00:00']))
        self.assertFalse(time_range_spans_multidays(['01:01', '08:04']))
        self.assertFalse(time_range_spans_multidays(['00:00', '23:59']))



if __name__ == "__main__":
    unittest.main()