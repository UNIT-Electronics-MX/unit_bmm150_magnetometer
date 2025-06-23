#include <Wire.h>
#include "DFRobot_BMM150.h"

// Crear un nuevo bus I2C en los pines GPIO 6 (SDA) y 7 (SCL)
TwoWire I2CBMM = TwoWire(1);

// Dirección I2C por defecto del BMM150 (depende del cableado de CS y SDO)
DFRobot_BMM150_I2C bmm150(&I2CBMM, I2C_ADDRESS_4);

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Iniciar el nuevo bus I2C
  I2CBMM.begin(6, 7);  // SDA = 6, SCL = 7

  // Iniciar sensor
  while (bmm150.begin()) {
    Serial.println("bmm150 init failed, Please try again!");
    delay(1000);
  }
  Serial.println("bmm150 init success!");

  bmm150.setOperationMode(BMM150_POWERMODE_NORMAL);
  bmm150.setPresetMode(BMM150_PRESETMODE_HIGHACCURACY);
  bmm150.setRate(BMM150_DATA_RATE_10HZ);
  bmm150.setMeasurementXYZ();
}

void loop() {
  sBmm150MagData_t magData = bmm150.getGeomagneticData();
  Serial.print("mag x = "); Serial.print(magData.x); Serial.println(" uT");
  Serial.print("mag y = "); Serial.print(magData.y); Serial.println(" uT");
  Serial.print("mag z = "); Serial.print(magData.z); Serial.println(" uT");

  float compassDegree = bmm150.getCompassDegree();
  Serial.print("Compass angle (deg): ");
  Serial.println(compassDegree);
  Serial.println("------------------------------");

  delay(200);
}