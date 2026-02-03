"""
Health Check and Monitoring Service.

Provides comprehensive health monitoring for the application,
including database connectivity, circuit breaker status, and system metrics.
"""

import asyncio
import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from app.services.circuit_breaker import get_circuit_breaker, _circuit_breakers
from app.services.dynamodb import DynamoDBClient
from app.core.config import settings
from app.utils.exceptions import HealthCheckException

logger = logging.getLogger(__name__)


class HealthStatus:
    """Health status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class HealthCheckResult:
    """Result of a health check."""
    
    def __init__(
        self,
        component: str,
        status: str,
        message: str,
        response_time: Optional[float] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.component = component
        self.status = status
        self.message = message
        self.response_time = response_time
        self.details = details or {}
        self.timestamp = datetime.utcnow()


class HealthMonitor:
    """
    Health monitoring service for the application.
    
    Monitors various components and provides overall health status.
    """
    
    def __init__(self, dynamodb_client: Optional[DynamoDBClient] = None):
        self.dynamodb_client = dynamodb_client
        self.last_check_time: Optional[datetime] = None
        self.check_history: List[Dict[str, Any]] = []
        self.max_history_size = 100
    
    async def check_database_health(self) -> HealthCheckResult:
        """Check DynamoDB connectivity and performance."""
        start_time = time.time()
        
        try:
            if not self.dynamodb_client:
                return HealthCheckResult(
                    component="dynamodb",
                    status=HealthStatus.UNHEALTHY,
                    message="DynamoDB client not initialized"
                )
            
            # Simple connectivity check - try to get a health rule
            await self.dynamodb_client.get_health_rule("normal", "none")
            
            response_time = time.time() - start_time
            
            return HealthCheckResult(
                component="dynamodb",
                status=HealthStatus.HEALTHY,
                message="DynamoDB connection successful",
                response_time=response_time,
                details={
                    "endpoint": self.dynamodb_client.endpoint_url or "AWS",
                    "region": self.dynamodb_client.region_name
                }
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            logger.error(f"Database health check failed: {e}")
            
            return HealthCheckResult(
                component="dynamodb",
                status=HealthStatus.UNHEALTHY,
                message=f"Database connection failed: {str(e)}",
                response_time=response_time,
                details={"error": str(e)}
            )
    
    async def check_circuit_breakers(self) -> List[HealthCheckResult]:
        """Check the status of all circuit breakers."""
        results = []
        
        for name, breaker in _circuit_breakers.items():
            stats = breaker.get_stats()
            
            # Determine status based on circuit state and success rate
            if breaker.state.value == "open":
                status = HealthStatus.UNHEALTHY
                message = f"Circuit breaker is OPEN"
            elif breaker.state.value == "half_open":
                status = HealthStatus.DEGRADED
                message = f"Circuit breaker is HALF_OPEN"
            elif stats["success_rate"] < 80:
                status = HealthStatus.DEGRADED
                message = f"Low success rate: {stats['success_rate']:.1f}%"
            else:
                status = HealthStatus.HEALTHY
                message = f"Circuit breaker is {breaker.state.value.upper()}"
            
            result = HealthCheckResult(
                component=f"circuit_breaker_{name}",
                status=status,
                message=message,
                details={
                    "state": breaker.state.value,
                    "failure_count": stats["failure_count"],
                    "success_rate": stats["success_rate"],
                    "total_calls": stats["total_calls"],
                    "last_failure_time": stats["last_failure_time"]
                }
            )
            
            results.append(result)
        
        return results
    
    async def check_system_resources(self) -> HealthCheckResult:
        """Check system resource usage."""
        try:
            import psutil
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # Determine overall status
            if cpu_percent > 90 or memory_percent > 90 or disk_percent > 90:
                status = HealthStatus.UNHEALTHY
                message = "Critical resource usage detected"
            elif cpu_percent > 70 or memory_percent > 70 or disk_percent > 80:
                status = HealthStatus.DEGRADED
                message = "High resource usage detected"
            else:
                status = HealthStatus.HEALTHY
                message = "Resource usage is normal"
            
            return HealthCheckResult(
                component="system_resources",
                status=status,
                message=message,
                details={
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory_percent,
                    "disk_percent": disk_percent,
                    "memory_available_gb": memory.available / (1024**3),
                    "disk_free_gb": disk.free / (1024**3)
                }
            )
            
        except ImportError:
            return HealthCheckResult(
                component="system_resources",
                status=HealthStatus.DEGRADED,
                message="psutil not available for resource monitoring",
                details={"reason": "missing_dependency"}
            )
        except Exception as e:
            return HealthCheckResult(
                component="system_resources",
                status=HealthStatus.UNHEALTHY,
                message=f"Resource monitoring failed: {str(e)}",
                details={"error": str(e)}
            )
    
    async def check_application_health(self) -> HealthCheckResult:
        """Check application-specific health metrics."""
        try:
            # Check configuration
            config_issues = []
            
            if not settings.aws_access_key_id:
                config_issues.append("AWS access key not configured")
            
            if not settings.aws_secret_access_key:
                config_issues.append("AWS secret key not configured")
            
            # Check if environment variables are properly set
            if config_issues:
                return HealthCheckResult(
                    component="application",
                    status=HealthStatus.DEGRADED,
                    message=f"Configuration issues: {', '.join(config_issues)}",
                    details={"issues": config_issues}
                )
            
            return HealthCheckResult(
                component="application",
                status=HealthStatus.HEALTHY,
                message="Application configuration is valid",
                details={
                    "environment": settings.environment,
                    "debug_mode": settings.debug,
                    "app_version": settings.app_version
                }
            )
            
        except Exception as e:
            return HealthCheckResult(
                component="application",
                status=HealthStatus.UNHEALTHY,
                message=f"Application health check failed: {str(e)}",
                details={"error": str(e)}
            )
    
    async def perform_full_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check of all components."""
        if not settings.health_check_enabled:
            return {
                "status": HealthStatus.HEALTHY,
                "message": "Health checks are disabled",
                "timestamp": datetime.utcnow().isoformat(),
                "checks": []
            }
        
        start_time = time.time()
        all_results = []
        
        # Run all health checks concurrently
        checks = [
            self.check_database_health(),
            self.check_application_health(),
            self.check_system_resources()
        ]
        
        # Add circuit breaker checks
        circuit_breaker_checks = await self.check_circuit_breakers()
        checks.extend(circuit_breaker_checks)
        
        # Wait for all checks to complete
        results = await asyncio.gather(*checks, return_exceptions=True)
        
        # Process results
        unhealthy_count = 0
        degraded_count = 0
        
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Health check failed with exception: {result}")
                all_results.append(
                    HealthCheckResult(
                        component="unknown",
                        status=HealthStatus.UNHEALTHY,
                        message=f"Health check exception: {str(result)}"
                    )
                )
                unhealthy_count += 1
            else:
                all_results.append(result)
                if result.status == HealthStatus.UNHEALTHY:
                    unhealthy_count += 1
                elif result.status == HealthStatus.DEGRADED:
                    degraded_count += 1
        
        # Determine overall status
        if unhealthy_count > 0:
            overall_status = HealthStatus.UNHEALTHY
            overall_message = f"{unhealthy_count} components are unhealthy"
        elif degraded_count > 0:
            overall_status = HealthStatus.DEGRADED
            overall_message = f"{degraded_count} components are degraded"
        else:
            overall_status = HealthStatus.HEALTHY
            overall_message = "All components are healthy"
        
        total_time = time.time() - start_time
        self.last_check_time = datetime.utcnow()
        
        # Store check history
        check_summary = {
            "timestamp": self.last_check_time.isoformat(),
            "status": overall_status,
            "unhealthy_count": unhealthy_count,
            "degraded_count": degraded_count,
            "total_time": total_time
        }
        
        self.check_history.append(check_summary)
        if len(self.check_history) > self.max_history_size:
            self.check_history.pop(0)
        
        return {
            "status": overall_status,
            "message": overall_message,
            "timestamp": self.last_check_time.isoformat(),
            "total_time": total_time,
            "checks": [
                {
                    "component": result.component,
                    "status": result.status,
                    "message": result.message,
                    "response_time": result.response_time,
                    "details": result.details
                }
                for result in all_results
            ],
            "summary": {
                "total_checks": len(all_results),
                "healthy": len([r for r in all_results if r.status == HealthStatus.HEALTHY]),
                "degraded": degraded_count,
                "unhealthy": unhealthy_count
            }
        }
    
    def get_health_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent health check history."""
        return self.check_history[-limit:]
    
    async def start_monitoring(self):
        """Start continuous health monitoring."""
        if not settings.health_check_enabled:
            logger.info("Health monitoring is disabled")
            return
        
        logger.info(f"Starting health monitoring with {settings.health_check_interval}s interval")
        
        while True:
            try:
                await asyncio.sleep(settings.health_check_interval)
                result = await self.perform_full_health_check()
                
                if result["status"] != HealthStatus.HEALTHY:
                    logger.warning(f"Health check failed: {result['message']}")
                
            except Exception as e:
                logger.error(f"Health monitoring error: {e}")
                await asyncio.sleep(settings.health_check_interval)


# Global health monitor instance
_health_monitor: Optional[HealthMonitor] = None


def get_health_monitor(dynamodb_client: Optional[DynamoDBClient] = None) -> HealthMonitor:
    """Get or create health monitor instance."""
    global _health_monitor
    if _health_monitor is None:
        _health_monitor = HealthMonitor(dynamodb_client)
    return _health_monitor


async def health_check_endpoint() -> Dict[str, Any]:
    """FastAPI health check endpoint."""
    monitor = get_health_monitor()
    return await monitor.perform_full_health_check()
