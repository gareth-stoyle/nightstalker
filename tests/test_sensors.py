import unittest
from sensors import DHTSensor
import threading
import Adafruit_DHT as DHT # DHT11 sensor


# Set pin for testing (replace with actual pin)
DHT_PIN = 4

class TestDHTSensor(unittest.TestCase):

  # Test initialization
  def test_init(self):
    sensor = DHTSensor(DHT_PIN)
    self.assertEqual(sensor.dht_sensor, DHT.DHT11)
    self.assertEqual(sensor.dht_pin, DHT_PIN)
    self.assertEqual(sensor.reading_cadence, 1)
    self.assertEqual(sensor.log_cadence, 60)

  # Test record_data with successful readings and logging (requires actual sensor)
  def test_record_data_success(self):
    sensor = DHTSensor(DHT_PIN)
    sensor.start_recording()  # Run in main thread for testing
    sensor.stop_recording()  # Ensure recording stops after test

  # Test start_recording and stop_recording
  def test_start_stop_recording(self):
    sensor = DHTSensor(DHT_PIN)
    sensor.start_recording()
    self.assertTrue(sensor.recording)
    self.assertIsInstance(sensor.thread, threading.Thread)

    sensor.stop_recording()
    self.assertFalse(sensor.recording)
    self.assertIsNone(sensor.thread)  # Thread should join


if __name__ == '__main__':
  unittest.main
