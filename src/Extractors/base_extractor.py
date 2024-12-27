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

    @abstractmethod
    def validate_source(self, source_path: str) -> bool:
        """
                Проверява дали източникът на данни е валиден.

                Args:
                    source_path (str): Път до източника на данни

                Returns:
                    bool: True ако източникът е валиден, False в противен случай
                """
        pass

    @abstractmethod
    def read_data(self, source_path: str, **kwargs) -> pd.DataFrame:
        """
            Чете данните от източника.

            Args:
                source_path (str): Път до източника на данни
                **kwargs: Допълнителни параметри за четене

            Returns:
                pd.DataFrame: Прочетените данни като pandas DataFrame
        """
        pass
