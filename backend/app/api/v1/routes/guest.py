"""
Guest API routes (v1).

Endpoints for guest session management and cleanup.
Routes:
- POST /api/v1/guest/session - Create guest session
- POST /api/v1/guest/suggest-item - Get guest suggestion
- DELETE /api/v1/guest/session/{session_id} - Delete guest session
- POST /api/v1/guest/cleanup - Clean up expired sessions (admin)
"""

from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from app.models.user_models import (
    GuestSessionRequest,
    GuestSessionResponse,
    GuestSuggestionRequest,
    SuggestionResponse
)
from app.services.dynamodb import DynamoDBClient
from app.services.enhanced_health_logic import HealthLogicService
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/guest",
    tags=["guest"],
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
    "/session",
    response_model=GuestSessionResponse,
    summary="Create Guest Session",
    description="Create a temporary guest session for quick recommendations."
)
async def create_guest_session(
    db: DynamoDBClient = Depends(get_db_client)
) -> GuestSessionResponse:
    """
    Create a temporary guest session.
    
    **Returns:**
    - session_id: Unique session identifier
    - expires_at: Session expiry time (30 minutes)
    - message: Status message
    
    **Session Details:**
    - Valid for 30 minutes from creation
    - No personal data required
    - Can be used for health questionnaire and recommendations
    """
    try:
        logger.debug("🎭 Creating new guest session")
        
        # Create guest session
        session_data = await db.create_guest_session()
        logger.info(f"✅ Guest session created: {session_data['session_id']}")
        
        return GuestSessionResponse(
            session_id=session_data["session_id"],
            expires_at=session_data["expires_at"],
            message="Guest session created successfully"
        )
    
    except Exception as e:
        logger.error(f"🔥 Error creating guest session: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating guest session: {str(e)}"
        )


@router.post(
    "/suggest-item",
    response_model=SuggestionResponse,
    summary="Get Guest Food Suggestion",
    description="Get food recommendation using guest session and health data."
)
async def suggest_guest_item(
    request: GuestSuggestionRequest,
    db: DynamoDBClient = Depends(get_db_client)
) -> SuggestionResponse:
    """
    Generate a food suggestion for guest user.
    
    **Request:**
    - session_id: Valid guest session identifier
    - health_data: Guest health profile (no personal info required)
    
    **Suggestion Logic:** Same as registered users
    1. Medical Condition Rules (Highest Priority)
    2. BMI Category
    3. Health Goal
    
    **Returns:**
    - health_summary: 1-2 line health status
    - bmi_category: Computed BMI classification
    - suggested_item: ONE recommended food item
    - reason: Max 2-line explanation
    
    **Raises:**
    - 401: Invalid or expired session
    - 404: No suitable items found
    - 500: Processing error
    """
    try:
        # 1. Validate guest session
        is_valid = await db.validate_guest_session(request.session_id)
        if not is_valid:
            raise HTTPException(
                status_code=401, 
                detail="Invalid or expired guest session"
            )
        
        logger.debug(f"🎭 Processing guest suggestion for session: {request.session_id}")
        
        # 2. Extract health data
        health_data = request.health_data
        
        # 3. Calculate BMI
        bmi, bmi_category = await db.calculate_bmi(
            height_cm=health_data.height_cm,
            weight_kg=health_data.weight_kg
        )
        
        # 4. Initialize health logic service
        health_service = HealthLogicService(db)
        
        # 5. Generate suggestion using same logic as registered users
        suggestion = await health_service.suggest_item(
            bmi=bmi,
            bmi_category=bmi_category,
            medical_condition=health_data.medical_condition,
            health_goal=health_data.health_goal,
            diet_type=health_data.diet_type,
            spice_tolerance=health_data.spice_tolerance,
            age=health_data.age,
            weight_kg=health_data.weight_kg,
            height_cm=health_data.height_cm
        )
        
        logger.info(f"✅ Guest suggestion generated for session: {request.session_id}")
        return suggestion
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"🔥 Error generating guest suggestion: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating suggestion: {str(e)}"
        )


@router.delete(
    "/session/{session_id}",
    summary="Delete Guest Session",
    description="Manually delete a guest session before expiry."
)
async def delete_guest_session(
    session_id: str,
    db: DynamoDBClient = Depends(get_db_client)
):
    """
    Delete a guest session manually.
    
    **Path Parameters:**
    - session_id: Guest session identifier to delete
    
    **Returns:**
    - Success message if session was deleted
    - 404 if session not found
    """
    try:
        # Validate session exists first
        is_valid = await db.validate_guest_session(session_id)
        if not is_valid:
            raise HTTPException(
                status_code=404,
                detail="Session not found or already expired"
            )
        
        # Delete the session by marking as inactive
        async with db.session.client(
            "dynamodb", 
            region_name=db.region_name,
            endpoint_url=db.endpoint_url
        ) as dynamodb:
            await dynamodb.update_item(
                TableName="guest_sessions",
                Key={"session_id": {"S": session_id}},
                UpdateExpression="SET is_active = :false",
                ExpressionAttributeValues={":false": {"BOOL": False}}
            )
        
        logger.info(f"🗑️ Guest session deleted: {session_id}")
        return {"message": "Guest session deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔥 Error deleting guest session: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting session: {str(e)}"
        )


@router.post(
    "/cleanup",
    summary="Clean Up Expired Sessions",
    description="Clean up expired guest sessions (admin endpoint)."
)
async def cleanup_expired_sessions(
    db: DynamoDBClient = Depends(get_db_client)
):
    """
    Clean up expired guest sessions.
    
    **Returns:**
    - Number of sessions cleaned
    - Cleanup statistics
    
    **Note:** This is an admin endpoint for maintenance purposes.
    """
    try:
        logger.info("🧹 Starting manual cleanup of expired guest sessions")
        
        cleaned_count = await db.cleanup_expired_sessions()
        
        return {
            "message": "Cleanup completed successfully",
            "cleaned_sessions": cleaned_count,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"🔥 Error during cleanup: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error during cleanup: {str(e)}"
        )
