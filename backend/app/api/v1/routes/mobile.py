"""
Mobile API Endpoints
Handles mobile questionnaire and recommendation requests
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid
from datetime import datetime, timedelta

router = APIRouter(prefix="/mobile", tags=["mobile"])

# Simple in-memory session storage (in production, use Redis)
mobile_sessions: Dict[str, Dict] = {}

class MobileQuestionnaireRequest(BaseModel):
    session_id: str
    questionnaire_data: Dict[str, Any]

class MobileQuestionnaireResponse(BaseModel):
    success: bool
    message: str
    recommendation: Optional[Dict[str, Any]] = None

@router.post("/questionnaire", response_model=MobileQuestionnaireResponse)
async def submit_mobile_questionnaire(request: MobileQuestionnaireRequest):
    """
    Submit questionnaire data from mobile device
    """
    try:
        # Validate session
        if request.session_id not in mobile_sessions:
            # Create new session if it doesn't exist
            mobile_sessions[request.session_id] = {
                "created_at": datetime.now(),
                "questionnaire_data": request.questionnaire_data,
                "status": "completed"
            }
        else:
            # Update existing session
            mobile_sessions[request.session_id]["questionnaire_data"] = request.questionnaire_data
            mobile_sessions[request.session_id]["status"] = "completed"
        
        # Generate mock recommendation (in production, call your recommendation engine)
        mock_recommendation = {
            "item_name": "Masala Dosa",
            "calories": 250,
            "spice_level": "medium",
            "diet_type": "vegetarian",
            "image_url": "/api/placeholder/300/200",
            "reason": "Perfect for your fitness goals and dietary preferences",
            "bmi_category": "Normal",
            "health_summary": "Balanced meal with moderate calories",
            "similar_items": [
                {
                    "item_id": "2",
                    "item_name": "Plain Dosa",
                    "calories": 180,
                    "spice_level": "low",
                    "diet_type": "vegetarian",
                    "image_url": "/api/placeholder/300/200"
                }
            ]
        }
        
        return MobileQuestionnaireResponse(
            success=True,
            message="Questionnaire submitted successfully",
            recommendation=mock_recommendation
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/{session_id}")
async def get_mobile_session(session_id: str):
    """
    Get mobile session data
    """
    if session_id not in mobile_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "status": mobile_sessions[session_id]["status"],
        "created_at": mobile_sessions[session_id]["created_at"],
        "questionnaire_data": mobile_sessions[session_id].get("questionnaire_data", {})
    }

@router.post("/session")
async def create_mobile_session():
    """
    Create a new mobile session
    """
    session_id = str(uuid.uuid4())
    mobile_sessions[session_id] = {
        "created_at": datetime.now(),
        "questionnaire_data": {},
        "status": "created"
    }
    
    return {
        "session_id": session_id,
        "status": "created",
        "expires_at": datetime.now() + timedelta(hours=24)
    }

@router.get("/recommendation/{session_id}")
async def get_mobile_recommendation(session_id: str):
    """
    Get recommendation for a mobile session
    """
    if session_id not in mobile_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = mobile_sessions[session_id]
    
    if session["status"] != "completed":
        raise HTTPException(status_code=400, detail="Questionnaire not completed")
    
    # Return the same mock recommendation (in production, generate based on questionnaire data)
    mock_recommendation = {
        "item_name": "Masala Dosa",
        "calories": 250,
        "spice_level": "medium",
        "diet_type": "vegetarian",
        "image_url": "/api/placeholder/300/200",
        "reason": "Perfect for your fitness goals and dietary preferences",
        "bmi_category": "Normal",
        "health_summary": "Balanced meal with moderate calories",
        "similar_items": [
            {
                "item_id": "2",
                "item_name": "Plain Dosa",
                "calories": 180,
                "spice_level": "low",
                "diet_type": "vegetarian",
                "image_url": "/api/placeholder/300/200"
            }
        ]
    }
    
    return {
        "session_id": session_id,
        "recommendation": mock_recommendation,
        "generated_at": datetime.now()
    }

# Cleanup expired sessions (run periodically)
@router.delete("/cleanup")
async def cleanup_expired_sessions():
    """
    Clean up expired sessions (older than 24 hours)
    """
    expired_sessions = []
    current_time = datetime.now()
    
    for session_id, session_data in mobile_sessions.items():
        if current_time - session_data["created_at"] > timedelta(hours=24):
            expired_sessions.append(session_id)
    
    for session_id in expired_sessions:
        del mobile_sessions[session_id]
    
    return {
        "cleaned_sessions": len(expired_sessions),
        "remaining_sessions": len(mobile_sessions)
    }
