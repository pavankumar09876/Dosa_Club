"""
Seed Menu Items with Images

This script updates existing menu items in DynamoDB to include image_url fields.
It assigns random images from the uploads directory to items that don't have images.
"""

import asyncio
import sys
import os
from typing import List, Dict, Any
import aioboto3

# Add the parent directory to the path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.dynamodb import DynamoDBClient
from app.core.config import settings

# List of available food images from uploads directory
DEFAULT_IMAGES = [
    "/assets/uploads/1769768504596_R.jpeg",
    "/assets/uploads/OIP.webp",
    "/assets/uploads/OIP (1).webp",
    "/assets/uploads/OIP (2).webp",
    "/assets/uploads/OIP (3).webp",
    "/assets/uploads/OIP (4).webp",
    "/assets/uploads/OIP (5).webp",
    "/assets/uploads/OIP (6).webp",
    "/assets/uploads/OIP (7).webp",
    "/assets/uploads/OIP (8).webp",
    "/assets/uploads/OIP (9).webp",
    "/assets/uploads/OIP (10).webp",
    "/assets/uploads/download.webp"
]

def get_consistent_image_for_item(item_name: str) -> str:
    """Generate a consistent image for a given item name."""
    # Create a simple hash from the item name
    hash_value = 0
    for char in item_name:
        hash_value = ((hash_value << 5) - hash_value) + ord(char)
        hash_value = hash_value & hash_value  # Convert to 32-bit integer
    
    # Use the hash to select an image consistently
    index = abs(hash_value) % len(DEFAULT_IMAGES)
    return DEFAULT_IMAGES[index]

async def seed_menu_images():
    """Seed existing menu items with image URLs."""
    print("[IMAGE] Seeding menu items with images...")
    
    try:
        print(f"[DEBUG] Using AWS credentials:")
        print(f"  Access Key ID: {(settings.aws_access_key_id or 'dummy')[:10]}...")
        print(f"  Region: {settings.aws_region}")
        print(f"  Endpoint: {settings.dynamodb_endpoint or 'http://localhost:8001'}")
        print(f"  Session Token: {'Present' if settings.aws_session_token else 'None'}")

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
        
        print("[DB] Connected to DynamoDB")
        
        # Get all existing menu items
        async with session.client(
            "dynamodb",
            endpoint_url=endpoint_url,
            region_name=settings.aws_region
        ) as dynamodb:
            response = await dynamodb.scan(TableName="menu_items")
            items = response.get("Items", [])
            
            print(f"[FOUND] Found {len(items)} menu items")
            
            updated_count = 0
            skipped_count = 0
            
            for item in items:
                item_id = item.get("item_id", {}).get("S", "")
                item_name = item.get("item_name", {}).get("S", "")
                existing_image_url = item.get("image_url", {}).get("S", None)
                
                if existing_image_url:
                    print(f"[SKIP] Skipping '{item_name}' - already has image: {existing_image_url}")
                    skipped_count += 1
                    continue
                
                # Assign a consistent image based on item name
                new_image_url = get_consistent_image_for_item(item_name)
                
                # Update the item with the new image URL
                update_expression = "SET image_url = :image_url"
                expression_values = {
                    ":image_url": {"S": new_image_url}
                }
                
                await dynamodb.update_item(
                    TableName="menu_items",
                    Key={"item_id": {"S": item_id}},
                    UpdateExpression=update_expression,
                    ExpressionAttributeValues=expression_values
                )
                
                print(f"[DONE] Updated '{item_name}' with image: {new_image_url}")
                updated_count += 1
            
            print(f"\n[COMPLETE] Seeding complete!")
            print(f"[SUMMARY]:")
            print(f"   [UPDATED] Updated: {updated_count} items")
            print(f"   [SKIPPED] Skipped: {skipped_count} items (already had images)")
            print(f"   [TOTAL] Total: {len(items)} items")
            
    except Exception as e:
        print(f"[ERROR] Error seeding menu images: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(seed_menu_images())
