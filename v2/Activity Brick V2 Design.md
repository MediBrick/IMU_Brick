# Activity Brick V2 Electronics Design

## Description

The Activity Brick V2 is based on an accelerometer, gyroscope, magnetometer, barometer and optional standard GNSS or RTK GNSS receiver. It connects to an Adafruit Feather ESP32-S3 host processor. The Feather is not part of this PCB; it provides the host interfaces, a LiPo connector, the V_BATtery (`V_BAT`) output, and a 3.3 V output.

The PCB contains footprints for both GNSS options, but they are mutually exclusive assembly options.

## Components

- IMU: BMI323
- Magnetometer: BMM350
- Barometer: BMP581
- Standard GNSS assembly option: MAX-M10S-00B
- RTK GNSS assembly option: ZED-F9P-05B
- External GNSS antenna: selectable separately for the MAX-M10S and ZED-F9P assembly options, either as an internal patch antenna mounted inside the plastic enclosure or as an external antenna connected through an on-board U.FL connector and SMA pigtail cable; see [GNSS Antenna Options](#gnss-antenna-options)

### Datasheets

| Component | File |
|---|---|
| BMI323 (IMU) | `datasheets/BMI323.pdf` |
| BMM350 (magnetometer) | `datasheets/BMM350.pdf` |
| BMP581 (barometer) | `datasheets/bst_bmp581_ds004-2950309.pdf` |
| MAX-M10S-00B (GNSS) | `datasheets/MAX-M10S.pdf` |
| MAX-M10S hardware integration | `datasheets/MAX-M10S_IntegrationManual_UBX-20053088.pdf` |
| ZED-F9P-05B (RTK GNSS) | `datasheets/ZED-F9P.pdf` |
| ZED-F9P hardware integration | `datasheets/ZED-F9P_IntegrationManual_UBX-18010802.pdf` |
| MCP1700 1.8 V and 3.0 V LDOs | `datasheets/MCP1700.pdf` |
| AP2112 alternative LDO | `datasheets/AP2112.pdf` |
| TPS63802 GNSS buck-boost converter | `datasheets/TPS63802.pdf` |
| NCV8705 3.3 V low-noise GNSS LDO | `datasheets/NCV8705.pdf` |


Use the local integration manuals for the detailed MAX-M10S and ZED-F9P application circuits.

For the RTK validation reference antenna, use the [u-blox ANN-MB2 data sheet](https://content.u-blox.com/sites/default/files/documents/ANN-MB2_DataSheet_UBXDOC-963802114-12775.pdf).

## Power Supply and Logic Domains

The devices do not all use the same core supply:

| Rail | Source | Loads |
|---|---|---|
| `3V3` | Adafruit Feather ESP32-S3 3.3 V output | BMI323 VDD/VDDIO, BMP581 VDD/VDDIO, BMM350 VDDIO, digital pull-ups and low-current indicators |
| `1V8` | MCP1700T-1802E/TT from `3V3` | BMM350 VDD only |
| `3V8` | TPS63802 buck-boost converter from Feather `V_BAT` | Input to the NCV8705 3.3 V low-noise LDO |
| `GNSS_3V3` | NCV8705MT33TCG from `3V8` | VCC of the one populated GNSS module (both ZED-F9P VCC_1 and VCC_2), MAX-M10S V_IO, and ZED USB LDO enable; the populated module's VCC_RF output supplies an active antenna through its dedicated bias circuit |
| `ZED_USB_3V3` | Dedicated 3.3 V LDO from USB VBUS, enabled by `GNSS_3V3` | ZED-F9P V_USB only; separate from `GNSS_3V3` |
| `V_BACKUP` | MCP1700T-3002E/TT from Feather `V_BAT` | V_BCKP of the one populated GNSS module |

The BMM350 core VDD accepts only 1.72–1.98 V and its separate VDDIO pin uses `3V3`. 

Interface pins must be high-impedance whenever the associated device supply is off.

### Budget

The saved design powers the selected GNSS module and its antenna from the dedicated `V_BAT` → `3V8` → `GNSS_3V3` path, **not** from the Feather 3.3 V regulator. The Feather 3.3 V rail supplies the sensors, digital pull-ups and indicators. Its stated 500 mA peak regulator capability must still be checked against ESP32-S3 Wi-Fi peaks, Feather support circuits and simultaneous Brick sensor/LED current; the 340 mA ESP32-S3 peak used for preliminary budgeting is not an entire-board current measurement.

For preliminary GNSS-path sizing, allow 100 mA MAX startup or 130 mA ZED acquisition current plus up to 50 mA for an active antenna. At 3.3 V, this is approximately 0.495 W (MAX) or 0.594 W (ZED). Assuming 80% TPS63802 efficiency and 3.8 V NCV8705 input, battery input for the GNSS path is approximately 0.238/0.285 A at 3.0 V or 0.170/0.204 A at 4.2 V, respectively. These are estimates, not verified worst-case limits; they omit startup-capacitor charging, regulator ground currents, host loads, LED combinations and tolerances. See the [power/interface/RF review](KiCAD/reports/power-interface-rf-review-2026-09-21.md) for the open measurements and thermal checks. The shared battery and Feather power path must support simultaneous Wi-Fi and GNSS transients without excessive sag.

### GNSS Power Architecture

```text
Feather V_BAT (3.0–4.2 V)
        |
        v
TPS63802 buck-boost (~3V8)
        |
        v
NCV8705MT33TCG low-noise LDO (GNSS_3V3)
        |
        +---- GNSS VCC
        +---- MAX-M10S V_IO
        +---- GNSS VCC_RF output and selected active-antenna bias network
```

```text
Feather V_BAT (3.0–4.2 V)
        |
        v
MCP1700T-3002E/TT (V_BACKUP, always enabled)
        |
        +---- GNSS V_BCKP
```

TPS63802 configured for ~ 3.8 V to give NCV8705 enough dropout headroom. 

The NCV8705 is low-noise, high-PSRR supply directly connected to the GNSS module without a ferrite bead or series resistor (u-blox ZED-F9P reference supply)

`GNSS_EN` from a non-strapping ESP32-S3 GPIO controls TPS63802 EN. With 100 kΩ pulldown on EN supply defaults off during ESP32 reset and deep sleep. Connect TPS63802 power-good (`PG`) to NCV8705 EN and an optional ESP32-S3 input, and pull `PG` up to `3V8`; the NCV8705 then starts only after the pre-regulator is valid. 

### ZED-F9P development USB interface

Provide an optional USB-C interface for development, configuration, logging and
testing. It is not intended to be externally accessible in the final product.
The receptacle shall be **vertical, with the cable mating axis perpendicular to
the PCB**. The current development assembly specifies GCT `USB4120-03-C`.
Its drawing recommends a 1.00 ± 0.10 mm PCB, whereas the saved board is 1.60 mm.
The four 0.95 mm shell stakes will sit within their holes rather than protrude
through the back; the 16 signal contacts remain surface mounted. This board
thickness is accepted for the optional development connector. Confirm the
shell-stake soldering method with the assembler, plus enclosure height and
cable clearance. The existing GCT USB4105-GF-A is a
horizontal receptacle and does not satisfy this requirement; its footprint
must not be reused for the vertical part.

The receiver always operates from the existing `V_BAT`-powered GNSS regulators.
Connect **VCC_1 (pin 33) and VCC_2 (pin 34) to `GNSS_3V3`**. USB VBUS supplies
only a separate 3.3 V LDO for **V_USB (pin 38)**. Connect the USB LDO's **EN
directly to `GNSS_3V3`**, so its output is enabled only while the receiver's
main supply is present. Use the LDO's integrated enable function; no separate
power-source switch or power mux is required.

```text
V_BAT -> TPS63802 -> NCV8705 -> GNSS_3V3 -> ZED VCC_1, pin 33
                                       +-> ZED VCC_2, pin 34
                                       +-> USB LDO EN

Vertical USB-C VBUS --+--> USB 3.3 V LDO --> ZED_USB_3V3
                     |                         +--> V_USB, pin 38
                     |                         +--> 1 uF to GND
                     |                         +--> 100 kohm to GND
                     +--> USBLC6-2SC6 pin 5 (pin 2 to GND)
```

Keep `ZED_USB_3V3` and `GNSS_3V3` separate, with a common ground. There is no
internal selection between VCC and V_USB: VCC powers the receiver and V_USB
powers the USB interface and indicates host availability. Unplugging USB
leaves GNSS and UART operation running while `GNSS_3V3` remains enabled and
stable. With `GNSS_3V3` off, the USB LDO is disabled; a USB cable alone cannot
operate the receiver. Loss of USB also removes any corrections supplied over
that connection.

Use separate 5.1 kohm CC1 and CC2 pulldowns for the USB-C device port. Join the
receptacle's duplicate D+ contacts and duplicate D- contacts near the connector;
leave SBU contacts unused. Use **USBLC6-2SC6** (SOT23-6L) for D+/D-
steering-diode protection and its integrated VBUS-to-GND ESD clamp, matching
the selected simple USB reference circuit. CC1 and CC2 have only their separate
5.1 kohm pulldowns; no dedicated CC ESD array is populated. Connect connector
VBUS directly to AP2112 VIN and USBLC6 pin 5 (VBUS). This baseline has ESD
protection but no sustained-overvoltage disconnect. The USBLC6 clamp does not
guarantee that a faulty VBUS remains below the AP2112 input limit.

Retain 27 ohm series resistors on USB_DP and USB_DM near the ZED, a 1 uF
capacitor adjacent to V_USB, a 100 kohm V_USB pulldown and the AP2112's 1 uF
input/output capacitors. An additional 100 nF output bypass as shown in the
reference is optional; it does not replace the required 1 uF at V_USB.
The USB LDO EN connects to GNSS_3V3, not VBUS, and its output is ZED_USB_3V3,
not the board's main 3.3 V rail.

Retain UART1 and recovery test access independently of USB. For assemblies
without the USB option, connect V_USB to GND through an assembly-selectable
link and leave USB_DP/USB_DM open. Never populate that grounding link together
with the USB LDO output connection.

References: [ZED-F9P integration manual](datasheets/ZED-F9P_IntegrationManual_UBX-18010802.pdf),
section 3.8.4 and Figure 23; [ZED-F9P-05B datasheet](datasheets/ZED-F9P.pdf),
pin assignment and USB supply specifications. Verify the final connector,
LDO and protection symbols/footprints against their exact manufacturer drawings
before schematic or PCB implementation.

## GNSS Antenna Options

Antenna selection is deferred until the desired size, receiver population, and required positioning performance are known. 

The MAX-M10S can use a passive or active L1 antenna. The ZED-F9P-05B
requires an **active L1/L2** antenna for its dual-band RTK operation. 

A broader L1/L2/L5 antenna is electrically acceptable and may aid future receiver reuse,
but the ZED-F9P-05B itself does not receive L5.

Each GNSS path terminates at its own on-board **Hirose U.FL-R-SMT-1(10)**
connector. The MAX and ZED RF nets, connectors, ESD protectors and bias branches
are electrically independent and are never joined. For an **external antenna**,
use a short U.FL-to-SMA pigtail cable.

For gain passive antennas normally quote peak element gain, 
active antennas may quote LNA gain or total gain. 
Availability and one-piece prices are distributor snapshots checked 2026-09-05 and must be
rechecked before the BOM is released.

### Standard GNSS candidates for MAX-M10S

| Antenna | Type | Bands | Active voltage and current | Published gain | Approximate size and connection | Mounting | MAX-M10S | Availability and indicative cost |
|---|---|---|---|---|---|---|---|---|
| [Adafruit 2461](https://www.adafruit.com/product/2461) | Passive, embedded patch | GPS L1 (1575.42 MHz); other constellations not specified | 0 V; no bias current | Approximately 1 dBi | 15 × 15 × 6.8 mm; 50 mm U.FL cable | **Internal**, plugs directly into J2 (Hirose U.FL); mount sky-facing inside the plastic enclosure | **Budget internal candidate**; leave JP4 open and validate reception in the enclosure | Approximately US$3.95; supplier snapshot checked 2026-10-31 |
| [Abracon AANI-AP-0200-1](https://abracon.com/datasheets/AANI-AP-0200.pdf) | Active, embedded patch with pre-filtering | GPS L1 / Galileo E1 / GLONASS G1 / QZSS L1 / SBAS L1; BeiDou B1 not specified | 1.8–5.0 V; 5 ± 3 mA | 0.8 dBic typical peak patch gain (0.16–2.1 dBic) on a 70 × 70 mm ground plane; separately, 15 ± 3 dB LNA gain | 18 × 18 × 6.6 mm; 100 mm U.FL/MHF1 cable | **Internal**, adhesive mount; plugs directly into J2 (Hirose U.FL); mount sky-facing inside the plastic enclosure | **Preferred budget internal active candidate for testing**; close JP4, verify antenna voltage under load, validate ground plane/enclosure reception, and evaluate receiver internal-LNA bypass mode | [DigiKey 535-AANI-AP-0200-1-ND](https://www.digikey.com/en/products/detail/abracon-llc/AANI-AP-0200-1/26813086); approximately US$6.44; supplier snapshot checked 2026-11-01 |
| [Abracon AANI-AP-0158-1](https://abracon.com/datasheets/AANI-AP-0158.pdf) | Active, embedded patch with pre-filtering | GPS L1 / Galileo E1 / GLONASS G1 / BeiDou B1 (1561 MHz) / QZSS L1 / SBAS L1 | 3.0–5.0 V; 15–25 mA | Typical RHCP patch gain: 4.0 dBic L1/E1, 4.6 dBic G1, 3.8 dBic B1, on a 70 × 70 mm ground plane; separately, 28 ± 2 dB LNA gain | 27.2 × 27.2 × 9.3 mm; 100 mm U.FL/MHF1 cable | **Internal**, adhesive mount; plugs directly into J2 (Hirose U.FL); mount sky-facing inside the plastic enclosure | **Internal active candidate with BeiDou B1 coverage**; close JP4, verify at least 3.0 V at the antenna under load (limited margin through bias network), validate ground plane/enclosure reception, and evaluate receiver internal-LNA bypass mode | [DigiKey 535-AANI-AP-0158-1-ND](https://www.digikey.com/en/products/detail/abracon-llc/AANI-AP-0158-1/26813087); [Mouser](https://www.mouser.com/en/ProductDetail/ABRACON/AANI-AP-0158-1?qs=CoAU%2FpHVZXyZDb8RMUIcDw%3D%3D) snapshot approximately US$7.26; checked 2026-11-01; recheck DigiKey price |
| [Molex 2066400001](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/productspecificationpdf/206/206640/2066400001-PS.pdf) | Active, embedded patch | GPS L1 / Galileo E1 / GLONASS G1 / BeiDou B1 | 2.7–3.3 V; 8.5 ± 3 mA at 3.0 V | 4.5 dBic peak patch gain on a 70 × 70 mm ground plane; separately, 28 ± 3 dB LNA gain | 25 × 25 × 6.5 mm; integrated ground plane; 60 mm U.FL cable | **Internal**, plugs directly into J2 (Hirose U.FL); mount sky-facing inside the plastic enclosure | **Budget internal active candidate**; close JP4, verify 2.7–3.3 V at the antenna under load, and validate ground plane/enclosure reception | [DigiKey WM21807-ND](https://www.digikey.com/en/products/detail/molex/2066400001/9094611); approximately US$11.86; supplier snapshot checked 2026-11-01 |
| [SparkFun GPS-14986](https://www.sparkfun.com/gps-gnss-magnetic-mount-antenna-3m-sma.html) | Active, magnetic-mount puck | GPS L1 / GLONASS G1; specified range 1575–1610 MHz | 3–5 V; approximately 10 mA | 28 dB LNA gain | 50 × 38 × 17 mm; 3 m cable with SMA connector | **External**, via U.FL-to-SMA pigtail and bulkhead jack; magnetic base for a metal mounting surface | **Budget external candidate**; close JP4 and verify at least 3.0 V at the antenna under load | Approximately US$16.50 plus pigtail; supplier snapshot checked 2026-10-31 |
| [Taoglas TS.15.0111](https://www.taoglas.com/product/ts-15-0111-accura-passive-direct-mount-antenna-covering-all-gps-glonass-galileo-beidou-bands/) | Passive, direct mount, IP67 | L1/B1/G1/E1 | 0 V; no bias current | 1.2–2.3 dBi peak, band dependent | Ø27.25 × 60 mm; SMA male | **External**, via U.FL-to-SMA pigtail and bulkhead jack | **Suitable** where minimum power matters and the RF run is short | Regional stock; approximately US$60 or €49 |
| [Taoglas TS.16.0111](https://www.taoglas.com/datasheets/TS.16.0111.pdf) | Active, direct mount, IP67 | L1/B1/G1/E1 | 1.8–5.5 V; approximately 12 mA at 3 V | 27.9–28.9 dB active gain at 3 V | Ø27.25 × 60 mm; SMA male | **External**, via U.FL-to-SMA pigtail and bulkhead jack | **Preferred external option** | Widely stocked; approximately €52 or US$60 |

The internal Adafruit 2461 patch plugs straight into the MAX-M10S J2 U.FL
connector and is mounted inside the enclosure, with JP4 open. The internal
active Molex 2066400001 also plugs directly into J2, with JP4 closed; verify
its 2.7–3.3 V supply range under load and validate its ground plane and enclosure
placement. Molex specifies 4.5 dBic peak patch gain on a 70 × 70 mm ground
plane and separately specifies 28 ± 3 dB LNA gain; these are different quantities.
The module includes its own ground plane. The [Molex application specification](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/applicationspecificationspdf/206/206640/2066400001-AS.pdf)
describes testing the compact module, but does not establish a mandatory external
metal plate or guarantee 4.5 dBic with only the integrated ground plane. Validate
the installed configuration before relying on that peak-gain figure. The external
SparkFun GPS-14986 puck and direct-mount SMA options (TS.15, TS.16) require the U.FL-to-SMA pigtail cable
and a bulkhead jack at the faceplate; they are no longer mated straight to a
board-edge SMA jack.

### RTK GNSS candidates for ZED-F9P

| Antenna | Type | Bands | Active voltage and current | Published gain | Approximate size and connection | Mounting | MAX-M10S | ZED-F9P-05B | Availability and indicative cost |
|---|---|---|---|---|---|---|---|---|---|
| [Taoglas AHP2258.07.0060A](https://www.taoglas.com/datasheets/AHP2258.07.0060A.pdf) | Active, embedded patch | L1/L2 | 1.8–5.5 V; approximately 5 ± 2 mA | 24.3–29.5 dB LNA/filter gain, band dependent | 35 × 35 × 12.4 mm assembly; 60 mm U.FL cable | **Internal**, plugs directly into the on-board U.FL connector | Electrically suitable but over-specified | **Preferred compact internal RTK option**; validate its ground plane and enclosure | Stocked; approximately US$31 |
| [Taoglas GPDF357B](https://www.taoglas.com/product/passive-gps-patch-antenna-gpsl1l2/) | Passive embedded patch | L1/L2 | 0 V; no bias current | Approximately 2.8 dBi peak | 35 × 35 × 7.15 mm; pin feed | **Internal**, mechanically integrated, needs a matched feed/ground plane | Suitable for L1 if matched and mechanically integrated | **Not directly suitable**; ZED-F9P requires an active antenna | Mixed stock; approximately US$18 |
| [u-blox ANN-MB-00](https://content.u-blox.com/sites/default/files/documents/ANN-MB_DataSheet_UBX-18049862.pdf) | Active, external magnetic-mount antenna | L1/L2/E5b/B2I; GPS, GLONASS, Galileo and BeiDou | 3.0–5.0 V; typically 15 mA (specified at 5 V) | Typical patch gain: 3.5 dBic L1, 0–2 dBic L2/E5b/B2I on a Ø150 mm ground plane; separately, 28 ± 3 dB LNA gain and approximately 21.4–22.4 dB gain after the 5 m cable (specified at 5 V) | 82 × 60 × 22.5 mm; 5 m cable with SMA male | **External**, magnetic base or screw mount; via U.FL-to-SMA pigtail and bulkhead jack to J3 | Electrically suitable for L1 with compatible bias; use separate MAX J2 path and close JP4 | **Budget external RTK candidate**; leave JP11 closed, verify at least 3.0 V at the antenna under load, and validate installation/ground plane | [Future Electronics](https://www.futureelectronics.com/p/semiconductors--wireless-rf--antennas--gps-antennas/ann-mb-00-u-blox-6120194); listed in stock, approximately US$38.66; supplier snapshot checked 2026-11-01 |
| [u-blox ANN-MB2-00](https://content.u-blox.com/sites/default/files/documents/ANN-MB2_DataSheet_UBXDOC-963802114-12775.pdf) | Active, external reference antenna | L1/L2/L5/E6/B3/L | 3.0–5.0 V; approximately 15 mA | Approximately 31 dB LNA gain and 23 dB total gain after its 5 m cable | 108.5 × 92.9 × 24.7 mm; 5 m cable with SMA male | **External**, via U.FL-to-SMA pigtail and bulkhead jack | Electrically suitable but large and unnecessary for L1 GNSS | **Preferred validation/reference option** | In production and stocked; approximately US$81 |
| [Taoglas TS.125.0111W](https://www.taoglas.com/datasheets/TS.125.0111W.pdf) | Active, direct mount, IP67 | L1/L2/L5/L-band | 2.0–5.5 V; 7–13 mA | 25.9–32.7 dB active gain at 3 V, band dependent | Ø40.5 × 58.5 mm; SMA male | **External**, via U.FL-to-SMA pigtail and bulkhead jack | Electrically suitable but over-specified | **Preferred external compact RTK option** | Limited/regional stock; approximately US$365 (€300 class) |

The GPDF357B is included to show the passive dual-band size/cost tradeoff, but
it must not connect directly to the ZED-F9P. Adding a suitable low-noise
amplifier and filters would turn it into an active antenna subsystem that must
be validated against the ZED-F9P gain, noise, linearity, and out-of-band
rejection requirements. The internal patch option (AHP2258) plugs straight
into the on-board U.FL connector; the external SMA options (ANN-MB, ANN-MB2, TS.125)
require the U.FL-to-SMA pigtail cable and a bulkhead jack at the faceplate.

### PCB antenna interface and bias selection

- Provide a mechanically supported, board-mounted, 50 Ω **Hirose
  U.FL-R-SMT-1(10)** connector for each mutually exclusive receiver path. This
  reverts the board-edge SMA jack back to an on-board miniature connector so
  an internal patch antenna's U.FL cable can plug in directly, or a
  **U.FL-to-SMA pigtail cable** can route the RF signal to a bulkhead SMA jack
  on the enclosure faceplate for an external antenna. Choose the exact
  connector has a project-local symbol, footprint and STEP model. Confirm cable
  routing and enclosure clearance before placement is frozen.
- Keep the MAX-M10S and ZED-F9P U.FL paths independent. Populate only the U.FL
  connector, matching network, protection, and bias parts associated with the
  installed receiver. Do not use a splitter or join the paths.
- Put the antenna-power solder jumper in the **DC bias branch**, never in series
  with the RF trace. Keep the MAX jumper normally open because MAX can use a
  passive antenna. Make the ZED jumper normally closed because ZED-F9P-05B
  requires an active antenna; cutting the trace disables bias for measurements
  or an externally powered antenna without interrupting the RF path.
- Feed the closed jumper from the populated module's `VCC_RF` output through
  the specified current-limit/protection component and RF choke. Place the
  bypass capacitor on the supply side of the choke and keep the bias tee and RF
  protection layout compact.
- For MAX-M10S, leave the jumper open for a passive antenna and bridge it for an
  active antenna after checking the antenna voltage/current rating. For
  ZED-F9P, use VCC_RF through a 10 Ω current-limiting resistor, a 100 nF shunt
  capacitor, and Murata LQG15HS47NJ02D (47 nH) into `GNSS_RF_ZED`. u-blox
  requires the bias choke to exceed 500 Ω across 1–1.8 GHz and specifies at
  least 300 mA current capability. Keep the branch short and beside RF_IN.

`VCC_RF` is the antenna-voltage source; the resistor, capacitor, and choke do
not generate a voltage. They limit fault current, filter the supply, and inject
DC onto the RF trace while presenting high impedance to the GNSS signal. The
voltage at the antenna is therefore approximately `VCC_RF` minus the voltage
drop across the 10 Ω resistor and choke. The current ZED circuit uses the
simple u-blox bias topology and does not connect `ANT_OFF`, `ANT_DETECT`, or
`ANT_SHORT_N`, so it provides no automatic antenna fault detection or shutdown.
JP11 is the manual bias disconnect.

The two receiver paths may use the same connector and protection-device types,
but their bias-network values must follow the receiver-specific integration
manual:

| Receiver/reference | Series resistor | Shunt capacitor | RF choke | Default bias state |
|---|---:|---:|---:|---|
| MAX-M10S u-blox reference | 10 Ω, 0.25 W minimum; LCSC candidate is 0.75 W, with sustained-short behavior still to verify | 10 nF | Murata `LQG15HN27NH02D`, 27 nH, greater than 500 Ω at L1 | JP4 open; close for an active antenna |
| ZED-F9P u-blox reference used here | 10 Ω; design uses 1 W | 100 nF | Murata `LQG15HS47NJ02D`, 47 nH, greater than 500 Ω from 1–1.8 GHz | JP11 normally closed |
| SparkFun GPS-RTK2 ZED-F9P implementation | 33 Ω | 47 pF | Murata `LQW15ANR12J00D`, 120 nH | Always connected |

SparkFun's network is a board-specific alternative, not the MAX-M10S network.
Keep the u-blox ZED reference values for this design unless RF measurement and
antenna-fault requirements justify a tested alternative. An active dual-band
L1/L2 antenna selected for ZED may also receive L1 signals for MAX, but a
passive or L1-only MAX antenna is not a valid ZED-F9P antenna. The board retains
two separate connectors and RF networks even when the same antenna model could
serve both assembly options.

Selected bias components and PCB footprints:

| Receiver | Reference | Selected component | KiCad footprint |
|---|---|---|---|
| MAX-M10S | R40, current limiter | Vishay `CRCW121010R0FKEAHP` (LCSC `C844442`), 10 Ω, 1%, 0.75 W; short-fault dissipation review open | `Resistor_SMD:R_1210_3225Metric` |
| MAX-M10S | C16, bias filter | Murata `GRM155R71C103KA01J`, 10 nF, 10%, 16 V, X7R | `PCM_SparkFun-Capacitor:C_0402_1005Metric` |
| MAX-M10S | L2, RF choke | Murata `LQG15HN27NH02D`, 27 nH, 3%, 300 mA | `Inductor_SMD:L_0402_1005Metric` |
| ZED-F9P | R32, current limiter | Bourns `CMP2010-FX-10R0ELF`, 10 Ω, 1%, 1 W, high-power anti-surge | `Resistor_SMD:R_2010_5025Metric` |
| ZED-F9P | C20, bias filter | Murata `GRM155R71C104JA88D`, 100 nF, 5%, 16 V, X7R | `PCM_SparkFun-Capacitor:C_0402_1005Metric` |
| ZED-F9P | L3, RF choke | Murata `LQG15HS47NJ02D`, 47 nH, 5%, at least 300 mA | `Inductor_SMD:L_0402_1005Metric` |

Both capacitors and both RF chokes are therefore 0402/1005 metric. The MAX
datasheet lists 250 mA as an **absolute maximum** VCC_RF source current, not
a current-limit threshold. At 250 mA, 10 Ω dissipates 0.625 W; a direct short
with a 3.3 V source would instead imply 1.09 W (1.30 W at 3.6 V), unless the
source voltage collapses or a verified protection circuit interrupts the
fault. Do not approve the 0.75 W R40 for a sustained antenna short based only
on the 250 mA absolute-maximum rating.
The MAX current limiter is 1210/3225 metric and the ZED current limiter is 2010/5025
metric. At the specified 50 mA operating limit, either
10 Ω resistor dissipates only 25 mW. Under a direct short, the ZED absolute
maximum of 300 mA corresponds to 0.9 W and the MAX absolute maximum of 250 mA
corresponds to 0.625 W. u-blox lists 0.25 W for the MAX reference resistor, but
the present simple bias branches do not implement automatic short shutdown.
The MAX resistor is presently rated 0.75 W, while the ZED resistor is rated
1 W. Neither receiver's absolute-maximum VCC_RF current is a guaranteed
short-circuit clamp; sustained-fault behavior remains to be tested. Maintain
adequate pad copper and apply each manufacturer's temperature derating.

```text
MAX VCC_RF -- 10 ohm, 0.75 W, 1210 -- normally-open JP4 --+-- 27 nH choke, 0402 --+
                                                   |                  |
                                            10 nF, 0402 to GND       +-- GNSS_RF_MAX -- J2 U.FL
MAX RF_IN ------------------------------------------------------------+
```

JP4 remains open for a passive MAX-M10S antenna. Bridge JP4 only when
installing a voltage-compatible active antenna; opening or closing JP4 does
not interrupt the continuous `MAX RF_IN` to `GNSS_RF_MAX` RF path.

```text
ZED VCC_RF -- 10 ohm, 1 W, 2010 -- normally-closed JP11 --+-- 47 nH choke, 0402 --+
                                                     |                  |
                                             100 nF, 0402 to GND       +-- GNSS_RF_ZED -- J3 U.FL
ZED RF_IN --------------------------------------------------------------+
```

Initial selection recommendation: use ADFGP.25A or GP.1575.25.4.A.02 with
MAX-M10S when an internal patch antenna mounted inside the enclosure is
wanted, or TS.16.0111/TS.15.0111 through the U.FL-to-SMA pigtail when an
external antenna is wanted. Use AHP2258 as the internal RTK patch option, or
ANN-MB2/TS.125 through the U.FL-to-SMA pigtail as the external RTK option; ANN-MB2
remains the validation baseline. Do not freeze the production antenna in the
BOM until these mechanical and RF tests are complete.

## Component Categories

1. **Power regulation** – retain a dedicated 1.8 V LDO for BMM350 VDD. Power the selected GNSS module from the `V_BAT`-powered TPS63802 approximately 3.8 V buck-boost and NCV8705 3.3 V low-noise LDO. Use a separate, always-enabled MCP1700 3.0 V LDO for GNSS backup power.
2. **RF antenna connectors and bias selection** – provide two independent on-board U.FL (miniature) connector RF paths: one dedicated to MAX-M10S and one dedicated to ZED-F9P. Support either a direct-plug internal patch antenna or a U.FL-to-SMA pigtail cable to a bulkhead jack for an external antenna. Give each path a DC-branch solder jumper so active-antenna power can be disabled without breaking the RF path. Populate only the connector and RF components associated with the installed GNSS module. Do not use an RF splitter.
3. **Selectable GNSS antennas** – select the standard-GNSS and RTK antennas independently using the tables above. Use ANN-MB2-00 as the ZED-F9P validation reference, but defer the production choice until enclosure and RF testing are complete.
4. **GNSS backup power** – derive `V_BACKUP` from the Feather LiPo `V_BAT` output. A raw LiPo can reach 4.2 V, exceeding the 3.6 V absolute maximum of both GNSS V_BCKP inputs, so it must not connect directly. The MCP1700-3.0 may enter dropout near the bottom of the V_BATtery range, but its output remains within the GNSS V_BCKP operating range while the V_BATtery remains above the system cutoff.
5. **ESD and surge protection** – protect each antenna connector and all externally exposed USB or digital lines using parts with capacitance appropriate for that interface.
6. **ZED-F9P USB interface** (development option) – use a vertical USB-C receptacle and a separate VBUS-powered 3.3 V LDO enabled by `GNSS_3V3`, as specified in [ZED-F9P development USB interface](#zed-f9p-development-usb-interface). Both VCC_1 and VCC_2 remain powered by `GNSS_3V3`; no power mux is required. If USB is omitted, connect ZED-F9P V_USB to ground and leave USB_DP/USB_DM open.
7. **Host/board interconnect** – provide 2.54 mm header connections to the Feather, including multiple ground contacts and adequate power contacts.
8. **Status indicators** – provide optional power, GNSS-fix and RTK-status LEDs with assembly options so their current can be removed for low-power operation.
9. **Service interface** – provide UART and control-signal test points for configuration, recovery and firmware updates. The GNSS modules do not use an exposed SWD programming interface.

## Suggested Active Components

| Category | Suggested part | Notes |
|---|---|---|
| BMM350 1.8 V regulation | **MCP1700T-1802E/TT** | Supplies BMM350 VDD only; approximately 1.6 µA quiescent current. Alternative: AP2112N-1.8. |
| GNSS pre-regulator | **TPS63802DLAR** | Buck-boost from the 3.0–4.2 V `V_BAT` rail to approximately 3.8 V. Approximately 11 µA operating quiescent current; true shutdown/load disconnect; controlled by `GNSS_EN`. |
| GNSS final 3.3 V regulation | **NCV8705MT33TCG** | 500 mA low-noise, high-PSRR LDO recommended in the u-blox ZED-F9P reference supply. Input from the approximately 3.8 V pre-regulator; EN driven by TPS63802 `PG`. |
| GNSS backup power | **MCP1700T-3002E/TT** | Produces nominal 3.0 V from the LiPo `V_BAT` rail for the populated module's V_BCKP input. |
| ZED-F9P V_USB detection supply | **AP2112K-3.3TRG1** | Input from USB VBUS; EN connected to `GNSS_3V3`; output `ZED_USB_3V3` feeds only V_USB. Both ZED VCC_1 and VCC_2 remain on `GNSS_3V3`. Only populate with the development USB option. |
| GNSS antenna | **Select from the GNSS Antenna Options tables** | Choose independently for standard GNSS and RTK. ANN-MB2-00 is the ZED-F9P reference, not a mandatory production antenna. |
| RF antenna connectors | **Two Hirose U.FL-R-SMT-1(10)** | Use one connector for `GNSS_RF_MAX` and a second connector for `GNSS_RF_ZED`; never join the paths. Project-local symbol, footprint and STEP are present. Use a U.FL-to-SMA pigtail and bulkhead SMA jack for an external antenna. |
| RF ESD protection | **Nexperia PESD0402-140** | Verify capacitance, working voltage and layout against the RF interface. |
| USB ESD protection | **STMicroelectronics USBLC6-2SC6**, SOT23-6L | Two data channels with an integrated VBUS clamp; CC1/CC2 use only their 5.1 kΩ pulldowns. Replaces the unavailable PRTR5V0U2F selection. Mouser listed stock on 2026-09-17; recheck at purchase. |
| USB interface | **GCT `USB4120-03-C`** | Vertical development/test option, not externally accessible in the final product. On the 1.60 mm board its 0.95 mm shell stakes do not protrude through the back; signal contacts are surface mounted. Confirm shell-stake soldering and cable/enclosure access with the assembler. |
| Host/board interconnect | **2.54 mm pin header** | Molex KK or equivalent header/socket. |
| Status indicators | **Everlight 19-217/GHC-YR1S2/3T** | Optional power, GNSS-fix and RTK-status indicators. |
| Service header | **Samtec FTSH-105** | UART and control/test header; it is not an SWD interface for the GNSS modules. |

## Suggested Passive Components

- **BMI323**
  - VDD decoupling – 100 nF
  - VDDIO decoupling – 100 nF
- **BMM350**
  - VDD (1.8 V) decoupling – 100 nF
  - VDDIO (3.3 V) decoupling – 100 nF
  - CRST capacitor – Samsung `CL21B225KOFNNNE` (LCSC `C28234`), 2.2 µF, 16 V, X7R, 10%, 0805/2012; place immediately beside CRST and GND. This stocked replacement for the obsolete Bosch-recommended TDK part is an accepted engineering exception: Samsung does not specify nonmagnetic construction, so verify installed-board magnetometer offsets during prototype validation.
- **BMP581**
  - VDD decoupling – 100 nF
  - VDDIO decoupling – 100 nF
  - VDD inrush limiter – 10 Ω in series with the VDD supply branch
  - VDDIO inrush limiter – 10 Ω in series with the VDDIO supply branch
  - Place each 100 nF capacitor after its 10 Ω resistor, next to the corresponding sensor pin
- **MAX-M10S assembly option**
  - VCC decoupling – 100 nF + 1 µF
  - V_IO decoupling – 100 nF
  - V_BCKP decoupling – 100 nF
  - Active-antenna current-limit resistor – Vishay `CRCW121010R0FKEAHP` (LCSC `C844442`), 10 Ω, 1%, 0.75 W, 1210; sustained-short behavior requires verification
  - Active-antenna bias capacitor – Murata `GRM155R71C103KA01J`, 10 nF, 10%, 16 V, X7R, 0402
  - Active-antenna bias choke – Murata `LQG15HN27NH02D`, 27 nH, 3%, 300 mA, 0402; verify the installed RF impedance with the final layout and antenna
  - Active-antenna power jumper – normally-open solder jumper in the VCC_RF bias branch; leave open for passive antennas and bridge only for voltage-compatible active antennas
  - RF matching pi-network footprints – normally DNP; tune only if measurements require it
  - Do not add a redundant RF series DC-block capacitor; MAX-M10S RF_IN includes an internal DC block
- **ZED-F9P assembly option**
  - VCC decoupling at the module – 100 nF + 1 µF with a short, low-impedance connection to both VCC pins
  - V_BCKP capacitor – 2 µF placed at V_BCKP
  - V_USB capacitor – C28, 1 µF placed at V_USB when USB is populated
  - USB_DM and USB_DP series resistors – R38 and R39, 27 Ω each, placed close to the module
  - V_USB discharge/pulldown resistor – R41, 100 kΩ
  - AP2112 V_USB LDO input/output capacitors – C21 and C24, 1 µF X5R/X7R at each pin
  - USB-omitted V_USB grounding link – JP14, normally open; close only when U4 and the development USB option are omitted
  - Active-antenna bias filter – Murata `GRM155R71C104JA88D`, 100 nF, 5%, 16 V, X7R, 0402
  - Active-antenna bias choke – Murata `LQG15HS47NJ02D`, 47 nH, 5%, greater than 500 Ω from 1–1.8 GHz, at least 300 mA, 0402
  - Active-antenna current-limit resistor – Bourns `CMP2010-FX-10R0ELF`, 10 Ω, 1%, 1 W, 2010 high-power anti-surge resistor; LCSC `C1880468`
  - Active-antenna power jumper – solder jumper in the VCC_RF bias branch; normally closed because ZED-F9P requires an active antenna
  - RF matching pi-network footprints – normally DNP; tune only if measurements require it
- **TPS63802 GNSS buck-boost pre-regulator**
  - Input capacitor – 10 µF ceramic, placed at VIN and ground
  - Output capacitors – two 22 µF ceramic capacitors, placed at VOUT and ground; account for DC-bias derating
  - Inductor – 0.47 µH with saturation-current and DC-resistance ratings meeting the TPS63802 datasheet; TI example: Coilcraft XFL4015-471ME
  - Approximately 3.8 V feedback divider – 604 kΩ upper resistor and 91 kΩ lower resistor, 1%, producing approximately 3.82 V nominal
  - EN pulldown – 100 kΩ to ground; drive EN from the ESP32-S3 `GNSS_EN` signal
  - MODE – tie high to VIN for forced-PWM operation and minimum output ripple while GNSS is powered
  - PG pull-up – 100 kΩ to `3V8`; route PG to NCV8705 EN and optionally to an ESP32-S3 input
- **NCV8705 3.3 V GNSS LDO**
  - Input capacitor – 10 µF X7R ceramic at IN
  - Output capacitor – 10 µF X7R ceramic at OUT
  - EN – driven by the TPS63802 power-good signal
  - Connect the 3.3 V output directly to the selected GNSS module supply; do not insert a ferrite bead or series resistor in the GNSS VCC path
- **MCP1700-1.8 LDO**
  - Input/output capacitors – separate local 1 µF / 1 µF X7R ceramic capacitors at the LDO pins; retain the BMM350 100 nF VDD and VDDIO capacitors at the sensor
- **MCP1700-3.0 backup LDO**
  - Input/output capacitors – 1 µF / 1 µF X7R ceramic
- **I2C bus**
  - SDA/SCL pull-up resistors – 2.2–4.7 kΩ, one pair for the bus; verify the final value using total bus capacitance and the internal u-blox pull-ups
- **Status LEDs**
  - Series resistor – approximately 1–2.2 kΩ per LED, subject to the selected GPIO drive rating and desired brightness

## Suggested Pin Connections

The exact ESP32-S3 GPIO numbers can be assigned during schematic capture. Use the following electrical connections and named nets.

- **BMI323**
  - CSB – connect to `3V3` to select I2C/I3C operation
  - SDO – connect to GND for the default I2C address `0x68`; connect to VDDIO for `0x69` if required
  - SDA, SCL – connect to the ESP32-S3 sensor I2C bus and use the shared external pull-ups
  - INT1, INT2 – connect the interrupts required by firmware to ESP32-S3 GPIOs or test pads
- **BMM350**
  - ADSEL – connect to GND for I2C address `0x14`; VDDIO selects `0x15`; do not leave floating
  - BYPASS – connect directly to GND
  - CRST – connect through 2.2 µF to GND and keep both traces extremely short. C12 is the selected Samsung `CL21B225KOFNNNE`; its magnetic behavior is not characterized by the manufacturer and must be checked during installed-board magnetometer validation.
  - SDA, SCK – connect to the ESP32-S3 sensor I2C bus; SCK functions as SCL in I2C mode
  - INT – connect to an ESP32-S3 GPIO or test pad; optional if firmware polls the device
- **BMP581**
  - CSB – connect to `3V3` after the VDDIO 10 Ω resistor; hard-wire high for I2C/I3C operation
  - SDO – connect to GND for I2C address `0x46`; VDDIO selects `0x47`
  - SDA, SCL – connect to the ESP32-S3 sensor I2C bus; do not drive these pins while VDDIO is off
  - INT – connect to an ESP32-S3 GPIO or GND; if unused, ground it and keep the interrupt output disabled
- **TPS63802**
  - VIN – connect to Feather `V_BAT`, nominally 3.0–4.2 V
  - EN – connect to ESP32-S3 `GNSS_EN` and add a 100 kΩ pulldown; active high; the pulldown keeps the GNSS supply off when the ESP32 pin floats
  - MODE – connect to Feather `V_BAT` to select forced-PWM operation for minimum ripple while enabled
  - PG – connect to NCV8705 EN and optionally an ESP32-S3 input; add a 100 kΩ pull-up to `3V8`; this sequences the final LDO after the pre-regulator is valid and can provide a firmware-visible power-good signal
- **NCV8705**
  - IN – connect to `3V8` and add the specified local input capacitor
  - OUT – connect directly to `GNSS_3V3` with a low-impedance connection to the selected GNSS supply
- **MAX-M10S**
  - VIO_SEL – leave open to select 3.3 V V_IO operation
  - VCC, V_IO – connect to `GNSS_3V3`; switching both rails off permits true hardware backup; add the specified local decoupling
  - V_BCKP – connect to `V_BACKUP`; this remains powered when `GNSS_3V3` is disabled
  - UART TXD/RXD – connect to an ESP32-S3 UART; this is the preferred host connection when GNSS power gating is used; set the ESP32 pins to high-impedance before shutdown
  - SDA, SCL – route through normally-open solder jumpers and leave them open for the default UART assembly; do not connect an unpowered receiver directly to the always-pulled-up sensor I2C bus
  - SAFEBOOT_N – a 33 Ω series connection to a dedicated host GPIO or test point is electrically acceptable, but the resistor does not prevent safeboot entry if the host holds the signal low during receiver startup. For a robust general-purpose assembly, make the resistor DNP by default; populate it only when the host pin is guaranteed high-impedance or inactive throughout reset and power-up
  - RESET_N – connect to an ESP32-S3 GPIO or test point; keep inactive with the internal pull-up during normal operation
  - TIMEPULSE – connect to an ESP32-S3 GPIO or test point as an optional precise time reference
- **ZED-F9P**
  - D_SEL – leave open to select UART1 plus I2C; grounding D_SEL selects SPI instead
  - ANT_DETECT, ANT_OFF, ANT_SHORT_N – leave unconnected when the optional antenna-supervisor circuit is not implemented; do not ground ANT_DETECT
  - VCC_1 (pin 33), VCC_2 (pin 34) – connect both to `GNSS_3V3` and add the specified low-impedance local decoupling; these pins always receive power from the battery-derived GNSS regulators
  - V_USB (pin 38) – connect only to `ZED_USB_3V3`, the separate AP2112 USB LDO output; C28 is the adjacent 1 µF capacitor and R41 is the 100 kΩ pulldown. Do not join this net to `GNSS_3V3`. JP14 is the mutually exclusive V_USB-to-GND link for assemblies without USB
  - USB_DM (pin 39) – connect through R38, 27 Ω near the module, to the receptacle D- net protected by USBLC6-2SC6
  - USB_DP (pin 40) – connect through R39, 27 Ω near the module, to the receptacle D+ net protected by USBLC6-2SC6
  - V_BCKP – connect to `V_BACKUP`; this remains powered when `GNSS_3V3` is disabled
  - UART1 TXD/RXD – connect to an ESP32-S3 UART as the primary configuration, service, and firmware-update interface
  - UART2 RXD – connect to ESP32-S3 UART TX; the ESP32-S3 obtains RTCM/SPARTN corrections, for example over Wi-Fi/NTRIP, and forwards them to the ZED-F9P
  - UART2 TXD – connect to ESP32-S3 UART RX or a test point for an optional correction/status return path; do not use UART2 as the only service interface
  - SDA, SCL – leave open or route through disabled test links/interface isolation when UART is used; do not connect to an always-pulled-up bus without power-domain isolation
  - SAFEBOOT_N – provide TP8 and leave R28 DNP by default so the pin remains open during normal operation
  - RESET_N – connect to an ESP32-S3 GPIO or test point; the pin has an internal pull-up and should be asserted low only for reset
  - TIMEPULSE – connect to an ESP32-S3 GPIO or test point as an optional precise time reference
  - RTK_STAT – connect to an ESP32-S3 GPIO and the optional JP9/R29/D6 indicator. The 1 kΩ direct LED path draws less than the datasheet's 2 mA characterized digital-output test current at 3.3 V; open JP9 if the indicator is unnecessary
- **AP2112K-3.3TRG1 USB LDO — SOT-25 / SOT-23-5**
  - Pin 1, VIN – connect to `USB_VBUS`, directly from the USB connector VBUS; C21 is the 1 µF X5R/X7R input capacitor
  - Pin 2, GND – connect to the common board ground, shared with the connector and ZED
  - Pin 3, EN – connect directly to `GNSS_3V3`; active high. This enables only the USB LDO while the receiver's main rail is on; no separate switching circuit or power mux is needed
  - Pin 4, NC – leave unconnected
  - Pin 5, VOUT – connect to `ZED_USB_3V3` and ZED V_USB (pin 38); C24 is the 1 µF X5R/X7R output capacitor, separate from local V_USB capacitor C28 and pulldown R41
  - Use the fixed 3.3 V **AP2112K**, not an AP2122 or a different AP2112 package pinout. The local [AP2112 datasheet](datasheets/AP2112.pdf), pages 1–3, specifies the pinout and application capacitors. The selected baseline assumes normal 5 V USB VBUS and does not include an overvoltage-disconnect IC
- **Vertical USB-C receptacle — USB 2.0 device connection**
  - VBUS contacts – join to `USB_VBUS`, AP2112 VIN and USBLC6-2SC6 pin 5; do not connect to `V_BAT` or `GNSS_3V3`
  - D+ contacts A6/B6 – join near the receptacle, connect to the D+ ESD channel, then through the module-side 27 Ω resistor to ZED USB_DP
  - D- contacts A7/B7 – join near the receptacle, connect to the D- ESD channel, then through the module-side 27 Ω resistor to ZED USB_DM
  - CC1 (A5), CC2 (B5) – connect each to its own 5.1 kΩ resistor to GND with no dedicated CC ESD array; do not join CC1 to CC2
  - GND contacts and shield/shell mounting contacts – connect to board GND, following the selected reference circuit; SBU1/SBU2 – leave unconnected. Verify physical pad numbering and shell contacts against the selected vertical receptacle drawing
- **USBLC6-2SC6 USB ESD array — SOT23-6L**
  - Pin 1, I/O1 – connector D-
  - Pin 2, GND – short connection to board GND beside the receptacle
  - Pin 3, I/O2 – connector D+
  - Pin 4, I/O2 – protected D+ toward the ZED USB_DP 27 Ω series resistor
  - Pin 5, VBUS – `USB_VBUS` (5 V), shared with AP2112 VIN; not `GNSS_3V3` or `ZED_USB_3V3`
  - Pin 6, I/O1 – protected D- toward the ZED USB_DM 27 Ω series resistor
  - Pins 1/6 and 3/4 are internally connected pairs for flow-through routing. Use the exact SC6 SOT23-6L footprint; this is not footprint-compatible with PRTR5V0U2F
  - Source: [manufacturer datasheet](https://www.st.com/resource/en/datasheet/usblc6-2.pdf), page 1 functional diagram and SOT23-6L package drawing. Project-local symbol `ActivityBrick:USBLC6-2SC6`, footprint `ActivityBrick:USBLC6-2SC6_SOT23-6L` and linked STEP are imported and checked against [local ST datasheet](datasheets/DS_usblc6-2.pdf)

Only populate the GNSS-specific series links, zero-ohm routing options and pull components for the selected MAX-M10S or ZED-F9P assembly.

### GNSS Power-Down and Wake Sequence

Both GNSS modules support software-requested standby or backup modes, but software standby leaves the GNSS supply and regulator operating. For minimum current during ESP32-S3 deep sleep, use a graceful software request followed by hardware shutdown through TPS63802 EN. The always-on `V_BACKUP` rail preserves the selected receiver's real-time clock and V_BATtery-backed data.

Before ESP32-S3 deep sleep:

1. Send the appropriate u-blox standby/backup command and wait for the command transmission and acknowledgement to complete.
2. Stop the ESP32-S3 UART or I2C peripheral connected to the GNSS module.
3. Configure every ESP32-S3 signal connected to the GNSS module as an input with no internal pull-up or pull-down. This prevents back-powering through an interface pin.
4. Drive `GNSS_EN` low. The TPS63802 enters true shutdown, disconnects its output, and removes `3V8` and `GNSS_3V3`. For the MAX-M10S option, both VCC and V_IO are therefore removed together.
5. Enter ESP32-S3 deep sleep. The external 100 kΩ EN pulldown keeps the GNSS supply off even if the ESP32 GPIO subsequently becomes high-impedance.

After wake:

1. Keep the GNSS interface pins high-impedance and drive `GNSS_EN` high.
2. Wait for TPS63802 `PG` to release high and for the GNSS module power-on interval.
3. Reconfigure the ESP32-S3 UART and any GNSS control pins.
4. Resume communication. Because V_BCKP remained powered, the receiver can perform a warm or hot start when its retained data are valid.

Do not connect GNSS pins to always-powered external pull-ups unless a bus switch or other isolation makes the pins high-impedance when `GNSS_3V3` is off. If software-only standby is selected instead, hardware shutdown may be omitted, but the design must include the GNSS standby current and active regulator current in its sleep-current budget.

## PCB Footprint and Routing Rules

- **BMI323:** Keep a continuous ground reference plane beneath the device, but do not put vias underneath its package. The pin-1 marker is mechanical only and must not be electrically connected. Signal traces may leave the perimeter pads directly; keep the decoupling loops short.
- **BMP581:** A ground plane beneath the package is acceptable. Pin 1 (VDDIO) may be connected to pin 6 (CSB) with a short trace inside the footprint because both are on the post-resistor VDDIO net. Avoid vias beneath the package, minimize board stress, and keep solder paste controlled so that the reflowed solder height provides mechanical decoupling.
- **BMM350:** Define its pad and solder-mask geometry in the project footprint, not with a board-level drawing. The current footprint uses 0.25 mm NSMD copper pads with 0.025 mm radial mask expansion, producing nominal 0.30 mm mask openings on 0.40 mm pitch. Confirm that the PCB assembler can maintain the resulting 0.10 mm mask web. Keep the CRST-to-capacitor and capacitor-to-GND paths extremely short. The `A`, `C`, `1`, and `3` grid labels belong on `F.Fab` only; they are documentation aids and must not appear on silkscreen. Put `REF**` outside the component/courtyard on silkscreen. A large package-body outline may remain on `F.Fab`; an imported `User.Eco2` square has no manufacturing function and should be removed unless it is intentionally converted into a documented rule area.
- **Sensor copper:** Do not remove the ground planes beneath BMI323, BMP581, or BMM350 merely because they are MEMS sensors. Avoid vias directly beneath BMI323 and BMP581, and avoid unrelated switching or high-current routes beneath or near all three sensors.
- **MAX-M10S RF line:** Name the continuous receiver-to-connector RF net `GNSS_RF_MAX` and assign it to the `RF50` net class. Keep the bias jumper, resistor and bypass capacitor in the DC branch; only the RF choke joins that branch to `GNSS_RF_MAX`. Ground all U.FL shell pads and place the low-capacitance RF ESD protector at the connector with a very short ground return.
- **Preliminary two-layer RF geometry:** The present board model is 1.6 mm FR-4 with 1.51 mm dielectric, relative permittivity 4.5, loss tangent 0.02, 35 µm copper and 10 µm solder mask. The provisional grounded-coplanar geometry is approximately 1.0–1.05 mm trace width and 0.20 mm clearance to the top-layer ground pour over a continuous B.Cu ground plane. These are estimates, not controlled-impedance fabrication data; recalculate with the selected fabricator's actual stack-up.
- **RF via fence:** Place grounded 0.60/0.30 mm vias symmetrically about 1.1–1.3 mm from the RF trace center, corresponding to approximately 0.3–0.5 mm from the trace edge to the via-pad edge. Use approximately 1–2 mm pitch, with extra ground vias at the U.FL connector, ESD ground and changes in geometry.

## Component Placement

- **BMM350:** Place as far as practical from the GNSS antenna-bias choke, switching regulators, inductors, V_BATtery current paths, USB connector shell, speakers, magnets, steel fasteners and high-current traces. Prefer documented nonmagnetic capacitors around the sensor. C12 is the accepted Samsung exception and requires installed-board magnetic-offset validation. Keep the CRST capacitor immediately adjacent to CRST and GND.
- **BMI323:** Place on a mechanically rigid region of the PCB, away from board edges, mounting holes, connectors and sources of vibration. Align its axes to the documented Activity Brick coordinate system and mark the axes on silkscreen.
- **BMP581:** Place its pressure opening in clean, still air with a corresponding enclosure vent. Keep it away from heat sources and rapid airflow. Prevent solder flux, conformal coating, adhesive, liquid and particles from entering the pressure port, and minimize PCB bending stress beneath the package.
- **GNSS modules:** Place the populated module close to its dedicated on-board U.FL connector. Keep its RF path short and implement it as a 50 Ω grounded coplanar waveguide with an uninterrupted reference plane and ground-via fence. Keep RF circuitry away from ESP32-S3 clocks, buses, DC/DC switching nodes and the Feather Wi-Fi antenna.
- **Independent RF paths:** Give MAX-M10S and ZED-F9P separate U.FL connectors, ESD protection and antenna-bias branches. Mark both clearly and never connect `GNSS_RF_MAX` to `GNSS_RF_ZED`. Keep each solder jumper entirely in its DC bias branch. Populate the ZED bias link closed by default because its active L1/L2 antenna is mandatory.
- **Internal or external GNSS antenna:** For an internal antenna, plug an embedded patch antenna's U.FL cable directly into the on-board connector and mount the patch inside the plastic enclosure with an unobstructed sky view. For an external antenna, route a U.FL-to-SMA pigtail cable from the on-board connector to a bulkhead SMA jack at the faceplate, with strain support through the pigtail's own mounting hardware. In either case keep the antenna away from the user's body and sources of RF noise or multipath, and embedded patch choices require their specified ground plane and enclosure validation.
- **Power components:** Place every decoupling capacitor beside its device supply pin, before the trace branches to other loads. Keep ZED-F9P VCC routing wide, short and low impedance. Keep the TPS63802 input-switch-inductor-output loop compact and follow TI's recommended layer stack and ground connections. Place the TPS63802 and its shielded inductor away from the BMM350, BMP581, GNSS RF input and antenna paths. Place the NCV8705 close to the selected GNSS supply branch.
- **Feather placement:** Preserve the Adafruit antenna keep-out region and do not place copper, components or the GNSS RF path beneath or immediately in front of the Feather's 2.4 GHz antenna.

## Implementation Audit — 2026-09-13

This audit records the current `KiCAD/Activity_Brick.kicad_sch`, standalone `sensors.kicad_sch`, `power.kicad_sch`, `gnss.kicad_sch`, and `Activity_Brick.kicad_pcb`. A checked item means that the reviewed connectivity or layout feature is present; it does not replace ERC, DRC, manufacturer stack-up confirmation, or assembly review.

### Implemented

- [x] BMI323 CSB is high, SDO is low for address `0x68`, VDD/VDDIO have 100 nF decoupling, both grounds are connected, and both interrupt outputs are exposed.
- [x] BMI323 retains a ground reference plane and has no via directly beneath the package.
- [x] BMP581 VDD and VDDIO each use a 10 Ω feed followed by local 100 nF decoupling; CSB is tied to the post-resistor VDDIO node and SDO is low for address `0x46`.
- [x] BMP581 has no via directly beneath the package; the short pin-1-to-pin-6 connection is electrically valid.
- [x] BMM350 uses 1.8 V VDD and 3.3 V VDDIO, has 100 nF rail decoupling, 2.2 µF on CRST, BYPASS and ADSEL tied to ground, and the correct I2C address selection.
- [x] The BMM350 footprint uses explicit NSMD solder-mask expansion; the former `User.Eco2` body square is absent, grid labels are on `F.Fab`, and the reference is outside the body on `F.Silkscreen`.
- [x] TPS63802 MODE is high at `V_BAT`, EN has a 100 kΩ pulldown, PG has a 100 kΩ pull-up and controls NCV8705 EN, and two 22 µF output capacitors are present.
- [x] NCV8705 input/output capacitors and exposed-pad ground connection are present.
- [x] MCP1700-3.0 has 1 µF input/output capacitors and supplies the GNSS backup rail.
- [x] MAX-M10S VCC and V_IO share the switched GNSS 3.3 V rail, V_BCKP uses the backup rail, VIO_SEL is left open, and UART is the populated/default host interface.
- [x] MAX-M10S SDA/SCL are behind normally-open `JP5`/`JP6` links, avoiding I2C back-powering in the default UART assembly.
- [x] `JP4` is a normally-open antenna-bias jumper in the DC branch, while the RF path remains continuous for passive antennas.
- [x] `GNSS_RF_MAX` is assigned to the `RF50` net class; the U.FL shell pads are grounded, the RF ESD part is near the connector, and a two-sided 2 mm-pitch ground-via fence is present along the long RF run.
- [x] `sensors.kicad_sch`, `power.kicad_sch`, and `gnss.kicad_sch` are instantiated once as hierarchical sheets in the root schematic, and the root netlist contains the subsystem circuitry.
- [x] R32 uses `R_2010_5025Metric` in both the schematic and PCB and is repositioned and routed for Bourns `CMP2010-FX-10R0ELF`. The post-layout DRC reports zero unconnected items and no R32 violations.

### Historical fabrication-readiness verification (stale snapshot, 2026-09-18)

The checked items below record the state reviewed on 2026-09-18. They are
retained as design history and must not be treated as approval of a later PCB
revision or of regenerated manufacturing files.

- [x] MCP1700-1.8 (`U8`) has separate local 1 µF X7R input and output capacitors (`C23` and `C22`). `C14` remains the separate 100 nF BMM350 VDD bypass capacitor.
- [x] ZED uses Bourns `CMP2010-FX-10R0ELF`, 10 Ω, 1%, 1 W in 2010; MAX retains the 1210 footprint with Vishay `CRCW121010R0FKEAHP`, 10 Ω, 1%, 0.75 W as the LCSC candidate. The MAX sustained-short power check remains open. ZED uses Murata `LQG15HS47NJ02D` 47 nH and `GRM155R71C104JA88D` 100 nF; MAX uses Murata `LQG15HN27NH02D` 27 nH and `GRM155R71C103KA01J` 10 nF. Both chokes and both capacitors use 0402 footprints.
- [x] MAX-M10S SAFEBOOT resistor `R12` is DNP by default in both the schematic and PCB. Population is reserved for controlled recovery access. ZED SAFEBOOT resistor `R28` is also DNP by default.
- [x] The BMM350 custom rules allow its verified 0.15 mm fanout and local package clearances. The current DRC reports no active BMM350 violations.
- [x] `GNSS_RF_MAX` and `GNSS_RF_ZED` are both assigned to the `RF50` net class with a 1.05 mm nominal controlled-route width. The intentional transitions are 0.70 mm at the modules/connectors, 0.40 mm in bias branches, and 0.30 mm at ESD branches.
- [x] NCV8705 `U2` exposed-pad thermal vias use 0.30 mm drills with 0.50 mm copper diameters in both the project footprint and placed PCB footprint, satisfying the 0.30 mm drill and 0.10 mm annular-ring board minima.
- [x] The XFL4015 `L1` courtyard no longer produces a malformed-courtyard DRC violation.
- [x] Thermal and jumper-clearance checks pass. ZED-F9P ground pads use solid zone connections, and the selected solder-jumper internal-clearance rule covers `JP1`, `JP3`–`JP6`, `JP8`, and `JP11`–`JP14`. `JP11` uses the normally-closed copper-trace footprint on the PCB.
- [x] Rail names agree between the document and design: `3V8`, `GNSS_3V3`, `V_BACKUP`, `1V8`, `3V3`, and `V_BAT`.
- [x] The ZED-F9P option is synchronized to the PCB, including the separate `GNSS_RF_ZED` path, J3 U.FL connector, Littelfuse PESD0402-140, normally-closed JP11 bias link, Yageo 10 Ω/1 W limiter, 100 nF 0402 filter, and Murata 47 nH 0402 choke.
- [x] Intentional MAX-M10S open pins `LNA_EN` and `VIO_SEL` have no-connect markers. Header pins 14–16 are connected to `RXD2`, `TXD2`, and `RTK_STAT`. Power-input nets have explicit `PWR_FLAG` symbols where required.
- [x] Schematic-to-PCB parity is current: 119 references match, all 424 numbered schematic pins map to PCB pads, and there are zero net mismatches. KiCad DRC reports zero active violations and zero unconnected pads; its 25 reported items are reviewed exclusions. ERC reports zero active errors and 13 active pin-type warnings from third-party symbols; the 10 reported errors and 11 additional warnings are reviewed exclusions.

The automated checks verify connectivity and encoded design rules. Fabrication release still requires the normal manual RF-layout, mechanical, polarity/orientation, assembly-option, and manufacturing-output review. MAX-M10S and ZED-F9P remain mutually exclusive assembly options with separate antenna paths.

### Proposed production-release checklist

Complete this checklist against the exact revision sent to the PCB fabricator
and assembler. Archive the reports and manufacturing outputs with that
revision. A checked automated result verifies only the rules encoded in KiCad;
it does not establish RF, mechanical, assembly, or physical performance.
Checklist states: `[x]` complete, `[-]` partially complete with remaining work
described below, and `[ ]` not yet complete.

#### Design baseline and automated checks

- [x] Save all schematic sheets in KiCad and refill every PCB copper zone.
- [x] Run **Update PCB from Schematic** and confirm that no unexpected
  footprints, nets, or properties are changed by the update. If the design does
  change, repeat the downstream review, ERC/DRC, and freeze steps.
- [x] Confirm schematic-to-PCB parity: all intended symbols have footprints,
  reference designators agree, numbered symbol pins map to the intended pads,
  and KiCad reports no unconnected pads. The archived
  [parity report](KiCAD/reports/freeze-2026-09-19/PARITY.md) records 119
  schematic components, 424 matching numbered pin/pad assignments, and zero
  net mismatches.
- [x] Review the final ratsnest and highlighted nets after zone refill. Check
  ground continuity, thermal-relief connections, neck-downs, copper islands,
  return paths, and clearances around mounting holes and the board perimeter.
  The archived [layout review](KiCAD/reports/freeze-2026-09-19/LAYOUT_REVIEW.md)
  records the connectivity, zone, track-width, thermal, outline, and visual
  copper checks.
- [x] Re-run ERC on the release-candidate revision. Resolve every error and
  review every warning individually. Record the reason for each accepted
  warning instead of relying on a broad exclusion. All 13 warnings have an
  itemized disposition in the archived
  [ERC warning review](KiCAD/reports/freeze-2026-09-19/ERC_WARNING_REVIEW.md).
- [x] Re-run DRC using the selected fabricator's minimum track, clearance,
  annular-ring, via, hole, solder-mask, and board-edge capabilities. Resolve or
  explicitly document every violation and exclusion.
- [ ] Freeze the current schematic and PCB revision and archive verified source hashes.
  The previous [2026-09-19 freeze](KiCAD/reports/freeze-2026-09-19/VALIDATION.md)
  predates the C12 metadata change and R32 PCB update; create a new snapshot
  after the remaining release issues are resolved.

#### Components, footprints, and assembly variants

- [x] Create a separate
  [production BOM workbook](Activity_Brick_Production_BOM.xlsx) from the raw
  KiCad CSV without modifying [Activity_Brick.csv](Activity_Brick.csv). Include
  engineering requirements, known exact manufacturer parts, procurement
  columns, and the original KiCad export for traceability.
- [x] Create separate BOM variants for MAX-M10S production, ZED-F9P
  production without development USB, and ZED-F9P development with USB. The
  workbook excludes the unselected GNSS subsystem from each variant and marks
  the ZED USB components DNP in the production variant.
- [x] Complete the procurement fields with manufacturer and exact ordering code
  for every populated commodity part, LCSC part number where available,
  approved supplier, stock quantity, and stock-check date. The 2026-09-20 stock
  snapshots are accepted; the ZED-F9P-05B Mouser quantity was updated on
  2026-09-21. J1 is DNP, with plated through-holes only. Lifecycle verification
  is not part of this release checklist.
- [x] Finalize the population matrix and generate matching placement variants.
  Verify optional LEDs, jumper states, test features, and every option-specific
  link. Confirm that the unused GNSS module, its RF connector/path, bias parts,
  and indicators are excluded; never populate both GNSS options. Three
  [placement CSVs and the assembly matrix](KiCAD/assembly_variants/README.md)
  specify 53 MAX, 60 ZED Production, and 71 ZED Development placements.
  `J1` and the respective SAFEBOOT resistor are DNP. The MAX default is a
  passive antenna with `JP4` open; the ZED default leaves `JP11` closed.
- [x] Verify every custom symbol pin number and every footprint pad number
  against the exact manufacturer ordering code and package drawing. Check pin 1,
  polarity, connector mating side, U.FL orientation, USB-C contact numbering,
  exposed pads, and NC pins. Do not use the 3D rendering as proof of pinout.
  The [2026-09-21 pin/pad audit](KiCAD/reports/pin-pad-audit-2026-09-21.md)
  records the manufacturer-source comparison and CAD exceptions.
- [-] Review solder-mask and paste apertures for the BMI323, BMM350, BMP581,
  TPS63802, NCV8705 exposed pad, USBLC6-2SC6, MAX-M10S, and ZED-F9P. Confirm the
  BMM350 NSMD requirement, thermal-via treatment, stencil reductions, and the
  assembler's via-in-pad policy. The [2026-09-21 aperture audit](KiCAD/reports/mask-paste-audit-2026-09-21.md)
  confirms the saved CAD geometry. NCV8705 pad 7 now has no in-pad holes; two
  ordinary GND vias sit outside its solder apertures. BMM350 mask-web and
  GNSS-module stencil decisions remain for the fabricator/assembler.
- [-] Confirm capacitor dielectric and DC-bias performance, resistor power
  ratings, inductor saturation current and DCR, nonmagnetic parts near BMM350,
  and voltage ratings at maximum battery and USB voltage. The
  [2026-09-21 passive/rating audit](KiCAD/reports/passive-rating-audit-2026-09-21.md)
  confirms the nominal ratings and documents remaining exact-part DC-bias,
  antenna-short, and installed-board magnetic-offset checks.
- [x] Review all default jumper states and assembly notes, including active-
  antenna bias, I2C links, SAFEBOOT links, USB omission link JP14, status LEDs,
  and the normally closed ZED antenna-bias link JP11. The
  [assembly matrix](KiCAD/assembly_variants/README.md) records the default
  state of each jumper and the USB-specific `JP14` bridge operation.

#### Power, interfaces, and RF review

- [-] Recalculate the worst-case power budget at minimum and maximum battery
  voltage, including regulator efficiency, GNSS acquisition peaks, USB option,
  active-antenna current, LEDs, backup supply, and startup/inrush current. Check
  component temperature rise and copper current capacity. The
  [2026-09-21 power/interface/RF review](KiCAD/reports/power-interface-rf-review-2026-09-21.md)
  corrects the rail allocation and gives preliminary 3.0/4.2 V estimates;
  bounded inrush, simultaneous loads and measured temperature remain open.
- [-] Manually review power sequencing and back-power paths for every powered
  and unpowered state: Feather off/on, `GNSS_EN` off/on, battery connected,
  USB connected/disconnected, and V_BACKUP present. Verify that UART, I2C,
  GPIO, USB VBUS/V_USB, and ESD devices cannot unintentionally power a disabled
  rail. The review records the required host-pin high-impedance behavior and
  the unverified AP2112 EN-high/VIN-zero state.
- [-] Verify USB-C device wiring, independent 5.1 kOhm CC1/CC2 pulldowns,
  D+/D- polarity, ESD flow-through routing, 27 ohm resistor placement, VBUS
  clearance, connector-shell grounding, and AP2112 input/output capacitors.
  Static wiring matches the design; C28 was moved to (131.70, 93.13) mm,
  about 3.1 mm from ZED V_USB pin 38. Review its final trace and ground
  return as part of the manual USB layout check.
- [-] Obtain the actual fabricator stack-up and recalculate both GNSS grounded-
  coplanar waveguides. Confirm trace width/gap with the fabricator or request
  controlled impedance; do not release using only the preliminary FR-4 model.
  The saved board is two-layer, 1.6 mm nominal, with a provisional 1.51 mm
  FR-4 core and 35 µm copper. PCBWay's published stack-up selector covers
  four or more layers, so it does not establish this board's actual two-layer
  core, finished copper, Dk or mask. A provisional arithmetic estimate is
  1.6 − 2(0.035) − 2(0.010) = 1.51 mm between copper layers, assuming
  35 µm finished copper and 10 µm mask on each face; this is the KiCad model,
  not a PCBWay stack-up. Obtain the order-specific values and
  PCBWay's 50 Ω coplanar trace-width/gap review before checking this item.
- [-] Perform a manual RF layout review of both independent paths: uninterrupted
  reference plane, return-via placement, via-fence spacing, connector launch,
  ESD stub and ground inductance, bias-tee branch, choke orientation, and absence
  of copper/route discontinuities. Confirm the unused GNSS path is DNP. The
  tiny ZED RF dangling stub was removed and DRC is clear. Each U.FL has a
  nearby GND via on both sides. The saved PCB has a GND zone and filled
  polygons on both F.Cu and B.Cu; inspect local continuity under both RF
  paths, pad-to-via connections, and the Gerbers.
- [-] Confirm the chosen antenna, cable, and bias voltage/current are compatible.
  Validate active-antenna short-current behavior and passive-antenna operation
  where applicable. Freeze the production antenna ordering code only after the
  enclosure test. Candidate compatibility is documented; production antenna,
  pigtail and enclosure/short-fault tests remain open.

#### Mechanical and manufacturability review

- [ ] Import the final board and STEP assembly into the enclosure model. Check
  board dimensions, mounting-hole locations, fastener heads, component heights,
  Feather headers, vertical USB access, U.FL cable bend radius and strain,
  antenna clearance, and assembly/tool access.
- [ ] Verify the Feather 2.4 GHz antenna keep-out in all copper layers and the
  final enclosure. Verify separation between GNSS antennas/RF paths and the
  ESP32 antenna, switching regulator, digital buses, and user/body locations.
- [-] Confirm BMI323 axis orientation and mechanical rigidity, BMM350 magnetic
  clearance and material choices, and a clean enclosure vent for the BMP581
  pressure port. Ensure assembly cleaning, coating, adhesive, and packaging
  processes cannot contaminate the pressure port. Saved U7 BMI323 and U5
  BMM350 are both on F.Cu at 0°. Viewed from above, both +X axes point up;
  BMI323 +Y points left and +Z out of the board, while BMM350 +Y points
  right and +Z into the board. Map BMM350 readings into the BMI323 frame as
  `(X, -Y, -Z)` (a 180° rotation about X). Confirm the signs with a physical
  orientation test; mechanical rigidity, installed-board magnetic offsets,
  enclosure clearance/materials, and the BMP581 vent/process checks remain.
- [-] Review silkscreen readability, reference/polarity markings, exposed test
  pads, fiducials, tooling needs, board-edge clearances, solderability, and
  hand-rework access with the intended assembler. Obtain assembler approval for
  fine-pitch LGA/BGA parts and bottom-terminated components.

#### Manufacturing-output review

- [ ] Recheck supplier availability immediately before ordering parts, using
  the exact approved manufacturer and supplier numbers in the BOM.
- [ ] Regenerate Gerbers, plated and non-plated drill files, Gerber job file,
  BOM, and component-position files only after the design is frozen. Do not mix
  outputs from different timestamps or revisions.
- [ ] Open the generated Gerbers and drills in an independent viewer. Inspect
  every layer, copper polarity, zone fill, solder-mask openings, paste apertures,
  silkscreen clipping, drill sizes, plated/non-plated classification, slots, and
  the single closed board outline. Compare the viewed output with KiCad.
- [ ] Verify the assembler's coordinate origin, units, top/bottom designation,
  bottom-side mirroring, centroid positions, and component rotations using a
  placement preview. Pay particular attention to connectors, diodes, LEDs,
  sensors, regulators, and GNSS modules.
- [ ] Put board thickness, layer count, copper weight, material/stack-up,
  impedance requirement, surface finish, solder-mask color, silkscreen color,
  minimum finished-hole requirements, panelization constraints, and any special
  via instructions on the fabrication order or drawing.
- [ ] Archive the released KiCad sources, PDF schematic, ERC/DRC reports,
  Gerbers, drills, BOM, placement files, fabrication notes, assembly-variant
  definition, and file checksums under one immutable revision or release tag.

#### Prototype and first-article validation

- [ ] Order a small prototype/first-article build before the production lot and
  inspect it optically for orientation, solder bridges, opens, void-prone pads,
  connector alignment, and pressure-port contamination. Use X-ray inspection
  for hidden joints when the assembler recommends it.
- [ ] Current-limit the first power-up. Measure shorts/resistance before power,
  then verify `1V8`, `3V8`, `GNSS_3V3`, `V_BACKUP`, and USB V_USB at minimum,
  nominal, and maximum expected inputs. Record startup waveforms, ripple,
  sequencing, shutdown discharge, and sleep current.
- [ ] Run a firmware smoke test for sensor identity, configuration, interrupts,
  sample data, axis signs, UART communication, GNSS enable/shutdown/wake, backup
  retention, time pulse, RTK status, and the development USB interface when
  populated.
- [ ] Validate GNSS cold/warm start, satellite reception, antenna-bias voltage
  and current, active-antenna short handling, RF coexistence with ESP32 Wi-Fi,
  and RTK correction/fix operation using the final antenna and enclosure.
- [ ] Calibrate and test the complete unit over the required orientation,
  vibration, temperature, supply-voltage, and use conditions. Include
  magnetometer hard/soft-iron behavior and BMP581 pressure response with the
  final enclosure vent.
- [ ] Define and execute the product-appropriate ESD, radiated/conducted
  emissions, immunity, battery/power, environmental, and regulatory test plan
  before volume production.

USB ESD procurement decision (2026-09-17): select STMicroelectronics USBLC6-2SC6. [Mouser](https://www.mouser.com/ProductDetail/STMicroelectronics/USBLC6-2SC6) reported 74,194 in stock in the retrieved listing. Littelfuse SP3003-02XTG remains a smaller SOT553 alternative requiring its own verified pinout and footprint. The imported PRTR5V0U4D,125 is an unused four-channel reference, not a substitute.
