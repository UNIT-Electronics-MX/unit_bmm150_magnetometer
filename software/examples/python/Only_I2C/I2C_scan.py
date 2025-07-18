from machine import I2C, Pin


while 1:
    i2c = I2C(0, scl=Pin(5), sda=Pin(4))
    print(i2c.scan())
