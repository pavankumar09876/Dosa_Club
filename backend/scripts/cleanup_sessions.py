#!/usr/bin/env python3
"""
Guest Session Cleanup Script

Periodically cleans up expired guest sessions from DynamoDB.
Can be run as a cron job or scheduled task.

Usage:
    python scripts/cleanup_guest_sessions.py
"""

import asyncio
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path to import app modules
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load .env file from backend root explicitly
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

from app.services.dynamodb import DynamoDBClient
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def cleanup_guest_sessions():
    """
    Clean up expired guest sessions from DynamoDB.
    
    This function:
    1. Connects to DynamoDB
    2. Scans for expired sessions
    3. Deletes expired sessions
    4. Reports cleanup statistics
    """
    try:
        logger.info("🧹 Starting guest session cleanup...")
        
        # Initialize DynamoDB client
        db_client = DynamoDBClient(
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            aws_session_token=settings.aws_session_token,
            endpoint_url=settings.dynamodb_endpoint
        )
        
        # Clean up expired sessions
        cleaned_count = await db_client.cleanup_expired_sessions()
        
        if cleaned_count > 0:
            logger.info(f"✅ Successfully cleaned up {cleaned_count} expired guest sessions")
        else:
            logger.info("ℹ️ No expired sessions found")
            
        return cleaned_count
        
    except Exception as e:
        logger.error(f"🔥 Error during cleanup: {e}")
        raise


async def main():
    """Main function to run the cleanup process."""
    start_time = datetime.utcnow()
    
    try:
        cleaned_count = await cleanup_guest_sessions()
        
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        logger.info(f"🏁 Cleanup completed in {duration:.2f} seconds")
        logger.info(f"📊 Total sessions cleaned: {cleaned_count}")
        
    except Exception as e:
        logger.error(f"💥 Cleanup failed: {e}")
        exit(1)


if __name__ == "__main__":
    # Run the cleanup
    asyncio.run(main())
