import RPi.GPIO as GPIO
import Adafruit_DHT as DHT # DHT11 sensor
import db
import time
import datetime
import statistics
import threading

GPIO.setmode(GPIO.BCM)
               
class DHTSensor:
    def __init__(self, dht_pin, database='databases/sensors.json'):
        self.dht_sensor = DHT.DHT11
        self.dht_pin = dht_pin
        self.reading_cadence = 1
        self.log_cadence = self.reading_cadence * 60
        self.database = db.DB(sensor_db=database)
    
    def get_status(self):
        status = DHT.read(self.dht_sensor, self.dht_pin)
        return status
    
    def record_data(self):
        start_date = datetime.datetime.now().strftime("%Y-%m-%d")
        humidity_readings = []
        temp_readings = []
        counter = 0
        log_start_time = time.time()

        while self.recording:
            start_time = time.time()  # Record start time
            counter += 1
            humidity, temp = self.get_status()

            if humidity and temp:
                humidity_readings.append(humidity)
                temp_readings.append(temp)

            elapsed_time = time.time() - start_time  # Calculate elapsed time
            sleep_time = max(0, self.reading_cadence - elapsed_time)  # Calculate sleep time to compensate for elapsed time
            time.sleep(sleep_time)

            log_elapsed_time = time.time() - log_start_time  # Calculate elapsed time since last log
            if log_elapsed_time >= self.log_cadence:
                log_time = int(time.time())
                try:
                    humidity_avg = int(statistics.fmean(humidity_readings))
                    temp_avg = int(statistics.fmean(temp_readings))
                    self.database.insert_sensor_entry(start_date, 'temperature', log_time, temp_avg)
                    self.database.insert_sensor_entry(start_date, 'humidity', log_time, humidity_avg)
                except Exception as e:
                    print(e)
                humidity_readings = []
                temp_readings = []
                log_start_time = time.time()

    def start_recording(self):
        self.recording = True
        self.thread = threading.Thread(target=self.record_data)
        self.thread.start()

    def stop_recording(self):
        self.recording = False
        if self.thread is not None:
            self.thread.join()

