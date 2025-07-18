from machine import I2C
import time
import struct

class BMM150:
    def __init__(self, i2c, address=0x13):
        self.i2c = i2c
        self.addr = address

        # Encender el sensor: write 0x01 al registro 0x4B (power control)
        self._write_reg(0x4B, 0x01)
        time.sleep(0.05)

        # Leer el chip ID varias veces
        for attempt in range(5):
            try:
                chip_id = self.i2c.readfrom_mem(self.addr, 0x40, 1)[0]
                print("Chip ID leído:", hex(chip_id))
                if chip_id == 0x32:
                    break
            except:
                pass
            time.sleep(0.05)
        else:
            raise Exception("BMM150 not found!")

        # Setear a modo normal
        self._write_reg(0x4C, 0x00)
        time.sleep(0.01)

    def _write_reg(self, reg, val):
        self.i2c.writeto_mem(self.addr, reg, bytes([val]))

    def _read_reg(self, reg, length):
        return self.i2c.readfrom_mem(self.addr, reg, length)

    def read_raw(self):
        data = self._read_reg(0x42, 8)
        x = struct.unpack("<h", data[0:2])[0] >> 3
        y = struct.unpack("<h", data[2:4])[0] >> 3
        z = struct.unpack("<h", data[4:6])[0] >> 1
        return (x, y, z)
