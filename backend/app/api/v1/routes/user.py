"""
User API routes (v1).

Endpoints for user health data collection and food suggestions.
Routes:
- POST /api/v1/user/intake - Collect user health data
- POST /api/v1/user/suggest-item - Get food suggestion
- GET /api/v1/user/profile/{phone_number} - Get user profile
- PUT /api/v1/user/profile/{phone_number} - Update user profile
- GET /api/v1/user/history/{phone_number} - Get suggestion history
- POST /api/v1/user/favorites - Add favorite item
- GET /api/v1/user/favorites/{phone_number} - Get user favorites
- DELETE /api/v1/user/favorites - Remove favorite item
"""

from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from app.models.user_models import (
    UserIntakeRequest,
    UserResponse,
    SuggestionResponse,
    UserUpdateRequest,
    UserHistoryResponse,
    FavoriteItemRequest,
    FavoriteResponse
)
from app.services.dynamodb import DynamoDBClient
from app.services.enhanced_health_logic import HealthLogicService
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/user",
    tags=["user"],
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
    "/intake",
    response_model=UserResponse,
    summary="User Health Data Intake",
    description="Collect user's basic and health information. Calculates BMI and stores profile."
)
async def user_intake(
    request: UserIntakeRequest,
    db: DynamoDBClient = Depends(get_db_client)
) -> UserResponse:
    """
    Collect user health data and register profile.
    
    **Request Fields:**
    - name: User's full name
    - phone_number: 10-digit contact number
    - age: User's age (18-120)
    - gender: male/female/other
    - height_cm: Height in centimeters (100-250)
    - weight_kg: Weight in kilograms (30-300)
    - diet_type: veg or egg
    - health_goal: weight_loss, weight_gain, or balanced
    - medical_condition: none, diabetes, bp, or acidity
    - spice_tolerance: low, medium, or high
    
    **Returns:**
    - user_id: Unique identifier for registered user
    - Calculated BMI and BMI category
    - All submitted health information
    
    Register a new user with health and dietary info.
    """
    try:
        logger.debug(f"📝 Processing user intake for: {request.name}, phone: {request.phone_number}")
        
        # Calculate BMI
        bmi, bmi_category = await db.calculate_bmi(request.height_cm, request.weight_kg)
        logger.debug(f"📊 Calculated BMI: {bmi} ({bmi_category})")
        
        # Prepare user data for storage
        user_data = {
            "name": request.name,
            "phone_number": request.phone_number,
            "age": request.age,
            "gender": request.gender,
            "height_cm": request.height_cm,
            "weight_kg": request.weight_kg,
            "bmi": bmi,
            "bmi_category": bmi_category,
            "diet_type": request.diet_type,
            "health_goal": request.health_goal,
            "medical_condition": request.medical_condition,
            "spice_tolerance": request.spice_tolerance,
        }
        
        # Create user in database
        user_id = await db.create_user(user_data)
        logger.info(f"✅ Created user {user_id} - BMI: {bmi} ({bmi_category})")
        
        return UserResponse(
            user_id=user_id,
            name=request.name,
            phone_number=request.phone_number,
            age=request.age,
            gender=request.gender,
            height_cm=request.height_cm,
            weight_kg=request.weight_kg,
            bmi=bmi,
            bmi_category=bmi_category,
            diet_type=request.diet_type,
            health_goal=request.health_goal,
            medical_condition=request.medical_condition,
            spice_tolerance=request.spice_tolerance,
            created_at=datetime.utcnow()
        )
    
    except ValueError as e:
        logger.error(f"❌ Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"🔥 Error processing intake: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing intake: {str(e)}"
        )


@router.post(
    "/suggest-item",
    response_model=SuggestionResponse,
    summary="Get Food Suggestion",
    description="Get ONE suitable food item based on health profile."
)
async def suggest_item(
    request: UserIntakeRequest,
    db: DynamoDBClient = Depends(get_db_client)
) -> SuggestionResponse:
    """
    Generate a food suggestion based on user's health profile.
    
    **Suggestion Logic (Priority Order):**
    1. Medical Condition Rules (Highest Priority)
       - Diabetes: Low-calorie, low-sugar items
       - BP: Low-oil, low-sodium items
       - Acidity: Mild, easy-to-digest items
    
    2. BMI Category
       - Underweight: Higher calories preferred
       - Normal: Balanced nutrition
       - Overweight: Lower calories, low oil
       - Obese: Minimal calories
    
    3. Health Goal
       - Weight Loss: Lower calorie items
       - Weight Gain: Higher calorie items
       - Balanced: Moderate nutrition
    
    **Constraints Applied:**
    - Spice tolerance respected
    - Diet type matched (veg/egg)
    - ONE item returned only
    
    **Returns:**
    - health_summary: 1-2 line health status
    - bmi_category: Computed BMI classification
    - suggested_item: ONE recommended food item
    - reason: Max 2-line explanation
    
    **Raises:**
    - 404: No suitable items found for criteria
    - 500: Processing error
    """
    try:
        # 1. Calculate BMI
        bmi, bmi_category = await db.calculate_bmi(
            height_cm=request.height_cm,
            weight_kg=request.weight_kg
        )
        
        # 2. SAVE USER DATA (New Feature)
        # Verify user data is complete enough to save
        if request.name and request.phone_number:
            user_data = {
                "name": request.name,
                "phone_number": request.phone_number,
                "age": request.age,
                "email": request.email,
                "gender": request.gender,
                "height_cm": request.height_cm,
                "weight_kg": request.weight_kg,
                "bmi": bmi,
                "bmi_category": bmi_category,
                "diet_type": request.diet_type,
                "health_goal": request.health_goal,
                "medical_condition": request.medical_condition,
                "spice_tolerance": request.spice_tolerance,
                "created_at": datetime.utcnow().isoformat()
            }
            try:
                await db.create_user(user_data)
                logger.info(f"💾 User {request.name} saved during suggestion flow.")
            except Exception as db_err:
                logger.error(f"⚠️ Failed to save user during suggestion: {db_err}")
                # Don't block suggestion on save failure
        
        # 3. Initialize health logic service
        health_service = HealthLogicService(db)
        
        # 4. Generate suggestion using intelligence engine
        suggestion = await health_service.suggest_item(
            bmi=bmi,
            bmi_category=bmi_category,
            medical_condition=request.medical_condition,
            health_goal=request.health_goal,
            diet_type=request.diet_type,
            spice_tolerance=request.spice_tolerance,
            age=request.age,
            weight_kg=request.weight_kg,
            height_cm=request.height_cm
        )
        
        return suggestion
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating suggestion: {str(e)}"
        )


@router.get(
    "/profile/{phone_number}",
    response_model=UserResponse,
    summary="Get User Profile",
    description="Retrieve user profile by phone number."
)
async def get_user_profile(
    phone_number: str,
    db: DynamoDBClient = Depends(get_db_client)
) -> UserResponse:
    """
    Get user profile by phone number.
    Returns the latest profile if multiple exist.
    """
    try:
        user_data = await db.get_user_by_phone(phone_number)
        
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
            
        return UserResponse(**user_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching profile: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching profile: {str(e)}"
        )
