# USB library import — 2026-09-17

Imported from the three files in `dowbloads/`; originals preserved.

| Source | Project-local result | Status |
| --- | --- | --- |
| ul_USB4120-03-C.zip | USB4120-03-C symbol; USB4120-03-C_GCT footprint | Imported; no STEP supplied |
| LIB_PRTR5V0U4D,125.zip | PRTR5V0U4D,125 symbol and STEP; PRTR5V0U4D_SOT457 footprint | Unused four-channel reference; not the selected USB protection |
| SOT886.step | 3dmodels/ActivityBrick.3dshapes/SOT886.step | Stored unattached; does not match U4D SOT457 |

Symbols are in `symbols/ActivityBrick.kicad_symdir/`, footprints in `footprints/ActivityBrick.pretty/`, models in `3dmodels/ActivityBrick.3dshapes/`.

USB4120 checked against the manufacturer GCT A3 drawing, saved in `../datasheets/USB4120_GCT_A3.pdf` (manufacturer drawing obtained from https://www.avelmak.sk/media/dsc_items/91622/usb4120.pdf). Corrected shell slots to 1.10 × 0.60 mm, shell pads to 1.35 × 0.85 mm, contacts to 0.30 × 0.87 mm, and locating holes to unnumbered NPTH (0.52 mm circle and 0.72 × 0.52 mm oval). Added S1–S4 shield pins to symbol and footprint. Manufacturer drawing specifies 1.00 ± 0.10 mm PCB thickness; mechanical compatibility remains to be confirmed.

PRTR5V0U4D checked against https://assets.nexperia.com/documents/data-sheet/PRTR5V0U4D.pdf: pins 1/3/4/6 are I/O, 2 GND, 5 VCC; SOT457 has 0.95 mm pitch. Vendor IPC pads are retained; they differ from the manufacturer's recommended land pattern, so review before any future use. The model uses a project-relative ${KIPRJMOD} path; vendor transform is retained and 3D alignment remains unverified.

Validation: both symbols upgraded and exported with KiCad 10 CLI; both footprints exported to SVG successfully. Symbol-to-footprint pin sets match (20 connector pins including shield; 6 U4D pins). STEP headers checked; this does not establish model alignment. No schematic or PCB was changed, so ERC/DRC was not run. Library checks do not constitute electrical, layout or mechanical signoff.

Selected USB ESD is now STMicroelectronics USBLC6-2SC6. Its CAD was subsequently imported as described below; the downloaded PRTR files are retained only as references.

## USBLC6-2SC6 follow-up import

Sources: `dowbloads/USBLC6-2SC6.zip` and `dowbloads/SOT23-6L_STM.step`; originals preserved.

- Symbol: `symbols/ActivityBrick.kicad_symdir/USBLC6-2SC6.kicad_sym`; reference D, passive terminals, explicit names, local footprint link, manufacturer datasheet link. KiCad 10 upgrade and SVG export passed.
- Footprint: `footprints/ActivityBrick.pretty/USBLC6-2SC6_SOT23-6L.kicad_mod`. Verified pin grouping against ST DS4260 Rev 7 page 1 (1/6 I/O1, 2 GND, 3/4 I/O2, 5 VBUS). Package pitch is 0.95 mm and fab body 1.625 × 2.925 mm, within page 12 limits. Replaced vendor IPC pads (1.21 × 0.59 mm at x ±1.255 mm) with Figure 19 recommended lands (1.20 × 0.60 mm at x ±1.15 mm), retaining 0.95 mm pitch. Removed vendor mask expansion override; moved pin-1 marker inside expanded courtyard.
- Linked model: `3dmodels/ActivityBrick.3dshapes/SOT23-6L_STM.step` via `${KIPRJMOD}`, unity scale and zero transform. Model checked in a temporary KiCad board render: six leads align with pads and pin-1 marker matches. STEP export succeeded. Model coordinate ranges agree with SOT23-6L package limits.
- ZIP model: `3dmodels/ActivityBrick.3dshapes/USBLC6-2SC6.step`, retained unlinked. It uses different axes/origin and is not interchangeable without a transform.

The local `datasheets/DS_usblc6-2.pdf` is the technical source. No project schematic or PCB was edited. ERC/DRC was not run; library parsing, STEP export and manual model alignment checks do not replace assembled-board electrical or mechanical validation.
