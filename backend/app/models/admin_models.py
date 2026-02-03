"""
Admin-related Pydantic models.

Defines schemas for menu management, health rules, and analytics.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum


class Allergen(str, Enum):
    """Common food allergens."""
    GLUTEN = "gluten"
    DAIRY = "dairy"
    NUTS = "nuts"
    SOY = "soy"
    EGGS = "eggs"
    FISH = "fish"
    SHELLFISH = "shellfish"
    PEANUTS = "peanuts"
    SESAME = "sesame"
    NONE = "none"


class NutrientType(str, Enum):
    """Nutrient types for detailed nutrition."""
    PROTEIN = "protein"
    CARBOHYDRATES = "carbohydrates"
    FAT = "fat"
    FIBER = "fiber"
    SUGAR = "sugar"
    SODIUM = "sodium"
    CHOLESTEROL = "cholesterol"
    VITAMIN_A = "vitamin_a"
    VITAMIN_C = "vitamin_c"
    CALCIUM = "iron"
    IRON = "iron"


class NutritionInfo(BaseModel):
    """Detailed nutritional information."""
    protein_g: float = Field(..., ge=0, description="Protein in grams")
    carbohydrates_g: float = Field(..., ge=0, description="Carbohydrates in grams")
    fat_g: float = Field(..., ge=0, description="Total fat in grams")
    fiber_g: float = Field(0, ge=0, description="Dietary fiber in grams")
    sugar_g: float = Field(0, ge=0, description="Total sugar in grams")
    sodium_mg: float = Field(0, ge=0, description="Sodium in milligrams")
    cholesterol_mg: float = Field(0, ge=0, description="Cholesterol in milligrams")
    
    # Vitamins and minerals (optional)
    vitamin_a_mcg: Optional[float] = Field(None, ge=0, description="Vitamin A in micrograms")
    vitamin_c_mg: Optional[float] = Field(None, ge=0, description="Vitamin C in milligrams")
    calcium_mg: Optional[float] = Field(None, ge=0, description="Calcium in milligrams")
    iron_mg: Optional[float] = Field(None, ge=0, description="Iron in milligrams")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "protein_g": 8.5,
                "carbohydrates_g": 35.2,
                "fat_g": 3.8,
                "fiber_g": 2.1,
                "sugar_g": 1.5,
                "sodium_mg": 420,
                "cholesterol_mg": 0,
                "vitamin_a_mcg": 45,
                "vitamin_c_mg": 2.1,
                "calcium_mg": 120,
                "iron_mg": 1.8
            }
        }


class HealthBenefit(BaseModel):
    """Health benefits of a food item."""
    category: str = Field(..., description="Benefit category (e.g., 'heart', 'digestion', 'immunity')")
    title: str = Field(..., description="Short benefit title")
    description: str = Field(..., description="Detailed benefit description")
    importance: str = Field(..., pattern="^(low|medium|high)$", description="Benefit importance level")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "category": "heart",
                "title": "Heart Healthy",
                "description": "Low in saturated fat and sodium, supports cardiovascular health",
                "importance": "high"
            }
        }


class MenuItemRequest(BaseModel):
    """
    Menu item creation/update request.
    
    Used by admins to add or modify food items in the system.
    """
    
    item_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Food item name"
    )
    
    calories: int = Field(
        ...,
        gt=0,
        lt=2000,
        description="Caloric content (0-2000 cal)"
    )
    
    spice_level: str = Field(
        ...,
        pattern="^(low|medium|high)$",
        description="Spice level: low, medium, or high"
    )
    
    oil_level: str = Field(
        ...,
        pattern="^(low|medium|high)$",
        description="Oil content: low, medium, or high"
    )
    
    diet_type: str = Field(
        ...,
        pattern="^(veg|egg|non-veg)$",
        description="Diet type: veg, egg, or non-veg"
    )
    
    suitable_for: Dict[str, List[str]] = Field(
        ...,
        description="Suitable BMI categories and medical conditions"
    )

    image_url: Optional[str] = Field(
        None,
        description="URL to the food item image"
    )
    
    # Enhanced nutritional information
    nutrition: Optional[NutritionInfo] = Field(
        None,
        description="Detailed nutritional information"
    )
    
    allergens: List[Allergen] = Field(
        default=[],
        description="List of allergens present in the food item"
    )
    
    health_benefits: List[HealthBenefit] = Field(
        default=[],
        description="Health benefits of the food item"
    )
    
    preparation_time_minutes: Optional[int] = Field(
        None,
        ge=0,
        le=120,
        description="Preparation time in minutes"
    )
    
    serving_size_g: Optional[float] = Field(
        None,
        gt=0,
        description="Standard serving size in grams"
    )
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "item_name": "Vegetable Idli with Sambar",
                "calories": 180,
                "spice_level": "low",
                "oil_level": "low",
                "diet_type": "veg",
                "image_url": "https://example.com/idli.jpg",
                "suitable_for": {
                    "bmi_categories": ["underweight", "normal", "overweight"],
                    "medical_conditions": ["none", "diabetes", "bp", "acidity"]
                },
                "nutrition": {
                    "protein_g": 8.5,
                    "carbohydrates_g": 35.2,
                    "fat_g": 3.8,
                    "fiber_g": 2.1,
                    "sugar_g": 1.5,
                    "sodium_mg": 420,
                    "cholesterol_mg": 0
                },
                "allergens": ["none"],
                "health_benefits": [
                    {
                        "category": "digestion",
                        "title": "Easy to Digest",
                        "description": "Fermented batter aids digestion and gut health",
                        "importance": "high"
                    }
                ],
                "preparation_time_minutes": 15,
                "serving_size_g": 150
            }
        }


class MenuItem(BaseModel):
    """
    Menu item response.
    
    Complete menu item data returned from database.
    """
    
    item_id: str = Field(..., description="Unique item identifier")
    item_name: str = Field(..., description="Food item name")
    calories: int = Field(..., description="Caloric content")
    spice_level: str = Field(..., description="Spice level")
    oil_level: str = Field(..., description="Oil content level")
    diet_type: str = Field(..., description="Diet type")
    image_url: Optional[str] = Field(None, description="Image URL")
    suitable_for: Dict[str, List[str]] = Field(..., description="Suitability criteria")
    
    # Enhanced nutritional information
    nutrition: Optional[NutritionInfo] = Field(None, description="Detailed nutritional information")
    allergens: List[Allergen] = Field(default=[], description="List of allergens")
    health_benefits: List[HealthBenefit] = Field(default=[], description="Health benefits")
    preparation_time_minutes: Optional[int] = Field(None, description="Preparation time in minutes")
    serving_size_g: Optional[float] = Field(None, description="Standard serving size in grams")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class HealthRuleRequest(BaseModel):
    """
    Health rule creation request.
    
    Maps BMI category + medical condition to allowed food items.
    Used for rule-based suggestions.
    """
    
    bmi_category: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="BMI category (underweight, normal, overweight, obese)"
    )
    
    medical_condition: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Medical condition (none, diabetes, bp, acidity)"
    )
    
    allowed_items: List[str] = Field(
        ...,
        min_items=1,
        description="List of allowed menu item IDs"
    )
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "bmi_category": "overweight",
                "medical_condition": "diabetes",
                "allowed_items": ["item-id-1", "item-id-2", "item-id-3"]
            }
        }


class HealthRule(BaseModel):
    """
    Health rule response.
    
    Rule mapping for medical-condition-based item suggestions.
    """
    
    rule_id: str = Field(..., description="Unique rule identifier")
    bmi_category: str = Field(..., description="BMI category")
    medical_condition: str = Field(..., description="Medical condition")
    allowed_items: List[str] = Field(..., description="Allowed item IDs")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True





class AdminResponse(BaseModel):
    """
    Generic admin operation response.
    
    Used for menu and rule creation endpoints.
    """
    
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Operation message")
    item_id: Optional[str] = Field(None, description="Created/updated item ID")
    rule_id: Optional[str] = Field(None, description="Created rule ID")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Menu item created successfully",
                "item_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
