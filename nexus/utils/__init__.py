"""
Utility Functions
"""

import logging
import time
from typing import Dict, Any, List
from collections import defaultdict


class Logger:
    """Enhanced logging with context."""

    def __init__(self, level: str = "INFO"):
        self.logger = logging.getLogger("NEXUS")
        self.logger.setLevel(getattr(logging, level))

        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - NEXUS - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)


class MetricsCollector:
    """Collect and aggregate performance metrics."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.metrics = defaultdict(list)
        self.counters = defaultdict(int)

    def record(self, metric: Dict[str, Any]):
        """Record a metric."""
        if not self.enabled:
            return

        for key, value in metric.items():
            if isinstance(value, (int, float)):
                self.metrics[key].append(value)
            elif isinstance(value, bool):
                self.counters[f"{key}_{'true' if value else 'false'}"] += 1
            else:
                self.counters[key] += 1

    def get_stats(self) -> Dict[str, Any]:
        """Get aggregated statistics."""
        stats = {}

        for key, values in self.metrics.items():
            if values:
                stats[key] = {
                    "avg": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "count": len(values),
                }

        stats["counters"] = dict(self.counters)

        return stats

    @property
    def avg_response_time(self) -> float:
        """Average response time."""
        times = self.metrics.get("execution_time", [])
        return sum(times) / len(times) if times else 0.0

    @property
    def tool_success_rate(self) -> float:
        """Tool success rate."""
        success = self.counters.get("success_true", 0)
        failure = self.counters.get("success_false", 0)
        total = success + failure
        return success / total if total > 0 else 0.0

    @property
    def ocr_accuracy(self) -> float:
        """OCR accuracy (placeholder)."""
        # Would calculate from actual OCR validation
        return 0.95

    @property
    def satisfaction_score(self) -> float:
        """User satisfaction score (placeholder)."""
        # Would aggregate from user feedback
        return 0.0


class Timer:
    """Context manager for timing code blocks."""

    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None
        self.elapsed = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        self.elapsed = time.time() - self.start_time
        print(f"{self.name} took {self.elapsed:.2f}s")


def validate_url(url: str) -> bool:
    """Validate URL format."""
    import re

    pattern = re.compile(
        r"^https?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain
        r"localhost|"  # localhost
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # IP
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return pattern.match(url) is not None


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max length."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix
