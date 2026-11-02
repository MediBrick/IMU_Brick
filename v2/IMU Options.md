# IMU Options

Sparkfun:
- IMU: IM19 expensive
- GNSS: mosaic-G5 P3 
- GPS-RTK: ZED-F9R
- Accelerometer: LIS3DH 3 axis (no gyroscope)
- IMU: BNO086 CEVA 9 axis full processor
- IMU: BMI270 Bosch 6 axis motion
- IMU: LSM6DSV16X STM 6 axis
- IMU: ISM330DHCX STM 6 axis
- ISM330DHCX + MMC5983MA 
- ICM-20948 TDK 9 axis EOL
    - Replace with
    - ICM-45605 TDK 6 axis host side fusion
    - ICM-42670-P TDK 

Pixhawk 6X:
- IMU: ICM45686
- Baro: ICP20100, BMP388,580,581
- MAG: BMM150

Pixhawk 6X Pro:
- IMU: ADIS16470
- IMU: ICM45686
- IMU: IIM-42652
- Baro: ICP20100. BMP388
- MAG: BMM150

## Selection for Activity Brick

- IMU BMI323
- MAG BME350
- Pressure BMP581
- GPS MAX-M10S-00B
- RTK GPS ZED-F9P-05B

*Lifecycle and distributor availability were checked on 2026-09-03 and can change quickly.*

## 9 Axis IMUs

| Manufacturer / solution  | Architecture  | Noise or orientation performance  |  Running current | Interfaces  | Motion processing: internal versus host | Approx. cost | Availability |
| --- | --- | --- | ---: | --- | --- | ---: | --- |
| **CEVA BNO086**  | **Single-package 9-axis SiP**: accel + gyro + magnetometer + Cortex-M0+; 5.2 × 3.8 mm, 28-LGA | Rotation vector: 2° static, 3.5° dynamic; game vector: 1.5° static and 0.5°/min heading drift; magnetometer accuracy 1.4 µT | Approximately **10.4 mA / 34 mW** for 100-Hz 6/9-axis fusion; 57 µA idle | I²C, SPI, UART  | **Internal:** complete SH-2 6/9-axis fusion, calibrated sensors, quaternion/rotation vectors, gravity, linear acceleration, steps, tap, activity and stability detection. **Host:** only selects reports and reads processed output | $13.93 each; $10.87 at 100 | Excellent: about 10,000 at DigiKey; active, 16-week stated lead time ([DigiKey][1])  |
| **CEVA BNO085**  | Same 9-axis SiP and footprint as BNO086 | Essentially the same standard SH-2 fusion outputs; BNO086 is the newer drop-in version  | Approximately **10.7 mA / 35 mW** at 100-Hz fusion | I²C, SPI, UART  | Same internal SH-2 processing; BNO086 is preferred for new design | $13.57 each; $10.58 at 100 | Active but currently zero at DigiKey; approximately 4,000 expected September 2026 ([ceva-ip.com][2]) |
| **Bosch BHI360 + BMM350**  | Two-chip smart 9-axis system: programmable 6-axis sensor hub + external TMR magnetometer  | BHI360 fusion: approximately 2° static and 7° dynamic heading accuracy; BMM350 noise 190 nT X/Y, 450 nT Z | BHI360 **840 µA** for 100-Hz 9-axis rotation vector + BMM350 approximately 200 µA: total approximately **1.04 mA** | Host I²C or SPI; secondary I²C/SPI sensor-master interfaces | **Internal:** complete Bosch BSX 6/9-axis fusion, quaternion, gravity, gyro and magnetometer calibration, steps, gestures and activity recognition; programmable 32-bit MCU for custom algorithms. **Host:** reads virtual-sensor outputs | $7.48 total each; about $5.60 at 100 | BMM350 excellent; BHI360 has about 7,300 at Mouser, although DigiKey presently shows zero ([bosch-sensortec.com][3]) |
| **ST LSM6DSV16X + BMM350** | Two-chip 9-axis system; 6-axis IMU with internal 6-axis fusion plus external magnetometer | Gyro 2.8 mdps/√Hz; accel 60 µg/√Hz; BMM350 190/450 nT RMS | 650 µA IMU + 200 µA magnetometer: approximately **0.85 mA**, excluding host processing | I²C, SPI, I3C; ST sensor hub for external sensors | **Internal:** 6-axis quaternion, gravity and gyro-bias estimation; FSM, machine-learning core, events and steps. **Host:** must incorporate magnetometer and perform the final 9-axis fusion/absolute-yaw correction  | $8.18 total each; about $6.12 at 100 | Good: approximately 4,000 LSM6DSV16X and tens of thousands of BMM350s available ([www.st.com][4])  |
| **Bosch BMI323 + BMM350**  | Two discrete sensors; all fusion on host  | Gyro 7 mdps/√Hz; accel 180 µg/√Hz; BMM350 190/450 nT RMS  | 790 µA + 200 µA: approximately **0.99 mA**, excluding host | I²C, SPI, I3C; magnetometer connects separately to host | **Internal:** steps, tap, tilt, orientation categories and motion events. **Host:** calibration, synchronization and complete 9-axis quaternion/fusion  | $5.77 total each; about $4.28 at 100 | Excellent: large stock of both components ([www.bosch-sensortec.com][5]) |
| **Bosch BMI270 + BMM350**  | Two-chip system; BMI270 can act as I²C master for magnetometer  | Gyro 7 mdps/√Hz; accel 160 µg/√Hz; BMM350 190/450 nT RMS  | 685 µA + 200 µA: approximately **0.89 mA**, excluding host | Host I²C/SPI; secondary AUX-I²C or OIS-SPI  | **Internal:** wrist gestures, steps and motion/activity events. BMI270 can synchronize magnetometer data into its FIFO. **Host:** complete 9-axis fusion and quaternion | $6.31 total each; about $4.69 at 100 | Excellent: more than 60,000 BMI270s and substantial BMM350 stock ([www.bosch-sensortec.com][6])  |
| **TDK ICM-45605/45686 + BMM350** | Two-chip system; TDK 6-axis IMU includes auxiliary I²C master | Gyro 3.8 mdps/√Hz; accel 70 µg/√Hz; strong vibration rejection  | 420 µA + 200 µA: approximately **0.62 mA**, excluding host | I²C, SPI, I3C; auxiliary I²C master | **Internal:** APEX motion events, steps, tap, free fall and activity detection. **Host:** complete 9-axis fusion, quaternion and magnetometer calibration | Approximately $7.34 total each; about $5.49 at 100 | BMM350 excellent; ICM-45605/45686 distributor supply is presently poor or inconsistent ([www.invensense.tdk.com][7]) |

