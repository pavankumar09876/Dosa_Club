"""
Fallback Service for Graceful Degradation.

Provides fallback responses when primary services are unavailable,
ensuring the application remains functional during outages.
"""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from app.models.admin_models import MenuItem, HealthRule
from app.utils.exceptions import ServiceUnavailableException

logger = logging.getLogger(__name__)


class FallbackService:
    """
    Service providing fallback responses for graceful degradation.
    
    When DynamoDB or other services are unavailable, this service
    provides sensible defaults and cached responses.
    """
    
    def __init__(self):
        self._fallback_menu_items: List[MenuItem] = []
        self._fallback_health_rules: List[HealthRule] = []
        self._initialize_fallback_data()
    
    def _initialize_fallback_data(self):
        """Initialize fallback data for critical operations."""
        logger.info("Initializing fallback data...")
        
        # Fallback menu items - safe, popular options
        self._fallback_menu_items = [
            MenuItem(
                item_id="fallback_idli",
                item_name="Plain Idli",
                calories=58,
                spice_level="low",
                oil_level="low",
                diet_type="vegetarian",
                image_url=None,
                suitable_for={
                    "bmi_categories": ["underweight", "normal", "overweight", "obese"],
                    "medical_conditions": ["none", "diabetes", "bp", "acidity"]
                }
            ),
            MenuItem(
                item_id="fallback_dosa",
                item_name="Plain Dosa",
                calories=133,
                spice_level="low",
                oil_level="medium",
                diet_type="vegetarian",
                image_url=None,
                suitable_for={
                    "bmi_categories": ["underweight", "normal", "overweight"],
                    "medical_conditions": ["none", "bp"]
                }
            ),
            MenuItem(
                item_id="fallback_pongal",
                item_name="Ven Pongal",
                calories=178,
                spice_level="low",
                oil_level="medium",
                diet_type="vegetarian",
                image_url=None,
                suitable_for={
                    "bmi_categories": ["underweight", "normal"],
                    "medical_conditions": ["none"]
                }
            ),
            MenuItem(
                item_id="fallback_upma",
                item_name="Rava Upma",
                calories=210,
                spice_level="low",
                oil_level="medium",
                diet_type="vegetarian",
                image_url=None,
                suitable_for={
                    "bmi_categories": ["underweight", "normal"],
                    "medical_conditions": ["none", "acidity"]
                }
            ),
            MenuItem(
                item_id="fallback_curd_rice",
                item_name="Curd Rice",
                calories=146,
                spice_level="low",
                oil_level="low",
                diet_type="vegetarian",
                image_url=None,
                suitable_for={
                    "bmi_categories": ["normal", "overweight", "obese"],
                    "medical_conditions": ["none", "diabetes", "bp", "acidity"]
                }
            )
        ]
        
        # Fallback health rules - conservative recommendations
        self._fallback_health_rules = [
            HealthRule(
                rule_id="fallback_normal_none",
                bmi_category="normal",
                medical_condition="none",
                allowed_items=["prefer_balanced", "prefer_low_oil"]
            ),
            HealthRule(
                rule_id="fallback_diabetes",
                bmi_category="normal",
                medical_condition="diabetes",
                allowed_items=["avoid_sweet", "prefer_low_oil", "prefer_high_fiber"]
            ),
            HealthRule(
                rule_id="fallback_bp",
                bmi_category="normal",
                medical_condition="bp",
                allowed_items=["prefer_low_salt", "prefer_low_oil"]
            ),
            HealthRule(
                rule_id="fallback_acidity",
                bmi_category="normal",
                medical_condition="acidity",
                allowed_items=["prefer_low_spice", "prefer_low_oil"]
            ),
            HealthRule(
                rule_id="fallback_obese",
                bmi_category="obese",
                medical_condition="none",
                allowed_items=["prefer_very_low_calorie", "prefer_low_oil"]
            )
        ]
        
        logger.info(f"Initialized {len(self._fallback_menu_items)} fallback menu items")
        logger.info(f"Initialized {len(self._fallback_health_rules)} fallback health rules")
    
    def get_fallback_menu_items(
        self, 
        bmi_category: str = "normal",
        medical_condition: str = "none",
        diet_type: str = "vegetarian",
        spice_tolerance: str = "medium"
    ) -> List[MenuItem]:
        """
        Get fallback menu items based on criteria.
        
        Returns safe, universally acceptable options when database is unavailable.
        """
        logger.warning(
            f"Using fallback menu items for criteria: "
            f"bmi={bmi_category}, condition={medical_condition}, "
            f"diet={diet_type}, spice={spice_tolerance}"
        )
        
        # Filter fallback items based on basic criteria
        suitable_items = []
        
        for item in self._fallback_menu_items:
            # Check diet type compatibility
            if diet_type != "vegetarian" and item.diet_type == "vegetarian":
                continue
            
            # Check BMI category compatibility
            if bmi_category not in item.suitable_for["bmi_categories"]:
                continue
            
            # Check medical condition compatibility
            if medical_condition not in item.suitable_for["medical_conditions"]:
                continue
            
            # Check spice tolerance
            if spice_tolerance == "low" and item.spice_level == "high":
                continue
            
            suitable_items.append(item)
        
        # If no items match, return the safest options
        if not suitable_items:
            logger.warning("No fallback items match criteria, returning safest options")
            safe_items = [
                item for item in self._fallback_menu_items
                if (item.spice_level == "low" and 
                    item.oil_level == "low" and
                    item.diet_type == "vegetarian")
            ]
            return safe_items[:3]  # Return up to 3 safest options
        
        return suitable_items[:5]  # Return up to 5 matching items
    
    def get_fallback_health_rule(
        self, 
        bmi_category: str = "normal",
        medical_condition: str = "none"
    ) -> Optional[HealthRule]:
        """
        Get fallback health rule based on criteria.
        
        Returns conservative health recommendations when database is unavailable.
        """
        logger.warning(
            f"Using fallback health rule for: "
            f"bmi={bmi_category}, condition={medical_condition}"
        )
        
        # Try to find exact match
        for rule in self._fallback_health_rules:
            if (rule.bmi_category == bmi_category and 
                rule.medical_condition == medical_condition):
                return rule
        
        # Try to find BMI category match with "none" condition
        for rule in self._fallback_health_rules:
            if (rule.bmi_category == bmi_category and 
                rule.medical_condition == "none"):
                return rule
        
        # Try to find "normal" BMI with matching condition
        for rule in self._fallback_health_rules:
            if (rule.bmi_category == "normal" and 
                rule.medical_condition == medical_condition):
                return rule
        
        # Return the most conservative rule
        for rule in self._fallback_health_rules:
            if (rule.bmi_category == "obese" and 
                rule.medical_condition == "none"):
                return rule
        
        # Last resort - return first rule
        return self._fallback_health_rules[0] if self._fallback_health_rules else None
    
    def get_fallback_user_response(self, phone_number: str) -> Optional[Dict[str, Any]]:
        """
        Get fallback user response when user service is unavailable.
        
        Returns None to indicate user not found, forcing registration.
        """
        logger.warning(f"User service unavailable for phone: {phone_number}")
        return None
    
    def get_fallback_guest_session(self, session_id: str) -> bool:
        """
        Get fallback guest session validation when session service is unavailable.
        
        Returns False to force new session creation.
        """
        logger.warning(f"Guest session service unavailable for session: {session_id}")
        return False
    
    def get_fallback_suggestion_response(
        self,
        bmi_category: str = "normal",
        medical_condition: str = "none",
        health_goal: str = "maintain_weight",
        diet_type: str = "vegetarian",
        spice_tolerance: str = "medium"
    ) -> Dict[str, Any]:
        """
        Get fallback suggestion response when recommendation engine is unavailable.
        
        Returns safe, conservative recommendations.
        """
        logger.warning(
            f"Using fallback suggestion for: "
            f"bmi={bmi_category}, condition={medical_condition}, "
            f"goal={health_goal}, diet={diet_type}, spice={spice_tolerance}"
        )
        
        # Get fallback menu items
        fallback_items = self.get_fallback_menu_items(
            bmi_category, medical_condition, diet_type, spice_tolerance
        )
        
        # Get fallback health rule
        fallback_rule = self.get_fallback_health_rule(bmi_category, medical_condition)
        
        # Build response
        response = {
            "recommendations": [
                {
                    "item_id": item.item_id,
                    "item_name": item.item_name,
                    "calories": item.calories,
                    "spice_level": item.spice_level,
                    "oil_level": item.oil_level,
                    "diet_type": item.diet_type,
                    "recommendation_reason": "Safe option based on your health profile",
                    "health_benefits": "Nutritious and suitable for your condition",
                    "fallback_mode": True
                }
                for item in fallback_items[:3]  # Return top 3
            ],
            "health_rule": {
                "rule_id": fallback_rule.rule_id if fallback_rule else "fallback",
                "bmi_category": bmi_category,
                "medical_condition": medical_condition,
                "allowed_items": fallback_rule.allowed_items if fallback_rule else ["prefer_balanced"],
                "fallback_mode": True
            },
            "user_profile": {
                "bmi_category": bmi_category,
                "medical_condition": medical_condition,
                "health_goal": health_goal,
                "diet_type": diet_type,
                "spice_tolerance": spice_tolerance
            },
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "fallback_mode": True,
                "message": "Showing recommendations from fallback data due to service unavailability"
            }
        }
        
        return response
    
    def get_service_status_message(self, service_name: str) -> Dict[str, Any]:
        """
        Get standardized service unavailable message.
        """
        return {
            "error": f"{service_name} service is currently unavailable",
            "message": "We're experiencing technical difficulties. Please try again later.",
            "fallback_active": True,
            "timestamp": datetime.utcnow().isoformat(),
            "retry_after": 30  # Suggest retry after 30 seconds
        }


# Global fallback service instance
_fallback_service: Optional[FallbackService] = None


def get_fallback_service() -> FallbackService:
    """Get or create global fallback service instance."""
    global _fallback_service
    if _fallback_service is None:
        _fallback_service = FallbackService()
    return _fallback_service
