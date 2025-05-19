# Magnetometer BMM150

## Introduction
The **BMM150** is a compact, ultra-low-power 3-axis digital magnetometer designed for accurate orientation sensing, electronic compass applications, and inertial navigation. Its versatile I²C and SPI interfaces ensure easy integration with popular platforms such as Arduino, ESP32, and Raspberry Pi.

<a href="#"><img src="hardware/resourcesproduct.png" width="500px" alt="Magnetometer BMM150"><br/>Magnetometer BMM150</a>



## Key Features
- **Axes:** 3 (X, Y, Z)
- **Measurement Range:** ±1300 µT
- **Resolution:** ~0.3 µT
- **Power Consumption:** Ultra-low power consumption for battery-operated devices
- **Interfaces:** I²C and SPI
- **Supply Voltage:** 3.3 V
- **Operating Temperature:** Wide operating range suitable for various environments
- **Additional Signals:**  
  - **DRDY** (Data Ready)  
  - **INT** (Programmable Interrupt)  
  - **SDO/ADDR** (I²C address select / SPI MISO)


## Applications

| Application                           | Description                                                                                       |
| ------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Electronic Compass                    | Detects Earth’s magnetic field to determine the device orientation.                             |
| Inertial Navigation (INS)             | Integrates with accelerometers and gyroscopes to improve position and orientation estimation.    |
| Augmented Reality (AR)                | Dynamically adjusts AR content on smart devices based on precise orientation data.                |
| Metal Detection / Proximity Sensing   | Monitors magnetic field variations to detect metallic objects and machinery anomalies.           |
| Mobile Robotics and Drones            | Provides reliable heading information, essential for indoor navigation and autonomous operation. |
| Wearables and Portable Devices        | Enhances personal navigation in smartwatches, fitness trackers, and other portable devices.        |
| Indoor Geolocation                    | Improves indoor positioning accuracy by compensating for sensor drift and interference.          |

## Documentation and Setup

### Overview
This repository contains firmware and documentation for integrating the BMM150 magnetometer into your project. The examples provided demonstrate sensor configuration, data acquisition, and interfacing via both I²C and SPI.

### Installation
1. Clone the repository:
   ```
   git clone git@github.com:UNIT-Electronics-MX/unit_bmm150_magnetometer.git
   ```
2. Navigate to the project directory:
   ```
   cd ./unit_bmm150_magnetometer
   ```
3. Follow the platform-specific setup instructions detailed in the project documentation.

### Usage
Include the sensor initialization and configuration routines in your main project file. Sample code snippets and detailed explanations can be found in the documentation folder of the repository.



## Support
For any issues or further assistance, please open an issue on the GitHub repository or contact our support team.
