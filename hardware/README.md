# Hardware

<div align="center">

<a href="#"><img src="resources/Schematics_icon.jpg" width="450px"><br/> Schematic</a>

</div>

## Pinout

<div align="center">

<a href="#"><img src="resources/unit_pinout_v_1_0_ue0066_bmm150_en.jpg" width="500px"><br/> Pinout</a>
</div>

### Description

<div align="center">

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
</div>

---

## Dimensions

<div align="center">

<a href="#"><img src="resources/unit_dimension_v_0_0_1_ue0066_bmm150.png" width="450px"><br/> Dimensions</a>

</div>

## Topology

<div align="center">

<a href="#"><img src="./resources/unit_topology_v_0_0_1_ue0066_bmm150.png" width="450px"><br/> Dimensions</a>

</div>


<div align="center">

| Ref.  | Description                                                  |
|:-----:|:-------------------------------------------------------------|
| IC1   | BMM150 Magnetometer                                          |
| U1    | AP2112K 3V3 Regulator                                        |
| L1    | Power On LED                                                 |
| SW1   | Dip Switch for Mode and Address Selector                                                               |
| J1    | QWIIC Connector (JST 1mm for I2C)                            |
| J2    | QWIIC Connector (JST 1mm for I2C)                            |
| J3    | JST Connector 1mm Pitch for SPI                              |
| JP1   | 2.54mm Castellated Holes                                     |

</div>

---