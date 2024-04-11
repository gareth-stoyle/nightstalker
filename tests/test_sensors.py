import unittest
import threading
import time
import Adafruit_DHT as DHT

from sensors import DHTSensor

TEST_DHT_PIN = 18

class TestDHTSensor(unittest.TestCase):
	def setUp(self):
		self.sensor = DHTSensor(TEST_DHT_PIN, database='/home/gareth/Desktop/nightstalker/tests/test_sensors.json')
		
	def test_init(self):
		self.assertEqual(self.sensor.dht_sensor, DHT.DHT11)
		self.assertEqual(self.sensor.dht_pin, TEST_DHT_PIN)
		self.assertEqual(self.sensor.reading_cadence, 1)
		self.assertEqual(self.sensor.log_cadence, 60)

	def test_start_stop_recording(self):
		self.sensor.start_recording()
		self.assertTrue(self.sensor.recording)
		self.assertIsInstance(self.sensor.thread, threading.Thread)
		time.sleep(1)
		self.sensor.stop_recording()
		self.assertFalse(self.sensor.recording)
		self.assertFalse(self.sensor.thread.is_alive())


if __name__ == '__main__':
	unittest.main
