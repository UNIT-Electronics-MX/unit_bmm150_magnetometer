from machine import I2C, Pin
import time
from bmm150_automatic_addr import BMM150

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)
sensor = BMM150(i2c)

while True:
    x, y, z = sensor.read_raw()
    print("X: {}  Y: {}  Z: {}".format(x, y, z))
    time.sleep(0.5)
