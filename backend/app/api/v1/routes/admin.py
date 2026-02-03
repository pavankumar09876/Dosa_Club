"""
Admin API routes (v1).

Endpoints for menu management, health rules, and analytics.
Routes:
- POST /api/v1/admin/menu - Add/update menu items
- POST /api/v1/admin/health-rule - Create health rules
- GET /api/v1/admin/users - List all users
- GET /api/v1/admin/suggestions - View suggestion history
"""

from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from typing import List, Dict, Any
import shutil
import os
from app.models.admin_models import (
    MenuItemRequest,
    MenuItem,
    HealthRuleRequest,
    HealthRule,
    AdminResponse
)
from app.models.user_models import UserResponse
from app.services.dynamodb import DynamoDBClient
from app.core.config import settings

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}}
)


def get_db_client() -> DynamoDBClient:
    """Dependency: Get DynamoDB client instance."""
    return DynamoDBClient(
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        endpoint_url=settings.dynamodb_endpoint
    )


@router.post(
    "/menu",
    response_model=AdminResponse,
    summary="Add/Update Menu Item",
    description="Create or update a food item in the menu catalog."
)
async def create_or_update_menu_item(
    request: MenuItemRequest,
    db: DynamoDBClient = Depends(get_db_client)
) -> AdminResponse:
    """
    Create or update a menu item.
    
    **Menu Item Fields:**
    - item_name: Name of the food item
    - calories: Caloric content (0-2000)
    - spice_level: low, medium, or high
    - oil_level: low, medium, or high
    - diet_type: veg or egg
    - suitable_for:
      - bmi_categories: List of suitable BMI categories
      - medical_conditions: List of safe medical conditions
    
    **Returns:**
    - success: Boolean operation status
    - message: Operation result message
    - item_id: Created/updated item ID
    
    **Raises:**
    - 400: Invalid menu item data
    - 500: Database error
    """
    try:
        if not isinstance(request.suitable_for, dict):
            raise ValueError(
                "suitable_for must contain bmi_categories and medical_conditions"
            )
        
        item_data = {
            "item_name": request.item_name,
            "calories": request.calories,
            "spice_level": request.spice_level,
            "oil_level": request.oil_level,
            "diet_type": request.diet_type,
            "image_url": request.image_url,
            "suitable_for": request.suitable_for
        }
        
        item_id = await db.create_or_update_menu_item(item_data)
        
        return AdminResponse(
            success=True,
            message="Menu item created/updated successfully",
            item_id=item_id
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating menu item: {str(e)}"
        )


@router.get(
    "/menu",
    response_model=List[MenuItem],
    summary="Get All Menu Items",
    description="Retrieve all menu items from the catalog."
)
async def get_menu_items(
    db: DynamoDBClient = Depends(get_db_client)
) -> List[MenuItem]:
    """
    Retrieve all menu items for display in menu explorer.
    
    Returns list of all available menu items with nutritional info.
    """
    try:
        async with db.session.client(
            "dynamodb",
            region_name=db.region_name,
            endpoint_url=db.endpoint_url
        ) as dynamodb:
            response = await dynamodb.scan(TableName="menu_items")
            
            menu_items = []
            for item in response.get("Items", []):
                # Extract suitable_for nested structure
                suitable_for_data = item.get("suitable_for", {}).get("M", {})
                bmi_categories = [s["S"] for s in suitable_for_data.get("bmi_categories", {}).get("L", [])]
                medical_conditions = [s["S"] for s in suitable_for_data.get("medical_conditions", {}).get("L", [])]
                
                menu_items.append(MenuItem(
                    item_id=item.get("item_id", {}).get("S", ""),
                    item_name=item.get("item_name", {}).get("S", ""),
                    calories=int(item.get("calories", {}).get("N", "0")),
                    spice_level=item.get("spice_level", {}).get("S", ""),
                    oil_level=item.get("oil_level", {}).get("S", ""),
                    diet_type=item.get("diet_type", {}).get("S", ""),
                    image_url=item.get("image_url", {}).get("S", None),
                    suitable_for={
                        "bmi_categories": bmi_categories,
                        "medical_conditions": medical_conditions
                    }
                ))
            
            return menu_items
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching menu items: {str(e)}"
        )


