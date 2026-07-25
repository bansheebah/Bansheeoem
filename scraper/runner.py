from __future__ import annotations

import logging
import time
from pathlib import Path

from .exporter import export
from .http import fetch_html, fetch_html_browser
from .models import PartRow, SectionLink
from .parser import parse_page


def load_links(path: Path) -> list[SectionLink]:
    links: list[SectionLink] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"): continue
        section, sep, url = line.partition("|")
        if not sep or not url.startswith("http"):
            raise ValueError(f"Invalid links.txt row: {line}")
        links.append(SectionLink(section.strip(), url.strip()))
    return links


def run(links_file: Path, *, browser: bool, limit: int | None, delay: bool) -> int:
    links = load_links(links_file)
    if limit is not None: links = links[:limit]
    rows: list[PartRow] = []; errors: list[dict] = []
    print(f"Processing {len(links)} OEM sections...")
    for number, link in enumerate(links, 1):
        print(f"[{number}/{len(links)}] {link.section}")
        try:
            html = fetch_html_browser(link.url) if browser else fetch_html(link.url)
            found = parse_page(html, link.section, link.url)
            if not found:
                errors.append({"assembly": link.section, "source_url": link.url, "error": "No OEM-looking rows parsed. Re-run with --browser or update parser selectors."})
            rows.extend(found)
            logging.info("%s: %d rows", link.section, len(found))
        except Exception as exc:
            logging.exception("Failed: %s", link.section)
            errors.append({"assembly": link.section, "source_url": link.url, "error": str(exc)})
        if delay and number < len(links): time.sleep(1.25)
    export(rows, errors)
    print(f"Done: {len(rows)} rows. See output/ and logs/extractor.log.")
    return 0 if not errors else 2

