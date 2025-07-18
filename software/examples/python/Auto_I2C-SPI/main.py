# ⚠️ IMPORTANT HARDWARE NOTICE – BMM150 I2C/SPI interface
#
# The BMM150 sensor cannot use I2C and SPI simultaneously, as the SDO and CS pins are shared
# between both interfaces and behave differently depending on wiring.
#
# 🔸 If CS is tied to GND, the sensor enters SPI mode and will not respond to I2C commands.
# 🔸 If CS is high or floating (with pull-up), the sensor is in I2C mode.
# 🔸 Having both I2C and SPI buses physically connected at the same time may cause signal interference,
#     especially if SPI pins (MOSI, MISO, SCK, CS) are active while the sensor is in I2C mode.
#
# ✅ Recommended best practices:
# - Disconnect the SPI bus when using I2C (or add 1kΩ series resistors to reduce interference).
# - Use jumpers or DIP switches to toggle between I2C and SPI mode.
# - Never connect both I2C and SPI to the same sensor module simultaneously unless using isolation.
#
# This is especially important when using auto-detection between I2C and SPI.

from machine import I2C, SPI, Pin
import time
from bmm150_auto_interface import BMM150_Auto

# I2C on GPIO 4 (SDA) and 5 (SCL)
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)

# SPI on GPIO 18 (SCK), 19 (MOSI), 16 (MISO) and CS on GPIO 17
spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
cs = Pin(17, Pin.OUT)

sensor = BMM150_Auto(i2c, spi, cs)

while True:
    x, y, z = sensor.read_raw()
    print("X: {}  Y: {}  Z: {}".format(x, y, z))
    time.sleep(0.5)