@router.delete(
    "/menu/{item_id}",
    response_model=AdminResponse,
    summary="Delete Menu Item",
    description="Delete a menu item from the catalog."
)
async def delete_menu_item(
    item_id: str,
    db: DynamoDBClient = Depends(get_db_client)
):
    """
    Delete a menu item from the database.
    
    **Use Cases:**
    - Remove discontinued items
    - Remove items with quality issues
    - Clean up duplicate entries
    
    **Parameters:**
    - item_id: Unique identifier of the menu item to delete
    
    **Returns:**
    - success: Boolean operation status
    - message: Operation result message
    - item_id: Deleted item ID
    
    **Raises:**
    - 404: Item not found
    - 500: Database error
    """
    try:
        success = await db.delete_menu_item(item_id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Menu item not found"
            )
        
        return AdminResponse(
            success=True,
            message="Menu item deleted successfully",
            item_id=item_id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting menu item: {str(e)}"
        )


@router.get(
    "/menu-items",
    response_model=List[MenuItem],
    summary="List All Menu Items",
    description="Retrieve all menu items from the catalog (admin only)."
)
async def get_all_menu_items(
    db: DynamoDBClient = Depends(get_db_client)
) -> List[MenuItem]:
    """
    Retrieve all menu items from the database.
    
    **Use Cases:**
    - View entire menu catalog
    - Menu management and editing
    - Analytics on item distribution
    - Menu planning and organization
    
    **Returns:**
    - List of all menu items with complete details:
      - item_id: Unique identifier
      - item_name: Food item name
      - calories: Caloric content
      - spice_level: Spice intensity
      - oil_level: Oil content
      - diet_type: Dietary classification
      - suitable_for: Health suitability criteria
    
    **Raises:**
    - 500: Database error
    """
    try:
        async with db.session.client(
            "dynamodb",
            region_name=db.region_name,
            endpoint_url=db.endpoint_url
        ) as dynamodb:
            response = await dynamodb.scan(TableName="menu_items")
            
            menu_items = []
            for item in response.get("Items", []):
                # Extract suitable_for nested structure
                suitable_for_data = item.get("suitable_for", {}).get("M", {})
                bmi_categories = [s["S"] for s in suitable_for_data.get("bmi_categories", {}).get("L", [])]
                medical_conditions = [s["S"] for s in suitable_for_data.get("medical_conditions", {}).get("L", [])]
                
                menu_items.append(MenuItem(
                    item_id=item.get("item_id", {}).get("S", ""),
                    item_name=item.get("item_name", {}).get("S", ""),
                    calories=int(item.get("calories", {}).get("N", "0")),
                    spice_level=item.get("spice_level", {}).get("S", ""),
                    oil_level=item.get("oil_level", {}).get("S", ""),
                    diet_type=item.get("diet_type", {}).get("S", ""),
                    image_url=item.get("image_url", {}).get("S", None),
                    suitable_for={
                        "bmi_categories": bmi_categories,
                        "medical_conditions": medical_conditions
                    }
                ))
            
            return menu_items
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching menu items: {str(e)}"
        )


