# ERC warning dispositions — 2026-09-20

KiCad ERC reports zero errors and the following 13 pin-type warnings. Each
connection below was reviewed against its intended circuit function. These
dispositions apply only while the cited symbol pin types and nets remain
unchanged.

| # | Connection reported by ERC | Disposition |
|---:|---|---|
| 1 | U8 pin 1 GND, `Unspecified`, to GND power input | Accepted. The imported MCP1700 symbol types the ground pin as unspecified; the pin is intentionally connected to board GND. |
| 2 | U6 pin 5 SDO, `Bidirectional`, to GND/PWR_FLAG | Accepted. BMP581 SDO is intentionally strapped low to select I2C address `0x46`; the warning arises because the ground net contains a PWR_FLAG. |
| 3 | U7 pin 1 SDO, `Bidirectional`, to GND/PWR_FLAG | Accepted. BMI323 SDO is intentionally strapped low to select I2C address `0x68`; the warning arises because the ground net contains a PWR_FLAG. |
| 4 | U8 pin 3 VIN, `Unspecified`, to passive C23 | Accepted. C23 is the required local MCP1700 input bypass capacitor; the imported regulator symbol uses an unspecified VIN pin type. |
| 5 | U8 pin 2 VOUT, `Unspecified`, to passive C22 | Accepted. C22 is the required local MCP1700 output capacitor; the imported regulator symbol uses an unspecified VOUT pin type. |
| 6 | U5 pin C2 CRST, `Unspecified`, to passive C12 | Accepted. C12 is the required BMM350 CRST capacitor. |
| 7 | U5 pin B2 ADSEL, `Unspecified`, to GND power input | Accepted. BMM350 ADSEL is intentionally strapped low to select I2C address `0x14`. |
| 8 | L1 pin 1, `Unspecified`, to U1 pin 9 L1, `Unspecified` | Accepted. This is one end of the TPS63802 switching-inductor connection. |
| 9 | L1 pin 2, `Unspecified`, to U1 pin 7 L2, `Unspecified` | Accepted. This is the other end of the TPS63802 switching-inductor connection. |
| 10 | U4 pin 1 VIN, `Unspecified`, to passive C21 | Accepted. C21 is the required AP2112 USB-LDO input capacitor; the imported LDO symbol uses an unspecified VIN pin type. |
| 11 | U4 pin 2 GND, `Unspecified`, to GND power input | Accepted. The AP2112 ground pin is intentionally connected to board GND; the imported symbol uses an unspecified pin type. |
| 12 | U4 pin 5 VOUT, `Unspecified`, to passive C24 | Accepted. C24 is the required AP2112 output capacitor; the imported LDO symbol uses an unspecified VOUT pin type. |
| 13 | U4 pin 3 EN, `Unspecified`, to the net containing passive C27 | Accepted. AP2112 EN is intentionally driven by `GNSS_3V3`; C27 is a passive bypass capacitor on that rail. |

**Result: ACCEPTED.** These warnings describe intentional connections and
third-party/custom symbol pin typing. None indicates an open circuit, conflicting
output, or unintended power source. Re-run and re-review ERC if any cited symbol
or net changes.
