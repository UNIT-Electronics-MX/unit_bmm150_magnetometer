from machine import I2C, SPI, Pin
import time
import struct

class BMM150_I2C:
    POSSIBLE_I2C_ADDRESSES = [0x10, 0x11, 0x12, 0x13]

    def __init__(self, i2c: I2C):
        self.i2c = i2c
        self.addr = None
        self.initialized = False
        self.try_initialize()

    def try_initialize(self):
        for address in self.POSSIBLE_I2C_ADDRESSES:
            try:
                self.i2c.writeto_mem(address, 0x4B, bytes([0x01]))
                time.sleep(0.05)
                chip_id = self.i2c.readfrom_mem(address, 0x40, 1)[0]
                if chip_id == 0x32:
                    self.addr = address
                    print("✅ BMM150 detectado por I2C en dirección:", hex(address))
                    self._write_reg(0x4C, 0x00)
                    time.sleep(0.01)
                    self.initialized = True
                    return True
            except OSError:
                continue
        print("❌ No se detectó BMM150 por I2C.")
        return False

    def _write_reg(self, reg, val):
        if self.addr is not None:
            self.i2c.writeto_mem(self.addr, reg, bytes([val]))

    def _read_reg(self, reg, length):
        if self.addr is not None:
            return self.i2c.readfrom_mem(self.addr, reg, length)
        return bytes([0] * length)

    def read_raw(self):
        try:
            data = self._read_reg(0x42, 8)
            x = struct.unpack("<h", data[0:2])[0] >> 3
            y = struct.unpack("<h", data[2:4])[0] >> 3
            z = struct.unpack("<h", data[4:6])[0] >> 1
            return (x, y, z)
        except:
            print("⚠️ Error leyendo datos I2C")
            self.initialized = False
            return (0, 0, 0)

class BMM150_SPI:
    def __init__(self, spi: SPI, cs: Pin):
        self.spi = spi
        self.cs = cs
        self.cs.init(Pin.OUT, value=1)
        self.initialized = False
        self.try_initialize()

    def _read_reg(self, reg, length=1):
        self.cs(0)
        self.spi.write(bytearray([reg | 0x80]))
        result = self.spi.read(length)
        self.cs(1)
        return result

    def _write_reg(self, reg, val):
        self.cs(0)
        self.spi.write(bytearray([reg & 0x7F, val]))
        self.cs(1)

    def try_initialize(self):
        try:
            self._write_reg(0x4B, 0x01)
            time.sleep(0.05)
            chip_id = self._read_reg(0x40)[0]
            if chip_id == 0x32:
                print("✅ BMM150 detectado por SPI")
                self._write_reg(0x4C, 0x00)
                time.sleep(0.01)
                self.initialized = True
                return True
        except:
            pass
        print("❌ No se detectó BMM150 por SPI.")
        return False

    def read_raw(self):
        try:
            data = self._read_reg(0x42, 8)
            x = struct.unpack("<h", data[0:2])[0] >> 3
            y = struct.unpack("<h", data[2:4])[0] >> 3
            z = struct.unpack("<h", data[4:6])[0] >> 1
            return (x, y, z)
        except:
            print("⚠️ Error leyendo datos SPI")
            self.initialized = False
            return (0, 0, 0)

class BMM150_Auto:
    def __init__(self, i2c: I2C, spi: SPI, cs: Pin):
        self.i2c_driver = None
        self.spi_driver = None
        self.driver = None
        self.i2c = i2c
        self.spi = spi
        self.cs = cs
        self.auto_detect()

    def auto_detect(self):
        print("🔍 Buscando sensor BMM150...")
        self.i2c_driver = BMM150_I2C(self.i2c)
        if self.i2c_driver.initialized:
            self.driver = self.i2c_driver
            return

        self.spi_driver = BMM150_SPI(self.spi, self.cs)
        if self.spi_driver.initialized:
            self.driver = self.spi_driver
            return

        print("❌ No se pudo encontrar el sensor por I2C ni SPI.")

    def read_raw(self):
        if self.driver is None or not self.driver.initialized:
            print("🔁 Intentando reconexión...")
            self.auto_detect()

        return self.driver.read_raw() if self.driver else (0, 0, 0)
