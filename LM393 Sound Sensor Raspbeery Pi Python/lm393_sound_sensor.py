import RPi.GPIO as GPIO
import time

# Global variable
LED_STATE = False

# Pin Declaration
greenLEDPin = 20
soundSensorPin = 26

# GPIO Settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(soundSensorPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(greenLEDPin, GPIO.OUT, initial = GPIO.LOW)

def soundSensorHandler(argument):
    global LED_STATE
    endTime = int(round(time.time() * 1000)) + int(500)
    currentTime = int(round(time.time() * 1000))
    soundPeak = 1
    GPIO.remove_event_detect(soundSensorPin)
    while(currentTime <= endTime):
        if GPIO.input(soundSensorPin):
            soundPeak = soundPeak + 1
            time.sleep(0.1)
            print soundPeak
        currentTime = int(round(time.time() * 1000))
    if soundPeak >= 6:
        if LED_STATE:
            GPIO.output(greenLEDPin, GPIO.LOW)
            print "Turned of LED"
            LED_STATE = False
        else:
            GPIO.output(greenLEDPin,GPIO.HIGH)
            print "Turned On LED"
            LED_STATE = True
    else:
        print "No Sound Detected"

    GPIO.add_event_detect(soundSensorPin, GPIO.RISING, callback=soundSensorHandler, bouncetime=300)

GPIO.add_event_detect(soundSensorPin, GPIO.RISING, callback=soundSensorHandler, bouncetime = 300)

while True:
        time.sleep(5)