[1]: https://www.digikey.com/en/products/detail/ceva-technologies-inc/BNO086/14114190?msockid=3c441527c99e6a2a060203d8c8f86b9e&utm_source=chatgpt.com "BNO086 CEVA Technologies, Inc. | IMUs (Inertial Measurement Units)"
[2]: https://www.ceva-ip.com/wp-content/uploads/BNO080_085-Datasheet.pdf?utm_source=chatgpt.com "BNO08X Datasheet"
[3]: https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bhi360-ds000.pdf?utm_source=chatgpt.com "BHI360 Preliminary Datasheet"
[4]: https://www.st.com/resource/en/datasheet/lsm6dsv16x.pdf?utm_source=chatgpt.com "Datasheet - LSM6DSV16X - 6-axis inertial measurement unit (IMU) and AI sensor with embedded sensor fusion, Qvar for high-end applications"
[5]: https://www.bosch-sensortec.com/en/products/motion-sensors/imus/bmi323?utm_source=chatgpt.com "Inertial Measurement Unit BMI323"
[6]: https://www.bosch-sensortec.com/en/products/motion-sensors/imus/bmi270?utm_source=chatgpt.com "Inertial Measurement Unit BMI270"
[7]: https://www.invensense.tdk.com/en-us/products/icm-45605?utm_source=chatgpt.com "ICM-45605"


## 6 Axis IMUs and 3 Axis Accelerometers

