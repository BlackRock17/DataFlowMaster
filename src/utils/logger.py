from loguru import logger
import sys
from ..config.settings import LOG_FILE, LOG_LEVEL


# Конфигурация на логъра
def setup_logger():
    """
    Конфигурира логъра с подходящи настройки за нашия проект.
    Записва логовете както в конзолата, така и във файл.
    """
    # Премахваме стандартния handler
    logger.remove()

    # Добавяме handler за конзолата
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=LOG_LEVEL,
        colorize=True
    )

    # Добавяме handler за файл
    logger.add(
        LOG_FILE,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=LOG_LEVEL,
        rotation="10 MB",  # Нов файл на всеки 10MB
        retention="1 week"  # Пази логовете 1 седмица
    )

    return logger


# Създаваме глобална инстанция на логъра
app_logger = setup_logger()


# Помощни функции за често използвани логове
def log_start_process(process_name: str):
    """Логва започването на процес"""
    app_logger.info(f"Започва процес: {process_name}")


def log_end_process(process_name: str):
    """Логва завършването на процес"""
    app_logger.info(f"Завършва процес: {process_name}")


def log_error(error: Exception, process_name: str = None):
    """Логва грешка с детайли"""
    if process_name:
        app_logger.error(f"Грешка в процес {process_name}: {str(error)}")
    else:
        app_logger.error(f"Грешка: {str(error)}")