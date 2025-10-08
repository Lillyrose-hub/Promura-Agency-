"""
Enhanced Logging System for PROMURA Dashboard
Tracks API calls, success rates, errors, and performance metrics
"""

import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from collections import defaultdict, deque
import threading

class PromuraLogger:
    """Comprehensive logging system with metrics tracking"""

    def __init__(self, log_dir: Optional[Path] = None):
        """Initialize the logging system"""
        # Set up directories
        self.log_dir = log_dir or Path.home() / ".onlysnarf" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Log files
        self.api_log = self.log_dir / "api_calls.log"
        self.error_log = self.log_dir / "errors.log"
        self.metrics_log = self.log_dir / "metrics.json"
        self.posts_log = self.log_dir / "posts.log"

        # Configure Python logging
        self._setup_logging()

        # Metrics storage
        self.metrics = {
            "api_calls": defaultdict(lambda: {"success": 0, "failure": 0, "total": 0}),
            "posts": defaultdict(lambda: {"completed": 0, "failed": 0, "scheduled": 0}),
            "errors": defaultdict(list),
            "performance": defaultdict(list),
            "session_start": datetime.now().isoformat()
        }

        # Real-time tracking
        self.recent_api_calls = deque(maxlen=100)  # Last 100 API calls
        self.recent_errors = deque(maxlen=50)  # Last 50 errors
        self.response_times = deque(maxlen=100)  # Response time tracking

        # Thread safety
        self.lock = threading.Lock()

        # Load existing metrics
        self._load_metrics()

        self.logger.info("🚀 PROMURA Logger initialized")

    def _setup_logging(self):
        """Configure Python logging handlers"""
        # Main logger
        self.logger = logging.getLogger("PROMURA")
        self.logger.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_format)

        # File handler for all logs
        file_handler = logging.FileHandler(self.log_dir / "promura.log")
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
        )
        file_handler.setFormatter(file_format)

        # Error file handler
        error_handler = logging.FileHandler(self.error_log)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_format)

        # Add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)

    def _load_metrics(self):
        """Load existing metrics from file"""
        if self.metrics_log.exists():
            try:
                with open(self.metrics_log, 'r') as f:
                    saved_metrics = json.load(f)
                    # Merge with current metrics
                    for key in saved_metrics:
                        if key != "session_start":
                            self.metrics[key].update(saved_metrics[key])
            except Exception as e:
                self.logger.warning(f"Could not load metrics: {e}")

    def _save_metrics(self):
        """Save current metrics to file"""
        with self.lock:
            try:
                # Convert defaultdicts to regular dicts for JSON serialization
                save_data = {
                    "api_calls": dict(self.metrics["api_calls"]),
                    "posts": dict(self.metrics["posts"]),
                    "errors": dict(self.metrics["errors"]),
                    "performance": dict(self.metrics["performance"]),
                    "session_start": self.metrics["session_start"],
                    "last_updated": datetime.now().isoformat()
                }

                with open(self.metrics_log, 'w') as f:
                    json.dump(save_data, f, indent=2)
            except Exception as e:
                self.logger.error(f"Could not save metrics: {e}")

    def log_api_call(self, endpoint: str, method: str, success: bool,
                     response_time: float, details: Optional[Dict] = None):
        """Log an API call with metrics"""
        with self.lock:
            # Update metrics
            self.metrics["api_calls"][endpoint]["total"] += 1
            if success:
                self.metrics["api_calls"][endpoint]["success"] += 1
            else:
                self.metrics["api_calls"][endpoint]["failure"] += 1

            # Track response time
            self.response_times.append(response_time)
            self.metrics["performance"][endpoint].append({
                "time": response_time,
                "timestamp": datetime.now().isoformat()
            })

            # Log entry
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "endpoint": endpoint,
                "method": method,
                "success": success,
                "response_time": response_time,
                "details": details or {}
            }

            # Add to recent calls
            self.recent_api_calls.append(log_entry)

            # Write to log file
            with open(self.api_log, 'a') as f:
                f.write(json.dumps(log_entry) + "\n")

            # Log to console
            status = "✅" if success else "❌"
            self.logger.info(
                f"{status} API Call: {method} {endpoint} "
                f"({response_time:.2f}s)"
            )

            # Save metrics periodically
            if len(self.recent_api_calls) % 10 == 0:
                self._save_metrics()

    def log_post_completion(self, post_id: str, status: str,
                           models: List[str], content: str,
                           schedule_time: Optional[str] = None):
        """Log post completion with details"""
        with self.lock:
            # Update post metrics
            if status == "completed":
                self.metrics["posts"]["overall"]["completed"] += 1
            elif status == "failed":
                self.metrics["posts"]["overall"]["failed"] += 1
            elif status == "scheduled":
                self.metrics["posts"]["overall"]["scheduled"] += 1

            # Log entry
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "post_id": post_id,
                "status": status,
                "models": models,
                "content_preview": content[:100] if content else "",
                "schedule_time": schedule_time
            }

            # Write to posts log
            with open(self.posts_log, 'a') as f:
                f.write(json.dumps(log_entry) + "\n")

            # Log to console
            emoji = {
                "completed": "✅",
                "scheduled": "🕐",
                "failed": "❌"
            }.get(status, "❓")

            self.logger.info(
                f"{emoji} Post {status}: {post_id} to {len(models)} models"
            )

    def log_error(self, error_type: str, message: str,
                 details: Optional[Dict] = None, exception: Optional[Exception] = None):
        """Log error with categorization"""
        with self.lock:
            # Create error entry
            error_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": error_type,
                "message": message,
                "details": details or {},
                "exception": str(exception) if exception else None
            }

            # Add to metrics
            self.metrics["errors"][error_type].append(error_entry)
            self.recent_errors.append(error_entry)

            # Log to error logger
            if exception:
                self.logger.error(f"{error_type}: {message}", exc_info=exception)
            else:
                self.logger.error(f"{error_type}: {message}")

            # Save metrics
            self._save_metrics()

    def get_success_rate(self, endpoint: Optional[str] = None) -> float:
        """Get API success rate"""
        with self.lock:
            if endpoint:
                stats = self.metrics["api_calls"].get(endpoint, {})
                total = stats.get("total", 0)
                if total == 0:
                    return 0.0
                return (stats.get("success", 0) / total) * 100
            else:
                # Overall success rate
                total_success = sum(
                    stats["success"] for stats in self.metrics["api_calls"].values()
                )
                total_calls = sum(
                    stats["total"] for stats in self.metrics["api_calls"].values()
                )
                if total_calls == 0:
                    return 0.0
                return (total_success / total_calls) * 100

    def get_average_response_time(self) -> float:
        """Get average API response time"""
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)

    def get_error_summary(self) -> Dict[str, int]:
        """Get summary of errors by type"""
        with self.lock:
            return {
                error_type: len(errors)
                for error_type, errors in self.metrics["errors"].items()
            }

    def get_post_statistics(self) -> Dict[str, Any]:
        """Get post completion statistics"""
        with self.lock:
            posts = self.metrics["posts"].get("overall", {})
            total = sum(posts.values())

            return {
                "total": total,
                "completed": posts.get("completed", 0),
                "failed": posts.get("failed", 0),
                "scheduled": posts.get("scheduled", 0),
                "success_rate": (
                    (posts.get("completed", 0) / total * 100) if total > 0 else 0
                )
            }

    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """Get all metrics for dashboard display"""
        return {
            "api": {
                "success_rate": self.get_success_rate(),
                "avg_response_time": self.get_average_response_time(),
                "total_calls": sum(
                    stats["total"] for stats in self.metrics["api_calls"].values()
                ),
                "recent_calls": list(self.recent_api_calls)[-10:]  # Last 10
            },
            "posts": self.get_post_statistics(),
            "errors": {
                "summary": self.get_error_summary(),
                "recent": list(self.recent_errors)[-5:]  # Last 5 errors
            },
            "performance": {
                "uptime": str(
                    datetime.now() - datetime.fromisoformat(self.metrics["session_start"])
                ),
                "avg_response_time": f"{self.get_average_response_time():.2f}s"
            }
        }

    def export_logs(self, output_file: Optional[Path] = None) -> Path:
        """Export all logs to a single file"""
        output = output_file or self.log_dir / f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        export_data = {
            "exported_at": datetime.now().isoformat(),
            "metrics": self.get_dashboard_metrics(),
            "full_metrics": {
                "api_calls": dict(self.metrics["api_calls"]),
                "posts": dict(self.metrics["posts"]),
                "errors": dict(self.metrics["errors"])
            }
        }

        with open(output, 'w') as f:
            json.dump(export_data, f, indent=2)

        self.logger.info(f"📊 Logs exported to {output}")
        return output

    def clear_old_logs(self, days: int = 30):
        """Clear logs older than specified days"""
        cutoff = datetime.now() - timedelta(days=days)

        for log_file in self.log_dir.glob("*.log"):
            if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff:
                log_file.unlink()
                self.logger.info(f"Deleted old log: {log_file.name}")

# Global logger instance
logger = PromuraLogger()