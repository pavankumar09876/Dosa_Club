#!/usr/bin/env python3
"""
Enhanced Menu Items Seeder with Console Messaging and Skip Logic.

Loads menu items from seed_data.py and inserts them into the menu_items table.
Skips items that already exist to allow multiple runs.
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
import uuid
from seed_data import MENU_ITEMS
from app.core.config import settings


def print_banner():
    """Print script banner."""
    print("=" * 80)
    print("DOSA CLUB - MENU ITEMS SEEDER")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"DynamoDB Endpoint: {settings.dynamodb_endpoint or 'AWS (Real Service)'}")
    print(f"Region: {settings.aws_region}")
    print("-" * 80)


async def check_existing_item(ddb, item_name: str) -> bool:
    """Check if menu item already exists."""
    try:
        response = await ddb.scan(
            TableName="menu_items",
            FilterExpression="item_name = :name",
            ExpressionAttributeValues={":name": {"S": item_name}},
            Limit=1
        )
        return len(response.get("Items", [])) > 0
    except Exception as e:
        print(f"Error checking existing item {item_name}: {e}")
        return False


async def seed_menu_items():
    """Seed menu items from MENU_ITEMS list into DynamoDB."""
    print_banner()
    
    if not settings.aws_access_key_id or not settings.aws_secret_access_key:
        print("ERROR: AWS credentials not found in settings!")
        print(f"Checked for .env at: {os.path.abspath(dotenv_path)}")
        print("Please create a .env file in the backend/ directory with:")
        print("   AWS_ACCESS_KEY_ID=...")
        print("   AWS_SECRET_ACCESS_KEY=...")
        print("   AWS_REGION=...")
        return

    session = aioboto3.Session(
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        aws_session_token=settings.aws_session_token,
        region_name=settings.aws_region
    )
    
    try:
        async with session.client(
            "dynamodb",
            endpoint_url=settings.dynamodb_endpoint,
            region_name=settings.aws_region
        ) as ddb:
            
            # Check if table exists
            try:
                await ddb.describe_table(TableName="menu_items")
                print("menu_items table found")
            except Exception:
                print("menu_items table not found! Please run setup_core_tables.py first")
                return

            print(f"Processing {len(MENU_ITEMS)} menu items...")
            print("-" * 80)
            
            added_count = 0
            skipped_count = 0
            error_count = 0
            
            for i, item in enumerate(MENU_ITEMS, 1):
                item_name = item.get("item_name", "Unknown")
                
                try:
                    # Check if item already exists
                    exists = await check_existing_item(ddb, item_name)
                    
                    if exists:
                        print(f"SKIPPING: {item_name} (already exists)")
                        skipped_count += 1
                        continue
                    
                    # Add new item
                    item_id = str(uuid.uuid4())
                    suitable_for = item.get("suitable_for", {})
                    
                    put_item = {
                        "item_id": {"S": item_id},
                        "item_name": {"S": item_name},
                        "calories": {"N": str(item.get("calories", 0))},
                        "spice_level": {"S": item.get("spice_level", "medium")},
                        "oil_level": {"S": item.get("oil_level", "medium")},
                        "diet_type": {"S": item.get("diet_type", "veg")},
                        "suitable_for": {
                            "M": {
                                "bmi_categories": {"L": [{"S": c} for c in suitable_for.get("bmi_categories", [])]},
                                "medical_conditions": {"L": [{"S": m} for m in suitable_for.get("medical_conditions", [])]}
                            }
                        },
                        "created_at": {"S": datetime.utcnow().isoformat()}
                    }

                    await ddb.put_item(TableName="menu_items", Item=put_item)
                    print(f"ADDED: {item_name} (ID: {item_id[:8]}...)")
                    added_count += 1
                    
                except Exception as e:
                    print(f"ERROR: {item_name} - {e}")
                    error_count += 1

            print("-" * 80)
            print("SUMMARY:")
            print(f"   Added: {added_count} new items")
            print(f"   Skipped: {skipped_count} existing items")
            print(f"   Errors: {error_count} items")
            print(f"   Total processed: {len(MENU_ITEMS)} items")
            
            if added_count > 0:
                print("Menu items seeding completed successfully!")
            else:
                print("All menu items already exist in database")
                
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        print("Make sure DynamoDB is accessible and credentials are correct")
    
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(seed_menu_items())
