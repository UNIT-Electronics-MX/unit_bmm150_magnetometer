from machine import I2C
import time
import struct

class BMM150:
    POSSIBLE_I2C_ADDRESSES = [0x10, 0x11, 0x12, 0x13]

    def __init__(self, i2c):
        self.i2c = i2c
        self.addr = None
        self.initialized = False
        self.try_initialize()

    def try_initialize(self):
        while True:
            for address in self.POSSIBLE_I2C_ADDRESSES:
                try:
                    # Power on
                    self.i2c.writeto_mem(address, 0x4B, bytes([0x01]))
                    time.sleep(0.05)
                    chip_id = self.i2c.readfrom_mem(address, 0x40, 1)[0]
                    if chip_id == 0x32:
                        self.addr = address
                        print("✅ BMM150 detectado en dirección I2C:", hex(address))
                        self._write_reg(0x4C, 0x00)  # modo normal
                        time.sleep(0.01)
                        self.initialized = True
                        return
                except OSError:
                    continue
            print("🔁 Reintentando detección de BMM150...")
            time.sleep(1)

    def _write_reg(self, reg, val):
        if self.addr is not None:
            self.i2c.writeto_mem(self.addr, reg, bytes([val]))

    def _read_reg(self, reg, length):
        if self.addr is not None:
            return self.i2c.readfrom_mem(self.addr, reg, length)
        return bytes([0] * length)

    def read_raw(self):
        if not self.initialized:
            self.try_initialize()

        try:
            data = self._read_reg(0x42, 8)
            x = struct.unpack("<h", data[0:2])[0] >> 3
            y = struct.unpack("<h", data[2:4])[0] >> 3
            z = struct.unpack("<h", data[4:6])[0] >> 1
            return (x, y, z)
        except:
            print("⚠️ Error leyendo datos, reintentando...")
            self.initialized = False
            self.try_initialize()
            return (0, 0, 0)
