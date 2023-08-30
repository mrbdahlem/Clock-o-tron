from machine import Pin, I2C, RTC
import machine
from ds3231 import DS3231
import time
from face import Display

PRESSED = 0
ON_COLOR = (64, 128, 0)
OFF_COLOR = (4, 0, 4)

min_btn = Pin(0, mode=Pin.IN, pull=Pin.PULL_UP)
hour_btn = Pin(1, mode=Pin.IN, pull=Pin.PULL_UP)
sqw = Pin(2, mode=Pin.IN, pull=None)
face_pin = Pin(13, mode=Pin.OUT, value=0)

trigger = 0
def set_trigger(pin):
    global trigger
    trigger += 1

sqw.irq(handler=set_trigger, trigger=Pin.IRQ_FALLING)

face = Display(face_pin, ON_COLOR, OFF_COLOR)

i2c = I2C(1, sda=Pin(14), scl=Pin(15))

ds = DS3231(i2c)
ds.square_wave(freq=ds.FREQ_1024) # Enable 1024 Hz output from RTC

rtc = machine.RTC()

now = ds.datetime()


face.show(0, 0, 63)
time.sleep(1)
face.show(0, 63, 0)
time.sleep(1)
face.show(15, 0, 0)
time.sleep(1)

# Set a default date and time
if now[0] < 2023:   # type: ignore
    year = 2023 # Can be yyyy or yy format
    month = 8
    mday = 15
    hour = 13 # 24 hour format only
    minute = 00
    seconds = 00

    now = (year, month, mday, hour, minute, seconds)
    ds.datetime(now)

    now = ds.datetime()
    print("time reset")

rtc.datetime(now)

print(rtc.datetime())

(year, month, mday, weekday, hour, minute, sec, _) = ds.datetime() # type: ignore

trigger = 0
hour_updated = False
minute_updated = False

while True:
    if trigger >= 34: #update at ~30Hz
        (year, month, mday, weekday, hour, minute, sec, _) = ds.datetime() # type: ignore
        face.show(hour, minute, sec)
        trigger = 0
    
    if min_btn.value() == PRESSED:
        if not minute_updated:
            minute = (minute + 1) % 60
            minute_updated = True
    else:
        minute_updated = False

    if hour_btn.value() == PRESSED:
        if not hour_updated:
            hour = (hour + 1) % 24
            hour_updated = True
    else:
        hour_updated = False

    if minute_updated or hour_updated:
        ds.datetime((year, month, mday, hour, minute, 0))
        face.show(hour, minute, sec)
    
    time.sleep_ms(100)