import time
import psutil
import pandas as pd
from functools import wraps
from ..config.settings import PERFORMANCE_LOG_FILE
from .logger import app_logger


class PerformanceMonitor:
    """
    Клас за мониторинг на производителността на операциите.
    Следи време за изпълнение, използвана памет и CPU натоварване.
    """

    def __init__(self):
        self.metrics = []
        self.process = psutil.Process()

    def measure_performance(self, operation_name):
        """
        Декоратор за измерване на производителността на функция.

        Пример на използване:
        @performance_monitor.measure_performance("read_csv")
        def read_csv_file(filename):
            # код тук
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Начално състояние
                start_time = time.time()
                start_memory = self.process.memory_info().rss / 1024 / 1024  # MB

                try:
                    # Изпълнение на функцията
                    result = func(*args, **kwargs)

                    # Крайно състояние
                    end_time = time.time()
                    end_memory = self.process.memory_info().rss / 1024 / 1024
                    cpu_percent = self.process.cpu_percent()

                    # Изчисляване на метрики
                    execution_time = end_time - start_time
                    memory_used = end_memory - start_memory

                    # Записване на метриките
                    metric = {
                        'timestamp': pd.Timestamp.now(),
                        'operation': operation_name,
                        'execution_time': round(execution_time, 3),
                        'memory_used_mb': round(memory_used, 2),
                        'cpu_percent': round(cpu_percent, 2),
                        'status': 'success'
                    }

                    self.metrics.append(metric)
                    self._log_metric(metric)

                    return result

                except Exception as e:
                    # Записване на метрики при грешка
                    end_time = time.time()
                    metric = {
                        'timestamp': pd.Timestamp.now(),
                        'operation': operation_name,
                        'execution_time': round(end_time - start_time, 3),
                        'status': 'error',
                        'error_message': str(e)
                    }
                    self.metrics.append(metric)
                    self._log_metric(metric)
                    raise

            return wrapper

        return decorator

    def _log_metric(self, metric):
        """Записва метриките във файл и лог"""
        # Форматиране на съобщението за лог
        if metric['status'] == 'success':
            message = (
                f"Операция: {metric['operation']} | "
                f"Време: {metric['execution_time']}s | "
                f"Памет: {metric['memory_used_mb']}MB | "
                f"CPU: {metric['cpu_percent']}%"
            )
        else:
            message = (
                f"Операция: {metric['operation']} | "
                f"Време: {metric['execution_time']}s | "
                f"Статус: ГРЕШКА | "
                f"Съобщение: {metric['error_message']}"
            )

        app_logger.info(message)

        # Запис във файл
        df = pd.DataFrame([metric])
        df.to_csv(PERFORMANCE_LOG_FILE, mode='a', header=not PERFORMANCE_LOG_FILE.exists(), index=False)

    def generate_performance_report(self):
        """
        Генерира отчет за производителността на базата на събраните метрики.
        """
        if not self.metrics:
            return "Няма налични метрики за производителност"

        df = pd.DataFrame(self.metrics)

        report = "=== Отчет за производителност ===\n\n"

        # Обобщение по операции
        summary = df[df['status'] == 'success'].groupby('operation').agg({
            'execution_time': ['count', 'mean', 'min', 'max'],
            'memory_used_mb': 'mean',
            'cpu_percent': 'mean'
        })

        for operation in summary.index:
            stats = summary.loc[operation]
            report += f"Операция: {operation}\n"
            report += f"  Брой изпълнения: {stats['execution_time']['count']}\n"
            report += f"  Средно време: {stats['execution_time']['mean']:.3f}s\n"
            report += f"  Мин/Макс време: {stats['execution_time']['min']:.3f}s / {stats['execution_time']['max']:.3f}s\n"
            report += f"  Средна използвана памет: {stats['memory_used_mb']['mean']:.2f}MB\n"
            report += f"  Средно CPU натоварване: {stats['cpu_percent']['mean']:.2f}%\n\n"

        # Грешки
        errors = df[df['status'] == 'error']
        if not errors.empty:
            report += "=== Грешки ===\n"
            for _, error in errors.iterrows():
                report += f"Операция: {error['operation']}\n"
                report += f"Време: {error['timestamp']}\n"
                report += f"Съобщение: {error['error_message']}\n\n"

        return report


# Създаваме глобална инстанция
performance_monitor = PerformanceMonitor()