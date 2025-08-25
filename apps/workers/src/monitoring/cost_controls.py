# Created automatically by Cursor AI (2025-08-25)
import json
import time
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import queue

class ResourceType(Enum):
    CPU = "cpu"
    MEMORY = "memory"
    STORAGE = "storage"
    NETWORK = "network"
    CONCURRENCY = "concurrency"

class LimitType(Enum):
    HARD = "hard"
    SOFT = "soft"
    WARNING = "warning"

class ViolationSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class ResourceLimit:
    resource_type: ResourceType
    limit_type: LimitType
    value: float
    unit: str
    description: str
    action: str

@dataclass
class ResourceUsage:
    resource_type: ResourceType
    current_usage: float
    peak_usage: float
    limit: float
    unit: str
    timestamp: datetime
    percentage: float

@dataclass
class ViolationEvent:
    resource_type: ResourceType
    limit_type: LimitType
    current_value: float
    limit_value: float
    severity: ViolationSeverity
    timestamp: datetime
    description: str
    action_taken: str

class CostControls:
    def __init__(self):
        self.limits = self._create_default_limits()
        self.usage_trackers: Dict[str, ResourceUsage] = {}
        self.violations: List[ViolationEvent] = []
        self.callbacks: Dict[str, List[Callable]] = {}
        self.lock = threading.Lock()
        
        # Initialize usage trackers
        for resource_type in ResourceType:
            self.usage_trackers[resource_type.value] = ResourceUsage(
                resource_type=resource_type,
                current_usage=0.0,
                peak_usage=0.0,
                limit=self._get_limit_value(resource_type),
                unit=self._get_unit(resource_type),
                timestamp=datetime.utcnow(),
                percentage=0.0
            )
    
    def _create_default_limits(self) -> Dict[str, List[ResourceLimit]]:
        """Create default resource limits for cost control"""
        return {
            "queue_concurrency": [
                ResourceLimit(
                    resource_type=ResourceType.CONCURRENCY,
                    limit_type=LimitType.HARD,
                    value=50.0,
                    unit="concurrent_jobs",
                    description="Maximum concurrent model runs",
                    action="reject_new_jobs"
                ),
                ResourceLimit(
                    resource_type=ResourceType.CONCURRENCY,
                    limit_type=LimitType.SOFT,
                    value=40.0,
                    unit="concurrent_jobs",
                    description="Soft limit for concurrent model runs",
                    action="throttle_new_jobs"
                ),
                ResourceLimit(
                    resource_type=ResourceType.CONCURRENCY,
                    limit_type=LimitType.WARNING,
                    value=30.0,
                    unit="concurrent_jobs",
                    description="Warning threshold for concurrent model runs",
                    action="log_warning"
                )
            ],
            "model_sandbox": [
                ResourceLimit(
                    resource_type=ResourceType.MEMORY,
                    limit_type=LimitType.HARD,
                    value=8192.0,
                    unit="MB",
                    description="Maximum memory per model run",
                    action="terminate_model"
                ),
                ResourceLimit(
                    resource_type=ResourceType.CPU,
                    limit_type=LimitType.HARD,
                    value=4.0,
                    unit="cores",
                    description="Maximum CPU cores per model run",
                    action="throttle_model"
                ),
                ResourceLimit(
                    resource_type=ResourceType.STORAGE,
                    limit_type=LimitType.HARD,
                    value=1024.0,
                    unit="MB",
                    description="Maximum temporary storage per model run",
                    action="cleanup_storage"
                )
            ],
            "export_size": [
                ResourceLimit(
                    resource_type=ResourceType.STORAGE,
                    limit_type=LimitType.HARD,
                    value=500.0,
                    unit="MB",
                    description="Maximum export file size",
                    action="reject_export"
                ),
                ResourceLimit(
                    resource_type=ResourceType.STORAGE,
                    limit_type=LimitType.SOFT,
                    value=250.0,
                    unit="MB",
                    description="Soft limit for export file size",
                    action="warn_user"
                ),
                ResourceLimit(
                    resource_type=ResourceType.STORAGE,
                    limit_type=LimitType.WARNING,
                    value=100.0,
                    unit="MB",
                    description="Warning threshold for export file size",
                    action="log_warning"
                )
            ],
            "api_rate_limits": [
                ResourceLimit(
                    resource_type=ResourceType.CONCURRENCY,
                    limit_type=LimitType.HARD,
                    value=100.0,
                    unit="requests_per_minute",
                    description="Maximum API requests per minute per user",
                    action="rate_limit_user"
                ),
                ResourceLimit(
                    resource_type=ResourceType.CONCURRENCY,
                    limit_type=LimitType.SOFT,
                    value=80.0,
                    unit="requests_per_minute",
                    description="Soft limit for API requests per minute",
                    action="throttle_user"
                )
            ],
            "database_connections": [
                ResourceLimit(
                    resource_type=ResourceType.CONCURRENCY,
                    limit_type=LimitType.HARD,
                    value=100.0,
                    unit="connections",
                    description="Maximum database connections",
                    action="reject_connection"
                ),
                ResourceLimit(
                    resource_type=ResourceType.CONCURRENCY,
                    limit_type=LimitType.SOFT,
                    value=80.0,
                    unit="connections",
                    description="Soft limit for database connections",
                    action="queue_connection"
                )
            ],
            "storage_quota": [
                ResourceLimit(
                    resource_type=ResourceType.STORAGE,
                    limit_type=LimitType.HARD,
                    value=100000.0,
                    unit="MB",
                    description="Maximum total storage usage",
                    action="reject_upload"
                ),
                ResourceLimit(
                    resource_type=ResourceType.STORAGE,
                    limit_type=LimitType.SOFT,
                    value=80000.0,
                    unit="MB",
                    description="Soft limit for total storage usage",
                    action="warn_admin"
                )
            ]
        }
    
    def _get_limit_value(self, resource_type: ResourceType) -> float:
        """Get the hard limit value for a resource type"""
        for category, limits in self.limits.items():
            for limit in limits:
                if limit.resource_type == resource_type and limit.limit_type == LimitType.HARD:
                    return limit.value
        return float('inf')
    
    def _get_unit(self, resource_type: ResourceType) -> str:
        """Get the unit for a resource type"""
        for category, limits in self.limits.items():
            for limit in limits:
                if limit.resource_type == resource_type:
                    return limit.unit
        return "units"
    
    def check_limit(self, resource_type: ResourceType, current_value: float, 
                   context: str = None) -> List[ViolationEvent]:
        """Check if current usage violates any limits"""
        violations = []
        
        with self.lock:
            # Update usage tracker
            tracker = self.usage_trackers[resource_type.value]
            tracker.current_usage = current_value
            tracker.peak_usage = max(tracker.peak_usage, current_value)
            tracker.timestamp = datetime.utcnow()
            tracker.percentage = (current_value / tracker.limit) * 100 if tracker.limit > 0 else 0
            
            # Check all limits for this resource type
            for category, limits in self.limits.items():
                for limit in limits:
                    if limit.resource_type == resource_type:
                        if self._is_violation(current_value, limit):
                            violation = self._create_violation(current_value, limit, context)
                            violations.append(violation)
                            self.violations.append(violation)
                            
                            # Trigger callbacks
                            self._trigger_callbacks(violation)
        
        return violations
    
    def _is_violation(self, current_value: float, limit: ResourceLimit) -> bool:
        """Check if current value violates a limit"""
        if limit.limit_type == LimitType.HARD:
            return current_value > limit.value
        elif limit.limit_type == LimitType.SOFT:
            return current_value > limit.value
        elif limit.limit_type == LimitType.WARNING:
            return current_value > limit.value
        return False
    
    def _create_violation(self, current_value: float, limit: ResourceLimit, 
                         context: str = None) -> ViolationEvent:
        """Create a violation event"""
        severity = self._determine_severity(limit.limit_type, current_value, limit.value)
        
        return ViolationEvent(
            resource_type=limit.resource_type,
            limit_type=limit.limit_type,
            current_value=current_value,
            limit_value=limit.value,
            severity=severity,
            timestamp=datetime.utcnow(),
            description=f"{limit.description} - Current: {current_value}{limit.unit}, Limit: {limit.value}{limit.unit}",
            action_taken=limit.action
        )
    
    def _determine_severity(self, limit_type: LimitType, current_value: float, 
                           limit_value: float) -> ViolationSeverity:
        """Determine violation severity"""
        if limit_type == LimitType.HARD:
            return ViolationSeverity.CRITICAL
        elif limit_type == LimitType.SOFT:
            return ViolationSeverity.ERROR
        elif limit_type == LimitType.WARNING:
            return ViolationSeverity.WARNING
        else:
            return ViolationSeverity.INFO
    
    def _trigger_callbacks(self, violation: ViolationEvent):
        """Trigger registered callbacks for violation"""
        callback_key = f"{violation.resource_type.value}_{violation.limit_type.value}"
        if callback_key in self.callbacks:
            for callback in self.callbacks[callback_key]:
                try:
                    callback(violation)
                except Exception as e:
                    print(f"Error in violation callback: {e}")
    
    def register_callback(self, resource_type: ResourceType, limit_type: LimitType, 
                         callback: Callable[[ViolationEvent], None]):
        """Register a callback for limit violations"""
        callback_key = f"{resource_type.value}_{limit_type.value}"
        if callback_key not in self.callbacks:
            self.callbacks[callback_key] = []
        self.callbacks[callback_key].append(callback)
    
    def get_usage_summary(self) -> Dict[str, Any]:
        """Get current usage summary"""
        with self.lock:
            summary = {
                "timestamp": datetime.utcnow().isoformat(),
                "usage": {},
                "violations": []
            }
            
            for resource_type, tracker in self.usage_trackers.items():
                summary["usage"][resource_type] = {
                    "current_usage": tracker.current_usage,
                    "peak_usage": tracker.peak_usage,
                    "limit": tracker.limit,
                    "unit": tracker.unit,
                    "percentage": tracker.percentage,
                    "timestamp": tracker.timestamp.isoformat()
                }
            
            # Add recent violations
            recent_violations = [
                v for v in self.violations 
                if v.timestamp >= datetime.utcnow() - timedelta(hours=24)
            ]
            summary["violations"] = [asdict(v) for v in recent_violations]
            
            return summary
    
    def get_resource_limits(self, category: str = None) -> Dict[str, Any]:
        """Get resource limits configuration"""
        if category:
            if category not in self.limits:
                return {}
            return {
                category: [asdict(limit) for limit in self.limits[category]]
            }
        else:
            return {
                cat: [asdict(limit) for limit in limits]
                for cat, limits in self.limits.items()
            }
    
    def update_limit(self, category: str, resource_type: ResourceType, 
                    limit_type: LimitType, new_value: float) -> bool:
        """Update a resource limit"""
        if category not in self.limits:
            return False
        
        for limit in self.limits[category]:
            if (limit.resource_type == resource_type and 
                limit.limit_type == limit_type):
                limit.value = new_value
                return True
        
        return False
    
    def add_limit(self, category: str, limit: ResourceLimit) -> bool:
        """Add a new resource limit"""
        if category not in self.limits:
            self.limits[category] = []
        
        self.limits[category].append(limit)
        return True
    
    def remove_limit(self, category: str, resource_type: ResourceType, 
                    limit_type: LimitType) -> bool:
        """Remove a resource limit"""
        if category not in self.limits:
            return False
        
        self.limits[category] = [
            limit for limit in self.limits[category]
            if not (limit.resource_type == resource_type and 
                   limit.limit_type == limit_type)
        ]
        return True

