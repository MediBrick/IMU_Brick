# Activity Brick Production BOM audit

Checked: 2026-09-20

This report records the public LCSC product-page identity and availability check used to clean the Engineering BOM and refresh the three assembly sheets. Stock is a point-in-time value and should be refreshed immediately before ordering.

## Findings

- **Wrong linked revision corrected:** `IC2` requires u-blox `ZED-F9P-05B`, but LCSC `C5120257` is `ZED-F9P-04B`. The LCSC number and hyperlink were removed from the Engineering BOM. The `-04B` remains only as an alternate requiring revision review.
- **C12 substitution accepted by engineering decision:** Samsung `CL21B225KOFNNNE` / `C28234` is 2.2 uF, 10%, X7R, 16 V, 0805 and was in stock. It replaces the obsolete Bosch-recommended TDK part. Samsung does not specify nonmagnetic construction, so installed-board BMM350 offset validation remains required.
- **R32 replacement implemented:** Bourns `CMP2010-FX-10R0ELF` / `C1880468` is 10 ohm, 1%, 1 W, 2010 and was in stock. It restores the ZED-F9P short-fault power requirement. The schematic and PCB now use the matching 2010 footprint, and the revised layout passes connectivity checks.
- **R40 fault case remains open:** Vishay `CRCW121010R0FKEAHP` / `C844442` is 10 ohm, 1%, 0.75 W, 1210 and in stock. MAX-M10S lists 250 mA as an absolute-maximum VCC_RF source rating, not a guaranteed short-current clamp. A hard short could dissipate 1.09 W at 3.3 V across 10 ohm if the supply remains up; verify the actual fault response before approving sustained-short operation.
- **Other linked selections:** manufacturer part numbers, nominal values, tolerances/ratings, and footprints are consistent with the Engineering BOM requirements. Capacitor dielectric cells now state the actual selected X5R or X7R material.
- **Availability:** every retained LCSC code below returned positive stock during the check. The required `ZED-F9P-05B` did not have a matching LCSC listing.

## LCSC selections