| Manufacturer / sensor  | Noise and principal performance | Typical running current | Interface/package | Motion processing: internal versus host  | Approx. cost | Availability |
| --- | --- | ---: | --- | --- | ---: | --- |
| **ST LIS3DH — 3-axis accelerometer only** | Approximately **220 µg/√Hz** noise density; ±2/4/8/16 g; 1 Hz to 5.3 kHz ODR. **It has no gyroscope and is not a 6-axis IMU.** | Down to **2 µA** in ultra-low-power mode; operating current depends strongly on ODR and resolution mode | I²C, SPI; 3 × 3 × 1 mm 16-LGA | **Internal:** 32-sample FIFO, free-fall, motion and 4D/6D orientation-category interrupts. **Host:** continuous attitude estimate; a separate gyroscope is required for a true 6-axis solution | Roughly $2–$3 each when stocked | ST lists LIS3DHTR as active and in volume production, but its own distributor lookup reports no stock and major-distributor inventory is inconsistent; verify before selecting it ([STMicroelectronics][10]) |
| **TDK ICM-45605** | Gyro **3.8 mdps/√Hz**; accel **70 µg/√Hz**; ±2000 dps, ±16 g; good vibration and temperature performance  | **0.42 mA** low-noise; 0.22 mA low-power | I²C, SPI, I3C; auxiliary I²C master; 2.5 × 3 mm 14-LGA  | **Internal:** APEX/eDMP pedometer, tilt, tap, raise-to-wake, WOM, free fall, significant motion, high/low-g. **Host:** quaternion/orientation and all magnetometer-based 9-axis fusion | $5.26 each; $3.97 at 100 | Production, but currently poor distributor stock; DigiKey shows zero and no firm restock date ([TDK InvenSense][1])  |
| **TDK ICM-45686** | Gyro **3.8 mdps/√Hz**; accel **70 µg/√Hz**; improved gyro temperature stability; ±4000 dps and ±32 g; external-clock support | **0.42 mA** low-noise; 0.22 mA low-power | I²C, SPI, I3C; auxiliary I²C master or OIS interface; 2.5 × 3 mm 14-LGA | **Internal:** APEX pedometer, tilt, tap, raise-to-wake, WOM, free fall, significant motion and high/low-g events. **Host:** orientation/quaternion and 9-axis fusion. The auxiliary interface can collect magnetometer data but does not perform documented 9-axis fusion | $5.26 each; about $4 at reel quantity | TDK lists it in production, but supply is constrained: only small authorized-channel quantities are immediately available, DigiKey and Mouser show zero, and Mouser quotes about a one-year factory lead time ([TDK InvenSense][2], [TrustedParts][11]) |
| **TDK IIM-42652** | Industrial-temperature 6-axis IMU; gyro **3.8 mdps/√Hz**; accel **70 µg/√Hz**; ±2000 dps, ±16 g; −40 to +105 °C; accurate external-clock input | **0.88 mA** in 6-axis low-noise mode; 7.5 µA full-chip sleep | I²C, SPI, I3C; 2.5 × 3 × 0.91 mm 14-LGA | **Internal:** APEX pedometer, tilt, tap, free fall, WOM and significant-motion events; 2 kB FIFO. **Host:** quaternion/orientation and magnetometer fusion | About $6–$7 each when orderable | In production, but poor immediate availability: DigiKey shows zero with 5,000 expected in August 2027; TDK's inventory lookup reports no inventory information ([TDK][12], [DigiKey][13]) |
| **Analog Devices ADIS16470** | Precision, factory-calibrated 6-DoF IMU; gyro **0.008°/s/√Hz**, 8°/h in-run bias stability and ±2000°/s; accel **100 µg/√Hz**, 13 µg in-run bias stability and ±40 g; 2000 SPS | **42 mA typical** at 3.3 V | SPI; approximately 11 × 15 × 11 mm 44-ball BGA module | **Internal:** calibrated accel/gyro, delta-angle and delta-velocity outputs, filtering, self-test and bias correction. **Host:** quaternion/navigation solution and any magnetometer fusion | **$345.16 at 1,000**; roughly $500–$550 each in small quantities | Recommended for new designs and orderable, but expensive with only small authorized-distributor inventories; the breakout board is more readily stocked than the bare module ([Analog Devices][14]) |
| **TDK ICM-42688-P** | Gyro **2.8 mdps/√Hz**; accel approximately **70 µg/√Hz**; excellent precision; ±2000 dps, ±16 g |  **0.88 mA** low-noise | I²C, SPI, I3C; 2.5 × 3 mm 14-LGA  | **Internal:** APEX pedometer, tilt, tap, WOM, raise-to-wake and significant motion. **Host:** sensor calibration/fusion, quaternion and external-magnetometer integration  | $4.91 each; $3.70 at 100 | Active but currently a serious sourcing problem: DigiKey and Mouser show zero and very long lead times ([www.invensense.tdk.com][3]) |
| **TDK ICM-42670-P** | Gyro **7 mdps/√Hz**; accel approximately **100 µg/√Hz**; ±2000 dps, ±16 g | **0.55 mA** low-noise; accel-only modes down to 4.4 µA | I²C, SPI, I3C; 2.5 × 3 mm 14-LGA  | **Internal:** APEX pedometer, tilt, low-g, free fall, WOM and significant motion. **Host:** quaternion and 9-axis fusion | $4.06 each; $2.70 at 100 | Only about 72 at Mouser; larger quantities on order, but approximately 45–53-week factory lead time ([TDK InvenSense][4])  |
| **ST LSM6DSV16X** | Gyro **2.8 mdps/√Hz**; accel **60 µg/√Hz**; ±4000 dps, ±16 g; separate UI/OIS/EIS data paths  | **0.65 mA** high-performance | I²C, SPI, I3C; auxiliary SPI and external-sensor hub; 2.5 × 3 mm 14-LGA | **Internal:** SFLP produces 6-axis quaternion, gravity vector and gyro bias; also pedometer, events, FSM, machine-learning core and adaptive self-configuration. **Host:** magnetometer-corrected 9-axis quaternion/absolute yaw. Internal SFLP does not incorporate the external magnetometer | $6.10 each; $4.60 at 100 | Active, about 3,500–4,000 at DigiKey; stated 24-week lead time ([Product - STMicroelectronics][5]) |
| **Bosch BMI323**  | Gyro **7 mdps/√Hz**; accel **180 µg/√Hz**; ±2000 dps, ±16 g; self-calibrating gyro sensitivity  | **0.79 mA** high-performance | I²C, SPI, I3C; 2.5 × 3 mm 14-LGA  | **Internal:** steps, activity/gesture recognition, tap, orientation, motion/no-motion and significant-motion interrupts. **Host:** quaternion, attitude estimation and magnetometer fusion | $3.69 each; $2.76 at 100 | Excellent: approximately 21,000 at Mouser and substantial additional DigiKey inventory ([Bosch Sensortec][6])  |
| **Bosch BMI270**  | Gyro **7 mdps/√Hz**; accel **160 µg/√Hz**; ±2000 dps, ±16 g; optimized for wearables  |  **0.685 mA** full ODR | I²C, SPI; auxiliary/OIS interfaces; 2.5 × 3 mm 14-LGA | **Internal:** step counter/detector, wrist gestures, activity/context recognition and motion interrupts. **Host:** Bosch fusion library or user algorithm for quaternion and 9-axis fusion | $4.23 each; $3.17 at 100 | Excellent: approximately 65,000 at DigiKey and 49,000 at Mouser ([Bosch Sensortec][7]) |
| **Bosch BMI088**  | Gyro **14 mdps/√Hz**; accel **175 µg/√Hz**; excellent vibration robustness; separate accel/gyro dies  | **5.15 mA** full operation | I²C, SPI; 3 × 4.5 mm 16-LGA | **Internal:** basic interrupt and motion detection only; no general feature engine or fusion. **Host:** synchronization, calibration, quaternion and magnetometer fusion | $5.92 each; $4.49 at 100 | Active; DigiKey inventory is temporarily zero with replenishment expected shortly; other authorized channels have stock ([Bosch Sensortec][8]) |
| **Bosch BHI360** | Smart 6-axis IMU/sensor hub; Bosch specifies fusion accuracy of approximately **2° static** and dynamic accuracy of **7° heading, 2° pitch/roll**; raw accel/gyro noise density is not separately specified | **689 µA** with accel+gyro in normal mode; **784 µA** producing a 100-Hz game rotation vector; 441 µA for 25-Hz low-power fusion; 974 µA in maximum-performance mode | I²C, SPI; two secondary sensor-master interfaces; 2.5 × 3 mm 20-LGA | **Internal:** programmable 32-bit Fuser2 MCU, Bosch BSX 6-axis quaternion/game rotation vector, gravity, calibration, steps, tap, gesture and activity recognition; custom algorithms can run inside the IMU. **Host:** mainly configuration and reading virtual-sensor results; complete 9-axis fusion can also run internally after adding a supported external magnetometer | $5.40 each; $4.08 at 100 | Active; about 7,300 available through Mouser, while DigiKey currently shows zero with 5,000 expected in November 2026 ([www.bosch-sensortec.com][9]) |

