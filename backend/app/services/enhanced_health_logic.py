"""
Enhanced Health Logic Service with Graceful Degradation.

Integrates caching and fallback mechanisms for resilient food recommendations.
"""

import asyncio
import logging
from typing import Optional

from app.models.admin_models import MenuItem, HealthRule
from app.services.dynamodb import DynamoDBClient
from app.services.cache_service import cache_get, cache_set, cache_key
from app.services.fallback_service import get_fallback_service
from app.utils.exceptions import ServiceUnavailableException
from app.core.config import settings

logger = logging.getLogger(__name__)


class HealthLogicService:
    """
    Enhanced health logic service with caching and graceful degradation.
    
    Provides intelligent food recommendations with multiple layers of fallback:
    1. Primary: DynamoDB with caching
    2. Secondary: Fallback service with safe defaults
    3. Tertiary: Emergency mode with minimal functionality
    """
    
    def __init__(self, db: DynamoDBClient):
        self.db = db
        self.fallback_service = get_fallback_service()
    
    async def suggest_item(
        self,
        bmi: float,
        bmi_category: str,
        medical_condition: str,
        health_goal: str,
        diet_type: str,
        spice_tolerance: Optional[str] = None,
        age: int = 25,
        weight_kg: float = 70.0,
        height_cm: float = 170.0
    ) -> dict:
        """
        Main suggestion engine with graceful degradation.
        
        Priority:
        1. Medical condition
        2. BMI category  
        3. Health goal
        
        Includes caching and fallback mechanisms.
        """
        
        # Use default spice tolerance if not provided
        if not spice_tolerance:
            spice_tolerance = "medium"
        
        # Try cache first for the complete suggestion
        cache_key_str = cache_key(
            "suggestion", bmi_category, medical_condition, health_goal,
            diet_type, spice_tolerance, age, weight_kg, height_cm
        )
        
        cached_suggestion = await cache_get(cache_key_str, "suggestions")
        if cached_suggestion:
            logger.debug(f"Cache hit for suggestion: {cache_key_str}")
            return cached_suggestion
        
        try:
            # Primary path: Get matching menu items from DynamoDB with timeout
            try:
                matching_items = await asyncio.wait_for(
                    self.db.get_menu_items_by_criteria(
                        bmi_category=bmi_category,
                        medical_condition=medical_condition,
                        diet_type=diet_type,
                        spice_tolerance=spice_tolerance
                    ),
                    timeout=3.0  # 3 second timeout for database query
                )
            except asyncio.TimeoutError:
                logger.warning("Database query timeout, using fallback service")
                raise ServiceUnavailableException("Database timeout")
            
            # Get health rule for additional filtering with timeout
            try:
                health_rule = await asyncio.wait_for(
                    self.db.get_health_rule(bmi_category, medical_condition),
                    timeout=2.0  # 2 second timeout for health rule
                )
            except asyncio.TimeoutError:
                logger.warning("Health rule query timeout, using default")
                health_rule = None
            
            # Build response
            suggestion_response = self._build_suggestion_response(
                matching_items=matching_items,
                health_rule=health_rule,
                bmi_category=bmi_category,
                medical_condition=medical_condition,
                health_goal=health_goal,
                diet_type=diet_type,
                spice_tolerance=spice_tolerance,
                bmi=bmi,
                age=age,
                weight_kg=weight_kg,
                height_cm=height_cm,
                fallback_mode=False
            )
            
            # Cache the successful response
            await cache_set(cache_key_str, suggestion_response, ttl=1200, prefix="suggestions")  # 20 min
            
            return suggestion_response
            
        except (ServiceUnavailableException, Exception) as e:
            logger.warning(f"Primary suggestion service failed: {e}. Using fallback service.")
            
            # Fallback path: Use fallback service
            try:
                fallback_items = self.fallback_service.get_fallback_menu_items(
                    bmi_category=bmi_category,
                    medical_condition=medical_condition,
                    diet_type=diet_type,
                    spice_tolerance=spice_tolerance
                )
                
                fallback_rule = self.fallback_service.get_fallback_health_rule(
                    bmi_category=bmi_category,
                    medical_condition=medical_condition
                )
                
                # Build fallback response
                suggestion_response = self._build_suggestion_response(
                    matching_items=fallback_items,
                    health_rule=fallback_rule,
                    bmi_category=bmi_category,
                    medical_condition=medical_condition,
                    health_goal=health_goal,
                    diet_type=diet_type,
                    spice_tolerance=spice_tolerance,
                    bmi=bmi,
                    age=age,
                    weight_kg=weight_kg,
                    height_cm=height_cm,
                    fallback_mode=True
                )
                
                # Cache fallback response for shorter time
                await cache_set(cache_key_str, suggestion_response, ttl=300, prefix="suggestions")  # 5 min
                
                return suggestion_response
                
            except Exception as fallback_error:
                logger.error(f"Both primary and fallback services failed: {fallback_error}")
                
                # Emergency mode: Return minimal safe response
                return self._build_emergency_response(
                    bmi_category=bmi_category,
                    medical_condition=medical_condition,
                    diet_type=diet_type,
                    spice_tolerance=spice_tolerance
                )
    
    def _build_suggestion_response(
        self,
        matching_items: list,
        health_rule: Optional[HealthRule],
        bmi_category: str,
        medical_condition: str,
        health_goal: str,
        diet_type: str,
        spice_tolerance: str,
        bmi: float,
        age: int,
        weight_kg: float,
        height_cm: float,
        fallback_mode: bool = False
    ) -> dict:
        """Build comprehensive suggestion response."""
        
        # Apply additional filtering based on health rule if available
        if health_rule:
            matching_items = self._filter_by_health_rule(matching_items, health_rule)
        
        # Sort by health score (calories, spice level, etc.)
        sorted_items = self._sort_by_health_score(matching_items, health_goal)
        
        # Build recommendations
        recommendations = []
        for item in sorted_items[:5]:  # Top 5 recommendations
            recommendation = {
                "item_id": item.item_id,
                "item_name": item.item_name,
                "calories": item.calories,
                "spice_level": item.spice_level,
                "oil_level": item.oil_level,
                "diet_type": item.diet_type,
                "image_url": item.image_url,
                "recommendation_reason": self._get_recommendation_reason(item, bmi_category, medical_condition),
                "health_benefits": self._get_health_benefits(item, health_goal),
                "health_score": self._calculate_health_score(item, health_goal, medical_condition)
            }
            
            if fallback_mode:
                recommendation["fallback_mode"] = True
                recommendation["message"] = "Safe recommendation from fallback data"
            
            recommendations.append(recommendation)
        
        # Build response matching SuggestionResponse model
        if recommendations:
            top_item = recommendations[0]
            response = {
                "health_summary": f"Your BMI is {round(bmi, 1)} ({bmi_category}). {medical_condition} considerations applied.",
                "bmi_category": bmi_category,
                "suggested_item": top_item["item_name"],
                "suggested_item_details": {
                    "item_id": top_item["item_id"],
                    "item_name": top_item["item_name"],
                    "calories": top_item["calories"],
                    "spice_level": top_item["spice_level"],
                    "oil_level": top_item["oil_level"],
                    "diet_type": top_item["diet_type"],
                    "image_url": top_item["image_url"],
                    "suitable_for": {"bmi_categories": [bmi_category], "medical_conditions": [medical_condition]}
                },
                "similar_items": [
                    {
                        "item_id": rec["item_id"],
                        "item_name": rec["item_name"],
                        "calories": rec["calories"],
                        "spice_level": rec["spice_level"],
                        "oil_level": rec["oil_level"],
                        "diet_type": rec["diet_type"],
                        "image_url": rec["image_url"],
                        "suitable_for": {"bmi_categories": [bmi_category], "medical_conditions": [medical_condition]}
                    } for rec in recommendations[1:4]
                ],
                "reason": top_item["recommendation_reason"]
            }
        else:
            # Emergency fallback
            response = {
                "health_summary": f"Your BMI is {round(bmi, 1)} ({bmi_category}). Using safe recommendation.",
                "bmi_category": bmi_category,
                "suggested_item": "Plain Idli",
                "suggested_item_details": None,
                "similar_items": [],
                "reason": "Safe, low-calorie option suitable for your health profile."
            }
        
        return response
    
    def _build_emergency_response(
        self,
        bmi_category: str,
        medical_condition: str,
        diet_type: str,
        spice_tolerance: str
    ) -> dict:
        """Build minimal emergency response when all services fail."""
        
        logger.error("All services failed, returning emergency response")
        
        emergency_items = [
            {
                "item_id": "emergency_plain_idli",
                "item_name": "Plain Idli (Safe Option)",
                "calories": 58,
                "spice_level": "low",
                "oil_level": "low",
                "diet_type": "vegetarian",
                "recommendation_reason": "Safest option - low calories, low spice, low oil",
                "health_benefits": "Easy to digest, suitable for all conditions",
                "health_score": 9.0,
                "emergency_mode": True
            }
        ]
        
        return {
            "recommendations": emergency_items,
            "user_profile": {
                "bmi_category": bmi_category,
                "medical_condition": medical_condition,
                "diet_type": diet_type,
                "spice_tolerance": spice_tolerance
            },
            "metadata": {
                "total_items_found": 1,
                "items_returned": 1,
                "emergency_mode": True,
                "message": "Emergency mode: Showing safest option only. All services are unavailable."
            }
        }
    
    def _filter_by_health_rule(self, items: list, health_rule: HealthRule) -> list:
        """Filter items based on maximum probability health rule."""
        if not health_rule or not health_rule.allowed_items:
            return items
        
        filtered_items = []
        allowed_item_names = health_rule.allowed_items
        
        for item in items:
            # Check if item name is in the allowed items list
            if item.item_name in allowed_item_names:
                filtered_items.append(item)
        
        # If no items match the rule, return top 3 safest items as fallback
        if not filtered_items:
            logger.warning(f"No items match health rule {health_rule.rule_id}, using safest fallback")
            # Return safest items (low calorie, low oil, low spice)
            safest_items = [
                item for item in items 
                if (item.calories < 150 and 
                    item.oil_level == 'low' and 
                    item.spice_level == 'low')
            ]
            return safest_items[:3] if safest_items else items[:3]
        
        logger.info(f"Health rule {health_rule.rule_id} matched {len(filtered_items)} items")
        return filtered_items
    
    def _sort_by_health_score(self, items: list, health_goal: str) -> list:
        """Sort items by health score based on health goal."""
        
        def calculate_score(item: MenuItem) -> float:
            score = 10.0  # Base score
            
            # Adjust based on calories
            if health_goal == "lose_weight":
                if item.calories < 100:
                    score += 2.0
                elif item.calories < 200:
                    score += 1.0
                elif item.calories > 300:
                    score -= 2.0
            elif health_goal == "gain_weight":
                if item.calories > 250:
                    score += 2.0
                elif item.calories > 200:
                    score += 1.0
                elif item.calories < 100:
                    score -= 1.0
            
            # Adjust based on spice level
            if item.spice_level == "low":
                score += 0.5
            elif item.spice_level == "high":
                score -= 0.5
            
            # Adjust based on oil level
            if item.oil_level == "low":
                score += 0.5
            elif item.oil_level == "high":
                score -= 0.5
            
            # Adjust based on diet type
            if item.diet_type == "vegetarian":
                score += 0.3
            
            return score
        
        return sorted(items, key=calculate_score, reverse=True)
    
    def _get_recommendation_reason(self, item: MenuItem, bmi_category: str, medical_condition: str) -> str:
        """Generate recommendation reason for item."""
        reasons = []
        
        if item.calories < 150:
            reasons.append("low calorie")
        if item.spice_level == "low":
            reasons.append("mild spice")
        if item.oil_level == "low":
            reasons.append("low oil")
        
        if medical_condition == "diabetes" and item.calories < 200:
            reasons.append("suitable for diabetes")
        elif medical_condition == "bp" and item.oil_level == "low":
            reasons.append("heart-friendly")
        elif medical_condition == "acidity" and item.spice_level == "low":
            reasons.append("easy on stomach")
        
        if not reasons:
            reasons.append("balanced nutrition")
        
        # Create a more natural sentence
        if len(reasons) > 1:
            reason_text = ", ".join(reasons[:-1]) + " and " + reasons[-1]
        else:
            reason_text = reasons[0]
            
        return f"Excellent choice for you due to its {reason_text}."
    
    def _get_health_benefits(self, item: MenuItem, health_goal: str) -> str:
        """Get health benefits for item."""
        benefits = []
        
        if item.calories < 150:
            benefits.append("helps maintain weight")
        if item.spice_level == "low":
            benefits.append("gentle on digestion")
        if item.oil_level == "low":
            benefits.append("heart-healthy")
        
        if health_goal == "lose_weight":
            benefits.append("supports weight loss")
        elif health_goal == "gain_weight":
            if item.calories > 200:
                benefits.append("provides energy")
        
        return ", ".join(benefits) if benefits else "nutritious and balanced"
    
    def _calculate_health_score(self, item: MenuItem, health_goal: str, medical_condition: str = "none") -> float:
        """Calculate health score for item based on goal and medical condition."""
        score = 7.0  # Base score
        
        # Calories scoring
        if health_goal == "lose_weight":
            if item.calories < 100:
                score += 2.0
            elif item.calories < 200:
                score += 1.0
            elif item.calories > 300:
                score -= 1.0
        elif health_goal == "gain_weight":
            if item.calories > 250:
                score += 1.5
            elif item.calories < 100:
                score -= 0.5
        
        # Spice level scoring
        if item.spice_level == "low":
            score += 0.5
        elif item.spice_level == "high":
            score -= 0.3
            if medical_condition == "acidity":
                score -= 2.0  # Heavy penalty for acidity
        
        # Oil level scoring
        if item.oil_level == "low":
            score += 0.5
            if medical_condition == "bp":
                score += 1.0  # Bonus for heart patients
        elif item.oil_level == "high":
            score -= 0.3
            if medical_condition in ["bp", "diabetes"]:
                score -= 1.5  # Heavy penalty
        
        # Diabetes specific
        if medical_condition == "diabetes":
            if item.diet_type == "high_fiber": # Assuming this might exist or just low calorie
                score += 1.0
            if item.calories > 250:
                score -= 1.0
        
        return min(10.0, max(0.0, score))
