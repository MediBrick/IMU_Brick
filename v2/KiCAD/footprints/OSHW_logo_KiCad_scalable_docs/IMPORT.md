# OSHW logo footprint import

Source archive: `/home/uutzinger/Downloads/OSHW_logo_KiCad_scalable.zip`

The legacy `OSHW-logo.mod` library was converted with KiCad 10.0.6 using
`kicad-cli fp upgrade`. The resulting 80 unpacked `.kicad_mod` files are in
`../OSHW.pretty/`, which is registered as the project-local `OSHW` footprint library.

The library provides 1–20 mm logo heights for silkscreen and copper, with
front and horizontally mirrored back variants. As described by the source
instructions, place a `*-back-*` variant and flip it in PCB Editor to put it
on the physical back layer.