# Specific cost control implementations
class QueueConcurrencyController:
    def __init__(self, cost_controls: CostControls):
        self.cost_controls = cost_controls
        self.active_jobs = 0
        self.job_queue = queue.Queue()
        self.max_concurrent = 50
        
        # Register callbacks
        self.cost_controls.register_callback(
            ResourceType.CONCURRENCY, 
            LimitType.HARD, 
            self._handle_hard_limit
        )
        self.cost_controls.register_callback(
            ResourceType.CONCURRENCY, 
            LimitType.SOFT, 
            self._handle_soft_limit
        )
    
    def submit_job(self, job_data: Dict[str, Any]) -> bool:
        """Submit a job with concurrency control"""
        # Check current concurrency
        violations = self.cost_controls.check_limit(
            ResourceType.CONCURRENCY, 
            self.active_jobs + 1
        )
        
        # Check for hard limit violations
        hard_violations = [v for v in violations if v.limit_type == LimitType.HARD]
        if hard_violations:
            return False  # Reject job
        
        # Check for soft limit violations
        soft_violations = [v for v in violations if v.limit_type == LimitType.SOFT]
        if soft_violations:
            # Queue job instead of immediate execution
            self.job_queue.put(job_data)
            return True
        
        # Execute job immediately
        self.active_jobs += 1
        return True
    
    def job_completed(self):
        """Mark a job as completed"""
        self.active_jobs = max(0, self.active_jobs - 1)
        
        # Process queued jobs if possible
        while not self.job_queue.empty() and self.active_jobs < self.max_concurrent:
            try:
                job_data = self.job_queue.get_nowait()
                self.active_jobs += 1
                # Process job_data...
            except queue.Empty:
                break
    
    def _handle_hard_limit(self, violation: ViolationEvent):
        """Handle hard concurrency limit violation"""
        print(f"CRITICAL: Hard concurrency limit exceeded: {violation.description}")
        # Implement emergency measures
    
    def _handle_soft_limit(self, violation: ViolationEvent):
        """Handle soft concurrency limit violation"""
        print(f"WARNING: Soft concurrency limit exceeded: {violation.description}")
        # Implement throttling measures

