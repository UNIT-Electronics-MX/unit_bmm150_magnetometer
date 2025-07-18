from machine import SPI, Pin
import time
from bmm150_spi import BMM150_SPI

spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
cs = Pin(17, Pin.OUT)

sensor = BMM150_SPI(spi, cs)

while True:
    x, y, z = sensor.read_raw()
    print("X: {}  Y: {}  Z: {}".format(x, y, z))
    time.sleep(0.5)

