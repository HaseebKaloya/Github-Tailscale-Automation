"""
Performance Monitor for Github&Tailscale-Automation
Author: Haseeb Kaloya

Monitors performance metrics and provides insights
"""

import time
import psutil
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from utils.logger import get_logger

@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_mb: float
    repositories_per_minute: float
    api_calls_per_minute: float
    errors_per_minute: float
    average_repo_time: float

class PerformanceMonitor:
    """Monitors and analyzes performance metrics"""
    
    def __init__(self):
        self.logger = get_logger()
        self.metrics_history: List[PerformanceMetrics] = []
        self.start_time = time.time()
        self.total_repos_created = 0
        self.total_api_calls = 0
        self.total_errors = 0
        self.repo_creation_times = []
    
    def record_repository_created(self, creation_time: float):
        """Record a repository creation event"""
        self.total_repos_created += 1
        self.repo_creation_times.append(creation_time)
        
        # Keep only recent times for accurate average
        if len(self.repo_creation_times) > 100:
            self.repo_creation_times = self.repo_creation_times[-100:]
    
    def record_api_call(self):
        """Record an API call"""
        self.total_api_calls += 1
    
    def record_error(self):
        """Record an error occurrence"""
        self.total_errors += 1
    
    def capture_current_metrics(self) -> PerformanceMetrics:
        """Capture current performance metrics"""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_mb = memory.used / (1024 * 1024)
            
            # Performance rates (per minute)
            elapsed_minutes = max((time.time() - self.start_time) / 60, 0.01)
            repositories_per_minute = self.total_repos_created / elapsed_minutes
            api_calls_per_minute = self.total_api_calls / elapsed_minutes
            errors_per_minute = self.total_errors / elapsed_minutes
            
            # Average repository creation time
            average_repo_time = sum(self.repo_creation_times) / len(self.repo_creation_times) if self.repo_creation_times else 0
            
            metrics = PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                memory_mb=memory_mb,
                repositories_per_minute=repositories_per_minute,
                api_calls_per_minute=api_calls_per_minute,
                errors_per_minute=errors_per_minute,
                average_repo_time=average_repo_time
            )
            
            # Store metrics (keep last 1000 entries)
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > 1000:
                self.metrics_history = self.metrics_history[-1000:]
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error capturing performance metrics: {e}")
            return None
    
    def get_performance_summary(self) -> Dict[str, any]:
        """Get comprehensive performance summary"""
        if not self.metrics_history:
            return {}
        
        latest = self.metrics_history[-1]
        elapsed_time = time.time() - self.start_time
        
        # Calculate trends (last 10 vs previous 10 metrics)
        cpu_trend = self._calculate_trend([m.cpu_percent for m in self.metrics_history[-20:]])
        memory_trend = self._calculate_trend([m.memory_percent for m in self.metrics_history[-20:]])
        
        return {
            'runtime': {
                'elapsed_seconds': elapsed_time,
                'elapsed_formatted': str(timedelta(seconds=int(elapsed_time)))
            },
            'throughput': {
                'total_repositories': self.total_repos_created,
                'repositories_per_minute': latest.repositories_per_minute,
                'average_repo_time': latest.average_repo_time,
                'estimated_completion': self._estimate_completion_time()
            },
            'system_resources': {
                'cpu_percent': latest.cpu_percent,
                'cpu_trend': cpu_trend,
                'memory_percent': latest.memory_percent,
                'memory_mb': latest.memory_mb,
                'memory_trend': memory_trend
            },
            'api_usage': {
                'total_api_calls': self.total_api_calls,
                'api_calls_per_minute': latest.api_calls_per_minute,
                'total_errors': self.total_errors,
                'errors_per_minute': latest.errors_per_minute,
                'error_rate': (self.total_errors / max(self.total_api_calls, 1)) * 100
            },
            'quality_metrics': {
                'success_rate': self._calculate_success_rate(),
                'performance_grade': self._calculate_performance_grade(latest)
            }
        }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from list of values"""
        if len(values) < 4:
            return "stable"
        
        mid_point = len(values) // 2
        first_half = sum(values[:mid_point]) / mid_point
        second_half = sum(values[mid_point:]) / (len(values) - mid_point)
        
        change_percent = ((second_half - first_half) / first_half) * 100 if first_half > 0 else 0
        
        if change_percent > 5:
            return "increasing"
        elif change_percent < -5:
            return "decreasing"
        else:
            return "stable"
    
    def _estimate_completion_time(self) -> Optional[str]:
        """Estimate completion time based on current rate"""
        if self.total_repos_created == 0:
            return None
        
        # This would need to be set based on total repositories to create
        # For now, return None since we don't have that context here
        return None
    
    def _calculate_success_rate(self) -> float:
        """Calculate overall success rate"""
        if self.total_api_calls == 0:
            return 100.0
        return ((self.total_api_calls - self.total_errors) / self.total_api_calls) * 100
    
    def _calculate_performance_grade(self, metrics: PerformanceMetrics) -> str:
        """Calculate performance grade based on metrics"""
        score = 100
        
        # Deduct for high resource usage
        if metrics.cpu_percent > 80:
            score -= 20
        elif metrics.cpu_percent > 60:
            score -= 10
        
        if metrics.memory_percent > 80:
            score -= 20
        elif metrics.memory_percent > 60:
            score -= 10
        
        # Deduct for high error rate
        error_rate = (self.total_errors / max(self.total_api_calls, 1)) * 100
        if error_rate > 10:
            score -= 30
        elif error_rate > 5:
            score -= 15
        
        # Deduct for slow throughput
        if metrics.repositories_per_minute < 1:
            score -= 20
        elif metrics.repositories_per_minute < 2:
            score -= 10
        
        if score >= 90:
            return "A (Excellent)"
        elif score >= 80:
            return "B (Good)"
        elif score >= 70:
            return "C (Fair)"
        elif score >= 60:
            return "D (Poor)"
        else:
            return "F (Critical)"
    
    def generate_performance_report(self) -> str:
        """Generate detailed performance report"""
        summary = self.get_performance_summary()
        
        if not summary:
            return "📊 Performance Report: No data available"
        
        report = [
            "📊 Performance Analysis Report",
            "=" * 50,
            f"⏱️  Runtime: {summary['runtime']['elapsed_formatted']}",
            f"🚀 Repositories Created: {summary['throughput']['total_repositories']}",
            f"📈 Creation Rate: {summary['throughput']['repositories_per_minute']:.1f}/min",
            f"⚡ Avg Creation Time: {summary['throughput']['average_repo_time']:.1f}s",
            "",
            "💻 System Resources:",
            f"  • CPU Usage: {summary['system_resources']['cpu_percent']:.1f}% ({summary['system_resources']['cpu_trend']})",
            f"  • Memory Usage: {summary['system_resources']['memory_percent']:.1f}% ({summary['system_resources']['memory_mb']:.0f} MB)",
            "",
            "🌐 API Usage:",
            f"  • Total API Calls: {summary['api_usage']['total_api_calls']}",
            f"  • API Rate: {summary['api_usage']['api_calls_per_minute']:.1f}/min",
            f"  • Error Rate: {summary['api_usage']['error_rate']:.1f}%",
            "",
            f"🎯 Overall Grade: {summary['quality_metrics']['performance_grade']}",
            f"✅ Success Rate: {summary['quality_metrics']['success_rate']:.1f}%"
        ]
        
        return '\n'.join(report)
