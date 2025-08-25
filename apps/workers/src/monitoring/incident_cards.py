# Created automatically by Cursor AI (2025-08-25)
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum

class IncidentSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IncidentStatus(Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    MITIGATED = "mitigated"
    RESOLVED = "resolved"
    CLOSED = "closed"

@dataclass
class IncidentCard:
    id: str
    title: str
    description: str
    severity: IncidentSeverity
    status: IncidentStatus
    created_at: datetime
    updated_at: datetime
    affected_services: List[str]
    symptoms: List[str]
    root_causes: List[str]
    mitigation_steps: List[str]
    resolution_steps: List[str]
    escalation_path: List[str]
    metrics_to_monitor: List[str]
    checklists: Dict[str, List[str]]

class IncidentResponseSystem:
    def __init__(self):
        self.incident_cards = self._create_incident_cards()
        self.active_incidents: Dict[str, IncidentCard] = {}
    
    def _create_incident_cards(self) -> Dict[str, IncidentCard]:
        """Create predefined incident response cards"""
        return {
            "websocket_degradation": self._create_websocket_degradation_card(),
            "nats_backlog": self._create_nats_backlog_card(),
            "redis_eviction": self._create_redis_eviction_card(),
            "postgis_bloat": self._create_postgis_bloat_card(),
            "api_timeout": self._create_api_timeout_card(),
            "database_connection_pool_exhaustion": self._create_db_pool_exhaustion_card(),
            "model_run_failures": self._create_model_run_failures_card(),
            "export_timeout": self._create_export_timeout_card()
        }
    
    def _create_websocket_degradation_card(self) -> IncidentCard:
        """WebSocket connection degradation incident card"""
        return IncidentCard(
            id="websocket_degradation",
            title="WebSocket Connection Degradation",
            description="Real-time map updates and collaboration features experiencing connection issues",
            severity=IncidentSeverity.HIGH,
            status=IncidentStatus.OPEN,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            affected_services=["frontend", "gateway", "orchestrator"],
            symptoms=[
                "Map updates not appearing in real-time",
                "Collaboration cursors not visible",
                "WebSocket connection timeouts",
                "Increased reconnection attempts",
                "User reports of 'connection lost' messages"
            ],
            root_causes=[
                "High WebSocket server load",
                "Network connectivity issues",
                "Memory pressure on WebSocket servers",
                "NATS message queue backlog",
                "Load balancer configuration issues"
            ],
            mitigation_steps=[
                "Scale WebSocket servers horizontally",
                "Implement connection pooling",
                "Add circuit breakers for WebSocket connections",
                "Enable WebSocket compression",
                "Implement exponential backoff for reconnections"
            ],
            resolution_steps=[
                "Monitor WebSocket connection count and error rates",
                "Check NATS queue depth and processing rates",
                "Verify load balancer health checks",
                "Review WebSocket server resource usage",
                "Implement connection limits and rate limiting"
            ],
            escalation_path=[
                "On-call engineer (immediate)",
                "Backend team lead (30 minutes)",
                "DevOps team (1 hour)",
                "CTO (2 hours)"
            ],
            metrics_to_monitor=[
                "websocket_connection_count",
                "websocket_error_rate",
                "websocket_message_latency",
                "nats_queue_depth",
                "api_response_time"
            ],
            checklists={
                "immediate": [
                    "Check WebSocket server logs for errors",
                    "Monitor connection count and error rates",
                    "Verify NATS connectivity and queue depth",
                    "Check load balancer health status",
                    "Notify users of potential connectivity issues"
                ],
                "investigation": [
                    "Analyze WebSocket server resource usage",
                    "Review recent deployment changes",
                    "Check for network connectivity issues",
                    "Monitor NATS message processing rates",
                    "Verify database connection pool status"
                ],
                "resolution": [
                    "Scale WebSocket servers if needed",
                    "Implement connection pooling",
                    "Add monitoring and alerting",
                    "Update runbooks with lessons learned",
                    "Schedule post-incident review"
                ]
            }
        )
    
    def _create_nats_backlog_card(self) -> IncidentCard:
        """NATS message queue backlog incident card"""
        return IncidentCard(
            id="nats_backlog",
            title="NATS Message Queue Backlog",
            description="Message processing delays due to NATS queue buildup",
            severity=IncidentSeverity.HIGH,
            status=IncidentStatus.OPEN,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            affected_services=["orchestrator", "workers", "gateway"],
            symptoms=[
                "Model runs taking longer than expected",
                "Real-time updates delayed",
                "Message processing errors",
                "Increased memory usage on NATS servers",
                "Worker queue depth increasing"
            ],
            root_causes=[
                "Worker capacity insufficient for message volume",
                "Slow message processing in workers",
                "NATS server resource constraints",
                "Message size too large",
                "Network connectivity issues between services"
            ],
            mitigation_steps=[
                "Scale worker instances",
                "Implement message prioritization",
                "Add circuit breakers for slow consumers",
                "Enable message compression",
                "Implement dead letter queues"
            ],
            resolution_steps=[
                "Monitor NATS queue depth and processing rates",
                "Scale worker capacity based on demand",
                "Optimize message processing in workers",
                "Review NATS server configuration",
                "Implement message size limits"
            ],
            escalation_path=[
                "On-call engineer (immediate)",
                "Backend team lead (30 minutes)",
                "DevOps team (1 hour)",
                "CTO (2 hours)"
            ],
            metrics_to_monitor=[
                "nats_queue_depth",
                "nats_message_processing_rate",
                "worker_queue_depth",
                "model_run_duration",
                "nats_memory_usage"
            ],
            checklists={
                "immediate": [
                    "Check NATS server logs and metrics",
                    "Monitor queue depth across all subjects",
                    "Verify worker health and capacity",
                    "Check for slow message consumers",
                    "Implement emergency worker scaling"
                ],
                "investigation": [
                    "Analyze message processing patterns",
                    "Review worker resource usage",
                    "Check for message size anomalies",
                    "Monitor network connectivity",
                    "Review recent deployment changes"
                ],
                "resolution": [
                    "Scale worker capacity",
                    "Implement message prioritization",
                    "Add monitoring and alerting",
                    "Optimize message processing",
                    "Schedule capacity planning review"
                ]
            }
        )
    
    def _create_redis_eviction_card(self) -> IncidentCard:
        """Redis memory eviction incident card"""
        return IncidentCard(
            id="redis_eviction",
            title="Redis Memory Eviction",
            description="Redis running out of memory, causing data eviction and potential data loss",
            severity=IncidentSeverity.CRITICAL,
            status=IncidentStatus.OPEN,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            affected_services=["gateway", "orchestrator", "frontend"],
            symptoms=[
                "Cache misses increasing",
                "Session data loss",
                "Rate limiting failures",
                "Redis memory usage at capacity",
                "Application errors related to cache"
            ],
            root_causes=[
                "Memory usage exceeding Redis capacity",
                "Memory leaks in application code",
                "Insufficient Redis memory allocation",
                "Large objects stored in Redis",
                "Expired keys not being cleaned up"
            ],
            mitigation_steps=[
                "Scale Redis memory capacity",
                "Implement cache eviction policies",
                "Add memory monitoring and alerting",
                "Optimize cache key patterns",
                "Implement cache warming strategies"
            ],
            resolution_steps=[
                "Monitor Redis memory usage and eviction rates",
                "Analyze cache hit/miss ratios",
                "Review cache key patterns and sizes",
                "Implement memory optimization",
                "Scale Redis cluster if needed"
            ],
            escalation_path=[
                "On-call engineer (immediate)",
                "Backend team lead (15 minutes)",
                "DevOps team (30 minutes)",
                "CTO (1 hour)"
            ],
            metrics_to_monitor=[
                "redis_memory_usage",
                "redis_eviction_rate",
                "redis_cache_hit_ratio",
                "redis_connection_count",
                "redis_commands_per_second"
            ],
            checklists={
                "immediate": [
                    "Check Redis memory usage and eviction stats",
                    "Monitor cache hit/miss ratios",
                    "Verify Redis configuration",
                    "Check for memory leaks",
                    "Implement emergency memory scaling"
                ],
                "investigation": [
                    "Analyze Redis memory usage patterns",
                    "Review cache key patterns and sizes",
                    "Check for expired key cleanup",
                    "Monitor application cache usage",
                    "Review recent deployment changes"
                ],
                "resolution": [
                    "Scale Redis memory capacity",
                    "Implement cache optimization",
                    "Add memory monitoring",
                    "Review cache strategies",
                    "Schedule capacity planning"
                ]
            }
        )
    
    def _create_postgis_bloat_card(self) -> IncidentCard:
        """PostGIS table bloat incident card"""
        return IncidentCard(
            id="postgis_bloat",
            title="PostGIS Table Bloat",
            description="Database performance degradation due to table and index bloat",
            severity=IncidentSeverity.MEDIUM,
            status=IncidentStatus.OPEN,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            affected_services=["gateway", "orchestrator", "workers"],
            symptoms=[
                "Slow spatial queries",
                "Increased query execution time",
                "High disk usage",
                "Index scan performance degradation",
                "Vacuum processes taking longer"
            ],
            root_causes=[
                "Frequent updates/deletes without proper cleanup",
                "Insufficient autovacuum configuration",
                "Large transaction sizes",
                "Index fragmentation",
                "Inadequate maintenance windows"
            ],
            mitigation_steps=[
                "Schedule regular VACUUM operations",
                "Optimize autovacuum settings",
                "Implement table partitioning",
                "Add monitoring for table bloat",
                "Schedule maintenance windows"
            ],
            resolution_steps=[
                "Monitor table and index bloat percentages",
                "Analyze query performance patterns",
                "Review autovacuum configuration",
                "Implement bloat monitoring",
                "Schedule regular maintenance"
            ],
            escalation_path=[
                "On-call engineer (immediate)",
                "Database team lead (1 hour)",
                "DevOps team (2 hours)",
                "CTO (4 hours)"
            ],
            metrics_to_monitor=[
                "postgis_query_time",
                "table_bloat_percentage",
                "index_bloat_percentage",
                "vacuum_duration",
                "database_size"
            ],
            checklists={
                "immediate": [
                    "Check table and index bloat percentages",
                    "Monitor query performance",
                    "Verify autovacuum settings",
                    "Check disk usage",
                    "Schedule maintenance window"
                ],
                "investigation": [
                    "Analyze bloat patterns across tables",
                    "Review update/delete patterns",
                    "Check autovacuum logs",
                    "Monitor transaction sizes",
                    "Review maintenance schedules"
                ],
                "resolution": [
                    "Run VACUUM operations",
                    "Optimize autovacuum settings",
                    "Implement bloat monitoring",
                    "Review maintenance procedures",
                    "Schedule regular maintenance"
                ]
            }
        )
    
    def _create_api_timeout_card(self) -> IncidentCard:
        """API timeout incident card"""
        return IncidentCard(
            id="api_timeout",
            title="API Response Timeouts",
            description="API endpoints experiencing increased response times and timeouts",
            severity=IncidentSeverity.HIGH,
            status=IncidentStatus.OPEN,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            affected_services=["gateway", "orchestrator", "frontend"],
            symptoms=[
                "API requests timing out",
                "Increased response times",
                "User interface becoming unresponsive",
                "Error rates increasing",
                "Load balancer health check failures"
            ],
            root_causes=[
                "Database query performance issues",
                "External service dependencies slow",
                "Insufficient API server capacity",
                "Memory leaks in application code",
                "Network connectivity issues"
            ],
            mitigation_steps=[
                "Scale API server capacity",
                "Implement request timeouts",
                "Add circuit breakers",
                "Optimize database queries",
                "Implement caching strategies"
            ],
            resolution_steps=[
                "Monitor API response times and error rates",
                "Analyze slow query patterns",
                "Review external service dependencies",
                "Optimize application performance",
                "Implement monitoring and alerting"
            ],
            escalation_path=[
                "On-call engineer (immediate)",
                "Backend team lead (30 minutes)",
                "DevOps team (1 hour)",
                "CTO (2 hours)"
            ],
            metrics_to_monitor=[
                "api_response_time",
                "api_error_rate",
                "database_query_time",
                "external_service_response_time",
                "api_server_cpu_usage"
            ],
            checklists={
                "immediate": [
                    "Check API server logs and metrics",
                    "Monitor response times and error rates",
                    "Verify database performance",
                    "Check external service health",
                    "Implement emergency scaling"
                ],
                "investigation": [
                    "Analyze slow query patterns",
                    "Review external service dependencies",
                    "Check for memory leaks",
                    "Monitor network connectivity",
                    "Review recent deployment changes"
                ],
                "resolution": [
                    "Scale API capacity",
                    "Optimize database queries",
                    "Implement caching",
                    "Add monitoring and alerting",
                    "Schedule performance review"
                ]
            }
        )
    
    def _create_db_pool_exhaustion_card(self) -> IncidentCard:
        """Database connection pool exhaustion incident card"""
        return IncidentCard(
            id="database_connection_pool_exhaustion",
            title="Database Connection Pool Exhaustion",
            description="All database connections in use, causing request queuing and timeouts",
            severity=IncidentSeverity.CRITICAL,
            status=IncidentStatus.OPEN,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            affected_services=["gateway", "orchestrator", "workers"],
            symptoms=[
                "Database connection timeouts",
                "Request queuing and delays",
                "Connection pool exhaustion errors",
                "Increased response times",
                "Application errors related to database connections"
            ],
            root_causes=[
                "Insufficient connection pool size",
                "Long-running database transactions",
                "Connection leaks in application code",
                "Database performance issues",
                "High concurrent request load"
            ],
            mitigation_steps=[
                "Increase connection pool size",
                "Implement connection timeout policies",
                "Add connection monitoring",
                "Optimize database queries",
                "Implement connection pooling best practices"
            ],
            resolution_steps=[
                "Monitor connection pool usage",
                "Analyze connection patterns",
                "Review database performance",
                "Implement connection monitoring",
                "Optimize application connection usage"
            ],
            escalation_path=[
                "On-call engineer (immediate)",
                "Backend team lead (15 minutes)",
                "Database team lead (30 minutes)",
                "CTO (1 hour)"
            ],
            metrics_to_monitor=[
                "database_connection_pool",
                "database_connection_time",
                "database_query_time",
                "database_active_connections",
                "database_waiting_connections"
            ],
            checklists={
                "immediate": [
                    "Check connection pool status",
                    "Monitor active and waiting connections",
                    "Verify database performance",
                    "Check for connection leaks",
                    "Implement emergency pool scaling"
                ],
                "investigation": [
                    "Analyze connection usage patterns",
                    "Review long-running transactions",
                    "Check for connection leaks",
                    "Monitor database performance",
                    "Review application connection usage"
                ],
                "resolution": [
                    "Scale connection pool size",
                    "Implement connection monitoring",
                    "Optimize database queries",
                    "Add connection timeout policies",
                    "Schedule capacity planning"
                ]
            }
        )
    
    def _create_model_run_failures_card(self) -> IncidentCard:
        """Model run failures incident card"""
        return IncidentCard(
            id="model_run_failures",
            title="Model Run Failures",
            description="Urban planning models experiencing high failure rates",
            severity=IncidentSeverity.HIGH,
            status=IncidentStatus.OPEN,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            affected_services=["workers", "orchestrator", "frontend"],
            symptoms=[
                "Model runs failing consistently",
                "Error rates increasing",
                "User reports of failed analyses",
                "Worker queue building up",
                "Model execution timeouts"
            ],
            root_causes=[
                "Insufficient worker resources",
                "Model input data issues",
                "External service dependencies failing",
                "Memory leaks in model code",
                "Configuration errors"
            ],
            mitigation_steps=[
                "Scale worker capacity",
                "Implement model validation",
                "Add error handling and retries",
                "Implement circuit breakers",
                "Add model monitoring"
            ],
            resolution_steps=[
                "Monitor model success rates and error patterns",
                "Analyze worker resource usage",
                "Review model input validation",
                "Implement comprehensive error handling",
                "Add model performance monitoring"
            ],
            escalation_path=[
                "On-call engineer (immediate)",
                "Data science team lead (30 minutes)",
                "Backend team lead (1 hour)",
                "CTO (2 hours)"
            ],
            metrics_to_monitor=[
                "model_run_success_rate",
                "model_run_duration",
                "worker_queue_depth",
                "model_error_rate",
                "worker_resource_usage"
            ],
            checklists={
                "immediate": [
                    "Check worker logs and error rates",
                    "Monitor model success rates",
                    "Verify worker capacity",
                    "Check for resource constraints",
                    "Implement emergency worker scaling"
                ],
                "investigation": [
                    "Analyze model error patterns",
                    "Review worker resource usage",
                    "Check model input validation",
                    "Monitor external dependencies",
                    "Review recent model changes"
                ],
                "resolution": [
                    "Scale worker capacity",
                    "Implement model validation",
                    "Add error handling",
                    "Add monitoring and alerting",
                    "Schedule model review"
                ]
            }
        )
    
    def _create_export_timeout_card(self) -> IncidentCard:
        """Export timeout incident card"""
        return IncidentCard(
            id="export_timeout",
            title="Export Operation Timeouts",
            description="Data export operations timing out or failing",
            severity=IncidentSeverity.MEDIUM,
            status=IncidentStatus.OPEN,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            affected_services=["workers", "gateway", "frontend"],
            symptoms=[
                "Export operations timing out",
                "Large file generation failures",
                "Export queue building up",
                "User reports of failed exports",
                "Storage quota issues"
            ],
            root_causes=[
                "Large dataset exports",
                "Insufficient worker resources",
                "Storage capacity issues",
                "Network connectivity problems",
                "Export format complexity"
            ],
            mitigation_steps=[
                "Implement export size limits",
                "Add export progress tracking",
                "Implement background processing",
                "Add storage monitoring",
                "Implement export validation"
            ],
            resolution_steps=[
                "Monitor export success rates and durations",
                "Analyze export patterns and sizes",
                "Review storage capacity and usage",
                "Implement export optimization",
                "Add export monitoring"
            ],
            escalation_path=[
                "On-call engineer (immediate)",
                "Backend team lead (1 hour)",
                "DevOps team (2 hours)",
                "CTO (4 hours)"
            ],
            metrics_to_monitor=[
                "export_success_rate",
                "export_duration",
                "export_file_size",
                "storage_usage",
                "export_queue_depth"
            ],
            checklists={
                "immediate": [
                    "Check export worker logs",
                    "Monitor export success rates",
                    "Verify storage capacity",
                    "Check for large export requests",
                    "Implement export size limits"
                ],
                "investigation": [
                    "Analyze export patterns",
                    "Review storage usage",
                    "Check export worker capacity",
                    "Monitor network connectivity",
                    "Review export configurations"
                ],
                "resolution": [
                    "Implement export optimization",
                    "Add storage monitoring",
                    "Implement progress tracking",
                    "Add export validation",
                    "Schedule capacity planning"
                ]
            }
        )
    
    def get_incident_card(self, incident_type: str) -> Optional[IncidentCard]:
        """Get a specific incident card by type"""
        return self.incident_cards.get(incident_type)
    
    def get_all_incident_cards(self) -> Dict[str, IncidentCard]:
        """Get all available incident cards"""
        return self.incident_cards
    
    def create_incident(self, incident_type: str, custom_data: Dict[str, Any] = None) -> IncidentCard:
        """Create a new incident based on a card template"""
        if incident_type not in self.incident_cards:
            raise ValueError(f"Unknown incident type: {incident_type}")
        
        base_card = self.incident_cards[incident_type]
        
        # Create a new incident with unique ID
        incident_id = f"{incident_type}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        incident = IncidentCard(
            id=incident_id,
            title=base_card.title,
            description=base_card.description,
            severity=base_card.severity,
            status=IncidentStatus.OPEN,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            affected_services=base_card.affected_services.copy(),
            symptoms=base_card.symptoms.copy(),
            root_causes=base_card.root_causes.copy(),
            mitigation_steps=base_card.mitigation_steps.copy(),
            resolution_steps=base_card.resolution_steps.copy(),
            escalation_path=base_card.escalation_path.copy(),
            metrics_to_monitor=base_card.metrics_to_monitor.copy(),
            checklists=base_card.checklists.copy()
        )
        
        # Apply custom data if provided
        if custom_data:
            for key, value in custom_data.items():
                if hasattr(incident, key):
                    setattr(incident, key, value)
        
        self.active_incidents[incident_id] = incident
        return incident
    
    def update_incident_status(self, incident_id: str, status: IncidentStatus, 
                             notes: str = None) -> bool:
        """Update incident status"""
        if incident_id not in self.active_incidents:
            return False
        
        incident = self.active_incidents[incident_id]
        incident.status = status
        incident.updated_at = datetime.utcnow()
        
        if notes:
            # Add notes to incident (would need to extend IncidentCard for this)
            pass
        
        return True
    
    def get_active_incidents(self) -> Dict[str, IncidentCard]:
        """Get all active incidents"""
        return self.active_incidents
    
    def close_incident(self, incident_id: str, resolution_notes: str = None) -> bool:
        """Close an incident"""
        if incident_id not in self.active_incidents:
            return False
        
        incident = self.active_incidents[incident_id]
        incident.status = IncidentStatus.RESOLVED
        incident.updated_at = datetime.utcnow()
        
        # Move to resolved incidents (would need separate storage)
        del self.active_incidents[incident_id]
        
        return True
    
    def export_incident_data(self, format: str = "json") -> str:
        """Export incident data in specified format"""
        data = {
            "active_incidents": {
                incident_id: asdict(incident) 
                for incident_id, incident in self.active_incidents.items()
            },
            "incident_templates": {
                incident_type: asdict(card)
                for incident_type, card in self.incident_cards.items()
            }
        }
        
        if format.lower() == "json":
            return json.dumps(data, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported format: {format}")
