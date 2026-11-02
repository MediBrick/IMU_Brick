# Assembly placement variants — 2026-09-21

These placement CSVs were generated from the `Populate` rows of the matching
sheets in [`Activity_Brick_Production_BOM.xlsx`](../../Activity_Brick_Production_BOM.xlsx)
and coordinates in the saved [`Activity_Brick.kicad_pcb`](../Activity_Brick.kicad_pcb).
Regenerate with `/usr/bin/python3 KiCAD/export_assembly_variants.py` from the
project root after any BOM population or PCB placement change. Coordinates are
in millimetres in the PCB file's coordinate system; confirm the assembler's
required origin, rotation convention and side convention before upload.

| Assembly | Placement CSV | Populated footprints |
| --- | --- | ---: |
| MAX-M10S production | [MAX_Production_positions.csv](MAX_Production_positions.csv) | 53 |
| ZED-F9P production, USB omitted | [ZED_Production_positions.csv](ZED_Production_positions.csv) | 60 |
| ZED-F9P development, USB populated | [ZED_Development_positions.csv](ZED_Development_positions.csv) | 71 |

The export checks that every populated reference exists on the PCB, that the
MAX sheet excludes the ZED module and RF connector, that both ZED sheets
exclude the MAX module and RF connector, and that the eleven development USB
parts appear only in the ZED development placement file. Bare PCB features,
test pads, mounting holes, unselected GNSS parts, and DNP parts are excluded.
Solder-jumper copper states are assembly operations and cannot be represented
by a component-position row.

## Assembly population and jumper matrix

The following are the default states for the three named builds. "Closed
trace" means the PCB copper bridge is left intact; "open" means no solder
bridge is added. These operations do not appear in the placement CSVs.

| Reference / feature | MAX Production | ZED Production | ZED Development |
| --- | --- | --- | --- |
| `IC1`, `J2`, MAX RF ESD/bias parts and MAX indicator `D3` | Populate | DNP | DNP |
| `IC2`, `J3`, ZED RF ESD/bias parts and ZED indicators `D5`–`D7` | DNP | Populate | Populate |
| `J4`, `U4` and the other nine USB parts | DNP | DNP | Populate |
| `J1` header | DNP; retain holes | DNP; retain holes | DNP; retain holes |
| Common blue LED `D1` | Populate | Populate | Populate |
| `JP1` I2C pull-up selector | Open, no pull-up selected | Open | Open |
| `JP3` common LED enable | Open (`D1` off) | Open (`D1` off) | Open (`D1` off) |
| `JP2` MAX indicator return | Closed trace | Not fitted with MAX circuit | Not fitted with MAX circuit |
| `JP4` MAX antenna bias | Open; default passive antenna | Not fitted with MAX circuit | Not fitted with MAX circuit |
| `JP5`, `JP6` MAX I2C links | Open; UART default | Not fitted with MAX circuit | Not fitted with MAX circuit |
| `JP7`, `JP9`, `JP10` ZED indicator returns | Not fitted with ZED circuit | Closed traces | Closed traces |
| `JP8` ZED interface select | Not fitted with ZED circuit | Open; UART/I2C mode | Open; UART/I2C mode |
| `JP11` ZED antenna bias | Not fitted with ZED circuit | Closed trace | Closed trace |
| `JP12`, `JP13` ZED I2C links | Not fitted with ZED circuit | Open; UART default | Open; UART default |
| `JP14` ZED `V_USB` grounding | Not fitted with ZED circuit | **Bridge closed** after USB circuit is omitted | **Open** with USB circuit populated |
| `R12`, `R28` SAFEBOOT resistors | `R12` DNP | `R28` DNP | `R28` DNP |
| `TP1`–`TP8` as applicable | Bare PCB pads, no parts | Bare PCB pads, no parts | Bare PCB pads, no parts |

The MAX production default uses a passive antenna. If an active MAX antenna
is selected for a different build, its bias voltage/current must be checked
and `JP4` bridged on that build's traveler. The ZED default has antenna bias
enabled through `JP11`. The MAX and ZED indicator LEDs are fitted and their
closed-trace returns remain intact; the common LED `D1` is fitted but off
because `JP3` is open. These are the specified assembly defaults, not a
claim that the LEDs have no battery-current impact. Never close `JP14` while
the USB LDO output is active.

## Release holds found during reconciliation

1. **MAX R40 short-fault review:** Vishay LCSC `C844442` is the selected 10 Ω,
   0.75 W, 1210 candidate. At the MAX datasheet's 250 mA absolute-maximum
   VCC_RF source current, dissipation would be 0.625 W, but that rating is not
   a guaranteed current clamp. A hard short across 3.3 V and 10 Ω could demand
   1.09 W if the source stays up. Verify the actual fault response or add
   protection before approving sustained-short operation. The exact 1 W
   Yageo `AC1210FR-7W10RL` is LCSC `C6114351` but was out of stock.
2. **ZED IC2 sourcing:** the approved source is Mouser
   [`134-ZED-F9P-05B`](https://www.mouser.com/ProductDetail/u-blox/ZED-F9P-05B),
   matching the required `ZED-F9P-05B`. LCSC `C5120257` is the different
   `-04B` revision and remains unapproved as a substitute. Recheck Mouser stock
   before ordering.
3. **Development USB J4 assembly check:** GCT's USB4120 drawing recommends a
   1.00 ± 0.10 mm PCB; the saved board is 1.60 mm. The chosen assembly accepts
   that its 0.95 mm shell stakes will stay inside the holes rather than protrude
   through the back. The 16 signal contacts are surface mounted. Confirm the
   shell-stake soldering method and cable/enclosure access with the assembler.
4. **BMM350 C12:** Samsung `CL21B225KOFNNNE` is the accepted 2.2 µF 0805
   substitution. Its magnetic behavior is not specified; installed-board
   magnetometer offset validation remains required.
5. **LED footprint verification:** the PCB footprint name for blue LED `D1`
   ends in `_Red`, though the BOM specifies a blue LED. Confirm pad geometry
   and polarity against the chosen LED in the footprint-validation step.

The component policy for this release is LCSC sourcing for parts available
there, with Mouser approved for the exact `ZED-F9P-05B` module.

`J1` is DNP in every assembly variant. Its plated through-holes remain on the
PCB, but no pin header is installed or ordered.

These files establish BOM-to-PCB placement selection, not electrical, RF,
mechanical, solder-paste or assembly signoff.
