# Hardware

<a href="#"><img src="resources/Schematics_icon.jpg" width="450px"><br/> Schematic</a>

## Pinout

<a href="#"><img src="resources/bmm150_PINOUT.jpg" width="500px"><br/> Pinout</a>

### Description


| Pin   | Signal     | Description                                                  |
|:-----:|:-----------|:-------------------------------------------------------------|
| VCC   | VCC        | Power supply                                                 |
| GND   | GND        | Ground                                                       |
| SCL   | SCL        | I²C clock                                                    |
| SDA   | SDA        | I²C data                                                     |
| SDO   | SDO / ADDR | SPI MISO / I²C address select                                |
| CS    | CS         | SPI chip-select (active LOW) / must be HIGH for I²C mode     |
| PS    | PS         | Protocol select (LOW=I²C, HIGH=SPI)                          |
| DRDY  | DRDY       | Data-Ready flag (new data available)                         |
| INT   | INT        | Programmable interrupt output (e.g. threshold, flip-over)    |

---


## Dimensions

<a href="#"><img src="hardware/resources/bmp_top.jpg" width="450px"><br/> Dimensions</a>