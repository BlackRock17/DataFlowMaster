from abc import ABC, abstractmethod
import pandas as pd
from pathlib import Path
from ..utils.logger import app_logger
from ..utils.performance_monitor import performance_monitor

class BaseExtractor(ABC):
    """
    Базов клас за всички extractors.
    Дефинира общия интерфейс и функционалност за извличане на данни.
    """

    def __init__(self):
        self.logger = app_logger