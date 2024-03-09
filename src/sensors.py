import RPi.GPIO as GPIO
import Adafruit_DHT as DHT # DHT11 sensor
import db
import time
import datetime
import statistics
import threading

GPIO.setmode(GPIO.BCM)

class Led:
    def __init__(self, pin):
        self.led_pin = pin
        GPIO.setup(self.led_pin, GPIO.OUT)

    def light_on(self):
        if not self.get_status():
            GPIO.output(self.led_pin, GPIO.HIGH)
    
    def light_off(self):
        if self.get_status():
            GPIO.output(self.led_pin, GPIO.LOW)

    def get_status(self):
        status = GPIO.input(self.led_pin)
        return status == GPIO.HIGH
    
#KS0052 motion sensor
class MotionSensor:
    def __init__(self, motion_pin):
        self.motion_pin = motion_pin
        GPIO.setup(self.motion_pin, GPIO.IN)
        self.reading_cadence = 1
        self.log_cadence = self.reading_cadence * 60
    
    def get_status(self):
        try:
            status = GPIO.input(self.motion_pin)
        except Exception as e:
            status = 0
            print(e)
        
        return status
    
    def record_data(self):
        start_date = datetime.datetime.now().strftime("%Y-%m-%d")
        motion_readings = []
        counter = 0
        log_start_time = time.time()

        while self.recording:
            start_time = time.time()  # Record start time
            counter += 1
            motion = self.get_status()
            motion_readings.append(motion)

            elapsed_time = time.time() - start_time 
            sleep_time = max(0, self.reading_cadence - elapsed_time) 
            time.sleep(sleep_time)

            log_elapsed_time = time.time() - log_start_time 
            if log_elapsed_time >= self.log_cadence:
                log_time = int(time.time())
                try:
                    motion_max = max(motion_readings)
                    db.insert_sensor_entry(start_date, 'motion', log_time, motion_max)
                except Exception as e:
                    print(e)
                motion_readings = []
                log_start_time = time.time()

    def start_recording(self):
        self.recording = True
        self.thread = threading.Thread(target=self.record_data)
        self.thread.start()

    def stop_recording(self):
        self.recording = False
        if self.thread is not None:
            self.thread.join()
               
class DHTSensor:
    def __init__(self, dht_pin):
        self.dht_sensor = DHT.DHT11
        self.dht_pin = dht_pin
        self.reading_cadence = 1
        self.log_cadence = self.reading_cadence * 60
    
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
                    db.insert_sensor_entry(start_date, 'temperature', log_time, temp_avg)
                    db.insert_sensor_entry(start_date, 'humidity', log_time, humidity_avg)
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

                
# KS0035 - microphone seems faulty
class Microphone:
    def __init__(self, mic_pin):
        self.mic_pin = mic_pin
        GPIO.setup(self.mic_pin, GPIO.IN)
    
    def get_status(self):
        status = GPIO.input(self.mic_pin)
        return status
