"""
Decorators for applying resilience patterns to functions.

Provides easy-to-use decorators for circuit breakers, retry logic,
and other resilience patterns.
"""

import asyncio
import logging
from typing import Any, Callable, List, Optional, Type, Union
from functools import wraps

from app.services.circuit_breaker import (
    CircuitBreakerConfig,
    get_circuit_breaker,
    circuit_breaker as circuit_breaker_decorator
)
from app.services.retry_service import (
    RetryConfig,
    RetryService,
    BackoffStrategy,
    retry_with_backoff
)
from app.utils.exceptions import (
    CircuitBreakerOpenException,
    RetryExhaustedException,
    DynamoDBException
)

logger = logging.getLogger(__name__)


def resilient_dynamodb_call(
    operation_type: str = "read",
    circuit_breaker_name: Optional[str] = None,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    timeout: float = 30.0
):
    """
    Decorator for DynamoDB operations with both circuit breaker and retry logic.
    
    Args:
        operation_type: Type of operation ('read', 'write', 'batch', 'critical')
        circuit_breaker_name: Name for circuit breaker (auto-generated if None)
        max_attempts: Maximum retry attempts
        base_delay: Base delay for backoff
        max_delay: Maximum delay for backoff
        timeout: Operation timeout
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate circuit breaker name if not provided
            if circuit_breaker_name is None:
                cb_name = f"dynamodb_{operation_type}_{func.__name__}"
            else:
                cb_name = circuit_breaker_name
            
            # Configure circuit breaker based on operation type
            if operation_type == "read":
                cb_config = CircuitBreakerConfig(
                    failure_threshold=3,
                    recovery_timeout=30,
                    timeout=timeout,
                    expected_exceptions=[DynamoDBException, Exception]
                )
                retry_config = RetryConfig(
                    max_attempts=max_attempts,
                    base_delay=base_delay,
                    max_delay=max_delay,
                    backoff_strategy=BackoffStrategy.EXPONENTIAL,
                    backoff_factor=2.0,
                    jitter=True
                )
            elif operation_type == "write":
                cb_config = CircuitBreakerConfig(
                    failure_threshold=5,
                    recovery_timeout=60,
                    timeout=timeout,
                    expected_exceptions=[DynamoDBException, Exception]
                )
                retry_config = RetryConfig(
                    max_attempts=max_attempts + 2,  # More retries for writes
                    base_delay=base_delay * 1.5,
                    max_delay=max_delay,
                    backoff_strategy=BackoffStrategy.EXPONENTIAL,
                    backoff_factor=2.0,
                    jitter=True
                )
            elif operation_type == "batch":
                cb_config = CircuitBreakerConfig(
                    failure_threshold=2,
                    recovery_timeout=120,
                    timeout=timeout,
                    expected_exceptions=[DynamoDBException, Exception]
                )
                retry_config = RetryConfig(
                    max_attempts=2,  # Fewer retries for batch operations
                    base_delay=base_delay * 2,
                    max_delay=max_delay,
                    backoff_strategy=BackoffStrategy.LINEAR,
                    jitter=True
                )
            elif operation_type == "critical":
                cb_config = CircuitBreakerConfig(
                    failure_threshold=7,
                    recovery_timeout=15,
                    timeout=timeout,
                    expected_exceptions=[DynamoDBException, Exception]
                )
                retry_config = RetryConfig(
                    max_attempts=max_attempts + 4,  # Many retries for critical ops
                    base_delay=base_delay * 0.5,
                    max_delay=max_delay * 0.5,
                    backoff_strategy=BackoffStrategy.EXPONENTIAL,
                    backoff_factor=1.5,
                    jitter=True
                )
            else:
                # Default configuration
                cb_config = CircuitBreakerConfig(
                    failure_threshold=5,
                    recovery_timeout=60,
                    timeout=timeout,
                    expected_exceptions=[DynamoDBException, Exception]
                )
                retry_config = RetryConfig(
                    max_attempts=max_attempts,
                    base_delay=base_delay,
                    max_delay=max_delay,
                    backoff_strategy=BackoffStrategy.EXPONENTIAL,
                    jitter=True
                )
            
            # Get circuit breaker and retry service
            circuit_breaker = get_circuit_breaker(cb_name, cb_config)
            retry_service = RetryService(retry_config)
            
            # Execute with both circuit breaker and retry logic
            try:
                return await circuit_breaker.call(
                    retry_service.execute_with_retry,
                    func,
                    *args,
                    **kwargs
                )
            except Exception as e:
                # Wrap exceptions with more context
                if "open" in str(e).lower():
                    raise CircuitBreakerOpenException(
                        f"Circuit breaker '{cb_name}' is open for operation {func.__name__}",
                        error_code="CIRCUIT_BREAKER_OPEN",
                        details={"circuit_breaker": cb_name, "operation": func.__name__}
                    )
                elif "exhausted" in str(e).lower() or "retry" in str(e).lower():
                    raise RetryExhaustedException(
                        f"Retry attempts exhausted for operation {func.__name__}",
                        attempts=max_attempts,
                        last_exception=e,
                        error_code="RETRY_EXHAUSTED",
                        details={"operation": func.__name__, "max_attempts": max_attempts}
                    )
                else:
                    # Re-raise the original exception
                    raise
        
        return wrapper
    return decorator


def safe_read(
    max_attempts: int = 3,
    base_delay: float = 0.5,
    timeout: float = 10.0
):
    """Decorator for safe read operations."""
    return resilient_dynamodb_call(
        operation_type="read",
        max_attempts=max_attempts,
        base_delay=base_delay,
        timeout=timeout
    )


def safe_write(
    max_attempts: int = 5,
    base_delay: float = 1.0,
    timeout: float = 15.0
):
    """Decorator for safe write operations."""
    return resilient_dynamodb_call(
        operation_type="write",
        max_attempts=max_attempts,
        base_delay=base_delay,
        timeout=timeout
    )


def safe_batch(
    max_attempts: int = 2,
    base_delay: float = 2.0,
    timeout: float = 45.0
):
    """Decorator for safe batch operations."""
    return resilient_dynamodb_call(
        operation_type="batch",
        max_attempts=max_attempts,
        base_delay=base_delay,
        timeout=timeout
    )


def safe_critical(
    max_attempts: int = 7,
    base_delay: float = 0.1,
    timeout: float = 5.0
):
    """Decorator for critical operations that must succeed."""
    return resilient_dynamodb_call(
        operation_type="critical",
        max_attempts=max_attempts,
        base_delay=base_delay,
        timeout=timeout
    )


def fallback_on_failure(
    fallback_func: Callable,
    fallback_exceptions: Optional[List[Type[Exception]]] = None
):
    """
    Decorator that provides fallback functionality when primary function fails.
    
    Args:
        fallback_func: Function to call as fallback
        fallback_exceptions: List of exceptions that trigger fallback
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if fallback_exceptions is None or any(
                    isinstance(e, exc_type) for exc_type in fallback_exceptions
                ):
                    logger.warning(
                        f"Primary function {func.__name__} failed: {e}. "
                        f"Using fallback function {fallback_func.__name__}"
                    )
                    return await fallback_func(*args, **kwargs)
                else:
                    raise
        
        return wrapper
    return decorator


def timeout_after(seconds: float):
    """
    Decorator to add timeout to async functions.
    
    Args:
        seconds: Timeout in seconds
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
            except asyncio.TimeoutError:
                logger.error(f"Function {func.__name__} timed out after {seconds} seconds")
                raise TimeoutError(f"Function {func.__name__} timed out after {seconds} seconds")
        
        return wrapper
    return decorator


def log_performance(operation_name: Optional[str] = None):
    """
    Decorator to log performance metrics for functions.
    
    Args:
        operation_name: Name for the operation (uses function name if None)
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            op_name = operation_name or func.__name__
            
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(f"Operation '{op_name}' completed in {duration:.3f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"Operation '{op_name}' failed after {duration:.3f}s: {e}")
                raise
        
        return wrapper
    return decorator
