import RPi.GPIO as GPIO
import Adafruit_DHT as DHT # DHT11 sensor
import db
import time
import datetime

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
    
    def get_status(self):
        status = GPIO.input(self.motion_pin)
        return status

               
class DHTSensor:
    def __init__(self, dht_pin):
        self.dht_sensor = DHT.DHT11
        self.dht_pin = dht_pin
    
    def get_status(self):
        status = DHT.read(self.dht_sensor, self.dht_pin)
        return status
    
    def start_recording(self):
        start_date = datetime.datetime.now().strftime("%Y-%m-%d")
        while True:
            humidity, temp = self.get_status()
            log_time = time.time()


            # db.insert_sensor_entry(start_date, 'temperature', log_time, temp)
            # db.insert_sensor_entry(start_date, 'humidity', log_time, humidity)

    def stop_recording(self):
        pass

                
# KS0035 - microphone seems faulty
class Microphone:
    def __init__(self, mic_pin):
        self.mic_pin = mic_pin
        GPIO.setup(self.mic_pin, GPIO.IN)
    
    def get_status(self):
        status = GPIO.input(self.mic_pin)
        return status


if __name__ == "__main__":
    motion_sensor = MotionSensor(motion_pin=21)
    dht_sensor = DHTSensor(dht_pin=22)
    # mic_sensor = Microphone(mic_pin=22)


    try:
        while True:
            print('###################')

            humidity, temp = dht_sensor.get_status()
            if humidity and temp:
                print("Temperature = {0:0.1f}C, Humidity = {1:0.1f}".format(temp, humidity))
            else:
                print("Sensor failure")

            print(mic_sensor.get_status())
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
    except Exception as e:
        print(e)