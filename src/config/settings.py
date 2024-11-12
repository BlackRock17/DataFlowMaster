import os
from pathlib import Path

# Базови пътища
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REPORTS_DIR = DATA_DIR / "reports"

# Създаване на директориите, ако не съществуват
for dir_path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, REPORTS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Конфигурация на логването
LOG_LEVEL = "INFO"
LOG_FILE = DATA_DIR / "app.log"

# Конфигурация на производителността
PERFORMANCE_LOG_FILE = DATA_DIR / "performance.log"

# Настройки за обработка на данни
CHUNK_SIZE = 10000  # Размер на chunk при четене на големи файлове
MAX_MEMORY_USE = "1G"  # Максимална използвана памет

# Типове поддържани файлове
SUPPORTED_FILE_TYPES = {
    'csv': ['.csv'],
    'json': ['.json', '.jsonl'],
    'excel': ['.xlsx', '.xls'],
    'parquet': ['.parquet']
}