| LCSC | Manufacturer part | References | Stock at check | Result |
|---|---|---|---:|---|
| [C77041](https://www.lcsc.com/product-detail/C77041.html) | `GRM188R60J106ME47D` | C1 | 204650 | Verified |
| [C77007](https://www.lcsc.com/product-detail/C77007.html) | `GRM155R61C105KE01D` | C2, C3, C22, C23, C7, C21, C24, C28, C27 | 279200 | Verified |
| [C84419](https://www.lcsc.com/product-detail/C84419.html) | `GRM188R61A226ME15D` | C4, C17 | 516685 | Verified |
| [C71629](https://www.lcsc.com/product-detail/C71629.html) | `GRM155R71C104KA88D` | C8, C9, C10, C11, C13, C14, C5, C6, C15, C26 | 2302200 | Verified |
| [C28234](https://www.lcsc.com/product-detail/C28234.html) | `CL21B225KOFNNNE` | C12 | 79940 | Selected; magnetic-offset validation required |
| [C90053](https://www.lcsc.com/product-detail/C90053.html) | `GRM188R61A106ME69D` | C18, C19 | 114880 | Verified |
| [C22355736](https://www.lcsc.com/product-detail/C22355736.html) | `XL-1005UBC` | D1, D7 | 267000 | Verified |
| [C18221164](https://www.lcsc.com/product-detail/C18221164.html) | `XFL4015-471MEC` | L1 | 4067 | Verified |
| [C60491](https://www.lcsc.com/product-detail/C60491.html) | `RC0402FR-07100KL` | R1, R2, R41 | 8343600 | Verified |
| [C138066](https://www.lcsc.com/product-detail/C138066.html) | `RC0402FR-0710RL` | R3, R4 | 1512400 | Verified |
| [C2085221](https://www.lcsc.com/product-detail/C2085221.html) | `CRCW0402604KFKED` | R5 | 400 | Verified |
| [C144733](https://www.lcsc.com/product-detail/C144733.html) | `AC0402FR-0791KL` | R6 | 44500 | Verified |
| [C114762](https://www.lcsc.com/product-detail/C114762.html) | `RC0402FR-072K2L` | R15, R17 | 1356300 | Verified |
| [C106235](https://www.lcsc.com/product-detail/C106235.html) | `RC0402FR-071KL` | R16, R18, R21, R29, R30 | 2630200 | Verified |
| [C2845237](https://www.lcsc.com/product-detail/C2845237.html) | `TPS63802DLAR` | U1 | 6650 | Verified |
| [C604084](https://www.lcsc.com/product-detail/C604084.html) | `NCV8705MT33TCG` | U2 | 4476 | Verified |
| [C62244](https://www.lcsc.com/product-detail/C62244.html) | `MCP1700T-3002E/TT` | U3 | 2870 | Verified |
| [C17225907](https://www.lcsc.com/product-detail/C17225907.html) | `BMM350` | U5 | 2789 | Verified |
| [C5362283](https://www.lcsc.com/product-detail/C5362283.html) | `BMP581` | U6 | 4000 | Verified |
| [C5368700](https://www.lcsc.com/product-detail/C5368700.html) | `BMI323` | U7 | 3524 | Verified |
| [C150796](https://www.lcsc.com/product-detail/C150796.html) | `MCP1700T-1802E/TT` | U8 | 3779 | Verified |
| [C3011655](https://www.lcsc.com/product-detail/C3011655.html) | `GRM155R71C103KA01J` | C16 | 9900 | Verified |
| [C10662](https://www.lcsc.com/product-detail/C10662.html) | `PESD0402-140` | D2, D4 | 73695 | Verified |
| [C25503856](https://www.lcsc.com/product-detail/C25503856.html) | `XL-1005UYC` | D3, D5 | 77500 | Verified |
| [C4153167](https://www.lcsc.com/product-detail/C4153167.html) | `MAX-M10S-00B` | IC1 | 763 | Verified |
| [C88373](https://www.lcsc.com/product-detail/C88373.html) | `U.FL-R-SMT-1(10)` | J2, J3 | 8975 | Verified |
| [C1331771](https://www.lcsc.com/product-detail/C1331771.html) | `LQG15HN27NH02D` | L2 | 4800 | Verified |
| [C138002](https://www.lcsc.com/product-detail/C138002.html) | `RC0402FR-0733RL` | R7, R8, R9, R10, R11, R13, R14, R12, R20, R22, R23, R24, R25, R26, R27, R31, R33, R36, R37, R28 | 8094900 | Verified |
| [C844442](https://www.lcsc.com/product-detail/C844442.html) | `CRCW121010R0FKEAHP` | R40 | 8610 at 2026-09-21 check | LCSC selection; short-fault review open |
| [C1880468](https://www.lcsc.com/product-detail/C1880468.html) | `CMP2010-FX-10R0ELF` | R32 | 1595 | Verified and implemented on PCB |
| [C7519](https://www.lcsc.com/product-detail/C7519.html) | `USBLC6-2SC6` | D8 | 21165 | Verified |
| [C3445864](https://www.lcsc.com/product-detail/C3445864.html) | `USB4120-03-C` | J4 | 557 | Verified |
| [C105872](https://www.lcsc.com/product-detail/C105872.html) | `RC0402FR-075K1L` | R34, R35 | 2165200 | Verified |
| [C138021](https://www.lcsc.com/product-detail/C138021.html) | `RC0402FR-0727RL` | R38, R39 | 35300 | Verified |
| [C51118](https://www.lcsc.com/product-detail/C51118.html) | `AP2112K-3.3TRG1` | U4 | 52940 | Verified |
| [C913742](https://www.lcsc.com/product-detail/C913742.html) | `GRM155R71C104JA88D` | C20 | 17050 | Verified |
| [C335109](https://www.lcsc.com/product-detail/C335109.html) | `GRM155R61C225KE44D` | C25 | 24100 | Verified |
| [C965793](https://www.lcsc.com/product-detail/C965793.html) | `XL-1005UGC` | D6 | 1209750 | Verified |
| [C97998](https://www.lcsc.com/product-detail/C97998.html) | `LQG15HS47NJ02D` | L3 | 56050 | Verified |

## Variant-sheet refresh

- `MAX Production` contains Common plus MAX-M10S records.
- `ZED Production` contains Common plus ZED-F9P records and marks the development USB option DNP.
- `ZED Development` contains Common plus ZED-F9P records and marks the development USB option populated.
- All three sheets were refreshed from the cleaned Engineering BOM, including direct LCSC hyperlinks, stock date/count, corrected LED manufacturer fields, and the procurement findings above.

## 2026-09-21 assembly follow-up

The saved PCB now carries R32 in the specified 2010 footprint. Matching
[placement CSVs](KiCAD/assembly_variants/README.md) were generated for all
three BOM variants. R40 is sourced at LCSC, but its short-fault behavior remains
to be verified. The exact `ZED-F9P-05B` still lacks a verified LCSC listing;
Mouser [`134-ZED-F9P-05B`](https://www.mouser.com/ProductDetail/u-blox/ZED-F9P-05B) is now the approved exact-part source; the
Engineering, ZED Production, and ZED Development sheets record it. For development USB J4,
the 1.60 mm board is accepted with the short shell stakes sitting within their
holes; confirm soldering and cable access with the assembler. An exact-part
STEP is now present in the project, correcting the earlier component-source
note.

LCSC lists the 1 W Yageo `AC1210FR-7W10RL` as
[C6114351](https://www.lcsc.com/product-detail/C6114351.html), but the
reviewed 2026-09-21 listing showed zero stock. The Vishay LCSC selection was
retained in the Engineering and MAX Production sheets. Its 0.75 W rating
cannot be signed off for a sustained hard short merely from the MAX 250 mA
absolute-maximum current specification.

## 2026-09-21 procurement-field audit

The user removed the lifecycle-status column and does not require an independent
lifecycle verification for this release. The ZED Production and ZED Development
sheets show the approved Mouser
`134-ZED-F9P-05B` number in their main procurement column and supplier column.
The IC2 stock cell now records the user's Mouser count of **791** on
2026-09-21 in the Engineering and both ZED variant sheets. The user accepted
the 2026-09-20 stock snapshots for the other selections.

`J1` is DNP in the Engineering BOM and all three variants by design. The
1×18 plated through-holes remain on the PCB for optional access; no pin header
is purchased or installed. This resolves the apparent Populate/DNP conflict.
The procurement-field checklist item is complete. Supplier availability will
be rechecked immediately before ordering, as a separate release task.

## Assembly-population review

The three variant sheets now specify the saved jumper defaults and the
different `JP14` operation for ZED Production versus ZED Development. `J1`
and the SAFEBOOT resistors remain DNP; test pads are bare PCB features. The
variant graphic rows identify `G1` as the Creative Commons artwork actually
on the PCB and `G***` as the OSHW logo. The matching placement exports have
53 MAX, 60 ZED Production, and 71 ZED Development rows. The export checks
that the unselected GNSS subsystem, its RF components and indicators, and the
production USB parts are absent from the respective placements.
