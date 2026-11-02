#!/usr/bin/env python3
"""Export PCBWay assembly BOMs from the approved variant workbook.

Uses only the Python standard library so the workbook is read without
re-saving or otherwise changing it.
"""

from __future__ import annotations

import csv
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "Activity_Brick_Production_BOM.xlsx"
OUT = ROOT / "PCBWay"
VARIANTS = {
    "MAX Production": (3, "MAX_Production_BOM.csv", "MAX_Production_positions.csv"),
    "ZED Production": (4, "ZED_Production_BOM.csv", "ZED_Production_positions.csv"),
    "ZED Development": (5, "ZED_Development_BOM.csv", "ZED_Development_positions.csv"),
}
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
FIELDS = [
    "Line #", "Quantity", "Designator", "MFG Part Number", "Footprint",
    "Manufacturer", "Description", "Type (SMD/THT)", "Distributor",
    "Distributor Part Number", "Value", "Your Instructions / Notes",
]


def shared_strings(archive: zipfile.ZipFile) -> list[str]:
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    return ["".join(item.itertext()) for item in root.findall("m:si", NS)]


def sheet_rows(archive: zipfile.ZipFile, sheet_number: int, strings: list[str]):
    root = ET.fromstring(archive.read(f"xl/worksheets/sheet{sheet_number}.xml"))
    for row in root.findall("m:sheetData/m:row", NS):
        result = {}
        for cell in row.findall("m:c", NS):
            value = cell.find("m:v", NS)
            inline = cell.find("m:is", NS)
            if value is not None:
                content = strings[int(value.text)] if cell.get("t") == "s" else value.text
            else:
                content = "".join(inline.itertext()) if inline is not None else ""
            column = re.match(r"[A-Z]+", cell.get("r", ""))
            if column:
                result[column.group()] = content or ""
        yield result


def references(text: str) -> list[str]:
    return [part.strip() for part in text.split(",") if part.strip()]


def export_one(archive: zipfile.ZipFile, strings: list[str], name: str,
               sheet_number: int, output_name: str, positions_name: str) -> None:
    source_rows = list(sheet_rows(archive, sheet_number, strings))[1:]
    position_file = ROOT / "KiCAD" / "assembly_variants" / positions_name
    with position_file.open(newline="", encoding="utf-8-sig") as handle:
        placement_refs = {row["Ref"] for row in csv.DictReader(handle)}
    bom_refs: set[str] = set()
    output_rows = []

    for source in source_rows:
        if source.get("C") != "Populate":
            continue
        refs = references(source.get("D", ""))
        qty = int(source.get("E", "0"))
        if len(refs) != qty or not refs or any(ref in bom_refs for ref in refs):
            raise ValueError(f"{name}: invalid quantity or duplicate references: {refs}")
        bom_refs.update(refs)
        mpn = source.get("J", "").strip()
        manufacturer = source.get("I", "").strip()
        if not mpn or mpn == "DNP" or not manufacturer or manufacturer == "DNP":
            raise ValueError(f"{name}: missing manufacturer/MPN for {refs}")
        supplier_part = (source.get("V") or source.get("K") or "").strip()
        supplier = "Mouser" if supplier_part.startswith("Mouser") else "LCSC"
        if supplier == "Mouser":
            supplier_part = supplier_part.removeprefix("Mouser ")
        if not supplier_part:
            raise ValueError(f"{name}: missing supplier number for {refs}")
        output_rows.append({
            "Line #": len(output_rows) + 1,
            "Quantity": qty,
            "Designator": ", ".join(refs),
            "MFG Part Number": mpn,
            "Footprint": source.get("H", ""),
            "Manufacturer": manufacturer,
            "Description": source.get("G", ""),
            "Type (SMD/THT)": "Hybrid" if "J4" in refs else "SMD",
            "Distributor": supplier,
            "Distributor Part Number": supplier_part,
            "Value": source.get("F", ""),
            "Your Instructions / Notes": source.get("U", ""),
        })

    if bom_refs != placement_refs:
        raise ValueError(f"{name}: BOM/placement mismatch: "
                         f"BOM only={sorted(bom_refs - placement_refs)}; "
                         f"positions only={sorted(placement_refs - bom_refs)}")
    output = OUT / output_name
    with output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\r\n")
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"{output.relative_to(ROOT)}: {len(output_rows)} lines, {len(bom_refs)} parts")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    with zipfile.ZipFile(SOURCE) as archive:
        strings = shared_strings(archive)
        for name, (sheet_number, output_name, positions_name) in VARIANTS.items():
            export_one(archive, strings, name, sheet_number, output_name, positions_name)


if __name__ == "__main__":
    main()
