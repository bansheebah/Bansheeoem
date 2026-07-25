# Banshee OEM Extractor

Starter project for exporting the 2006 Yamaha Banshee YFZ350V OEM fiches listed in `links.txt` into a searchable Excel workbook, CSV, and JSON file.

## What it does

- reads the 39 Yamaha Parts House section URLs in `links.txt`;
- fetches each page with `requests`, or with a real Chromium browser when `--browser` is used;
- extracts only OEM-looking part numbers and saves the original page title and URL for auditability;
- creates `output/Banshee_2006_OEM.xlsx`, including a master worksheet, one worksheet per section, and an `Errors` worksheet.

## Setup

Requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

First time using browser mode:

```bash
python -m playwright install chromium
```

## Run

Try a small normal run first:

```bash
python main.py --limit 1
```

If the `Errors` worksheet says no rows were parsed, use browser mode:

```bash
python main.py --browser
```

The source site can change its markup or rate-limit automated traffic. The extractor intentionally logs pages it cannot parse rather than inventing OEM data. Check `output/Banshee_2006_OEM.xlsx` and `logs/extractor.log` after every run.

## Links file format

Each non-comment row is:

```text
Assembly name|https://example.com/oem-page
```

The script preserves repeated hardware rows within an assembly. It does not deduplicate part numbers because the same hardware may be needed at more than one reference location.

## Phone use

This project is intended for a computer or GitHub Codespaces. Pythonista on iPhone generally cannot install Playwright/Chromium, so it can run only the ordinary `requests` mode if dependencies are available.

## Respect the source

Use a low request rate, do not bypass access controls, and review the site's terms before running large batches.

