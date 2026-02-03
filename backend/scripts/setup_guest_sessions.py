#!/usr/bin/env python3
"""
Create Guest Sessions Table

Script to create the guest_sessions DynamoDB table.
Run this script once to set up the table for guest mode functionality.

Usage:
    python scripts/create_guest_sessions_table.py
"""

import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Load .env file from backend root explicitly
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

from aioboto3 import Session
from app.core.config import settings


async def create_guest_sessions_table():
    """
    Create the guest_sessions DynamoDB table with the required schema.
    """
    try:
        print("Creating guest_sessions table...")
        
        # Create aioboto3 session
        session = Session(
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            aws_session_token=settings.aws_session_token,
            region_name=settings.aws_region
        )
        
        # Create DynamoDB client
        async with session.client(
            "dynamodb",
            region_name=settings.aws_region,
            endpoint_url=settings.dynamodb_endpoint
        ) as dynamodb:
            
            # Check if table already exists
            try:
                response = await dynamodb.describe_table(TableName="guest_sessions")
                print(f"Table 'guest_sessions' already exists")
                print(f"   Status: {response['Table']['TableStatus']}")
                return True
            except Exception:
                print("Table doesn't exist, creating...")
            
            # Create the table
            response = await dynamodb.create_table(
                TableName="guest_sessions",
                KeySchema=[
                    {
                        "AttributeName": "session_id",
                        "KeyType": "HASH"  # Partition key
                    }
                ],
                AttributeDefinitions=[
                    {
                        "AttributeName": "session_id",
                        "AttributeType": "S"
                    }
                ],
                BillingMode="PAY_PER_REQUEST",  # On-demand pricing
                Tags=[
                    {
                        "Key": "Project",
                        "Value": "DosaClub"
                    },
                    {
                        "Key": "Environment",
                        "Value": "Development"
                    }
                ]
            )
            
            print(f"Table creation initiated: {response['TableDescription']['TableName']}")
            print(f"   Status: {response['TableDescription']['TableStatus']}")
            print(f"   ARN: {response['TableDescription']['TableArn']}")
            
            # Wait for table to be created
            print("Waiting for table to become active...")
            waiter = dynamodb.get_waiter('table_exists')
            await waiter.wait(TableName="guest_sessions")
            
            print("Table 'guest_sessions' is now active and ready to use!")
            return True
            
    except Exception as e:
        print(f"Error creating table: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main function to create the table."""
    print("Starting guest_sessions table creation...")
    
    # Show configuration
    print(f"Configuration:")
    print(f"   AWS Region: {settings.aws_region}")
    print(f"   DynamoDB Endpoint: {settings.dynamodb_endpoint}")
    print(f"   Access Key ID: {settings.aws_access_key_id[:8]}..." if settings.aws_access_key_id else "   Access Key ID: None")
    print()
    
    # Create the table
    success = await create_guest_sessions_table()
    
    if success:
        print("\nGuest sessions table setup completed successfully!")
        print("\nNext steps:")
        print("   1. Restart your backend server")
        print("   2. Test the guest mode functionality")
        print("   3. The guest mode should now work without errors")
    else:
        print("\nTable creation failed!")
        print("   Please check the error messages above and fix any issues")
        sys.exit(1)


if __name__ == "__main__":
    # Run the table creation
    asyncio.run(main())
