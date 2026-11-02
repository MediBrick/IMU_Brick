# Schematic-to-PCB parity verification — 2026-09-20

The root schematic was exported as a KiCad XML netlist and compared with the
saved PCB through KiCad's `pcbnew` API. KiCad-generated net names were normalized
so `/` and `{slash}` were treated as equivalent encodings.

## Results

- Schematic components: **119**
- Schematic numbered pins: **424**
- Connected schematic pin/net assignments: **424**
- Missing PCB references: **0**
- Schematic pins without a matching PCB pad: **0**
- PCB electrical pads without a matching schematic pin: **0**
- Pin-to-net mismatches: **0**
- DRC unconnected pads: **0**
- DRC violations: **0**

The PCB contains 121 footprint references because it includes two additional
padless graphics: `G1` (`OSHW_Logo`) and `G***`
(`OSHW-logo_silkscreen-back_4mm`). Neither introduces electrical pads or nets.

**Result: PASS.**
