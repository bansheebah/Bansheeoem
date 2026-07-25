from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SectionLink:
    section: str
    url: str


@dataclass
class PartRow:
    assembly: str
    ref: str = ""
    oem_part_number: str = ""
    description: str = ""
    qty: str = ""
    status: str = ""
    superseded: str = ""
    source_url: str = ""
    page_title: str = ""
    notes: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