[1]: https://www.invensense.tdk.com/en-us/products/icm-45605?utm_source=chatgpt.com "ICM-45605"
[2]: https://www.invensense.tdk.com/en-us/products/6-axis/icm-45686?utm_source=chatgpt.com "ICM-45686"
[3]: https://www.invensense.tdk.com/en-us/products/consumer/icm-42688-p?utm_source=chatgpt.com "ICM-42688-P"
[4]: https://www.invensense.tdk.com/en-us/products/6-axis/icm-42670-p?utm_source=chatgpt.com "ICM-42670-P"
[5]: https://www.st.com/en/mems-and-sensors/lsm6dsv16x.html?utm_source=chatgpt.com "LSM6DSV16X"
[6]: https://www.bosch-sensortec.com/en/products/motion-sensors/imus/bmi323?utm_source=chatgpt.com "Inertial Measurement Unit BMI323"
[7]: https://www.bosch-sensortec.com/en/products/motion-sensors/imus/bmi270?utm_source=chatgpt.com "Inertial Measurement Unit BMI270"
[8]: https://www.bosch-sensortec.com/en/products/motion-sensors/imus/bmi088?utm_source=chatgpt.com "Inertial Measurement Unit BMI088"
[9]: https://www.bosch-sensortec.com/en/products/smart-sensor-systems/bhi360?utm_source=chatgpt.com "Smart sensor BHI360"
[10]: https://www.st.com/en/mems-and-sensors/lis3dh.html "LIS3DH"
[11]: https://www.trustedparts.com/en/search/ICM-45686 "ICM-45686 Authorized Inventory"
[12]: https://product.tdk.com/en/search/sensor/mortion-inertial/imu/info?part_no=IIM-42652 "IIM-42652"
[13]: https://www.digikey.com/en/products/detail/tdk-invensense/IIM-42652/13901975 "IIM-42652"
[14]: https://www.analog.com/en/products/adis16470.html "ADIS16470"


## Magnetometer 

| Manufacturer / part | Noise or principal performance | Typical running current | Interface | Supply and package | Approx. IC cost | Current Availability |
| --- | --- | ---: | --- | --- | ---: | --- |
| **Bosch BMM350** | **190 nT RMS X/Y, 450 nT RMS Z**; ±2000 µT range; 400 Hz maximum; magnetic-shock recovery  | **200 µA at 100 Hz** normal mode; approximately 122 µA at 100 Hz low-power mode | I²C, I3C  | VDD 1.72–1.98 V; VDDIO to 3.6 V; 1.28 × 1.28 mm 9-ball WLCSP  |  $2.08 each; $1.52 at 100 | Excellent: about 58,000 at DigiKey; active, 12-week stated lead time ([Bosch Sensortec][1])  |
| **Bosch BMM150** | **0.3 µT RMS** in high-accuracy preset; ±1300 µT X/Y and ±2500 µT Z typical range; up to 30 Hz; specified compass heading accuracy ±2.5° under ideal calibrated and tilt-compensated conditions | **170 µA at 10 Hz** low-power preset; 500 µA regular preset; 4.9 mA high-accuracy preset | I²C, SPI | VDD 1.62–3.6 V; VDDIO 1.2–3.6 V; 1.56 × 1.56 × 0.6 mm 12-ball WLCSP | Legacy pricing was roughly $2–$4 each | **Obsolete/EOL** with restricted residual availability; Bosch's BMM350 is the recommended replacement, so do not select BMM150 for a new design ([Bosch datasheet][8], [Mouser][9]) |
| **MEMSIC MMC5983MA**  | **40 nT RMS** in lowest-noise mode; ±800 µT; 18-bit; up to 1 kHz; built-in SET/RESET degaussing | 450 µA at 7 samples/s in lowest-noise mode; about 225 µA at 7 samples/s in 100-Hz-capable mode. Current scales with actual measurement rate | I²C, SPI  | 2.8–3.6 V; **3 × 3 mm 16-LGA**  |  $3.32 each; $2.47 at 100 | Excellent: approximately 40,000 at DigiKey; active, eight-week lead time ([DigiKey][2]) |
| **ST LIS2MDL** | **300 nT RMS** in high-resolution mode with LPF; ±5000 µT range; 50 Hz maximum |  About **475 µA at 50 Hz** high-resolution; 125 µA in 50-Hz low-power mode | I²C, SPI  | 1.71–3.6 V; **2 × 2 mm 12-LGA** |  $2.75 each; $1.94–2.03 at 100 | Active, but poor immediate availability: DigiKey and Mouser show zero; Mouser quotes 24 weeks ([st.com][3]) |
| **AKM AK09919C** | 0.15 µT/LSB; ±4900 µT range; up to 100 Hz; FIFO; designed specifically as an electronic compass | **1.1 mA at 100 Hz**; 1 µA power-down | I²C, I3C  | VDD 1.65–1.95 V; digital I/O can be higher; **0.76 × 0.76 mm 4-ball WLCSP**  |  $3.88 each; $2.38 at 100 | Good: about 11,500 at Mouser; AKM lists it in mass production ([Asahi Kasei Microdevices (AKM)][4]) |
| **Melexis MLX90393**  | Highly configurable; approximately 1–6 µT RMS depending on conversion time/filtering; wide programmable range; more of a general-purpose magnetic-field/position sensor than a premium compass | About **100 µA at 10 Hz** nominal; 2.3–4 mA during conversion; 1–5 µA idle | I²C, SPI  | 2.2–3.6 V; **3 × 3 mm 16-QFN**  | About $2.21 each | Good: roughly 5,900 of one stocked variant at Mouser; active; multiple address variants must be selected carefully ([DigiKey][5]) |
| **MEMSIC MMC34160PJ** | **150 nT RMS** at 16-bit setting; ±1600 µT; 125 Hz at best-resolution setting; built-in SET/RESET  | 140 µA at 7 measurements/s; approximately proportional to measurement rate | I²C  | 1.62–3.6 V; 12-ball WFBGA  |  $5.93 each; $4.50 at 100 | Excellent: more than 51,000 at DigiKey; active, eight-week lead time ([xonelec.com][6]) |
| **PNI RM3100** | **15 nT RMS** at 200-cycle setting; 13 nT resolution; ±1100 µT; exceptionally stable over temperature | 260 µA at 8 Hz, three axes, highest-resolution setting | I²C, SPI  | Approximately 3 V; separate controller and three sensor coils, or a larger module | Typically $25–40 for a module; chip-set sourcing varies | Specialty product rather than a convenient one-chip PCB solution; available from PNI and specialty suppliers ([pnisensor.com][7]) |

