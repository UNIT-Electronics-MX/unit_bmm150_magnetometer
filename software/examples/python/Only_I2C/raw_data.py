from machine import Pin, I2C
import time
from micropython_bmm150 import bmm150

i2c = I2C(0, sda=Pin(4), scl=Pin(5))
print("I2C scan result:", i2c.scan())

bmm = bmm150.BMM150(i2c, address=0x13)

print("Chip ID:", hex(bmm._device_id))
bmm.operation_mode = bmm150.NORMAL
time.sleep(0.1)

for _ in range(10):
    print("Raw data:", bmm._raw_data)
    time.sleep(1)
