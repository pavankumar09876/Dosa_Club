"""
User-related Pydantic models.

Defines request/response schemas for user intake and health data collection.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from app.models.admin_models import MenuItem


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class DietType(str, Enum):
    VEG = "veg"
    EGG = "egg"
    NON_VEG = "non-veg"


class HealthGoal(str, Enum):
    WEIGHT_LOSS = "weight_loss"
    WEIGHT_GAIN = "weight_gain"
    BALANCED = "balanced"


class MedicalCondition(str, Enum):
    NONE = "none"
    DIABETES = "diabetes"
    BP = "bp"
    ACIDITY = "acidity"


class SpiceTolerance(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class UserIntakeRequest(BaseModel):
    """
    User intake form submission.

    Collects basic and health information from tablet users.
    All fields are validated according to health guidelines.
    """

    # Basic Information
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="User's full name"
    )
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="User's age in years"
    )
    email: Optional[str] = Field(
        None,
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",
        description="User's email address"
    )
    phone_number: str = Field(
        ...,
        pattern=r"^\d{10}$",
        description="10-digit phone number"
    )

    # Demographic Information
    gender: Gender = Field(
        ...,
        description="Gender: male, female, or other"
    )

    # Physical Measurements
    height_cm: float = Field(
        ...,
        gt=100,
        lt=250,
        description="Height in centimeters (100-250)"
    )
    weight_kg: float = Field(
        ...,
        gt=30,
        lt=300,
        description="Weight in kilograms (30-300)"
    )

    # Dietary Preferences
    diet_type: DietType = Field(
        ...,
        description="Diet type: veg, egg, or non-veg"
    )

    # Health Goals
    health_goal: HealthGoal = Field(
        ...,
        description="Primary health goal"
    )

    # Medical Information
    medical_condition: MedicalCondition = Field(
        ...,
        description="Medical condition: none, diabetes, bp, or acidity"
    )

    # Food Preferences
    spice_tolerance: SpiceTolerance = Field(
        ...,
        description="Spice tolerance level: low, medium, or high"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "name": "Raj Kumar",
                "age": 35,
                "phone_number": "9876543210",
                "gender": "male",
                "height_cm": 175,
                "weight_kg": 85,
                "diet_type": "veg",
                "health_goal": "weight_loss",
                "medical_condition": "none",
                "spice_tolerance": "medium"
            }
        }


class UserResponse(BaseModel):
    """
    User profile response.

    Returned after user registration with calculated BMI and category.
    """

    user_id: str = Field(..., description="Unique user identifier (UUID)")
    name: str = Field(..., description="User's full name")
    phone_number: str = Field(..., description="Contact number")
    age: int = Field(..., description="Age in years")
    gender: Gender = Field(..., description="Gender")
    height_cm: float = Field(..., description="Height in cm")
    weight_kg: float = Field(..., description="Weight in kg")
    bmi: float = Field(..., description="Calculated BMI")
    bmi_category: str = Field(..., description="BMI classification")
    diet_type: DietType = Field(..., description="Diet type preference")
    health_goal: HealthGoal = Field(..., description="Health goal")
    medical_condition: MedicalCondition = Field(..., description="Medical condition")
    spice_tolerance: SpiceTolerance = Field(..., description="Spice tolerance")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Registration timestamp")
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class SuggestionResponse(BaseModel):
    """
    Food suggestion response.

    Provides health summary, BMI category, suggested item, and reasoning.
    Strictly formatted output: ONE item suggestion only.
    """

    health_summary: str = Field(
        ...,
        max_length=200,
        description="1-2 line health summary"
    )
    bmi_category: str = Field(
        ...,
        description="User's BMI category"
    )
    suggested_item: str = Field(
        ...,
        description="ONE suggested food item name"
    )
    suggested_item_details: Optional['MenuItem'] = Field(
        None,
        description="Full details of the suggested item"
    )
    similar_items: List['MenuItem'] = Field(
        default=[],
        description="List of similar/alternative item recommendations"
    )
    reason: str = Field(
        ...,
        max_length=300,
        description="Max 2 lines explaining the suggestion"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "health_summary": "Your BMI is 27.76 (overweight)",
                "bmi_category": "overweight",
                "suggested_item": "Vegetable Idli with Sambar",
                "reason": "Safe choice for weight loss. Lower calorie option (180cal)."
            }
        }


class UserUpdateRequest(BaseModel):
    """
    User profile update request.

    Allows partial updates to user profile information.
    """

    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="User's full name"
    )
    age: Optional[int] = Field(
        None,
        ge=18,
        le=120,
        description="User's age in years"
    )
    email: Optional[str] = Field(
        None,
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",
        description="User's email address"
    )
    gender: Optional[Gender] = Field(
        None,
        description="Gender: male, female, or other"
    )
    height_cm: Optional[float] = Field(
        None,
        gt=100,
        lt=250,
        description="Height in centimeters (100-250)"
    )
    weight_kg: Optional[float] = Field(
        None,
        gt=30,
        lt=300,
        description="Weight in kilograms (30-300)"
    )
    diet_type: Optional[DietType] = Field(
        None,
        description="Diet type: veg, egg, or non-veg"
    )
    health_goal: Optional[HealthGoal] = Field(
        None,
        description="Primary health goal"
    )
    medical_condition: Optional[MedicalCondition] = Field(
        None,
        description="Medical condition: none, diabetes, bp, or acidity"
    )
    spice_tolerance: Optional[SpiceTolerance] = Field(
        None,
        description="Spice tolerance level: low, medium, or high"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "name": "Updated Name",
                "age": 30,
                "email": "user@example.com",
                "weight_kg": 75.0,
                "health_goal": "balanced"
            }
        }


class UserHistoryResponse(BaseModel):
    """
    User suggestion history response.

    Lists all food suggestions made for a user.
    """

    suggestion_id: str = Field(..., description="Unique suggestion identifier")
    suggested_item: str = Field(..., description="Food item that was recommended")
    timestamp: str = Field(..., description="When suggestion was generated")
    health_summary: Optional[str] = Field(None, description="Health summary at time of suggestion")
    bmi_category: Optional[str] = Field(None, description="BMI category at time of suggestion")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "suggestion_id": "123e4567-e89b-12d3-a456-426614174000",
                "suggested_item": "Vegetable Idli with Sambar",
                "timestamp": "2023-12-01T10:30:00Z",
                "health_summary": "Your BMI is 25.5 (overweight)",
                "bmi_category": "overweight"
            }
        }


class FavoriteItemRequest(BaseModel):
    """
    Favorite item request.

    Used to add or remove favorite food items.
    """

    phone_number: str = Field(
        ...,
        pattern=r"^\d{10}$",
        description="User's 10-digit phone number"
    )
    item_id: str = Field(
        ...,
        description="ID of the menu item to favorite"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "phone_number": "9876543210",
                "item_id": "item_123"
            }
        }


class FavoriteResponse(BaseModel):
    """
    Favorite item response.

    Returns favorite food items for a user.
    """

    favorite_id: str = Field(..., description="Unique favorite identifier")
    phone_number: str = Field(..., description="User's phone number")
    item_id: str = Field(..., description="Menu item ID")
    item_name: str = Field(..., description="Menu item name")
    added_at: str = Field(..., description="When item was favorited")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "favorite_id": "fav_123",
                "phone_number": "9876543210",
                "item_id": "item_456",
                "item_name": "Masala Dosa",
                "added_at": "2023-12-01T10:30:00Z"
            }
        }


class GuestSessionRequest(BaseModel):
    """
    Guest session request for temporary health profile.

    Similar to UserIntakeRequest but without personal identifiers.
    Used for quick recommendations without profile creation.
    """

    # Demographic Information
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="User's age in years"
    )
    gender: Gender = Field(
        ...,
        description="Gender: male, female, or other"
    )

    # Physical Measurements
    height_cm: float = Field(
        ...,
        gt=100,
        lt=250,
        description="Height in centimeters (100-250)"
    )
    weight_kg: float = Field(
        ...,
        gt=30,
        lt=300,
        description="Weight in kilograms (30-300)"
    )

    # Dietary Preferences
    diet_type: DietType = Field(
        ...,
        description="Diet type: veg, egg, or non-veg"
    )

    # Health Goals
    health_goal: HealthGoal = Field(
        ...,
        description="Primary health goal"
    )

    # Medical Information
    medical_condition: MedicalCondition = Field(
        ...,
        description="Medical condition: none, diabetes, bp, or acidity"
    )

    # Food Preferences
    spice_tolerance: SpiceTolerance = Field(
        ...,
        description="Spice tolerance level: low, medium, or high"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "age": 35,
                "gender": "male",
                "height_cm": 175,
                "weight_kg": 85,
                "diet_type": "veg",
                "health_goal": "weight_loss",
                "medical_condition": "none",
                "spice_tolerance": "medium"
            }
        }


class GuestSessionResponse(BaseModel):
    """
    Guest session creation response.

    Returns session ID and expiry time for temporary guest access.
    """

    session_id: str = Field(..., description="Unique session identifier")
    expires_at: datetime = Field(..., description="Session expiry timestamp")
    message: str = Field(..., description="Session status message")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "session_id": "guest_session_123456",
                "expires_at": "2024-01-30T12:30:00Z",
                "message": "Guest session created successfully"
            }
        }


class GuestSuggestionRequest(BaseModel):
    """
    Guest suggestion request with session ID.

    Combines session identification with health data for recommendation.
    """

    session_id: str = Field(..., description="Guest session identifier")
    health_data: GuestSessionRequest = Field(..., description="Guest health profile data")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "session_id": "guest_session_123456",
                "health_data": {
                    "age": 35,
                    "gender": "male",
                    "height_cm": 175,
                    "weight_kg": 85,
                    "diet_type": "veg",
                    "health_goal": "weight_loss",
                    "medical_condition": "none",
                    "spice_tolerance": "medium"
                }
            }
        }
