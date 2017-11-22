#claymore hosts array
claymore_hosts = ['192.168.0.41', '192.168.0.43']
cycle_seconds = 10

# code modified, tweaked and tailored from code by bertwert
# on RPi forum thread topic 91796
import RPi.GPIO as GPIO
import time
import urllib2
import time
import itertools
import json

GPIO.setmode(GPIO.BCM)

# GPIO ports for the 7seg pins
segments =  (11,4,23,8,7,10,18,25)
# 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline

for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)

# GPIO ports for the digit 0-3 pins
digits = (22,27,17,24)
# 7seg_digit_pins (12,9,8,6) digits 0-3 respectively

for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)

num =  {' ':(0,0,0,0,0,0,0),
        '0':(1,1,1,1,1,1,0),
        '1':(0,1,1,0,0,0,0),
        '2':(1,1,0,1,1,0,1),
        '3':(1,1,1,1,0,0,1),
        '4':(0,1,1,0,0,1,1),
        '5':(1,0,1,1,0,1,1),
        '6':(1,0,1,1,1,1,1),
        '7':(1,1,1,0,0,0,0),
        '8':(1,1,1,1,1,1,1),
        '9':(1,1,1,1,0,1,1),
        'H':(0,1,1,0,1,1,1),
        'r':(0,0,0,0,1,0,1),
        'E':(1,0,0,1,1,1,1)}

try:
    while True:
        s = 'Err0'
        for host in itertools.cycle(claymore_hosts):
            try:
                result = urllib2.urlopen('http://'+host+':3333/').read().split('\r\n')[1].split('<br>')[0]
                data = json.loads(result)
                values = map(int, data['result'][3].split(';'))
                s = sum(values)
                while s > 1000:
                    s = int(s/1000)
                s = str(s).zfill(3) + 'H'
            except IOError, e:
                s = 'Err1'

            then = time.time()

            while time.time() - cycle_seconds < then:
                for digit in range(4):
                    for loop in range(0,7):
                        GPIO.output(segments[loop], num[s[digit]][loop])
                    GPIO.output(digits[digit], 0)
                    time.sleep(0.001)
                    GPIO.output(digits[digit], 1)
finally:
    GPIO.cleanup()
