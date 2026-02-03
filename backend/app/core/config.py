"""
Application configuration management.

This module handles all application settings including AWS configuration,
environment variables, and runtime settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings.

    Loads configuration from environment variables with sensible defaults.
    Attributes can be overridden via .env file.
    """

    # Application
    app_name: str = "DosaClub"
    app_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"
    environment: str = "development"
    debug: bool = True

    # AWS Configuration
    aws_region: str = "us-east-1"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_session_token: Optional[str] = None
    aws_profile: Optional[str] = None

    # DynamoDB Configuration
    dynamodb_endpoint: Optional[str] = "http://localhost:8001"
    dynamodb_tables: dict = {
        "users": "users",
        "menu_items": "menu_items",
        "health_rules": "health_rules"
    }

    # API Configuration
    cors_origins: list = ["*"]
    cors_credentials: bool = True
    cors_methods: list = ["*"]
    cors_headers: list = ["*"]

    # Server Configuration
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    reload: bool = True

    # Logging
    log_level: str = "DEBUG"

    # Circuit Breaker Configuration
    circuit_breaker_failure_threshold: int = 3
    circuit_breaker_recovery_timeout: int = 30
    circuit_breaker_half_open_max_calls: int = 3
    circuit_breaker_timeout: float = 5.0

    # Retry Configuration
    retry_max_attempts: int = 2
    retry_base_delay: float = 0.5
    retry_max_delay: float = 10.0
    retry_backoff_factor: float = 2.0
    retry_jitter: bool = True

    # Cache Configuration
    cache_ttl: int = 300  # 5 minutes
    cache_max_size: int = 1000
    cache_enabled: bool = True

    # Backup Configuration
    backup_enabled: bool = False
    backup_interval: int = 3600  # 1 hour
    backup_path: str = "./backups"
    backup_retention_days: int = 7

    # Health Check Configuration
    health_check_enabled: bool = True
    health_check_interval: int = 30  # seconds
    health_check_timeout: float = 5.0

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")


settings = Settings()
