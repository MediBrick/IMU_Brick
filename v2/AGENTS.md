# Activity Brick V2 agent instructions

These instructions apply to all files under `v2/`.

- Treat the datasheets in `datasheets/` as the primary technical sources.
- Keep KiCad project files and project-local libraries under `KiCAD/`.
- Use the unpacked KiCad 10 library formats:
  - one `.kicad_sym` file per symbol in
    `KiCAD/symbols/ActivityBrick.kicad_symdir/`;
  - one `.kicad_mod` file per footprint in
    `KiCAD/footprints/ActivityBrick.pretty/`.
- Store project-local STEP and WRL models in
  `KiCAD/3dmodels/ActivityBrick.3dshapes/` and reference them through
  `${KIPRJMOD}` paths.
- Store reusable schematic and PCB fragments in
  `KiCAD/design_blocks/ActivityBrick.kicad_blocks/`.
- Verify every generated or downloaded symbol and footprint against the exact
  manufacturer ordering code and datasheet package drawing before use.
- Preserve the existing `v1/` design and unrelated working-tree changes.
- Run KiCad ERC and DRC after schematic or PCB changes and clearly distinguish
  automated checks from manual electrical, RF, mechanical, and layout review.
- The MAX-M10S and ZED-F9P are mutually exclusive assembly options. Keep their
  antenna paths separate and mark the unused option as not populated.
