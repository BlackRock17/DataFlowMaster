import os
from pathlib import Path

# Base roads
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REPORTS_DIR = DATA_DIR / "reports"

# Create the directories if they do not exist
for dir_path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, REPORTS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Login configuration
LOG_LEVEL = "INFO"
LOG_FILE = DATA_DIR / "app.log"

# Performance configuration
PERFORMANCE_LOG_FILE = DATA_DIR / "performance.log"

# Data processing settings
CHUNK_SIZE = 10000  # Chunk size when reading large files
MAX_MEMORY_USE = "1G"  # Maximum memory used

# Supported file types
SUPPORTED_FILE_TYPES = {
    'csv': ['.csv'],
    'json': ['.json', '.jsonl'],
    'excel': ['.xlsx', '.xls'],
    'parquet': ['.parquet']
}