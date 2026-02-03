"""
Retry Service for DynamoDB Operations.

Implements intelligent retry logic with exponential backoff,
jitter, and different strategies for different operation types.
"""

import asyncio
import random
import time
import logging
from typing import Any, Callable, Dict, List, Optional, Type, Union
from functools import wraps
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class BackoffStrategy(Enum):
    """Backoff strategies for retry logic."""
    EXPONENTIAL = "exponential"
    LINEAR = "linear"
    FIXED = "fixed"
    FIBONACCI = "fibonacci"


@dataclass
class RetryConfig:
    """Configuration for retry logic."""
    max_attempts: int = 3
    base_delay: float = 1.0  # Base delay in seconds
    max_delay: float = 60.0  # Maximum delay in seconds
    backoff_strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL
    backoff_factor: float = 2.0  # Multiplier for exponential backoff
    jitter: bool = True  # Add randomness to prevent thundering herd
    retryable_exceptions: List[Type[Exception]] = field(default_factory=lambda: [
        # AWS/DynamoDB specific exceptions
        "ProvisionedThroughputExceededException",
        "ThrottlingException",
        "RequestLimitExceeded",
        "InternalServerError",
        "ServiceUnavailable",
        # Network exceptions
        "ConnectionError",
        "TimeoutError",
        # Generic exceptions
        "Exception"
    ])


class RetryError(Exception):
    """Raised when all retry attempts are exhausted."""
    def __init__(self, message: str, attempts: int, last_exception: Exception):
        super().__init__(message)
        self.attempts = attempts
        self.last_exception = last_exception