class ModelSandboxController:
    def __init__(self, cost_controls: CostControls):
        self.cost_controls = cost_controls
        self.active_models = {}
        
        # Register callbacks
        self.cost_controls.register_callback(
            ResourceType.MEMORY, 
            LimitType.HARD, 
            self._handle_memory_limit
        )
        self.cost_controls.register_callback(
            ResourceType.CPU, 
            LimitType.HARD, 
            self._handle_cpu_limit
        )
    
    def start_model(self, model_id: str, resource_requirements: Dict[str, float]) -> bool:
        """Start a model with resource limits"""
        # Check memory limit
        total_memory = sum(
            req.get('memory', 0) for req in self.active_models.values()
        ) + resource_requirements.get('memory', 0)
        
        violations = self.cost_controls.check_limit(
            ResourceType.MEMORY, 
            total_memory
        )
        
        if any(v.limit_type == LimitType.HARD for v in violations):
            return False
        
        # Check CPU limit
        total_cpu = sum(
            req.get('cpu', 0) for req in self.active_models.values()
        ) + resource_requirements.get('cpu', 0)
        
        violations = self.cost_controls.check_limit(
            ResourceType.CPU, 
            total_cpu
        )
        
        if any(v.limit_type == LimitType.HARD for v in violations):
            return False
        
        # Start model
        self.active_models[model_id] = resource_requirements
        return True
    
    def stop_model(self, model_id: str):
        """Stop a model and release resources"""
        if model_id in self.active_models:
            del self.active_models[model_id]
    
    def _handle_memory_limit(self, violation: ViolationEvent):
        """Handle memory limit violation"""
        print(f"CRITICAL: Memory limit exceeded: {violation.description}")
        # Terminate models to free memory
    
    def _handle_cpu_limit(self, violation: ViolationEvent):
        """Handle CPU limit violation"""
        print(f"CRITICAL: CPU limit exceeded: {violation.description}")
        # Throttle model execution

