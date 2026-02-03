"""
Custom exceptions for the application.

Defines custom exception types for better error handling
and circuit breaker integration.
"""

from typing import Optional, Any, Dict


class DosaClubException(Exception):
    """Base exception for DosaClub application."""
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}


class DatabaseException(DosaClubException):
    """Base exception for database-related errors."""
    pass


class DynamoDBException(DatabaseException):
    """Exception for DynamoDB-specific errors."""
    
    def __init__(
        self,
        message: str,
        operation: Optional[str] = None,
        table_name: Optional[str] = None,
        aws_error_code: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.operation = operation
        self.table_name = table_name
        self.aws_error_code = aws_error_code


class DynamoDBTimeoutException(DynamoDBException):
    """Exception for DynamoDB timeout errors."""
    pass


class DynamoDBThrottlingException(DynamoDBException):
    """Exception for DynamoDB throttling errors."""
    pass


class DynamoDBProvisionedException(DynamoDBException):
    """Exception for DynamoDB provisioned throughput exceeded errors."""
    pass


class CacheException(DosaClubException):
    """Exception for cache-related errors."""
    pass


class CircuitBreakerOpenException(DosaClubException):
    """Exception raised when circuit breaker is open."""
    pass


class RetryExhaustedException(DosaClubException):
    """Exception raised when all retry attempts are exhausted."""
    
    def __init__(
        self,
        message: str,
        attempts: int,
        last_exception: Optional[Exception] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.attempts = attempts
        self.last_exception = last_exception


class ServiceUnavailableException(DosaClubException):
    """Exception raised when a service is unavailable."""
    pass


class ValidationException(DosaClubException):
    """Exception for validation errors."""
    pass


class AuthenticationException(DosaClubException):
    """Exception for authentication errors."""
    pass


class AuthorizationException(DosaClubException):
    """Exception for authorization errors."""
    pass


class RateLimitException(DosaClubException):
    """Exception for rate limiting errors."""
    pass


class ConfigurationException(DosaClubException):
    """Exception for configuration errors."""
    pass


class BackupException(DosaClubException):
    """Exception for backup-related errors."""
    pass


class HealthCheckException(DosaClubException):
    """Exception for health check failures."""
    pass
