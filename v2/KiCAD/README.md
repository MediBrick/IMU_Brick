# Activity Brick V2 KiCad libraries

This directory is ready to hold the Activity Brick V2 KiCad project. KiCad
automatically reads the three project library tables when the project is saved
in this directory.

- `ActivityBrickV2.kicad_pro`: KiCad 10 project entry point
- `ActivityBrickV2.kicad_sch`: main schematic
- `ActivityBrickV2.kicad_pcb`: PCB layout
- `symbols/ActivityBrick.kicad_symdir/`: unpacked project-local symbol library;
  store each symbol in its own `.kicad_sym` file
- `footprints/ActivityBrick.pretty/`: project-local footprint library; store each
  footprint in its own `.kicad_mod` file
- `3dmodels/ActivityBrick.3dshapes/`: project-local STEP and WRL models
- `design_blocks/ActivityBrick.kicad_blocks/`: reusable schematic and PCB blocks

The design-block library contains empty, valid schematic blocks for `Power`,
`Sensors`, `GNSS_MAX_M10S`, `GNSS_ZED_F9P`, and `Feather_Interface`.

The PCB intentionally has no board outline yet. DRC will report
`invalid_outline` until the mechanical board dimensions are defined on
`Edge.Cuts`.

## Creating a design block

1. Open the Activity Brick V2 project in KiCad 10.
2. In the Schematic or PCB Editor, select **View -> Panels -> Design Blocks**.
3. Select the `ActivityBrick` library.
4. Use **Save Selection as Design Block** or **Save Current Sheet as Design Block**.

Keep downloaded or generated symbols and footprints in these project-local
libraries so the design does not depend on a machine-specific global library.
Reference project-local models from footprints using paths such as
`${KIPRJMOD}/3dmodels/ActivityBrick.3dshapes/BMI323.step`.

## Manufacturer component pages

- [Bosch Sensortec BMI323](https://www.bosch-sensortec.com/en/products/motion-sensors/imus/bmi323)
- [Bosch Sensortec BMM350](https://www.bosch-sensortec.com/en/products/motion-sensors/magnetometers/bmm350)
- [Bosch Sensortec BMP581](https://www.bosch-sensortec.com/en/products/environmental-sensors/pressure-sensors/bmp581)
- [u-blox MAX-M10 series (MAX-M10S-00B)](https://www.u-blox.com/en/product/max-m10-series?legacy=Current)
- [u-blox ZED-F9P series (ZED-F9P-05B)](https://www.u-blox.com/en/product/zed-f9p-module)
