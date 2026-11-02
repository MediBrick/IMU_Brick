#!/usr/bin/env python3
"""Export placement CSVs from the production BOM and saved KiCad PCB.

Run with /usr/bin/python3 from any directory. This requires KiCad's pcbnew
Python module; it does not modify the board or the BOM.
"""

import csv
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import pcbnew


ROOT = Path(__file__).resolve().parent.parent
WORKBOOK = ROOT / "Activity_Brick_Production_BOM.xlsx"
BOARD = ROOT / "KiCAD" / "Activity_Brick.kicad_pcb"
OUTPUT = ROOT / "KiCAD" / "assembly_variants"
SHEETS = ("MAX Production", "ZED Production", "ZED Development")
NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
REF = re.compile(r"[A-Z]+[0-9]+\Z")


def read_sheets():
    with zipfile.ZipFile(WORKBOOK) as archive:
        strings = [
            "".join(node.text or "" for node in item.iter(f"{{{NS['m']}}}t"))
            for item in ET.fromstring(archive.read("xl/sharedStrings.xml")).findall(
                "m:si", NS
            )
        ]
        book = ET.fromstring(archive.read("xl/workbook.xml"))
        relations = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        targets = {
            item.attrib["Id"]: item.attrib["Target"].lstrip("/")
            for item in relations
        }
        for sheet in book.find("m:sheets", NS):
            name = sheet.attrib["name"]
            if name not in SHEETS:
                continue
            target = targets[sheet.attrib[f"{{{NS['r']}}}id"]]
            if not target.startswith("xl/"):
                target = f"xl/{target}"
            root = ET.fromstring(archive.read(target))
            records = {}
            for row in root.findall(".//m:row", NS):
                cells = {}
                for cell in row.findall("m:c", NS):
                    value = cell.find("m:v", NS)
                    text = "" if value is None else value.text
                    if cell.attrib.get("t") == "s" and text:
                        text = strings[int(text)]
                    elif cell.attrib.get("t") == "inlineStr":
                        text = "".join(
                            node.text or ""
                            for node in cell.iter(f"{{{NS['m']}}}t")
                        )
                    column = re.match(r"[A-Z]+", cell.attrib["r"]).group()
                    cells[column] = text
                for reference in re.split(r"\s*,\s*", cells.get("D", "")):
                    if REF.fullmatch(reference):
                        if reference in records:
                            raise ValueError(f"{name}: duplicate {reference}")
                        records[reference] = cells
            yield name, records


def main():
    board = pcbnew.LoadBoard(str(BOARD))
    footprints = {item.GetReference(): item for item in board.GetFootprints()}
    OUTPUT.mkdir(exist_ok=True)
    for name, records in read_sheets():
        missing = sorted(set(records) - set(footprints))
        if missing:
            raise ValueError(f"{name}: BOM references absent from PCB: {missing}")
        populated = {ref for ref, row in records.items() if row.get("C") == "Populate"}
        if "J1" in populated:
            raise ValueError(f"{name}: J1 header must remain DNP (holes only)")
        if name == "MAX Production":
            if any(row.get("A") == "ZED-F9P" for row in records.values()):
                raise ValueError("MAX variant contains the wrong GNSS subsystem")
            if not {"IC1", "J2", "D2", "L2", "R40", "C16", "D3"} <= populated:
                raise ValueError("MAX variant is missing RF or indicator parts")
            if "R12" in populated:
                raise ValueError("MAX SAFEBOOT resistor R12 must be DNP")
        else:
            if any(row.get("A") == "MAX-M10S" for row in records.values()):
                raise ValueError(f"{name}: wrong GNSS subsystem")
            if not {"IC2", "J3", "D4", "L3", "R32", "C25", "D5", "D6", "D7"} <= populated:
                raise ValueError(f"{name}: missing RF or indicator parts")
            if "R28" in populated:
                raise ValueError(f"{name}: SAFEBOOT resistor R28 must be DNP")
            usb_parts = {"C21", "C24", "C28", "D8", "J4", "R34", "R35", "R38", "R39", "R41", "U4"}
            if name == "ZED Production" and populated & usb_parts:
                raise ValueError("ZED Production includes development USB components")
            if name == "ZED Development" and not usb_parts <= populated:
                raise ValueError("ZED Development is missing USB components")
        filename = OUTPUT / f"{name.replace(' ', '_')}_positions.csv"
        count = 0
        with filename.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            writer.writerow(
                ("Ref", "Value", "Footprint", "PosX_mm", "PosY_mm", "Rot_deg", "Side")
            )
            for reference in sorted(records):
                record = records[reference]
                if record.get("C") != "Populate":
                    continue
                footprint = footprints[reference]
                position = footprint.GetPosition()
                writer.writerow(
                    (
                        reference,
                        footprint.GetValue(),
                        footprint.GetFPIDAsString(),
                        f"{pcbnew.ToMM(position.x):.4f}",
                        f"{pcbnew.ToMM(position.y):.4f}",
                        f"{footprint.GetOrientationDegrees():.2f}",
                        "Front" if footprint.GetLayer() == pcbnew.F_Cu else "Back",
                    )
                )
                count += 1
        print(f"{name}: {count} placement rows -> {filename.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
