import time
import psutil
import pandas as pd
from functools import wraps
from ..config.settings import PERFORMANCE_LOG_FILE
from .logger import app_logger


class PerformanceMonitor:
    """
    Operations performance monitoring class.
    Next is execution time, memory used and CPU load.
    """

    def __init__(self):
        self.metrics = []
        self.process = psutil.Process()

    def measure_performance(self, operation_name):
        """
        A decorator to measure the performance of a function.

        Usage example:
        @performance_monitor.measure_performance("read_csv")
        def read_csv_file(filename):
            # code here
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Initial state
                start_time = time.time()
                start_memory = self.process.memory_info().rss / 1024 / 1024  # MB

                try:
                    # Execution of the function
                    result = func(*args, **kwargs)

                    # Final condition
                    end_time = time.time()
                    end_memory = self.process.memory_info().rss / 1024 / 1024
                    cpu_percent = self.process.cpu_percent()

                    # Calculating metrics
                    execution_time = end_time - start_time
                    memory_used = end_memory - start_memory

                    # Recording the metrics
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
                    # Logging metrics on error
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
        """Saves metrics to file and log"""
        # Format the log message
        if metric['status'] == 'success':
            message = (
                f"Operation: {metric['operation']} | "
                f"Time: {metric['execution_time']}s | "
                f"Memory: {metric['memory_used_mb']}MB | "
                f"CPU: {metric['cpu_percent']}%"
            )
        else:
            message = (
                f"Operation: {metric['operation']} | "
                f"Time: {metric['execution_time']}s | "
                f"Status: ERROR | "
                f"Message: {metric['error_message']}"
            )

        app_logger.info(message)

        # Save to file
        df = pd.DataFrame([metric])
        df.to_csv(PERFORMANCE_LOG_FILE, mode='a', header=not PERFORMANCE_LOG_FILE.exists(), index=False)

    def generate_performance_report(self):
        """
        Generates a performance report based on the metrics collected.
        """
        if not self.metrics:
            return "No performance metrics available"

        df = pd.DataFrame(self.metrics)

        report = "=== Performance report ===\n\n"

        # Summary of operations
        summary = df[df['status'] == 'success'].groupby('operation').agg({
            'execution_time': ['count', 'mean', 'min', 'max'],
            'memory_used_mb': 'mean',
            'cpu_percent': 'mean'
        })

        for operation in summary.index:
            stats = summary.loc[operation]
            report += f"Operation: {operation}\n"
            report += f"  Number of performances: {stats['execution_time']['count']}\n"
            report += f"  Average time: {stats['execution_time']['mean']:.3f}s\n"
            report += f"  Min/Max time: {stats['execution_time']['min']:.3f}s / {stats['execution_time']['max']:.3f}s\n"
            report += f"  Average memory used: {stats['memory_used_mb']['mean']:.2f}MB\n"
            report += f"  Average CPU load: {stats['cpu_percent']['mean']:.2f}%\n\n"

        # Errors
        errors = df[df['status'] == 'error']
        if not errors.empty:
            report += "=== Errors ===\n"
            for _, error in errors.iterrows():
                report += f"Operation: {error['operation']}\n"
                report += f"Време: {error['timestamp']}\n"
                report += f"Съобщение: {error['error_message']}\n\n"

        return report


# Създаваме глобална инстанция
performance_monitor = PerformanceMonitor()