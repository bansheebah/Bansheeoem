"""Project-wide defaults for the Yamaha OEM extractor."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LINKS_FILE = ROOT / "links.txt"
OUTPUT_DIR = ROOT / "output"
LOG_DIR = ROOT / "logs"

REQUEST_TIMEOUT_SECONDS = 35
REQUEST_DELAY_SECONDS = 1.25
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36 "
    "BansheeOEMExtractor/0.1"
)

OUTPUT_XLSX = OUTPUT_DIR / "Banshee_2006_OEM.xlsx"
OUTPUT_CSV = OUTPUT_DIR / "Banshee_2006_OEM.csv"
OUTPUT_JSON = OUTPUT_DIR / "Banshee_2006_OEM.json"
ERROR_LOG = LOG_DIR / "extractor.log"

