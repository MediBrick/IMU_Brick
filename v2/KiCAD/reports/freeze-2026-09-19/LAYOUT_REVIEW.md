# Final copper and ratsnest review — 2026-09-20

This review covers `Activity_Brick.kicad_pcb` from the frozen source manifest.
It combines KiCad connectivity and DRC results, PCB-data inspection through the
`pcbnew` API, and visual inspection of independent front and mirrored-back
copper plots.

## Connectivity and filled zones

- KiCad reports **0 unconnected pads**, **0 DRC violations**, and **0 footprint
  errors**.
- Schematic-to-PCB parity separately confirms all 424 numbered pin/pad net
  assignments with zero mismatches.
- The `3V8`, `V_BAT`, and two-layer `GND` zones are filled and report
  `NeedRefill = false`.
- The fourth zone object is the intentional two-layer rule area, not a copper
  zone.
- No isolated copper island is visible in either layer plot. The GND fill uses
  multiple contours around clearances, joined through the two-layer ground and
  stitching vias.

## Ground and thermal connections

- GND is poured on both copper layers and remains connected around the routed
  signal bundles. The back layer provides the main broad return plane; local
  detours around low-speed signal clearances do not divide it into separate
  regions.
- The GND zone defaults to thermal connections. There are 78 GND pads using
  the inherited zone setting and 56 deliberate solid GND-pad overrides,
  including the ZED-F9P ground array.
- The local `3V8` and `V_BAT` zones use solid connections as intended for their
  power paths.
- Ground stitching is present around both GNSS RF routes and along the board.

## Width transitions and return paths

- `GNSS_RF_MAX` and `GNSS_RF_ZED` use the documented 1.05 mm main route with
  intentional 0.70 mm launch, 0.40 mm bias-branch, and 0.30 mm ESD-branch
  transitions. No additional RF neck-down was found.
- `GNSS_3V3`, `3V8`, and `V_BAT` use wider 0.5 mm trunks or local copper zones;
  their 0.2/0.3 mm segments are short component fanouts rather than long supply
  bottlenecks.
- The two 0.15 mm GND segments are confined to fine-pitch package fanout. DRC
  accepts them under the existing local rules.
- The front and back copper plots show no complete ground-plane severing under
  either GNSS RF route. Low-speed digital routes cause local return-path
  detours, but a continuous ground path remains available around them.

## Board outline, holes, and perimeter

- The board outline is one closed 70 mm x 70 mm contour.
- Each 3.5 mm mounting hole has 2.0 mm from the finished-hole edge to the board
  edge. Copper clearances around all four holes are visible and DRC-clean.
- No copper-to-board-edge or copper-to-hole violation is reported. Visual
  inspection shows consistent clearance around the perimeter and mounting
  holes.

## Review plots

- [Front copper](layout-review/Front_Copper.svg)
- [Mirrored back copper](layout-review/Back_Copper_Mirrored.svg)

**Result: PASS.** No unresolved ratsnest, ground-continuity, thermal-connection,
neck-down, copper-island, return-path, mounting-hole, or perimeter-clearance
issue was found in this review. Fabricator stack-up confirmation and final RF
impedance calculation remain separate release tasks.