[1]: https://www.bosch-sensortec.com/en/products/motion-sensors/magnetometers/bmm350?utm_source=chatgpt.com "Magnetometer BMM350"
[2]: https://www.digikey.com/en/products/detail/memsic-inc/MMC5983MA/10452801?utm_source=chatgpt.com "MMC5983MA Memsic Inc. | Linear, Compass (ICs)"
[3]: https://www.st.com/resource/en/datasheet/lis2mdl.pdf?utm_source=chatgpt.com "Datasheet - LIS2MDL - Digital output magnetic sensor:  ultralow-power, high-performance 3-axis magnetometer"
[4]: https://www.akm.com/eu/en/products/electronic-compass/lineup-electronic-compass/ak09919c/?utm_source=chatgpt.com "AK09919C | Electronic Compass | Products"
[5]: https://www.digikey.in/en/htmldatasheets/production/1686159/0/0/1/mlx90393-datasheet.html?cur=INR&lang=en&site=IN&utm_source=chatgpt.com "MLX90393 by Melexis Technologies NV Datasheet"
[6]: https://www.xonelec.com/mpn/memsic/mmc34160pjb?utm_source=chatgpt.com "Global suppliers of MMC34160PJ-B MEMSIC Magnetic Sensor Development Tools"
[7]: https://www.pnisensor.com/rm3100/?utm_source=chatgpt.com "RM3100: Most Accurate Low-SWaP Tri-Axis Magnetometer"
[8]: https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmm150-ds001.pdf "BMM150 datasheet"
[9]: https://www.mouser.com/en/ProductDetail/Bosch-Sensortec/BMM150 "BMM150 lifecycle and availability"

## Atmospheric Pressure Sensors

| Manufacturer | Part | Pressure range | Pressure noise / altitude performance  | Accuracy / stability  |  Typical running current | Interface | Package | Indicative 1-pc cost / availability* | Why consider it  |
| --- | --- | ---: | --- | --- | ---: | --- | --- | --- | --- |
| **Bosch**  | **BMP581** — reference | 300–1250 hPa | **0.08 Pa** best mode, ≈0.7 cm pressure-equivalent; relative accuracy ±6 Pa, ≈±0.5 m | Absolute ±30 Pa; TCO ±0.5 Pa/K  | **1.3 µA at 1 Hz** | I²C, SPI, I3C | 2.0 × 2.0 × 0.75 mm LGA | ~$3.07; excellent stock  | Best overall combination of size, noise, power and availability. ([Bosch Sensortec][1])  |
| **Bosch**  | **BMP585** | 300–1250 hPa | **0.08 Pa**, ≈0.7 cm; relative accuracy ±6 Pa  | Absolute ±50 Pa; TCO ±0.5 Pa/K  | **1.3 µA at 1 Hz** | I²C, SPI, I3C | 3.25 × 3.25 × 1.86 mm LGA | ~$4.54; excellent stock  | Essentially the rugged, gel-protected choice when water, sweat or chemicals may reach the pressure port. ([Bosch Sensortec][2])  |
| **Bosch** | **BMP388** | 300–1250 hPa | **0.03 Pa** at lowest bandwidth/highest resolution, ≈0.25 cm pressure-equivalent; 1.2 Pa at full bandwidth; relative accuracy ±8 Pa | Absolute accuracy ±50 Pa in its best specified range; TCO ±0.75 Pa/K; long-term stability ±33 Pa/year | **3.4 µA at 1 Hz** | I²C, SPI | 2.0 × 2.0 × 0.75 mm 10-LGA | Legacy pricing roughly $3–$5; residual stock only | **Not available for new designs / obsolete**; Bosch recommends BMP390. Appropriate for maintaining an existing Pixhawk-compatible design, not a fresh BOM ([Bosch Sensortec][8]) |
| **STMicroelectronics** | **LPS22DF**  | 260–1260 hPa | **0.34 Pa**, ≈2.8 cm | Absolute accuracy around ±20 Pa; TCO 0.45 Pa/°C |  From **1.7 µA**, dependent on averaging and ODR | I²C, SPI, I3C | 2.0 × 2.0 mm HLGA | ~$3.12; currently backordered at DigiKey | Good general-purpose alternative with FIFO, interrupts and broad bus support, but verify supply before committing. ([Product - STMicroelectronics][3]) |
| **STMicroelectronics** | **LPS28DFW** | 260–1260 or 260–4060 hPa | **0.32 Pa**, ≈2.7 cm | Absolute accuracy around ±50 Pa |  From **1.7 µA** | I²C, I3C  | 2.8 × 2.8 mm CCLGA  | ~$4.7–$6.2; moderate stock | Water-resistant gel, O-ring sealing option and unusually high pressure range; useful for rugged or partially submerged products. No SPI. ([Product - STMicroelectronics][4]) |
| **Infineon** | **DPS368** | 300–1200 hPa | **0.2 Pa**, ≈1.7 cm; relative accuracy ±6 Pa, ≈±0.5 m  | Absolute accuracy approximately ±100 Pa | Pressure measurement **1.7 µA at 1 Hz**; ~0.5 µA standby | I²C, SPI  | 2.0 × 2.5 × 1.1 mm LGA  | ~$2.5–$3.5; stock varies by distributor  | Excellent rugged alternative: IPx8-rated sensor package and Infineon lists planned availability through at least 2034. ([Infineon Technologies][5])  |
| **TDK InvenSense** | **ICP-20100**  | 300–1100 hPa | **0.4 Pa RMS**, ≈3.3 cm  | Absolute accuracy ±20 Pa; relative accuracy ±1 Pa; TCO ±0.5 Pa/°C  | **1.0 µA at 1 Hz** | I²C, SPI, I3C | 2.0 × 2.0 × 0.72 mm 10-LGA | Legacy pricing about $5; no current authorized stock at DigiKey | **EOL/obsolete** and currently zero at DigiKey. Useful only for an existing Pixhawk-compatible design or secured lifetime buy; do not select for a new BOM ([TDK InvenSense][6], [DigiKey][9])  |
| **TE Connectivity**  | **MS5611-01BA03**  |  10–1200 hPa | Specified altitude resolution **10 cm**; pressure resolution depends heavily on oversampling | Absolute accuracy ±1.5 hPa, considerably worse than newer parts | About **0.9–12.5 µA**, depending on resolution/conversion rate | I²C, SPI  | 5.0 × 3.0 × 1.0 mm module | ~$11.56; good stock, active  | Mature, proven altimeter/variometer part with a very wide low-pressure range, but large and expensive compared with modern alternatives. ([te.com][7]) |

