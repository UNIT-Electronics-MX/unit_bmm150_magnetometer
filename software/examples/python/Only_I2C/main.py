from machine import I2C, Pin
import time
from micropython_bmm150 import bmm150

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400_000)
sensor = bmm150.BMM150(i2c, address=0x13)  # Usa la dirección correcta

print("Current Data rate setting: ", sensor.data_rate)

while True:
    x, y, z, _ = sensor.measurements
    print("X:", x, "Y:", y, "Z:", z)
    time.sleep(1)
