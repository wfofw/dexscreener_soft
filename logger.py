import logging
import os

LOG_DIR = "logs"
LOG_PREFIX = "log"
LOG_EXTENSION = ".txt"
MAX_LOG_SIZE_MB = 10  # limit of one log file

os.makedirs(LOG_DIR, exist_ok=True)

def get_next_log_filename():
    existing = [f for f in os.listdir(LOG_DIR) if f.startswith(LOG_PREFIX) and f.endswith(LOG_EXTENSION)]
    numbers = []

    for fname in existing:
        try:
            num = int(fname.replace(LOG_PREFIX, "").replace(LOG_EXTENSION, "").strip("_"))
            numbers.append(num)
        except ValueError:
            continue

    next_num = max(numbers, default=0) + 1
    return os.path.join(LOG_DIR, f"{LOG_PREFIX}_{next_num:03d}{LOG_EXTENSION}")

class CounterBasedFileHandler(logging.FileHandler):
    def emit(self, record):
        try:
            if os.path.exists(self.baseFilename):
                size = os.path.getsize(self.baseFilename)
                if size > MAX_LOG_SIZE_MB * 1024 * 1024:
                    self.baseFilename = get_next_log_filename()
                    self.stream.close()
                    self.stream = self._open()
            super().emit(record)
        except Exception:
            self.handleError(record)

def setup_logger(name="main_logger"):
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s — %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # First log file
    log_file = get_next_log_filename()
    file_handler = CounterBasedFileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info("LOG START\n\n")

    return logger