[1]: https://www.bosch-sensortec.com/en/products/environmental-sensors/pressure-sensors/bmp581?utm_source=chatgpt.com "BMP581"
[2]: https://www.bosch-sensortec.com/en/products/environmental-sensors/pressure-sensors/bmp585?utm_source=chatgpt.com "BMP585"
[3]: https://www.st.com/en/mems-and-sensors/lps22df.html?icmp=tt42822_gl_lnkon_feb2025&utm_source=chatgpt.com "LPS22DF"
[4]: https://www.st.com/en/mems-and-sensors/lps28dfw?utm_source=chatgpt.com "LPS28DFW"
[5]: https://www.infineon.com/part/DPS368?utm_source=chatgpt.com "DPS368 - Pressure sensors for IoT"
[6]: https://www.invensense.tdk.com/en-us/products/smartpressure/icp-20100 "ICP-20100"
[7]: https://www.te.com/commerce/DocumentDelivery/DDEController?Action=showdoc&DocId=Data+Sheet%7FMS5611-01BA03%7FB3%7Fpdf%7FEnglish%7FENG_DS_MS5611-01BA03_B3.pdf%7FCAT-BLPS0036&utm_source=chatgpt.com "MS5611 Datasheet"
[8]: https://www.bosch-sensortec.com/products/environmental-sensors/pressure-sensors/bmp388/ "BMP388"
[9]: https://www.digikey.com/en/products/filter/pressure-sensors-transducers/512?v=1428 "TDK pressure-sensor availability"


## GPS
| Manufacturer | Module | GNSS bands and constellations  | Typical positioning performance |  Tracking power | Host interface  | Antenna  | Size | Internal navigation capabilities | Approx. cost / availability* |  |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| **u-blox** | **MAX-M10S-00B** | Single-band L1; GPS, Galileo, GLONASS, BeiDou/QZSS; up to 4 concurrent | ~1.5 m CEP; −165 to −167 dBm tracking; up to approximately 10–20 Hz depending on constellation configuration  | **<25 mW**, approximately 8 mA at 3 V | UART, I²C; 1PPS | External active or passive antenna | 9.7 × 10.1 × 2.5 mm  | Position/velocity/time calculated internally; AssistNow; interference and spoofing detection; no IMU dead reckoning  | **$9.12**; excellent stock, >20k at Mouser. ([u-blox][1])  |  |
| **u-blox** | **MIA-M10Q-00B** | Single-band L1; GPS, Galileo, GLONASS, BeiDou/QZSS; 4 concurrent | ~1.5 m CEP; similar M10 performance to MAX-M10S | **<25 mW**, approximately 8 mA at 3 V | UART, I²C; 1PPS | External; integrated LNA and SAW filter  | **4.5 × 4.5 × 1.0 mm** | Internal PVT solution and AssistNow; no internal IMU fusion  | **$10.31**; presently backordered at DigiKey with long lead time | Excellent when board area is critical, but the small SiP is harder to assemble and inspect. ([u-blox][2])  |
| **u-blox** | **SAM-M10Q-00B** | Single-band L1; GPS, Galileo, GLONASS, BeiDou/QZSS; 4 concurrent | **1.5 m CEP**; −165 dBm; default multi-GNSS update rate 4–10 Hz depending on configuration  |  **37–38 mW**, approximately 12–13 mA | UART, I²C; 1PPS | **Integrated patch antenna** | 15.5 × 15.5 × 6.3 mm | Internal PVT, AssistNow, spoofing/jamming detection; no IMU fusion | **$13.75**; excellent stock, >8k at DigiKey  | Easiest antenna solution if the module can be placed at a board edge with open sky above it. ([u-blox][3]) |
| **Quectel**  | **LC76G-AB** | Single-band L1; GPS, Galileo, GLONASS, BeiDou and QZSS concurrently  | **2.0 m CEP**; −166 dBm tracking; up to 10 Hz |  Approximately **34 mA at 3.3 V**; 13 µA backup | UART, I²C; 1PPS | External active or passive; internal LNA | 10.1 × 9.7 × 2.4 mm  | Internal PVT, EASY assisted-GNSS prediction, anti-jamming; no IMU fusion | **$8.29 one-piece; ~$5.54 at 1k**; moderate stock  | Good lower-cost alternative to MAX-M10S, especially at production quantity. ([Quectel][4]) |
| **u-blox** | **NEO-F10N-00B** | **Dual-band L1+L5**; GPS/QZSS, Galileo, BeiDou and NavIC | Meter-level performance with substantially better urban multipath rejection than L1-only modules; −167 dBm tracking | Approximately **21 mA at 3 V**, about 63 mW | **UART only**; 1PPS | External dual-band active or passive antenna | 12.2 × 16.0 × 2.4 mm | Internal PVT, AssistNow and interference mitigation; firmware upgradeable; no internal IMU fusion  | **$16.22**; active, but current distributor stock is limited | Best option here when urban performance matters more than size and power. ([u-blox][5])  |
| **Quectel**  | **LC29H-AA** | **Dual-band L1+L5**, multi-constellation | **~1 m CEP** autonomous; −165 dBm tracking; improved multipath rejection  | Approximately **24 mA at 3.3 V**; 20–25 µA backup | UART, I²C and variant-dependent SPI; 1PPS | External dual-band active or passive antenna | 12.2 × 16.0 × 2.5 mm | Internal PVT and assisted GNSS; Galileo OSNMA authentication on AA version | Distributor-dependent; generally less expensive than comparable u-blox dual-band modules | Strong dual-band value option, but documentation access and distributor supply are not as convenient as u-blox. ([Quectel][6]) |
| **Quectel**  | **LC29H-BA/CA/DA** | Dual-band L1+L5, multi-constellation | Standard variants ~1 m; **RTK variants can reach centimetre-level accuracy** when correction data are supplied  | Approximately **25–30 mA at 3.3 V** | UART, I²C, variant-dependent SPI; correction-data input | External dual-band antenna | 12.2 × 16.0 × 2.5 mm | **BA:** RTK + dead reckoning; **CA:** standard precision + dead reckoning; **DA:** 1 Hz RTK; accepts GNSS and IMU data | Quote/distributor-dependent  | Particularly interesting because your board already has an IMU. Select the exact suffix carefully—the capabilities differ considerably. ([Quectel][6]) |
| **STMicroelectronics** | **Teseo-LIV4F**  | Dual-band L1+L5, multi-constellation | Improved urban performance; dual-band standard precision  |  **48.8 mA** during L1+L5 tracking; 10 µA standby | UART, I²C; 1PPS | External antenna | 9.7 × 10.1 × 2.55 mm | Internal PVT, assisted GNSS, embedded flash and configurable firmware  | Active, but currently difficult to source from major distributors  | Technically attractive and compact, but I would not select it until supply is confirmed. ([Product - STMicroelectronics][7]) |