class RetryService:
    """
    Intelligent retry service with configurable backoff strategies.
    
    Provides different retry strategies for different types of operations
    and implements jitter to prevent thundering herd problems.
    """
    
    def __init__(self, config: Optional[RetryConfig] = None):
        self.config = config or RetryConfig()
    
    def calculate_delay(self, attempt: int) -> float:
        """
        Calculate delay for given attempt number based on strategy.
        
        Args:
            attempt: Attempt number (0-based)
            
        Returns:
            Delay in seconds
        """
        if self.config.backoff_strategy == BackoffStrategy.EXPONENTIAL:
            delay = self.config.base_delay * (self.config.backoff_factor ** attempt)
        elif self.config.backoff_strategy == BackoffStrategy.LINEAR:
            delay = self.config.base_delay * (attempt + 1)
        elif self.config.backoff_strategy == BackoffStrategy.FIXED:
            delay = self.config.base_delay
        elif self.config.backoff_strategy == BackoffStrategy.FIBONACCI:
            delay = self.config.base_delay * self._fibonacci(attempt + 1)
        else:
            delay = self.config.base_delay
        
        # Apply maximum delay limit
        delay = min(delay, self.config.max_delay)
        
        # Add jitter if enabled
        if self.config.jitter:
            jitter_range = delay * 0.1  # 10% jitter
            delay += random.uniform(-jitter_range, jitter_range)
        
        return max(0, delay)  # Ensure non-negative
    
    def _fibonacci(self, n: int) -> int:
        """Calculate nth Fibonacci number."""
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b
    
    def is_retryable_exception(self, exception: Exception) -> bool:
        """
        Check if exception is retryable.
        
        Args:
            exception: Exception to check
            
        Returns:
            True if exception should be retried
        """
        exception_name = type(exception).__name__
        exception_class = type(exception)
        
        # Check by class name (for string-based configuration)
        if exception_name in self.config.retryable_exceptions:
            return True
        
        # Check by class type
        for retryable_type in self.config.retryable_exceptions:
            if isinstance(retryable_type, str):
                continue
            if isinstance(exception, retryable_type):
                return True
        
        return False
    
    async def execute_with_retry(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        Execute function with retry logic.
        
        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
            
        Raises:
            RetryError: When all retry attempts are exhausted
            Exception: Non-retryable exception
        """
        last_exception = None
        
        for attempt in range(self.config.max_attempts):
            try:
                result = await func(*args, **kwargs)
                
                if attempt > 0:
                    logger.info(
                        f"Operation succeeded on attempt {attempt + 1}/{self.config.max_attempts}"
                    )
                
                return result
                
            except Exception as e:
                last_exception = e
                
                # Check if exception is retryable
                if not self.is_retryable_exception(e):
                    logger.error(f"Non-retryable exception: {type(e).__name__}: {e}")
                    raise
                
                # Check if this was the last attempt
                if attempt == self.config.max_attempts - 1:
                    logger.error(
                        f"All {self.config.max_attempts} retry attempts exhausted. "
                        f"Last exception: {type(e).__name__}: {e}"
                    )
                    raise RetryError(
                        f"Failed after {self.config.max_attempts} attempts",
                        self.config.max_attempts,
                        last_exception
                    )
                
                # Calculate delay and wait
                delay = self.calculate_delay(attempt)
                logger.warning(
                    f"Attempt {attempt + 1}/{self.config.max_attempts} failed: "
                    f"{type(e).__name__}: {e}. Retrying in {delay:.2f}s..."
                )
                
                await asyncio.sleep(delay)
        
        # This should never be reached, but just in case
        raise RetryError(
            f"Failed after {self.config.max_attempts} attempts",
            self.config.max_attempts,
            last_exception
        )


# Predefined retry configurations for different operation types
READ_RETRY_CONFIG = RetryConfig(
    max_attempts=3,
    base_delay=0.5,
    max_delay=10.0,
    backoff_strategy=BackoffStrategy.EXPONENTIAL,
    backoff_factor=2.0,
    jitter=True
)

WRITE_RETRY_CONFIG = RetryConfig(
    max_attempts=5,
    base_delay=1.0,
    max_delay=30.0,
    backoff_strategy=BackoffStrategy.EXPONENTIAL,
    backoff_factor=2.0,
    jitter=True
)

BATCH_RETRY_CONFIG = RetryConfig(
    max_attempts=2,
    base_delay=2.0,
    max_delay=60.0,
    backoff_strategy=BackoffStrategy.LINEAR,
    jitter=True
)

CRITICAL_RETRY_CONFIG = RetryConfig(
    max_attempts=7,
    base_delay=0.1,
    max_delay=5.0,
    backoff_strategy=BackoffStrategy.EXPONENTIAL,
    backoff_factor=1.5,
    jitter=True
)


# Retry service instances
read_retry_service = RetryService(READ_RETRY_CONFIG)
write_retry_service = RetryService(WRITE_RETRY_CONFIG)
batch_retry_service = RetryService(BATCH_RETRY_CONFIG)
critical_retry_service = RetryService(CRITICAL_RETRY_CONFIG)


def retry_with_backoff(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    retryable_exceptions: Optional[List[Union[str, Type[Exception]]]] = None
):
    """
    Decorator for applying retry logic to async functions.
    
    Args:
        max_attempts: Maximum number of retry attempts
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        backoff_strategy: Strategy for calculating backoff
        backoff_factor: Multiplier for exponential backoff
        jitter: Whether to add randomness to delays
        retryable_exceptions: List of retryable exception types
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            config = RetryConfig(
                max_attempts=max_attempts,
                base_delay=base_delay,
                max_delay=max_delay,
                backoff_strategy=backoff_strategy,
                backoff_factor=backoff_factor,
                jitter=jitter,
                retryable_exceptions=retryable_exceptions or RetryConfig().retryable_exceptions
            )
            
            retry_service = RetryService(config)
            return await retry_service.execute_with_retry(func, *args, **kwargs)
        
        return wrapper
    return decorator


# Convenience decorators for common patterns
def read_retry(func: Callable):
    """Decorator for read operations with read-optimized retry config."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await read_retry_service.execute_with_retry(func, *args, **kwargs)
    return wrapper


def write_retry(func: Callable):
    """Decorator for write operations with write-optimized retry config."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await write_retry_service.execute_with_retry(func, *args, **kwargs)
    return wrapper


def batch_retry(func: Callable):
    """Decorator for batch operations with batch-optimized retry config."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await batch_retry_service.execute_with_retry(func, *args, **kwargs)
    return wrapper


def critical_retry(func: Callable):
    """Decorator for critical operations with aggressive retry config."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await critical_retry_service.execute_with_retry(func, *args, **kwargs)
    return wrapper