@router.post(
    "/health-rule",
    response_model=AdminResponse,
    summary="Create Health Rule",
    description="Create a rule mapping BMI category + medical condition to allowed items."
)
async def create_health_rule(
    request: HealthRuleRequest,
    db: DynamoDBClient = Depends(get_db_client)
) -> AdminResponse:
    """
    Create a health rule for intelligent suggestions.
    
    Maps a specific combination of:
    - BMI category (underweight, normal, overweight, obese)
    - Medical condition (none, diabetes, bp, acidity)
    To a list of safe/suitable menu items.
    
    **Rule Creation Logic:**
    - If a user matches this BMI + condition combination
    - System will only suggest items in the allowed_items list
    - Ensures medical safety and health appropriateness
    
    **Request Fields:**
    - bmi_category: Target BMI category
    - medical_condition: Target medical condition
    - allowed_items: List of safe item IDs
    
    **Returns:**
    - success: Boolean operation status
    - message: Operation result message
    - rule_id: Created rule identifier
    
    **Raises:**
    - 400: Invalid rule data
    - 500: Database error
    """
    try:
        rule_id = f"{request.bmi_category}_{request.medical_condition}"
        
        async with db.session.client(
            "dynamodb",
            region_name=db.region_name,
            endpoint_url=db.endpoint_url
        ) as dynamodb:
            await dynamodb.put_item(
                TableName="health_rules",
                Item={
                    "rule_id": {"S": rule_id},
                    "bmi_category": {"S": request.bmi_category},
                    "medical_condition": {"S": request.medical_condition},
                    "allowed_items": {"L": [{"S": item} for item in request.allowed_items]}
                }
            )
        
        return AdminResponse(
            success=True,
            message="Health rule created successfully",
            rule_id=rule_id
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating health rule: {str(e)}"
        )


@router.get(
    "/health-rules",
    response_model=List[HealthRule],
    summary="List All Health Rules",
    description="Retrieve all health rules from the system (admin only)."
)
async def get_all_health_rules(
    db: DynamoDBClient = Depends(get_db_client)
) -> List[HealthRule]:
    """
    Retrieve all health rules from the database.
    
    **Use Cases:**
    - View all BMI + medical condition mappings
    - Audit health rule configuration
    - Rule management and updates
    - System validation
    
    **Returns:**
    - List of all health rules with:
      - rule_id: Unique identifier (bmi_category_medical_condition)
      - bmi_category: Target BMI category
      - medical_condition: Target medical condition
      - allowed_items: List of safe menu item IDs
    
    **Raises:**
    - 500: Database error
    """
    try:
        async with db.session.client(
            "dynamodb",
            region_name=db.region_name,
            endpoint_url=db.endpoint_url
        ) as dynamodb:
            response = await dynamodb.scan(TableName="health_rules")
            
            health_rules = []
            for item in response.get("Items", []):
                allowed_items = [s["S"] for s in item.get("allowed_items", {}).get("L", [])]
                
                health_rules.append(HealthRule(
                    rule_id=item.get("rule_id", {}).get("S", ""),
                    bmi_category=item.get("bmi_category", {}).get("S", ""),
                    medical_condition=item.get("medical_condition", {}).get("S", ""),
                    allowed_items=allowed_items
                ))
            
            return health_rules
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching health rules: {str(e)}"
        )


@router.get(
    "/users",
    response_model=List[UserResponse],
    summary="List All Users",
    description="Retrieve all registered users (admin only)."
)
async def get_all_users(
    db: DynamoDBClient = Depends(get_db_client)
) -> List[UserResponse]:
    """
    Retrieve all registered users from the system.
    
    **Use Cases:**
    - User management
    - Analytics and reporting
    - User outreach campaigns
    - System auditing
    
    **Returns:**
    - List of user profiles with their health data
    - Includes calculated BMI and categorization
    
    **Raises:**
    - 500: Database error
    """
    try:
        users = await db.list_users()
        return users
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching users: {str(e)}"
        )





@router.post(
    "/upload",
    summary="Upload Image",
    description="Upload an image file to the server."
)
async def upload_image(
    file: UploadFile = File(...)
):
    """
    Upload an image file and save it to the frontend assets directory.
    Returns the URL to access the image.
    """
    try:
        # Define upload directory (relative to backend/app/api/v1/routes)
        # We need to go up to root, then into frontend/public/assets/uploads
        # Current file: backend/app/api/v1/routes/admin.py
        # Path: ../../../../../frontend/public/assets/uploads
        
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
        upload_dir = os.path.join(base_path, "frontend", "public", "assets", "uploads")
        
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        # Generate unique filename to avoid collisions
        # Use simple timestamp-based name
        import time
        timestamp = int(time.time() * 1000)
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(upload_dir, filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {"url": f"/assets/uploads/{filename}"}
        
    except Exception as e:
        print(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")
