# IMU / Activity Brick

This repository contains two generations of the MediBrick IMU board design.

## [v1 — IMU MediBrick](v1/README.md)

The original board, built around the TDK ICM-20948 9-axis IMU and Bosch
BMP581 pressure sensor with an SPI interface. This design is complete and has
been manufactured. ICM-20948 is no longer manufactured.

## [v2 — Activity Brick V2](v2/README.md)

A redesign around the Bosch BMI323 IMU, BMM350 magnetometer, BMP581
barometer, and an optional MAX-M10S or ZED-F9P GNSS/RTK receiver, interfacing
to an Adafruit Feather ESP32-S3 host.
