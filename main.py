"""CLI entry point for Banshee OEM Extractor."""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

from config import ERROR_LOG, LINKS_FILE, LOG_DIR, OUTPUT_DIR
from scraper.runner import run


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract Yamaha Banshee OEM fiche data.")
    parser.add_argument("--links", type=Path, default=LINKS_FILE, help="links.txt path")
    parser.add_argument("--browser", action="store_true", help="Use Playwright for JavaScript pages")
    parser.add_argument("--limit", type=int, help="Process only the first N sections")
    parser.add_argument("--no-delay", action="store_true", help="Skip courtesy delay (testing only)")
    return parser.parse_args()


def main() -> int:
    OUTPUT_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=ERROR_LOG,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    args = parse_args()
    return run(args.links, browser=args.browser, limit=args.limit, delay=not args.no_delay)


if __name__ == "__main__":
    raise SystemExit(main())

