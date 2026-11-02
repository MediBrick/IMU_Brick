# Datasheets, Footprints, Symbols and 3D files

## External Resources

This is the acquisition checklist for the Activity Brick V2 KiCad project. It
was derived from `Activity Brick V2 Design.md` and checked against the KiCad
10.0.6 libraries installed on 2026-09-03.

USB acquisition update: 2026-09-17. The USB-specific entries below reflect the
development-only vertical USB-C interface. Both ZED VCC pins remain on
`GNSS_3V3`; the separate VBUS-powered AP2112 LDO is enabled by `GNSS_3V3`.
USB library file presence was rechecked; unrelated component status retains
the earlier audit date.

### Acquisition and validation policy

Use sources in this order:

1. Exact manufacturer product page, package drawing, hardware integration
   manual, and manufacturer-supplied CAD model.
2. The installed KiCad 10 library, but only when its symbol pinout and footprint
   match the exact ordering code used by this design.
3. A manufacturer-linked Ultra Librarian model.
4. SnapMagic or SamacSys Component Search Engine.
5. Create a project-local model from the manufacturer drawing.

Useful source entry points:

- [Bosch BMI323 product resources](https://www.bosch-sensortec.com/en/products/motion-sensors/imus/bmi323)
- [Bosch BMM350 product resources](https://www.bosch-sensortec.com/en/products/motion-sensors/magnetometers/bmm350)
- [Bosch downloads, including handling/soldering instructions](https://www.bosch-sensortec.com/en/products/downloads)
- [u-blox MAX-M10S integration manual](https://content.u-blox.com/sites/default/files/MAX-M10S_IntegrationManual_UBX-20053088.pdf)
- [u-blox ZED-F9P integration manual](https://content.u-blox.com/sites/default/files/ZED-F9P_IntegrationManual_UBX-18010802.pdf)
- [Texas Instruments TPS63802 product and CAD resources](https://www.ti.com/product/TPS63802)
- [Microchip MCP1700 product and CAD resources](https://www.microchip.com/en-us/product/MCP1700)
- [onsemi NCV8705 product datasheet/package resources](https://www.onsemi.com/download/data-sheet/pdf/ncv8705-d.pdf)
- [Adafruit Feather ESP32-S3 design downloads](https://learn.adafruit.com/adafruit-esp32-s3-feather/downloads)
- [Ultra Librarian](https://www.ultralibrarian.com/)
- [SnapMagic KiCad downloads](https://support.snapmagic.com/en/articles/2957827-which-formats-does-snapmagic-export)

All accepted project parts shall be stored as individual files:

- Symbols: `KiCAD/symbols/ActivityBrick.kicad_symdir/<part>.kicad_sym`
- Footprints: `KiCAD/footprints/ActivityBrick.pretty/<part>.kicad_mod`
- 3D models: `KiCAD/3dmodels/ActivityBrick.3dshapes/<part>.step` or `.wrl`

Footprints shall reference these models with a portable path such as
`${KIPRJMOD}/3dmodels/ActivityBrick.3dshapes/<part>.step`.

For every imported model, verify the ordering code, pin numbers, pin-one
orientation, pad dimensions, pitch, exposed pads, solder-mask and paste
openings, courtyard, component height, and 3D-model origin/rotation. Database
models are starting points, not substitutes for the manufacturer drawing.

### Manual download manifest

Download the files from the exact links below and leave each vendor archive
unmodified in the project's `download/` intake folder. When an export format is
offered, select **KiCad v6+** for the symbol and footprint and **STEP** for the
3D model. Also download the linked manufacturer datasheet or drawing when it is
not already present in `datasheets/`.

"Available" in this table means that a suitable CAD download is currently
offered at the linked source; it does not mean that the physical component is
in stock. Stock changes continuously and shall be checked separately before the
BOM is frozen.

Library status: ✅ means an exact or explicitly shared symbol, footprint, and
3D model are present in the project-local libraries; ◐ means only part of the
set is present; ☐ means the CAD set is absent or the component selection is
still blocked. A check mark records file presence, not completion of the final
datasheet, 3D-alignment, or manufacturing review.

| Circuit item | Exact search/order code | Manual source | CAD availability and action |
|---|---|---|---|
| ✅ IMU | `BMI323` | [Ultra Librarian BMI323](https://app.ultralibrarian.com/details/5941cc9e-78c5-11ed-b159-0a34d6323d74/Bosch-Sensortec/BMI323) | Project library contains the symbol, footprint, and STEP model. Preserve the validation records with the source archive. |
| ✅ Magnetometer | `BMM350` | [Ultra Librarian BMM350](https://app.ultralibrarian.com/details/df0e31dd-2ba6-11ee-9288-0ae0a3b49db5/Bosch-Sensortec/BMM350) | Project library contains the symbol, footprint, and STEP model; the Bosch handling and soldering instructions are stored locally. |
| ✅ Barometer | `BMP581` | [Ultra Librarian BMP581](https://app.ultralibrarian.com/details/6b707625-f695-11ec-9c51-0a34d6323d74/Bosch-Sensortec/BMP581) | Project library contains the symbol, pressure-port-aware footprint, and STEP model. |
| ✅ Standard GNSS option | `MAX-M10S-00B` | [Component Search Engine MAX-M10S-00B](https://componentsearchengine.com/part-view/MAX-M10S-00B/u-blox) | Project library contains the exact symbol, footprint, and STEP model. Retain the [u-blox integration manual](https://content.u-blox.com/sites/default/files/MAX-M10S_IntegrationManual_UBX-20053088.pdf). |
| ✅ RTK GNSS option | `ZED-F9P-05B` | [Component Search Engine ZED-F9P-05B](https://componentsearchengine.com/part-preview/ZED-F9P-05B/u-blox?type=footprint) | Project library contains the exact `-05B` symbol, footprint, and STEP model. Retain the [05B datasheet](https://content.u-blox.com/sites/default/files/documents/ZED-F9P-05B_DataSheet_UBXDOC-963802114-12824.pdf) and [integration manual](https://content.u-blox.com/sites/default/files/ZED-F9P_IntegrationManual_UBX-18010802.pdf). |
| ✅ BMM350 1.8 V LDO | `MCP1700T-1802E/TT` | [DigiKey MCP1700T-1802E/TT](https://www.digikey.com/en/products/detail/microchip-technology/MCP1700T-1802E-TT/652671) | Project library contains the exact symbol and an explicitly shared SOT-23 footprint and STEP model. |
| ✅ GNSS backup LDO | `MCP1700T-3002E/TT` | [DigiKey MCP1700T-3002E/TT models](https://www.digikey.com/en/models/651114) | Newly imported: exact symbol, SOT-23 footprint, and STEP model. |
| ✅ GNSS buck-boost | `TPS63802DLAR` | [Ultra Librarian TPS63802DLAR](https://app.ultralibrarian.com/details/16adf68c-103f-11e9-ab3a-0a3560a4cccc/Texas-Instruments/TPS63802DLAR) | Project library contains the exact symbol, DLA footprint, and STEP model. |
| ✅ GNSS low-noise LDO | `NCV8705MT33TCG` | [DigiKey NCV8705MT33TCG](https://www.digikey.com/en/products/detail/onsemi/NCV8705MT33TCG/5257919) | Newly imported: corrected six-pin-plus-exposed-pad symbol, CASE 511BR footprint, and STEP model. The downloaded eight-pin Ultra Librarian symbol was rejected as the wrong package pinout. |
| ✅ Optional USB-detect LDO | `AP2112K-3.3TRG1` | [Ultra Librarian AP2112K-3.3TRG1](https://app.ultralibrarian.com/details/2c63a363-1d6d-11e9-ab3a-0a3560a4cccc/Diodes-Inc/AP2112K-3-3TRG1) | Newly imported: exact symbol, SOT25 footprint, and STEP model. The design now uses the complete orderable `K` part number. |
| ✅ RF ESD | `PESD0402-140`, Littelfuse | [DigiKey PESD0402-140](https://www.digikey.com/en/products/detail/littelfuse-inc/PESD0402-140/1968525) | Project library contains the exact symbol, footprint, and STEP model. Retain the [Littelfuse specification](https://www.littelfuse.com/~/media/electronics/product_specifications/polymer_esd_suppressors/littelfuse_polymer_esd_suppressor_pesd0402_140_product_specification.pdf.pdf). |
| ✅ Selected USB ESD | `USBLC6-2SC6`, STMicroelectronics | [Manufacturer datasheet](https://www.st.com/resource/en/datasheet/usblc6-2.pdf), [Mouser](https://www.mouser.com/ProductDetail/STMicroelectronics/USBLC6-2SC6) | Imported `ActivityBrick:USBLC6-2SC6` symbol, `ActivityBrick:USBLC6-2SC6_SOT23-6L` footprint and STEP models. Verified against local `DS_usblc6-2.pdf`; footprint uses ST Figure 19 lands. Mouser listing retrieved 2026-09-17 reports 74,194 in stock; recheck at purchase. Replaces unavailable PRTR5V0U2F. |
| ✅ Superseded USB ESD — reference only | `TPD4E05U06DQAR` | [Ultra Librarian TPD4E05U06DQAR](https://app.ultralibrarian.com/details/16994cb5-103f-11e9-ab3a-0a3560a4cccc/Texas-Instruments/TPD4E05U06DQAR) | Project library contains the symbol, DQA footprint, and STEP model. Retain existing files; the USB option now uses USBLC6-2SC6. |
| ◐ Vertical ZED USB connector | `USB4120-03-C` | [GCT](https://gct.co/connector/usb4120), [local manufacturer drawing](datasheets/USB4120_GCT_A3.pdf) | Symbol, corrected footprint, and exact-part STEP are present. The 1.60 mm board is accepted for the optional development build: its 0.95 mm shell stakes remain within the holes, while the 16 signal contacts are surface mounted. Confirm shell-stake soldering and cable access with the assembler. |
| ✅ Superseded horizontal USB connector — do not use for vertical option | `USB4105-GF-A` | [GCT drawing](https://gct.co/files/drawings/usb4105.pdf) | Existing symbol, footprint and STEP retained for reference. This horizontal receptacle does not meet the revised vertical requirement; do not rename its footprint or model as USB4120. |
| ✅ MAX RF connector | `U.FL-R-SMT-1(10)` | [DigiKey U.FL-R-SMT-1(10)](https://www.digikey.com/en/products/detail/hirose-electric-co-ltd/U-FL-R-SMT-1-10/2504612) | Project library contains the exact symbol, footprint, and STEP model; retain the Hirose drawing for validation. |
| ✅ ZED RF connector | `U.FL-R-SMT-1(10)`, Hirose | [DigiKey U.FL-R-SMT-1(10)](https://www.digikey.com/en/products/detail/hirose-electric-co-ltd/U-FL-R-SMT-1-10/2504612) | Use a second physical connector for the dedicated `GNSS_RF_ZED` path. The project-local symbol, footprint and STEP model are present. Do not share or join it with the MAX connector. The obsolete Molex 734120110 is no longer selected. |
| ✅ Service header | `FTSH-105-01-L-DV-K-TR` | [Samtec FTSH series/configurator](https://www.samtec.com/products/ftsh) | Project library contains the symbol, footprint, and STEP model for this complete suffix. Confirm that this is the intended assembly variant before schematic use. |
| ✅ Buck-boost inductor | `XFL4015-471MEC` | [Coilcraft XFL4015 series](https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xfl/xfl4015/) | Project library contains the exact symbol, footprint, and STEP model for the `C` packaging suffix. |
| ✅ ZED bias choke | `LQG15HS47NJ02D` | [Murata LQG15HS47NJ02 family](https://www.murata.com/en-us/products/productdetail?partno=LQG15HS47NJ02D) | Newly imported: exact 47 nH symbol, 1005 footprint, and STEP model for the `D` packaging suffix. It is specific to the ZED multiband path; do not substitute it for the MAX 27 nH choke. The downloaded `LQG15HS4N7C02D` archive is a different 4.7 nH part and was not imported. |
| ✅ MAX bias choke | `LQG15HN27NH02D`, Murata | [Murata product page](https://www.murata.com/products/productdetail?partno=LQG15HN27NH02%23), [DigiKey listing](https://www.digikey.com/en/products/detail/murata-electronics/LQG15HN27NH02D/6798500) | 27 nH, 3%, 300 mA, 0402. Active and stocked at verification time. It is specific to the MAX L1 path; confirm RF impedance after layout. |
| ◐ MAX bias current limiter, fault review open | `CRCW121010R0FKEAHP`, Vishay | [LCSC C844442](https://www.lcsc.com/product-detail/C844442.html) | 10 Ω, 1%, 0.75 W, 1210/3225 metric for R40. In stock at the 2026-09-21 check. The MAX 250 mA absolute-maximum source rating is not a guaranteed short-current limit; verify sustained-short dissipation. |
| ✅ ZED bias current limiter | `CMP2010-FX-10R0ELF`, Bourns | [LCSC C1880468](https://www.lcsc.com/product-detail/C1880468.html), [local datasheet](datasheets/Bourns_CMP.pdf) | 10 Ω, 1%, 1 W, high-power anti-surge, 2010/5025 metric for R32. Schematic, PCB, and BOM use the matching 2010 footprint. |
| ✅ MAX bias filter capacitor | `GRM155R71C103KA01J`, Murata | [DigiKey listing](https://www.digikey.com/en/products/detail/murata-electronics/GRM155R71C103KA01J/3845523) | 10 nF, 10%, 16 V, X7R, 0402/1005 metric. Place from the resistor/choke node to ground with a short return. |
| ✅ ZED bias filter capacitor | `GRM155R71C104JA88D`, Murata | [DigiKey listing](https://www.digikey.com/en/products/detail/murata-electronics/GRM155R71C104JA88D/490-6327-1-ND) | 100 nF, 5%, 16 V, X7R, 0402/1005 metric. Place from the resistor/choke node to ground with a short return. |

Do not rename or unpack the archives manually. Keeping the original filenames
and directory structure makes it easier to identify the source, license and
export format when the files are imported.

### USB component acquisition checklist

Use the connection lists in [Activity Brick V2 Design](Activity%20Brick%20V2%20Design.md#suggested-pin-connections)
when checking downloaded symbols. The USB circuit uses no power mux.

| Item | Quantity per USB assembly | Resource/action |
|---|---|---|
| Vertical USB-C receptacle | 1 | Drawing, symbol, footprint, and exact-part STEP are present for `USB4120-03-C`. The 1.60 mm board is accepted for development; confirm the assembler can solder its short shell stakes, and check the 6.50 mm height and cable access. |
| `AP2112K-3.3TRG1` USB LDO | 1 | Already local: symbol `AP2112K-3.3TRG1.kicad_sym`, footprint `SOT_RG1_DIO_AP2112K.kicad_mod`, model `AP2112K-3.3TRG1.step`, datasheet `AP2112.pdf`. No repeat CAD download required. Pin 1 VIN = USB VBUS; 2 GND; 3 EN = `GNSS_3V3`; 4 NC; 5 VOUT = `ZED_USB_3V3`. |
| `USBLC6-2SC6` USB ESD array | 1 | ST datasheet, symbol, SOT23-6L footprint and STEP are present and checked. Pins 1/6 = D-, 3/4 = D+, 2 = GND, 5 = USB VBUS. CC1/CC2 retain separate 5.1 kΩ pulldowns. |
| CC pulldown resistors | 2 × 5.1 kΩ, 1% | Standard resistor symbols/footprints; one resistor per CC pin. Select exact package and manufacturer code for the BOM. |
| USB data series resistors | 2 × 27 Ω | Standard resistor symbols/footprints; one per data line, near the ZED. |
| V_USB pulldown resistor | 1 × 100 kΩ | Standard resistor symbol/footprint; from `ZED_USB_3V3` to GND. |
| LDO input capacitor | 1 × 1 µF, X5R/X7R | Near AP2112 VIN; select voltage rating for the normal USB VBUS range and account for DC-bias capacitance loss. |
| LDO output and module USB capacitors | 2 × 1 µF, X5R/X7R | One near AP2112 VOUT and one adjacent to ZED V_USB. Select voltage rating and effective capacitance for 3.3 V. |
| Optional USB output bypass | 1 × 100 nF, X5R/X7R | Additional bypass as shown in the reference circuit; does not replace either required 1 µF output/module capacitor. Standard KiCad capacitor resources. |
| USB-omitted V_USB grounding link | 1 assembly option | Standard solder-jumper or zero-ohm-link resources. Populate only when the USB LDO output is disconnected and the USB option is omitted. |

For the new connector, save accepted files under the project-local symbol,
footprint and model directories specified above using the exact ordering code.
Keep the vendor archive intact in the intake folder. The workspace currently
contains an intake directory named `dowbloads/`; preserve existing archives
there rather than moving or renaming them as part of this document update.

The USB4120 archive has been imported and checked against the GCT A3 drawing.
The archive did not include a STEP model; an exact-part STEP was subsequently
added at `KiCAD/3dmodels/ActivityBrick.3dshapes/USB4120-03-C.stp` and linked
from the placed footprint. See [import report](KiCAD/library_import_2026-09-17.md).
The selected simple USB circuit connects VBUS directly to the AP2112 input
and USBLC6-2SC6 pin 5. It includes ESD protection but no sustained-overvoltage
disconnect; a separate VBUS protection IC is not part of this baseline.
Keep USB LDO EN on GNSS_3V3 and its output separate as ZED_USB_3V3.
USBLC6-2SC6 CAD is imported and checked against the local ST datasheet.
The footprint links `SOT23-6L_STM.step` through `${KIPRJMOD}`; the ZIP model
`USBLC6-2SC6.step` is retained as an unlinked alternative. Littelfuse SP3003-02XTG
is an alternative requiring a different footprint and pinout. The downloaded
PRTR5V0U4D,125 symbol, footprint and STEP are imported as unused references;
SOT886.step is stored separately and is not the U4D package.

### Standard KiCad resources that do not need external downloads

Use installed KiCad symbols and footprints for ordinary resistors, ceramic
capacitors, generic LEDs/test points where an exact mechanical model is not
needed, standard SOT-23 packages, and 2.54 mm headers. Still assign an exact
manufacturer part number in the BOM when voltage rating, dielectric,
magnetism, tolerance, current, or size matters.

The selected BMM350 CRST capacitor is Samsung `CL21B225KOFNNNE` ([Samsung product page](https://product.samsungsem.com/mlcc/CL21B225KOFNNN.do), [LCSC C28234](https://www.lcsc.com/product-detail/C28234.html)), 2.2 µF, 16 V, X7R, 10%, in 0805/2012. Use `Capacitor_SMD:C_0805_2012Metric`. It replaces Bosch's obsolete recommended TDK `CGB4B3X7R0J225K055AB`. Samsung does not characterize this standard MLCC as nonmagnetic, so the selection is an accepted engineering exception requiring installed-board BMM350 offset validation. The RF matching components and bias components also
need final RF-rated manufacturer selections even when their KiCad footprints
are standard sizes.

### OSHW logo footprints

The downloaded `OSHW_logo_KiCad_scalable.zip` legacy library was converted to
KiCad 10 and installed in the separate project-local `OSHW` footprint library.
It provides 80 `OSHW-logo_*` footprints: 1–20 mm sizes, silkscreen and copper,
with front and horizontally mirrored back variants. Use a silkscreen variant
for the normal board mark. The legacy unfilled silkscreen polygons have been
updated from a nearly invisible 0.00254 mm outline to a 0.20 mm stroke. Place a
`back` variant and flip it in PCB Editor for the physical back layer. Import
details and the source instructions are kept in
`KiCAD/footprints/OSHW_logo_KiCad_scalable_docs/`.

### Datasheet and reference-document status

Store these documents in `datasheets/`. Here, ✅ means the document is present,
☐ means it is still needed, and ◐ means the requirement depends on a pending
component selection.

| Status | Component or topic | Local file or remaining action |
|---|---|---|
| ✅ | BMI323 | `BMI323.pdf` |
| ✅ | BMM350 | `BMM350.pdf` |
| ✅ | BMM350 manufacturing guidance | `bst-bmm350-hs000.pdf` |
| ✅ | BMP581 | `bst_bmp581_ds004-2950309.pdf` |
| ✅ | MAX-M10S-00B | `MAX-M10S.pdf` |
| ✅ | MAX-M10S design guidance | `MAX-M10S_IntegrationManual_UBX-20053088.pdf` |
| ✅ | ZED-F9P-05B | `ZED-F9P.pdf` |
| ✅ | ZED-F9P design guidance | `ZED-F9P_IntegrationManual_UBX-18010802.pdf`; revision R16 explicitly covers the `-05B` initial production release |
| ✅ | MCP1700 1.8 V and 3.0 V LDOs | `MCP1700.pdf` |
| ✅ | AP2112K-3.3TRG1 LDO | `AP2112.pdf`; exact orderable `K` variant is selected |
| ✅ | TPS63802 buck-boost | `TPS63802.pdf` |
| ✅ | NCV8705 low-noise LDO | `NCV8705.pdf`, including WDFN6 CASE 511BR |
| ✅ | PESD0402-140 RF ESD | `Littelfuse-Polymer-ESD-Suppressor-PESD-Catalog-Datasheet.pdf`; includes the exact part, dimensions, recommended pad layout, and application limitations |
| ✅ | USBLC6-2SC6 selected USB ESD | Local [ST datasheet](datasheets/DS_usblc6-2.pdf); exact SC6 symbol pinout and package checked. STEP export and 3D alignment check passed on a temporary board. |
| ✅ | TPD4E05U06DQAR USB ESD — superseded | `tpd4e05u06.pdf`; includes the DQA USON-10 package |
| ◐ | USB4120-03-C vertical USB connector | Manufacturer drawing saved as `datasheets/USB4120_GCT_A3.pdf`; symbol, footprint, and exact-part STEP are present. The 1.60 mm board is accepted for the development option; shell-stake soldering and enclosure access remain assembly checks. |
| ✅ | USB4105-GF-A horizontal USB connector — superseded | `usb4105.pdf`; retained for reference only, not the drawing for the vertical connector |
| ☐ | U.FL-R-SMT-1(10) RF connector | Hirose manufacturer drawing |
| ✅ | ZED Hirose U.FL-R-SMT-1(10) RF connector | Uses the existing verified Hirose project-local symbol, footprint and STEP as a second physical connector; obtain and retain the Hirose manufacturer drawing. |
| ☐ | XFL4015-471MEC inductor | Coilcraft electrical and mechanical drawing |
| ☐ | LQG15HS47NJ02D bias choke | Murata electrical and mechanical drawing |
| ☐ | LQG15HN27NH02D MAX bias choke | Save the Murata electrical and mechanical drawing locally; generic 0402 footprint is assigned in the schematic. |
| ✅ | AC1210FR-7W10RL reference option | The official Yageo AC-series datasheet is saved as `datasheets/Yageo_AC_Series.pdf`. This 1 W part is not the LCSC-selected R40 because LCSC `C6114351` was out of stock at the check. |
| ✅ | CMP2010-FX-10R0ELF ZED current limiter | Official Bourns CMP-series datasheet saved as `datasheets/Bourns_CMP.pdf`; schematic, PCB, and BOM specify the standard KiCad 2010 footprint. |
| ☐ | GRM155R71C103KA01J MAX bias filter | Save the Murata product specification locally; 0402 footprint is assigned to C16. |
| ☐ | GRM155R71C104JA88D ZED bias filter | Save the Murata product specification locally; 0402 footprint is assigned to C20. |
| ☐ | FTSH-105-01-L-DV-K-TR service header | Samtec drawing after confirming this exact suffix |
| ✅ | ANN-MB2-00 reference antenna | `ANN-MB2_DataSheet_UBXDOC-963802114-12775.pdf` |
| ◐ | Production GNSS antennas | Download the selected MAX-M10S and ZED-F9P antenna datasheets after the production choices are frozen |
| ◐ | Adafruit Feather ESP32-S3 host | `Adafruit Feather ESP32-S3 Pinout.pdf` and `adafruit_products_FESP3_sch.png` are present; exact-revision EagleCAD/fabrication files, board outline, antenna keepout, and mechanical information are still needed |

### External database access recommendation

For **CAD files**, manual authenticated download is preferred. Manufacturer and
CAD-library sites often require accepting license terms, selecting the EDA
format, and visually choosing among package variants. Download the native KiCad
archive, BXL/EPW package, or STEP file and place it in a temporary untracked
intake folder. After validation, copy only accepted individual files into the
project libraries.

For **price, stock, lifecycle, and datasheet URLs**, an API is worthwhile:

1. **Mouser Search API** is the simplest first integration when a Mouser API key
   is available. It returns manufacturer part number, availability, lifecycle,
   datasheet URL, lead time, and price breaks. See the
   [Mouser Search API](https://www.mouser.com/en/api-search/).
2. **Nexar/Octopart GraphQL API** is preferable when aggregated multi-distributor
   coverage is more important than setup simplicity. See the
   [Nexar API](https://nexar.com/api).
3. **DigiKey Product Information API** is useful if DigiKey is the primary
   purchasing source, but its OAuth application and token setup is more involved.
   See the [DigiKey API developer resources](https://developer.digikey.com/resources).

No electronics-component database connector is currently exposed to Codex in
this workspace. Do not place API keys in this repository or in chat. Keep them
in a user secret store or environment variables and expose only the variable
names to an acquisition script. Any stored availability result must include the
source and retrieval timestamp because stock and lifecycle data change.