[1]: https://www.u-blox.com/en/product/max-m10-series?legacy=Current&utm_source=chatgpt.com "MAX-M10 series"
[2]: https://www.u-blox.com/en/product/mia-m10-series?legacy=Current&utm_source=chatgpt.com "MIA-M10 series"
[3]: https://www.u-blox.com/en/product/SAM-M10Q-module?utm_source=chatgpt.com "SAM-M10Q module"
[4]: https://www.quectel.com/product/gnss-lc76g-series/?utm_source=chatgpt.com "GNSS LC76G series"
[5]: https://www.u-blox.com/en/product/neo-f10n-module?utm_source=chatgpt.com "NEO-F10N module"
[6]: https://www.quectel.com/product/gnss-lc29h/?utm_source=chatgpt.com "GNSS LC29H series"
[7]: https://www.st.com/en/positioning/teseo-liv4f.html?utm_source=chatgpt.com "Teseo-LIV4F"


### Features on PCB

Even if the GNSS module is optional/DNP, I recommend including:

- A 50 Ω antenna trace terminating in either a U.FL connector or antenna footprint.
- A three-component π matching network with unpopulated shunt positions.
- Provision for powering an active antenna, preferably through a current-limited bias network.
- RF ESD protection with very low capacitance near an external connector.
- A separate, switchable GNSS supply capable of at least 100–150 mA peak current.
- Backup-supply provision for the GNSS RTC and retained orbit data.
- Connections for UART, I²C if supported, 1PPS, reset and an interrupt/time-mark input.
- A dedicated ground area and RF keep-out following the selected module’s integration manual.
- Enough bulk capacitance near the module; GNSS acquisition current is not as smooth as the average-current specification suggests.
- If using a dual-band receiver, a genuinely L1/L5-capable antenna. A normal GPS L1 antenna will eliminate much of the advantage.

## RTK GPS

