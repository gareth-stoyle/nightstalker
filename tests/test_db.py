import unittest
import os
from datetime import datetime, timedelta

from db import DB


class TestDB(unittest.TestCase):
    def setUp(self):
        self.db = DB(sensor_db='test_sensor_db.json', video_db='test_video_db.json')
        self.date = datetime.now()

    def tearDown(self):
        if os.path.exists('test_sensor_db.json'):
            os.remove('test_sensor_db.json')
        if os.path.exists('test_video_db.json'):
            os.remove('test_video_db.json')

    def test_insert_video_entry(self):
        date = self.date + timedelta(days=1)
        date = date.strftime("%Y-%m-%d")
        self.assertTrue(self.db.insert_video_entry(date, '08:00:00', '09:00:00'))
        self.assertFalse(self.db.insert_video_entry(date, '08:00:00', '09:00:00'))

    def test_insert_video_duration(self):
        date = self.date + timedelta(days=2)
        date = date.strftime("%Y-%m-%d")
        self.db.insert_video_entry(date, '08:00:00', '09:00:00')
        self.assertTrue(self.db.insert_video_duration(date, 820))
        self.assertFalse(self.db.insert_video_duration(date, '820'))

    def test_insert_clip_entry(self):
        date = self.date + timedelta(days=3)
        date = date.strftime("%Y-%m-%d")
        self.db.insert_video_entry(date, '08:00:00', '09:00:00')
        self.assertTrue(self.db.insert_clip_entry(date, 1, '08:15:00', '08:30:00'))

    def test_retrieve_video(self):
        date = self.date + timedelta(days=4)
        date = date.strftime("%Y-%m-%d")
        invalid_date = self.date + timedelta(days=40)
        invalid_date = invalid_date.strftime("%Y-%m-%d")
        self.db.insert_video_entry(date, '08:00:00', '09:00:00')
        self.assertEqual(self.db.retrieve_video(date)['start_time'], '08:00:00')
        self.assertFalse(self.db.retrieve_video(invalid_date))

    def test_retrieve_clips(self):
        date = self.date + timedelta(days=5)
        date = date.strftime("%Y-%m-%d")
        invalid_date = self.date + timedelta(days=50)
        invalid_date = invalid_date.strftime("%Y-%m-%d")
        self.db.insert_video_entry(date, '08:00:00', '09:00:00')
        self.db.insert_clip_entry(date, 1, '08:15:00', '08:30:00')
        self.assertTrue(self.db.retrieve_clips(date))
        self.assertFalse(self.db.retrieve_clips(invalid_date))

    def test_insert_sensor_entry(self):
        date = self.date + timedelta(days=6)
        date = date.strftime("%Y-%m-%d")
        self.assertTrue(self.db.insert_sensor_entry(date, 'temperature', '08:00:00', 25))

    def test_retrieve_sensor_entries(self):
        date = self.date + timedelta(days=7)
        date = date.strftime("%Y-%m-%d")
        invalid_date = self.date + timedelta(days=50)
        invalid_date = invalid_date.strftime("%Y-%m-%d")
        self.db.insert_sensor_entry(date, 'temperature', '08:00:00', 25)
        self.assertTrue(self.db.retrieve_sensor_entries(date, 'temperature'))
        self.assertFalse(self.db.retrieve_sensor_entries(invalid_date, 'temperature'))


if __name__ == '__main__':
    unittest.main()
