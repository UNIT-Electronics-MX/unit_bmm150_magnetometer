from machine import SPI, Pin
import time
import struct

class BMM150_SPI:
    def __init__(self, spi: SPI, cs: Pin):
        self.spi = spi
        self.cs = cs
        self.cs.init(Pin.OUT, value=1)
        self.initialized = False
        self.try_initialize()

    def _read_reg(self, reg, length=1):
        self.cs(0)
        self.spi.write(bytearray([reg | 0x80]))  # bit 7 = 1 for read
        result = self.spi.read(length)
        self.cs(1)
        return result

    def _write_reg(self, reg, val):
        self.cs(0)
        self.spi.write(bytearray([reg & 0x7F, val]))  # bit 7 = 0 for write
        self.cs(1)

    def try_initialize(self):
        while True:
            try:
                # Power up
                self._write_reg(0x4B, 0x01)
                time.sleep(0.05)

                chip_id = self._read_reg(0x40)[0]
                print("Chip ID leído:", hex(chip_id))
                if chip_id == 0x32:
                    print("✅ BMM150 detectado por SPI")
                    self._write_reg(0x4C, 0x00)  # modo normal
                    time.sleep(0.01)
                    self.initialized = True
                    return
            except:
                pass
            print("🔁 Reintentando conexión SPI...")
            time.sleep(1)

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
            return (0, 0, 0)
