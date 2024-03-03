import RPi.GPIO as GPIO
import Adafruit_DHT as DHT # DHT11 sensor
import time

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
        return status == GPIO.HIGH

               
class DHTSensor:
    def __init__(self, dht_pin):
        GPIO.setmode(GPIO.BCM)
        self.dht_sensor = DHT.DHT11
        self.dht_pin = dht_pin
    
    def get_status(self):
        status = DHT.read(self.dht_sensor, self.dht_pin)
        return status
                
# KS0035
class Microphone:

if __name__ == "__main__":
    motion_sensor = MotionSensor(motion_pin=21)
    dht_sensor = DHTSensor(dht_pin=18)
    mic_sensor = Microphone(mic_pin=4)


    try:
        while True:
            humidity, temp = dht_sensor.get_status()
            if humidity and temp:
                print("Temperature = {0:0.1f}C, Humidity = {1:0.1f}".format(temp, humidity))
            else:
                print("Sensor failure")

            motion_sensor.set_status()
            if motion_sensor.get_status():
                print("Motion detected")
            else:
                print("Motion not detected")
            time.sleep(4)
    except KeyboardInterrupt:
        GPIO.cleanup()
    except Exception as e:
        print(e)