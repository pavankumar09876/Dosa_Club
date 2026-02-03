#!/usr/bin/env python3
"""
Enhanced Core Tables Setup with Console Messaging and Skip Logic.

Creates DynamoDB tables using credentials from settings.
Skips existing tables to allow multiple runs.
"""

import asyncio
import sys
import os
from dotenv import load_dotenv
from datetime import datetime

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load .env file from backend root explicitly
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

import aioboto3
from botocore.exceptions import ClientError
from app.core.config import settings


def print_banner():
    """Print script banner."""
    print("=" * 80)
    print("DOSA CLUB - CORE TABLES SETUP")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"DynamoDB Endpoint: {settings.dynamodb_endpoint or 'AWS (Real Service)'}")
    print(f"Region: {settings.aws_region}")
    print("-" * 80)


async def create_tables():
    """Create DynamoDB tables using credentials from settings."""
    print_banner()
    
    # For local DynamoDB, use dummy credentials and local endpoint
    endpoint_url = settings.dynamodb_endpoint or "http://localhost:8001"
    
    # Create session with credentials (same pattern as other scripts)
    session_kwargs = {
        "aws_access_key_id": settings.aws_access_key_id or "dummy",
        "aws_secret_access_key": settings.aws_secret_access_key or "dummy",
        "region_name": settings.aws_region
    }
    
    # Only add session token if it exists
    if settings.aws_session_token:
        session_kwargs["aws_session_token"] = settings.aws_session_token
        
    session = aioboto3.Session(**session_kwargs)

    print(f"[DEBUG] Using AWS credentials:")
    print(f"  Access Key ID: {(settings.aws_access_key_id or 'dummy')[:10]}...")
    print(f"  Region: {settings.aws_region}")
    print(f"  Endpoint: {endpoint_url}")
    print(f"  Session Token: {'Present' if settings.aws_session_token else 'None'}")
    
    async with session.client(
        "dynamodb",
        endpoint_url=endpoint_url,
        region_name=settings.aws_region
    ) as ddb:
        existing = await ddb.list_tables()
        table_names = existing.get("TableNames", [])

        tables = [
            {
                "name": "users",
                "key_schema": [{"AttributeName": "user_id", "KeyType": "HASH"}],
                "attribute_definitions": [{"AttributeName": "user_id", "AttributeType": "S"}],
                "billing_mode": "PAY_PER_REQUEST"
            },
            {
                "name": "menu_items",
                "key_schema": [{"AttributeName": "item_id", "KeyType": "HASH"}],
                "attribute_definitions": [{"AttributeName": "item_id", "AttributeType": "S"}],
                "billing_mode": "PAY_PER_REQUEST"
            },
            {
                "name": "health_rules",
                "key_schema": [{"AttributeName": "rule_id", "KeyType": "HASH"}],
                "attribute_definitions": [{"AttributeName": "rule_id", "AttributeType": "S"}],
                "billing_mode": "PAY_PER_REQUEST"
            },
            {
                "name": "suggestions_log",
                "key_schema": [{"AttributeName": "suggestion_id", "KeyType": "HASH"}],
                "attribute_definitions": [{"AttributeName": "suggestion_id", "AttributeType": "S"}],
                "billing_mode": "PAY_PER_REQUEST"
            },
            {
                "name": "favorites",
                "key_schema": [{"AttributeName": "favorite_id", "KeyType": "HASH"}],
                "attribute_definitions": [{"AttributeName": "favorite_id", "AttributeType": "S"}],
                "billing_mode": "PAY_PER_REQUEST"
            },
            {
                "name": "guest_sessions",
                "key_schema": [{"AttributeName": "session_id", "KeyType": "HASH"}],
                "attribute_definitions": [{"AttributeName": "session_id", "AttributeType": "S"}],
                "billing_mode": "PAY_PER_REQUEST"
            }
        ]

        print(f"Processing {len(tables)} tables...")
        print("-" * 80)
        
        created_count = 0
        skipped_count = 0
        error_count = 0
        
        for i, table in enumerate(tables, 1):
            table_name = table["name"]
            
            try:
                if table_name in table_names:
                    print(f"Skipping: {table_name} (already exists)")
                    skipped_count += 1
                    continue
                
                await ddb.create_table(
                    TableName=table_name,
                    KeySchema=table["key_schema"],
                    AttributeDefinitions=table["attribute_definitions"],
                    BillingMode=table["billing_mode"]
                )
                
                print(f"Created: {table_name}")
                created_count += 1
                
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == 'ResourceInUseException':
                    print(f"Skipping: {table_name} (already exists)")
                    skipped_count += 1
                else:
                    print(f"Error: {table_name} - {error_code}")
                    error_count += 1
            except Exception as e:
                print(f"Error: {table_name} - {e}")
                error_count += 1

        print("-" * 80)
        print("Summary:")
        print(f"   Created: {created_count} new tables")
        print(f"   Skipped: {skipped_count} existing tables")
        print(f"   Errors: {error_count} tables")
        print(f"   Total processed: {len(tables)} tables")
        
        if created_count > 0:
            print("Table setup completed successfully!")
        else:
            print("All tables already exist in database")
    
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(create_tables())
