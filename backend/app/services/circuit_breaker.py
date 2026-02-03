"""
Circuit Breaker Service for DynamoDB Operations.

Implements the circuit breaker pattern to prevent cascading failures
when external services (DynamoDB) become unavailable.

States:
- CLOSED: Normal operation, requests pass through
- OPEN: All requests fail immediately
- HALF_OPEN: Limited requests allowed to test recovery
"""

import asyncio
import time
import logging
from typing import Any, Callable, Dict, Optional, List
from enum import Enum
from functools import wraps
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker."""
    failure_threshold: int = 5  # Number of failures before opening
    recovery_timeout: int = 60  # Seconds to wait before trying again
    half_open_max_calls: int = 3  # Max calls in half-open state
    expected_exceptions: List[type] = field(default_factory=lambda: [Exception])
    timeout: float = 30.0  # Operation timeout in seconds


class CircuitBreakerError(Exception):
    """Raised when circuit breaker is open."""
    pass


class CircuitBreaker:
    """
    Circuit breaker implementation for resilient service calls.
    
    Prevents cascading failures by stopping requests to failing services
    and providing automatic recovery detection.
    """
    
    def __init__(
        self,
        name: str,
        config: Optional[CircuitBreakerConfig] = None
    ):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        
        # State tracking
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.half_open_calls = 0
        
        # Statistics
        self.total_calls = 0
        self.successful_calls = 0
        self.failed_calls = 0
        
        logger.info(f"Circuit breaker '{name}' initialized with config: {self.config}")
    
    def _should_attempt_reset(self) -> bool:
        """Check if circuit should attempt to reset from OPEN to HALF_OPEN."""
        if self.state != CircuitState.OPEN:
            return False
        
        if self.last_failure_time is None:
            return False
        
        return (time.time() - self.last_failure_time) >= self.config.recovery_timeout
    
    def _call_succeeded(self):
        """Handle successful call."""
        self.successful_calls += 1
        self.failure_count = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.half_open_calls += 1
            if self.half_open_calls >= self.config.half_open_max_calls:
                self.state = CircuitState.CLOSED
                logger.info(f"Circuit breaker '{self.name}' reset to CLOSED state")
    
    def _call_failed(self, exception: Exception):
        """Handle failed call."""
        self.failed_calls += 1
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            logger.warning(f"Circuit breaker '{self.name}' returned to OPEN state")
        elif self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(f"Circuit breaker '{self.name}' opened after {self.failure_count} failures")
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection.
        
        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
            
        Raises:
            CircuitBreakerError: When circuit is open
            Exception: Original exception from function call
        """
        self.total_calls += 1
        
        # Check if circuit is open and should attempt reset
        if self.state == CircuitState.OPEN and self._should_attempt_reset():
            self.state = CircuitState.HALF_OPEN
            self.half_open_calls = 0
            logger.info(f"Circuit breaker '{self.name}' moved to HALF_OPEN state")
        
        # Fail fast if circuit is open
        if self.state == CircuitState.OPEN:
            raise CircuitBreakerError(
                f"Circuit breaker '{self.name}' is OPEN. "
                f"Last failure: {self.last_failure_time}"
            )
        
        # Execute the function with timeout
        try:
            result = await asyncio.wait_for(
                func(*args, **kwargs),
                timeout=self.config.timeout
            )
            self._call_succeeded()
            return result
            
        except asyncio.TimeoutError as e:
            logger.error(f"Timeout in circuit breaker '{self.name}': {e}")
            self._call_failed(e)
            raise
            
        except Exception as e:
            # Check if this is an expected exception
            is_expected = any(isinstance(e, exc_type) for exc_type in self.config.expected_exceptions)
            
            if is_expected:
                logger.error(f"Expected exception in circuit breaker '{self.name}': {e}")
                self._call_failed(e)
                raise
            else:
                # Unexpected exception - don't count as circuit breaker failure
                logger.error(f"Unexpected exception in circuit breaker '{self.name}': {e}")
                raise
    
    def get_stats(self) -> Dict[str, Any]:
        """Get circuit breaker statistics."""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "total_calls": self.total_calls,
            "successful_calls": self.successful_calls,
            "failed_calls": self.failed_calls,
            "success_rate": (
                self.successful_calls / self.total_calls * 100 
                if self.total_calls > 0 else 0
            ),
            "last_failure_time": self.last_failure_time,
            "config": {
                "failure_threshold": self.config.failure_threshold,
                "recovery_timeout": self.config.recovery_timeout,
                "half_open_max_calls": self.config.half_open_max_calls,
                "timeout": self.config.timeout
            }
        }
    
    def reset(self):
        """Manually reset circuit breaker to CLOSED state."""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.half_open_calls = 0
        logger.info(f"Circuit breaker '{self.name}' manually reset to CLOSED state")


# Global circuit breaker registry
_circuit_breakers: Dict[str, CircuitBreaker] = {}


def get_circuit_breaker(name: str, config: Optional[CircuitBreakerConfig] = None) -> CircuitBreaker:
    """Get or create circuit breaker instance."""
    if name not in _circuit_breakers:
        _circuit_breakers[name] = CircuitBreaker(name, config)
    return _circuit_breakers[name]


def circuit_breaker(
    name: str,
    failure_threshold: int = 5,
    recovery_timeout: int = 60,
    half_open_max_calls: int = 3,
    timeout: float = 30.0,
    expected_exceptions: Optional[List[type]] = None
):
    """
    Decorator for applying circuit breaker to async functions.
    
    Args:
        name: Circuit breaker name
        failure_threshold: Number of failures before opening
        recovery_timeout: Seconds to wait before trying again
        half_open_max_calls: Max calls in half-open state
        timeout: Operation timeout in seconds
        expected_exceptions: List of exceptions that count as failures
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            config = CircuitBreakerConfig(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                half_open_max_calls=half_open_max_calls,
                timeout=timeout,
                expected_exceptions=expected_exceptions or [Exception]
            )
            
            breaker = get_circuit_breaker(name, config)
            return await breaker.call(func, *args, **kwargs)
        
        return wrapper
    return decorator


# Circuit breaker instances for different DynamoDB operations
dynamodb_read_breaker = get_circuit_breaker(
    "dynamodb_read",
    CircuitBreakerConfig(
        failure_threshold=3,
        recovery_timeout=30,
        timeout=10.0
    )
)

dynamodb_write_breaker = get_circuit_breaker(
    "dynamodb_write",
    CircuitBreakerConfig(
        failure_threshold=5,
        recovery_timeout=60,
        timeout=15.0
    )
)

dynamodb_batch_breaker = get_circuit_breaker(
    "dynamodb_batch",
    CircuitBreakerConfig(
        failure_threshold=2,
        recovery_timeout=120,
        timeout=45.0
    )
)