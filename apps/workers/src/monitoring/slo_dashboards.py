# Created automatically by Cursor AI (2025-08-25)
import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import statistics

class MetricType(Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

class SLOStatus(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"

@dataclass
class SLOMetric:
    name: str
    value: float
    unit: str
    timestamp: datetime
    labels: Dict[str, str]
    status: SLOStatus

@dataclass
class SLOThreshold:
    target: float
    warning: float
    critical: float
    unit: str

class SLODashboard:
    def __init__(self):
        self.metrics: Dict[str, List[SLOMetric]] = {}
        self.thresholds = self._create_thresholds()
        self.slos = self._create_slos()
    
    def _create_thresholds(self) -> Dict[str, SLOThreshold]:
        """Define SLO thresholds for different metrics"""
        return {
            # Parcelization SLOs
            "parcelization_duration": SLOThreshold(
                target=30.0, warning=60.0, critical=120.0, unit="seconds"
            ),
            "parcelization_success_rate": SLOThreshold(
                target=99.0, warning=95.0, critical=90.0, unit="percent"
            ),
            "parcelization_accuracy": SLOThreshold(
                target=98.0, warning=95.0, critical=90.0, unit="percent"
            ),
            
            # Model Run SLOs
            "model_run_duration": SLOThreshold(
                target=300.0, warning=600.0, critical=1200.0, unit="seconds"
            ),
            "model_run_success_rate": SLOThreshold(
                target=98.0, warning=95.0, critical=90.0, unit="percent"
            ),
            "model_run_queue_depth": SLOThreshold(
                target=5.0, warning=20.0, critical=50.0, unit="jobs"
            ),
            
            # Optimizer SLOs
            "optimizer_duration": SLOThreshold(
                target=1800.0, warning=3600.0, critical=7200.0, unit="seconds"
            ),
            "optimizer_success_rate": SLOThreshold(
                target=95.0, warning=90.0, critical=85.0, unit="percent"
            ),
            "optimizer_pareto_points": SLOThreshold(
                target=50.0, warning=30.0, critical=20.0, unit="points"
            ),
            
            # Export SLOs
            "export_duration": SLOThreshold(
                target=60.0, warning=120.0, critical=300.0, unit="seconds"
            ),
            "export_success_rate": SLOThreshold(
                target=99.0, warning=97.0, critical=95.0, unit="percent"
            ),
            "export_file_size": SLOThreshold(
                target=50.0, warning=100.0, critical=200.0, unit="MB"
            ),
            
            # System SLOs
            "api_response_time": SLOThreshold(
                target=200.0, warning=500.0, critical=1000.0, unit="ms"
            ),
            "database_connection_pool": SLOThreshold(
                target=80.0, warning=60.0, critical=40.0, unit="percent"
            ),
            "redis_memory_usage": SLOThreshold(
                target=70.0, warning=85.0, critical=95.0, unit="percent"
            ),
            "postgis_query_time": SLOThreshold(
                target=100.0, warning=500.0, critical=1000.0, unit="ms"
            )
        }
    
    def _create_slos(self) -> Dict[str, Dict[str, Any]]:
        """Define SLO objectives and error budgets"""
        return {
            "parcelization": {
                "availability": 99.9,
                "latency_p50": 30.0,
                "latency_p95": 60.0,
                "latency_p99": 120.0,
                "error_budget": 0.1,
                "measurement_window": "30d"
            },
            "model_runs": {
                "availability": 99.5,
                "latency_p50": 300.0,
                "latency_p95": 600.0,
                "latency_p99": 1200.0,
                "error_budget": 0.5,
                "measurement_window": "30d"
            },
            "optimizer": {
                "availability": 99.0,
                "latency_p50": 1800.0,
                "latency_p95": 3600.0,
                "latency_p99": 7200.0,
                "error_budget": 1.0,
                "measurement_window": "30d"
            },
            "exports": {
                "availability": 99.9,
                "latency_p50": 60.0,
                "latency_p95": 120.0,
                "latency_p99": 300.0,
                "error_budget": 0.1,
                "measurement_window": "30d"
            }
        }
    
    def record_metric(self, name: str, value: float, unit: str, 
                     labels: Dict[str, str] = None, timestamp: datetime = None):
        """Record a new metric value"""
        if name not in self.metrics:
            self.metrics[name] = []
        
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        if labels is None:
            labels = {}
        
        # Determine status based on thresholds
        status = self._calculate_status(name, value)
        
        metric = SLOMetric(
            name=name,
            value=value,
            unit=unit,
            timestamp=timestamp,
            labels=labels,
            status=status
        )
        
        self.metrics[name].append(metric)
        
        # Keep only last 1000 metrics per name
        if len(self.metrics[name]) > 1000:
            self.metrics[name] = self.metrics[name][-1000:]
    
    def _calculate_status(self, metric_name: str, value: float) -> SLOStatus:
        """Calculate status based on thresholds"""
        if metric_name not in self.thresholds:
            return SLOStatus.GREEN
        
        threshold = self.thresholds[metric_name]
        
        # For success rates and availability, higher is better
        if "success_rate" in metric_name or "availability" in metric_name:
            if value >= threshold.target:
                return SLOStatus.GREEN
            elif value >= threshold.warning:
                return SLOStatus.YELLOW
            else:
                return SLOStatus.RED
        # For durations and latencies, lower is better
        else:
            if value <= threshold.target:
                return SLOStatus.GREEN
            elif value <= threshold.warning:
                return SLOStatus.YELLOW
            else:
                return SLOStatus.RED
    
    def get_metric_summary(self, name: str, window_hours: int = 24) -> Dict[str, Any]:
        """Get summary statistics for a metric over time window"""
        if name not in self.metrics:
            return {}
        
        cutoff_time = datetime.utcnow() - timedelta(hours=window_hours)
        recent_metrics = [
            m for m in self.metrics[name] 
            if m.timestamp >= cutoff_time
        ]
        
        if not recent_metrics:
            return {}
        
        values = [m.value for m in recent_metrics]
        statuses = [m.status for m in recent_metrics]
        
        return {
            "metric_name": name,
            "window_hours": window_hours,
            "count": len(recent_metrics),
            "min": min(values),
            "max": max(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "p95": self._percentile(values, 95),
            "p99": self._percentile(values, 99),
            "status_distribution": {
                "green": statuses.count(SLOStatus.GREEN),
                "yellow": statuses.count(SLOStatus.YELLOW),
                "red": statuses.count(SLOStatus.RED)
            },
            "current_status": recent_metrics[-1].status if recent_metrics else None,
            "unit": recent_metrics[0].unit if recent_metrics else None
        }
    
    def _percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile of values"""
        if not values:
            return 0.0
        sorted_values = sorted(values)
        index = (percentile / 100) * (len(sorted_values) - 1)
        if index.is_integer():
            return sorted_values[int(index)]
        else:
            lower = sorted_values[int(index)]
            upper = sorted_values[int(index) + 1]
            return lower + (upper - lower) * (index - int(index))
    
    def get_slo_dashboard(self, window_hours: int = 24) -> Dict[str, Any]:
        """Get comprehensive SLO dashboard data"""
        dashboard = {
            "timestamp": datetime.utcnow().isoformat(),
            "window_hours": window_hours,
            "slo_status": {},
            "metric_summaries": {},
            "alerts": []
        }
        
        # Get summaries for all metrics
        for metric_name in self.metrics.keys():
            summary = self.get_metric_summary(metric_name, window_hours)
            if summary:
                dashboard["metric_summaries"][metric_name] = summary
        
        # Calculate SLO status for each service
        for service, slo_config in self.slos.items():
            dashboard["slo_status"][service] = self._calculate_slo_status(
                service, slo_config, window_hours
            )
        
        # Generate alerts
        dashboard["alerts"] = self._generate_alerts(window_hours)
        
        return dashboard
    
    def _calculate_slo_status(self, service: str, slo_config: Dict[str, Any], 
                            window_hours: int) -> Dict[str, Any]:
        """Calculate SLO status for a service"""
        # This would integrate with actual metrics collection
        # For now, return mock data
        return {
            "service": service,
            "availability": {
                "target": slo_config["availability"],
                "current": 99.8,  # Mock value
                "status": SLOStatus.GREEN.value
            },
            "latency": {
                "p50": {"target": slo_config["latency_p50"], "current": 25.0},
                "p95": {"target": slo_config["latency_p95"], "current": 45.0},
                "p99": {"target": slo_config["latency_p99"], "current": 90.0}
            },
            "error_budget": {
                "remaining": 0.08,
                "consumed": 0.02,
                "window": slo_config["measurement_window"]
            }
        }
    
    def _generate_alerts(self, window_hours: int) -> List[Dict[str, Any]]:
        """Generate alerts based on current metrics"""
        alerts = []
        
        for metric_name, metrics in self.metrics.items():
            if not metrics:
                continue
            
            recent_metrics = [
                m for m in metrics[-100:]  # Last 100 metrics
                if m.timestamp >= datetime.utcnow() - timedelta(hours=window_hours)
            ]
            
            if not recent_metrics:
                continue
            
            # Check for consecutive failures
            red_metrics = [m for m in recent_metrics if m.status == SLOStatus.RED]
            if len(red_metrics) >= 3:
                alerts.append({
                    "severity": "critical",
                    "metric": metric_name,
                    "message": f"Critical threshold exceeded for {metric_name}",
                    "count": len(red_metrics),
                    "timestamp": red_metrics[-1].timestamp.isoformat()
                })
            
            # Check for degradation trend
            yellow_metrics = [m for m in recent_metrics if m.status == SLOStatus.YELLOW]
            if len(yellow_metrics) >= 5:
                alerts.append({
                    "severity": "warning",
                    "metric": metric_name,
                    "message": f"Performance degradation detected for {metric_name}",
                    "count": len(yellow_metrics),
                    "timestamp": yellow_metrics[-1].timestamp.isoformat()
                })
        
        return alerts
    
    def export_dashboard_data(self, format: str = "json") -> str:
        """Export dashboard data in specified format"""
        dashboard_data = self.get_slo_dashboard()
        
        if format.lower() == "json":
            return json.dumps(dashboard_data, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported format: {format}")

# Example usage and monitoring functions
class UrbanPlannerMonitor:
    def __init__(self):
        self.dashboard = SLODashboard()
    
    def monitor_parcelization(self, site_id: str, duration: float, 
                            success: bool, accuracy: float = None):
        """Monitor parcelization performance"""
        self.dashboard.record_metric(
            "parcelization_duration", duration, "seconds",
            {"site_id": site_id, "operation": "parcelization"}
        )
        
        success_rate = 100.0 if success else 0.0
        self.dashboard.record_metric(
            "parcelization_success_rate", success_rate, "percent",
            {"site_id": site_id, "operation": "parcelization"}
        )
        
        if accuracy is not None:
            self.dashboard.record_metric(
                "parcelization_accuracy", accuracy, "percent",
                {"site_id": site_id, "operation": "parcelization"}
            )
    
    def monitor_model_run(self, model_type: str, duration: float, 
                         success: bool, queue_depth: int = None):
        """Monitor model run performance"""
        self.dashboard.record_metric(
            "model_run_duration", duration, "seconds",
            {"model_type": model_type}
        )
        
        success_rate = 100.0 if success else 0.0
        self.dashboard.record_metric(
            "model_run_success_rate", success_rate, "percent",
            {"model_type": model_type}
        )
        
        if queue_depth is not None:
            self.dashboard.record_metric(
                "model_run_queue_depth", queue_depth, "jobs",
                {"model_type": model_type}
            )
    
    def monitor_optimizer(self, scenario_id: str, duration: float, 
                         success: bool, pareto_points: int = None):
        """Monitor optimizer performance"""
        self.dashboard.record_metric(
            "optimizer_duration", duration, "seconds",
            {"scenario_id": scenario_id}
        )
        
        success_rate = 100.0 if success else 0.0
        self.dashboard.record_metric(
            "optimizer_success_rate", success_rate, "percent",
            {"scenario_id": scenario_id}
        )
        
        if pareto_points is not None:
            self.dashboard.record_metric(
                "optimizer_pareto_points", pareto_points, "points",
                {"scenario_id": scenario_id}
            )
    
    def monitor_export(self, export_type: str, duration: float, 
                      success: bool, file_size_mb: float = None):
        """Monitor export performance"""
        self.dashboard.record_metric(
            "export_duration", duration, "seconds",
            {"export_type": export_type}
        )
        
        success_rate = 100.0 if success else 0.0
        self.dashboard.record_metric(
            "export_success_rate", success_rate, "percent",
            {"export_type": export_type}
        )
        
        if file_size_mb is not None:
            self.dashboard.record_metric(
                "export_file_size", file_size_mb, "MB",
                {"export_type": export_type}
            )
    
    def get_dashboard(self) -> Dict[str, Any]:
        """Get current dashboard state"""
        return self.dashboard.get_slo_dashboard()
