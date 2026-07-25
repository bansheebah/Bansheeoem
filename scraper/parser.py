from __future__ import annotations

import re
from bs4 import BeautifulSoup

from .models import PartRow

OEM_RE = re.compile(r"\b\d[A-Z0-9]{2}-[A-Z0-9]{4,5}-[A-Z0-9]{2}(?:-[A-Z0-9]{2})?\b", re.I)
SPACE_RE = re.compile(r"\s+")


def clean(value: str) -> str:
    return SPACE_RE.sub(" ", value or "").strip()


def first_match(pattern: re.Pattern[str], text: str) -> str:
    match = pattern.search(text)
    return match.group(0) if match else ""


def parse_page(html: str, assembly: str, url: str) -> list[PartRow]:
    """Best-effort parser for static OEM fiche markup.

    It deliberately exports only rows containing an OEM-shaped part number.  If a
    site redesigns its markup, those pages are listed in the workbook's Errors
    sheet instead of quietly creating made-up records.
    """
    soup = BeautifulSoup(html, "lxml")
    title = clean(soup.title.get_text(" ") if soup.title else "")
    rows: list[PartRow] = []
    seen: set[tuple[str, str, str]] = set()

    candidates = soup.select("tr, .part, .part-item, .product, li")
    for candidate in candidates:
        text = clean(candidate.get_text(" ", strip=True))
        oem = first_match(OEM_RE, text)
        if not oem or len(text) > 1300:
            continue
        cells = [clean(cell.get_text(" ", strip=True)) for cell in candidate.select("td, th")]
        ref = cells[0] if cells and re.fullmatch(r"\d+", cells[0]) else ""
        # Remove the OEM and common retail noise, retaining the site wording.
        description = clean(text.replace(oem, "", 1))
        description = re.sub(r"\b(?:Retail|Price|MSRP|Add to Cart|In Stock|Unavailable).*$", "", description, flags=re.I)
        qty_match = re.search(r"(?:Qty|QTY|#REQ)\s*[:x]?\s*(\d+)", text, re.I)
        status = "Discontinued" if re.search(r"discontinued|no longer available", text, re.I) else ""
        if not status and re.search(r"unavailable|out of stock", text, re.I):
            status = "Unavailable"
        sup = ""
        sup_match = re.search(r"(?:Supersedes|Replaces)\s*:?\s*([^|]+)", text, re.I)
        if sup_match:
            sup = clean(sup_match.group(1))
        key = (ref, oem.upper(), description)
        if key in seen:
            continue
        seen.add(key)
        rows.append(PartRow(
            assembly=assembly, ref=ref, oem_part_number=oem.upper(),
            description=description, qty=qty_match.group(1) if qty_match else "",
            status=status, superseded=sup, source_url=url, page_title=title,
        ))
    return rows

