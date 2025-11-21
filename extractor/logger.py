import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("github_extractor")
logger.setLevel(logging.INFO)

file_handler = TimedRotatingFileHandler(
    filename=LOG_DIR / "extractor.log",
    when="midnight",
    interval=1,
    backupCount=14,
    encoding="utf-8"
)

file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(file_formatter)
logger.addHandler(stream_handler)
