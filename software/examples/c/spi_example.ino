

#include "DFRobot_BMM150.h"
#include <SPI.h>

// Pines personalizados para ESP32-C6
#define PIN_MOSI 7
#define PIN_MISO 2
#define PIN_SCK  6
#define PIN_CS   18

// Crear instancia SPI con pines personalizados
SPIClass mySPI(FSPI);  // FSPI es el SPI principal en ESP32-C6

// Crear instancia del sensor BMM150 en SPI
DFRobot_BMM150_SPI bmm150(/*cs=*/PIN_CS, &mySPI);

void setup() {
  Serial.begin(115200);
  while (!Serial);

  // Inicializar SPI con pines personalizados
  mySPI.begin(PIN_SCK, PIN_MISO, PIN_MOSI, PIN_CS);

  // Iniciar sensor BMM150
  while (bmm150.begin()) {
    Serial.println("bmm150 init failed, please check wiring...");
    delay(1000);
  }
  Serial.println("bmm150 init success!");

  // Autotest y configuraciones
  Serial.println(bmm150.selfTest(BMM150_SELF_TEST_NORMAL));
  bmm150.setOperationMode(BMM150_POWERMODE_NORMAL);
  bmm150.setPresetMode(BMM150_PRESETMODE_HIGHACCURACY);
  bmm150.setRate(BMM150_DATA_RATE_30HZ);
  bmm150.setMeasurementXYZ();

  Serial.print("rate is ");
  Serial.print(bmm150.getRate());
  Serial.println(" HZ");
  Serial.println(bmm150.getMeasurementStateXYZ());
  Serial.println(bmm150.getOperationMode());

  // Soft reset
  bmm150.softReset();

  // ⚠️ Volver a configurar TODO después del reset
  bmm150.setOperationMode(BMM150_POWERMODE_NORMAL);
  bmm150.setPresetMode(BMM150_PRESETMODE_HIGHACCURACY);
  bmm150.setRate(BMM150_DATA_RATE_30HZ);
  bmm150.setMeasurementXYZ();
}

void loop() {
  // Confirmar modo de operación
  // Serial.println(bmm150.getOperationMode());

  // Leer datos magnéticos
  sBmm150MagData_t magData = bmm150.getGeomagneticData();

  Serial.print("X: ");
  Serial.print(magData.x);
  Serial.print(" uT\tY: ");
  Serial.print(magData.y);
  Serial.print(" uT\tZ: ");
  Serial.print(magData.z);
  Serial.println(" uT");

  delay(100); // 1 Hz (ajusta según frecuencia de datos)
}