| Manufacturer | Module | Bands / constellations  | RTK accuracy and convergence  |  Maximum RTK update |  Power while tracking | Interfaces / corrections  | On-module capabilities  | Size | Approx. module cost / availability* | |
| --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- | --- |
| **Quectel**  | **LC29H-DA** | L1+L5; GPS/QZSS, Galileo, BeiDou, GLONASS L1  | Horizontal **1 cm + 1 ppm**; vertical 2.5 cm + 1 ppm; typically <10 s to RTK fix  |  **1 Hz** |  Approximately **25 mA at 3.3 V** | UART, I²C; NMEA and RTCM 3.x  | RTK rover only; no DR; external active/passive antenna  | 12.2 × 16.0 × 2.5 mm | Core-module pricing generally quote-based; reseller boards approximately $30–$50; limited authorized-channel availability | Lowest-power, low-cost RTK option, but 1 Hz is unsuitable for fast motion control. ([quectel.com][1]) |
| **Quectel**  | **LC29H-EA** | L1+L5; GPS/QZSS, Galileo, BeiDou, GLONASS L1  | Horizontal **1 cm + 1 ppm**; vertical 2.5 cm + 1 ppm; <10 s typical | **10 Hz** | Approximately **25–30 mA at 3.3 V** | UART, I²C; NMEA and RTCM 3.x  | RTK rover plus **dual-antenna moving-baseline heading**; requires two suitable antennas | 12.2 × 16.0 × 2.5 mm | Module approximately $50–$65 from smaller suppliers; evaluation boards ~$130; authorized supply limited | Attractive for vehicles, bicycles, robots or drones where true heading is required while stationary. ([www.quectel.com][2]) |
| **Quectel**  | **LC29H-BA** | L1+L5, multi-constellation  | Firmware/version dependent; RTK plus dead reckoning | Variant-dependent | Approximately **30–32 mA at 3.3 V** | UART, I²C/SPI depending firmware; RTCM 3.x  | **RTK + automotive or two-wheel dead reckoning**; integrated IMU/fusion features  | 12.2 × 16.0 × 2.5 mm | Quote-based; sourcing less straightforward than u-blox  | Interesting for your IMU-oriented design, but get written confirmation from Quectel about RTK accuracy, update rate, firmware and whether external IMU data can be used. ([www.quectel.com][2]) |
| **u-blox** | **NEO-F9P-15B**  | L1+L5; GPS, Galileo, BeiDou and GLONASS | Centimeter-level RTK, typically **1 cm + 1 ppm** class  | Up to approximately **20 Hz** depending configuration | About **95 mA at 3 V** with all constellations; 135 mA acquisition peak | 2× UART, I²C, SPI, USB; RTCM 3.x; 1PPS  | RTK rover and survey-in base; raw carrier data; PointPerfect; logging; jamming detection  | **12.2 × 16.0 × 3.6 mm** | **$119–$129**; active, stock varies | Best compact option with strong documentation, software and authorized distribution. ([u-blox][3])  |
| **u-blox** | **ZED-F9P-05B**  | L1+L2; GPS/QZSS, Galileo, BeiDou and GLONASS  | Horizontal approximately **1 cm + 1 ppm**; centimeter fix typically in seconds  | Up to approximately **20 Hz** |  Approximately **90–95 mA at 3 V**, configuration dependent | 2× UART, I²C, SPI, USB; RTCM 3.x; 1PPS  | RTK rover and survey-in base; raw carrier data; PointPerfect; mature software ecosystem | 17.0 × 22.0 × 2.4 mm | **$127**; excellent stock, hundreds at DigiKey  | The most established and easiest RTK module to develop around; many libraries, breakout boards and reference designs. ([u-blox][4]) |
| **u-blox** | **ZED-X20P-00B** | **All-band L1/L2/L5/L6**, all major global constellations | RTK **1 cm + 1 ppm**; PPP approximately 10 cm; RTK convergence under 10 s under suitable conditions | **25 Hz** RTK | Approximately **55–64 mA at 3 V** | UART, I²C, SPI, USB and GPIO; high-rate RTCM/raw data | RTK, PPP-RTK and PPP; PointPerfect Global; advanced interference mitigation | 17.0 × 22.0 mm | **$187 one-piece, ~$153 at 250**; good current stock  | Best forward-looking u-blox selection. Better band coverage, lower current and higher update rate than the F9P, but more expensive. ([u-blox][5]) |
| **Unicore**  | **UM960**  | **All-constellation, multi-frequency L1/L2/L5/E5/E6** | Horizontal **0.8 cm + 1 ppm**; vertical 1.5 cm + 1 ppm; <5 s typical initialization | **20 Hz** | Approximately **450 mW**, about 135 mA at 3.3 V | 3× UART; optional I²C by firmware; RTCM 2.3/3.x and CMR | On-module RTK; raw carrier measurements; anti-jamming and spoofing detection  | **12.2 × 16.0 × 2.6 mm** | **$128 at MOQ 5, ~$108 at 250** through DigiKey Marketplace | Excellent band coverage and accuracy in a compact package; documentation and support ecosystem are smaller than u-blox. ([en.unicorecomm.com][6]) |
| **Unicore**  | **UM980**  | All-band/all-constellation including L6 and Galileo E6  | Horizontal **0.8 cm + 1 ppm**; vertical 1.5 cm + 1 ppm; PPP around 5 cm horizontal  | **50 Hz** | Higher than UM960; design for several hundred mW plus antenna power | 3× UART; firmware-dependent SPI, I²C and CAN; RTCM 3.x  | RTK, PPP, Galileo HAS, BeiDou PPP and Heading2 capability | 17.0 × 22.0 × 2.6 mm | **$188 at MOQ 5, ~$158 at 250**; moderate marketplace stock | Feature-rich alternative to ZED-X20P, particularly for high-rate positioning and satellite-delivered corrections. ([en.unicorecomm.com][7]) |
| **Septentrio** | **mosaic-X5**  | Full multi-band/all-constellation GNSS  | Horizontal **0.6 cm + 0.5 ppm**; vertical 1 cm + 1 ppm; about 7 s initialization  |  **100 Hz** |  Approximately **0.67–0.93 W** in common RTK configurations | Multiple UART, USB, Ethernet/SDIO-capable system interfaces; RTCM; event inputs and precise PPS | Base and rover; sophisticated AIM+ anti-jamming/spoofing; integrity monitoring; extensive raw-data processing | Approximately 31.5 × 31.5 mm | Around **$550** for module; good authorized stock | Premium industrial/scientific choice when interference resistance, diagnostics and 100 Hz output justify the cost and power. ([septentrio.com][8])  |

[1]: https://quectel.com/content/uploads/2024/03/Quectel_LC29H_Series_GNSS_Specification_V1.7.pdf?utm_source=chatgpt.com "Quectel LC29H Series"
[2]: https://www.quectel.com/product/gnss-lc29h/?utm_source=chatgpt.com "GNSS LC29H series"
[3]: https://www.u-blox.com/en/product/neo-f9p-module?legacy=Curr&utm_source=chatgpt.com "NEO-F9P module"
[4]: https://www.u-blox.com/en/product/zed-f9p-module?utm_source=chatgpt.com "ZED-F9P module"
[5]: https://www.u-blox.com/en/zed-x20p?utm_source=chatgpt.com "ZED-X20P"
[6]: https://en.unicorecomm.com/products/um960/?utm_source=chatgpt.com "Unicore Communications: Multi-Frequency UM960 GLONASS GPS GNSS RTK System"
[7]: https://en.unicorecomm.com/products/um980/?utm_source=chatgpt.com "Unicore Communications: UM980 RTK GNSS L1 L2 L5 GPS, GLONASS Galileo E5A E6 HAS"
[8]: https://www.septentrio.com/en/products/gnss-receivers/gnss-receiver-modules/mosaic-x5?utm_source=chatgpt.com "mosaic-X5 highly-accurate low power GNSS / GPS module"