class ExportSizeController:
    def __init__(self, cost_controls: CostControls):
        self.cost_controls = cost_controls
        
        # Register callbacks
        self.cost_controls.register_callback(
            ResourceType.STORAGE, 
            LimitType.HARD, 
            self._handle_hard_size_limit
        )
        self.cost_controls.register_callback(
            ResourceType.STORAGE, 
            LimitType.SOFT, 
            self._handle_soft_size_limit
        )
    
    def validate_export_size(self, estimated_size_mb: float) -> Dict[str, Any]:
        """Validate export size against limits"""
        violations = self.cost_controls.check_limit(
            ResourceType.STORAGE, 
            estimated_size_mb
        )
        
        result = {
            "allowed": True,
            "warnings": [],
            "errors": []
        }
        
        for violation in violations:
            if violation.limit_type == LimitType.HARD:
                result["allowed"] = False
                result["errors"].append(violation.description)
            elif violation.limit_type == LimitType.SOFT:
                result["warnings"].append(violation.description)
            elif violation.limit_type == LimitType.WARNING:
                result["warnings"].append(violation.description)
        
        return result
    
    def _handle_hard_size_limit(self, violation: ViolationEvent):
        """Handle hard size limit violation"""
        print(f"CRITICAL: Export size limit exceeded: {violation.description}")
        # Reject export
    
    def _handle_soft_size_limit(self, violation: ViolationEvent):
        """Handle soft size limit violation"""
        print(f"WARNING: Export size soft limit exceeded: {violation.description}")
        # Warn user but allow export

# Usage example
def create_cost_control_system() -> Dict[str, Any]:
    """Create and configure the cost control system"""
    cost_controls = CostControls()
    
    # Create controllers
    queue_controller = QueueConcurrencyController(cost_controls)
    sandbox_controller = ModelSandboxController(cost_controls)
    export_controller = ExportSizeController(cost_controls)
    
    return {
        "cost_controls": cost_controls,
        "queue_controller": queue_controller,
        "sandbox_controller": sandbox_controller,
        "export_controller": export_controller
    }
