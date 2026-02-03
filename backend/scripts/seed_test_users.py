import asyncio
import sys
import os
from dotenv import load_dotenv

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load .env file from backend root explicitly
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

import aioboto3
import uuid
from datetime import datetime
from app.core.config import settings


async def create_test_user(name: str):
    """Create a test user with sample data."""
    
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

    async with session.client(
        "dynamodb",
        endpoint_url=endpoint_url,
        region_name=settings.aws_region
    ) as ddb:
        user_id = str(uuid.uuid4())
        item = {
            "user_id": {"S": user_id},
            "name": {"S": name},
            "phone_number": {"S": "9999999999"},
            "age": {"N": "30"},
            "gender": {"S": "other"},
            "height_cm": {"N": "170"},
            "weight_kg": {"N": "70"},
            "bmi": {"N": "24.22"},
            "bmi_category": {"S": "normal"},
            "diet_type": {"S": "veg"},
            "health_goal": {"S": "balanced"},
            "medical_condition": {"S": "none"},
            "spice_tolerance": {"S": "medium"},
            "created_at": {"S": datetime.utcnow().isoformat()}
        }

        await ddb.put_item(TableName="users", Item=item)
        print(f"Created test user '{name}' (user_id={user_id})")
        return user_id


if __name__ == "__main__":
    asyncio.run(create_test_user("Dev Test User"))
