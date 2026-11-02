# PCBWay assembly BOMs

These three CSV files are exported from the `Populate` rows of
[`Activity_Brick_Production_BOM.xlsx`](../Activity_Brick_Production_BOM.xlsx).
They contain one line per workbook part group and exclude DNP parts, bare PCB
features, solder jumpers, mounting holes and graphics. Quantities are **per
assembled board**. UTF-8 BOM and CRLF line endings support Excel import.

| Assembly | BOM | Components | Matching placement file |
| --- | --- | ---: | --- |
| MAX production | [MAX_Production_BOM.csv](MAX_Production_BOM.csv) | 53 | [MAX_Production_positions.csv](MAX_Production_positions.csv) |
| ZED production, without USB | [ZED_Production_BOM.csv](ZED_Production_BOM.csv) | 60 | [ZED_Production_positions.csv](ZED_Production_positions.csv) |
| ZED development, with USB | [ZED_Development_BOM.csv](ZED_Development_BOM.csv) | 71 | [ZED_Development_positions.csv](ZED_Development_positions.csv) |

For PCBWay upload, the separate placement-file copies are
[MAX_Production_positions.csv](MAX_Production_positions.csv),
[ZED_Production_positions.csv](ZED_Production_positions.csv), and
[ZED_Development_positions.csv](ZED_Development_positions.csv). The common
[Activity_Brick_Gerber_Drill.zip](Activity_Brick_Gerber_Drill.zip) contains the
nine Gerber layers, Gerber job file, and plated/non-plated Excellon drill files
from `KiCAD/Gerber/`. It is one bare-board fabrication set for all three
assembly variants; the BOM and position file choose which parts are fitted.
The Gerber/drill files were generated after the saved PCB, and each copied
position row was compared with its current PCB footprint. These are current
working outputs, not the final frozen release package.

## PCB fabrication selections

Use the same bare-board order for all three assembly variants. The selections
below reflect the saved KiCad board and [PCBWay's published capabilities](https://www.pcbway.com/capabilities.html);
the fabricator must confirm the final stack-up and fine-pitch mask geometry.

| PCBWay order field | Select or enter | Reason / verification |
| --- | --- | --- |
| PCB type and quantity | Rigid PCB; choose the required order quantity | One common bare board; assembly populations differ. |
| Layers | **2** | The saved board uses F.Cu and B.Cu. |
| Dimensions | **70 × 70 mm nominal** | Check PCBWay's Gerber preview against the Edge.Cuts outline; KiCad's stroke-inclusive bounding box is 70.05 × 70.05 mm. |
| Board thickness | **1.6 mm** | Saved KiCad board thickness and development USB connector mechanical decision. |
| Material | **Standard FR-4** | KiCad's dielectric model is provisional; request the actual two-layer material, dielectric thickness and Dk for RF review. |
| Finished outer copper | **1 oz / approximately 35 µm**, both sides | Matches the KiCad stack-up estimate and current copper/clearance review. Confirm finished, not starting, copper weight. |
| Surface finish | **Immersion gold / ENIG** | Recommended for this fine-pitch BMM350 and other bottom-terminated parts; confirm PCBWay's menu label and assembler acceptance. |
| Solder mask | **Green, both sides** | Preferred for the BMM350 fine-pitch mask webs. White solder mask is offered, but PCBWay publishes less permissive bridge limits for white. |
| Silkscreen | **White, both sides** | White *silkscreen* is a separate, available selection; the design has F.Silkscreen and B.Silkscreen Gerbers. |
| Impedance | **Request PCBWay engineering review of both 50 Ω GNSS RF paths** | Give PCBWay the actual two-layer stack-up request and the existing RF Gerbers; do not treat KiCad's 1.51 mm FR-4 model as a confirmed fabrication stack-up. |
| Via treatment | **Tented vias, no via-in-pad fill/cap requested** | The saved board tents vias; NCV8705 thermal GND vias are outside its solder apertures. Confirm mask coverage at fine-pitch features. |
| Drill / slots | **Upload both PTH and NPTH drill files** | Preserve the routed-slot data in the supplied drill files, including USB connector shell stakes. Ask PCBWay to confirm plated/non-plated classification in its preview. |
| Panelization | **Individual boards unless PCBWay assembly requires a panel** | Get the assembler's panel/rail requirements before authorizing a production panel. |

**Fabrication note to attach to the order:** “Please review the BMM350 U5
0.40 mm-pitch, nine-pad NSMD pattern. The Gerbers call for separate 0.30 mm
mask openings on 0.25 mm copper pads, leaving nominal 0.10 mm mask webs.
Confirm those webs and the final paste/stencil plan with assembly engineering;
do not merge openings or change the mask pattern without approval. Please also
confirm the two-layer stack-up and review both GNSS 50 Ω grounded-coplanar
routes against it.” The [mask/paste audit](../KiCAD/reports/mask-paste-audit-2026-09-21.md)
records why this confirmation is needed. PCBWay's [solder-mask guidance](https://www.pcbway.com/pcb_prototype/PCB_Solder_mask.html)
lists white mask as available but gives tighter bridge conditions for it than
for green at 1 oz copper. Green is the recommended order choice here, **not**
proof that the 0.10 mm BMM350 webs will be fabricated as drawn.

The columns follow [PCBWay's assembly file requirements](https://www.pcbway.com/assembly-file-requirements.html)
and include the required manufacturer part number, designators, quantity and
footprint plus manufacturer, description, assembly type, approved distributor
number, value and workbook notes. The ZED-F9P-05B is sourced under Mouser
`134-ZED-F9P-05B`; the other populated entries use the workbook's LCSC numbers.
The development USB receptacle J4 is marked hybrid because its signal contacts
are surface-mount and its shell stakes use through-holes.

The [assembly matrix](../KiCAD/assembly_variants/README.md) is required
alongside these BOMs: in particular, ZED production requires the `JP14`
V_USB-to-GND bridge, whereas ZED development leaves `JP14` open. Solder-jumper
states are assembly instructions, not purchased BOM items. These are export
files for quote/assembly preparation; recheck stock and resolve the release
holds in the assembly matrix before ordering. After any BOM population change,
run `python3 PCBWay/export_boms.py` from the `v2` directory and review all
three generated files against their placement CSVs.
