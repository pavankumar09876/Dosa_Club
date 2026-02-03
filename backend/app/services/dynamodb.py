"""
DynamoDB Async Service.

Async database operations for DosaClub using aioboto3.
All operations are non-blocking and support concurrent requests.

Enhanced with circuit breakers, retry logic, and resilience patterns.
"""
 
import aioboto3
import uuid
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from botocore.exceptions import ClientError, BotoCoreError

from app.models.admin_models import MenuItem, HealthRule
from app.models.user_models import UserResponse
from app.services.decorators import safe_read, safe_write, safe_batch, safe_critical, fallback_on_failure
from app.services.cache_service import cache_get, cache_set, cache_delete, cache_key
from app.services.fallback_service import get_fallback_service
from app.utils.exceptions import DynamoDBException, DynamoDBTimeoutException, DynamoDBThrottlingException, ServiceUnavailableException

logger = logging.getLogger(__name__)


class DynamoDBClient:
    """Async DynamoDB client for all database operations"""
    
    def __init__(self, region_name: str = "us-east-1", 
                 aws_access_key_id: Optional[str] = None,
                 aws_secret_access_key: Optional[str] = None,
                 aws_session_token: Optional[str] = None,
                 endpoint_url: Optional[str] = None):
        self.session = aioboto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region_name
        )
        self.region_name = region_name
        self.endpoint_url = endpoint_url
    
    def _handle_dynamodb_error(self, error: Exception, operation: str, table_name: Optional[str] = None):
        """Handle DynamoDB errors and convert to appropriate exceptions."""
        if isinstance(error, ClientError):
            error_code = error.response['Error']['Code']
            error_message = error.response['Error']['Message']
            
            logger.error(f"DynamoDB {operation} error on {table_name}: {error_code} - {error_message}")
            
            # Convert to specific exceptions based on error code
            if error_code in ['ProvisionedThroughputExceededException', 'ThrottlingException']:
                raise DynamoDBThrottlingException(
                    f"DynamoDB throttling during {operation}: {error_message}",
                    operation=operation,
                    table_name=table_name,
                    aws_error_code=error_code
                )
            elif error_code in ['RequestTimeout', 'RequestTimeoutException']:
                raise DynamoDBTimeoutException(
                    f"DynamoDB timeout during {operation}: {error_message}",
                    operation=operation,
                    table_name=table_name,
                    aws_error_code=error_code
                )
            else:
                raise DynamoDBException(
                    f"DynamoDB error during {operation}: {error_message}",
                    operation=operation,
                    table_name=table_name,
                    aws_error_code=error_code
                )
        else:
            logger.error(f"Unexpected error during DynamoDB {operation}: {error}")
            raise DynamoDBException(
                f"Unexpected error during {operation}: {str(error)}",
                operation=operation,
                table_name=table_name
            )
    
    async def _execute_with_client(self, operation: str, func, *args, **kwargs):
        """Execute DynamoDB operation with error handling."""
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            self._handle_dynamodb_error(e, operation, kwargs.get('TableName'))
    
    @safe_write(max_attempts=5, base_delay=1.0, timeout=15.0)
    async def create_or_update_menu_item(self, item_data: Dict[str, Any]) -> str:
        """Create or update a menu item in the menu_items table"""
        
        async with self.session.client(
            "dynamodb", 
            region_name=self.region_name,
            endpoint_url=self.endpoint_url
        ) as dynamodb:
            # Check if item exists by name
            response = await dynamodb.scan(
                TableName="menu_items",
                FilterExpression="item_name = :name",
                ExpressionAttributeValues={":name": {"S": item_data["item_name"]}}
            )
            existing_items = response.get("Items", [])
            
            if existing_items:
                # Update existing item
                existing_item = existing_items[0]
                item_id = existing_item["item_id"]["S"]
                
                # Convert suitable_for to DynamoDB format
                suitable_for = item_data.get("suitable_for", {})
                bmi_categories = suitable_for.get("bmi_categories", [])
                medical_conditions = suitable_for.get("medical_conditions", [])
                
                await self._execute_with_client(
                    "update_menu_item",
                    dynamodb.update_item,
                    TableName="menu_items",
                    Key={"item_id": {"S": item_id}},
                    UpdateExpression="SET item_name = :name, calories = :cal, spice_level = :spice, oil_level = :oil, diet_type = :diet, image_url = :img, suitable_for = :suitable",
                    ExpressionAttributeValues={
                        ":name": {"S": item_data["item_name"]},
                        ":cal": {"N": str(item_data["calories"])},
                        ":spice": {"S": item_data["spice_level"]},
                        ":oil": {"S": item_data["oil_level"]},
                        ":diet": {"S": item_data["diet_type"]},
                        ":img": {"S": item_data.get("image_url", "")},
                        ":suitable": {
                            "M": {
                                "bmi_categories": {"L": [{"S": cat} for cat in bmi_categories]},
                                "medical_conditions": {"L": [{"S": cond} for cond in medical_conditions]}
                            }
                        }
                    }
                )
            else:
                # Create new item
                item_id = str(uuid.uuid4())
                
                # Convert suitable_for to DynamoDB format
                suitable_for = item_data.get("suitable_for", {})
                bmi_categories = suitable_for.get("bmi_categories", [])
                medical_conditions = suitable_for.get("medical_conditions", [])
                
                await self._execute_with_client(
                    "create_menu_item",
                    dynamodb.put_item,
                    TableName="menu_items",
                    Item={
                        "item_id": {"S": item_id},
                        "item_name": {"S": item_data["item_name"]},
                        "calories": {"N": str(item_data["calories"])},
                        "spice_level": {"S": item_data["spice_level"]},
                        "oil_level": {"S": item_data["oil_level"]},
                        "diet_type": {"S": item_data["diet_type"]},
                        "image_url": {"S": item_data.get("image_url", "")},
                        "suitable_for": {
                            "M": {
                                "bmi_categories": {"L": [{"S": cat} for cat in bmi_categories]},
                                "medical_conditions": {"L": [{"S": cond} for cond in medical_conditions]}
                            }
                        }
                    }
                )
        
        # Invalidate relevant caches
        await cache_delete(cache_key("menu_items_all"), "menu_items")
        
        return item_id

    @safe_write(max_attempts=5, base_delay=1.0, timeout=15.0)
    async def delete_menu_item(self, item_id: str) -> bool:
        """Delete a menu item from the menu_items table"""
        
        async with self.session.client(
            "dynamodb", 
            region_name=self.region_name,
            endpoint_url=self.endpoint_url
        ) as dynamodb:
            await self._execute_with_client(
                "delete_menu_item",
                dynamodb.delete_item,
                TableName="menu_items",
                Key={"item_id": {"S": item_id}}
            )
        
        # Invalidate relevant caches
        await cache_delete(cache_key("menu_items_all"), "menu_items")
        
        return True

    @safe_write(max_attempts=5, base_delay=1.0, timeout=15.0)
    async def create_user(self, user_data: Dict[str, Any]) -> str:
        """Create a new user in the users table"""
        user_id = str(uuid.uuid4())
        
        async with self.session.client(
            "dynamodb", 
            region_name=self.region_name,
            endpoint_url=self.endpoint_url
        ) as dynamodb:
            await self._execute_with_client(
                "create_user",
                dynamodb.put_item,
                TableName="users",
                Item={
                    "user_id": {"S": user_id},
                    "name": {"S": user_data["name"]},
                    "phone_number": {"S": user_data["phone_number"]},
                    "age": {"N": str(user_data["age"])},
                    "gender": {"S": user_data["gender"]},
                    "height_cm": {"N": str(user_data["height_cm"])},
                    "weight_kg": {"N": str(user_data["weight_kg"])},
                    "bmi": {"N": str(user_data["bmi"])},
                    "bmi_category": {"S": user_data["bmi_category"]},
                    "diet_type": {"S": user_data["diet_type"]},
                    "health_goal": {"S": user_data["health_goal"]},
                    "medical_condition": {"S": user_data["medical_condition"]},
                    "spice_tolerance": {"S": user_data["spice_tolerance"]},
                    "created_at": {"S": datetime.utcnow().isoformat()},
                }
            )
        
        # Invalidate cache for this user's phone number
        await cache_delete(cache_key("user_by_phone", user_data["phone_number"]), "users")
        
        return user_id

    @safe_read(max_attempts=3, base_delay=0.5, timeout=10.0)
    async def get_user_by_phone(self, phone_number: str) -> Optional[Dict[str, Any]]:
        """
        Get user profile by phone number.
        Returns the latest profile if multiple exist.
        """
        # Try cache first
        cache_key_str = cache_key("user_by_phone", phone_number)
        cached_user = await cache_get(cache_key_str, "users")
        if cached_user:
            logger.debug(f"Cache hit for user by phone: {phone_number}")
            return cached_user
        
        async with self.session.client(
            "dynamodb", 
            region_name=self.region_name,
            endpoint_url=self.endpoint_url
        ) as dynamodb:
            # Check if phone_number matches
            # Ideally this should be a GSI Query, but Scan is acceptable for MVP
            response = await self._execute_with_client(
                "get_user_by_phone",
                dynamodb.scan,
                TableName="users",
                FilterExpression="phone_number = :phone",
                ExpressionAttributeValues={":phone": {"S": phone_number}}
            )
            
            items = response.get("Items", [])
            if not items:
                return None
            
            # Convert DynamoDB items to Python dicts
            parsed_items = []
            for item in items:
                user_dict = {
                    "user_id": item.get("user_id", {}).get("S"),
                    "name": item.get("name", {}).get("S"),
                    "phone_number": item.get("phone_number", {}).get("S"),
                    "email": item.get("email", {}).get("S"),
                    "age": int(item.get("age", {}).get("N", 0)),
                    "gender": item.get("gender", {}).get("S"),
                    "height_cm": float(item.get("height_cm", {}).get("N", 0)),
                    "weight_kg": float(item.get("weight_kg", {}).get("N", 0)),
                    "bmi": float(item.get("bmi", {}).get("N", 0)),
                    "bmi_category": item.get("bmi_category", {}).get("S"),
                    "diet_type": item.get("diet_type", {}).get("S"),
                    "health_goal": item.get("health_goal", {}).get("S"),
                    "medical_condition": item.get("medical_condition", {}).get("S"),
                    "spice_tolerance": item.get("spice_tolerance", {}).get("S"),
                    "created_at": item.get("created_at", {}).get("S")
                }
                parsed_items.append(user_dict)
            
            # Sort by created_at descending to get latest
            parsed_items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            
            latest_user = parsed_items[0] if parsed_items else None
            
            # Cache the result for 10 minutes
            if latest_user:
                await cache_set(cache_key_str, latest_user, ttl=600, prefix="users")
            
            return latest_user
    
    async def calculate_bmi(self, height_cm: float, weight_kg: float) -> tuple[float, str]:
        """Calculate BMI and return category"""
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        if bmi < 18.5:
            category = "underweight"
        elif 18.5 <= bmi < 25:
            category = "normal"
        elif 25 <= bmi < 30:
            category = "overweight"
        else:
            category = "obese"
        
        return round(bmi, 2), category
    
    @safe_read(max_attempts=3, base_delay=0.5, timeout=10.0)
    async def get_health_rule(self, bmi_category: str, medical_condition: str) -> Optional[HealthRule]:
        """Get health rules for a given BMI category and medical condition"""
        # Try cache first
        cache_key_str = cache_key("health_rule", bmi_category, medical_condition)
        cached_rule = await cache_get(cache_key_str, "health_rules")
        if cached_rule:
            logger.debug(f"Cache hit for health rule: {bmi_category}_{medical_condition}")
            return HealthRule(**cached_rule)
        
        # Construct rule_id from bmi_category and medical_condition
        rule_id = f"{bmi_category}_{medical_condition}"
        
        async with self.session.client(
            "dynamodb", 
            region_name=self.region_name,
            endpoint_url=self.endpoint_url
        ) as dynamodb:
            response = await self._execute_with_client(
                "get_health_rule",
                dynamodb.get_item,
                TableName="health_rules",
                Key={
                    "rule_id": {"S": rule_id}
                }
            )
            
            if "Item" not in response:
                # Cache the negative result for shorter time
                await cache_set(cache_key_str, None, ttl=60, prefix="health_rules")
                return None
            
            item = response["Item"]
            health_rule = HealthRule(
                rule_id=item.get("rule_id", {}).get("S", ""),
                bmi_category=item.get("bmi_category", {}).get("S", ""),
                medical_condition=item.get("medical_condition", {}).get("S", ""),
                allowed_items=[s["S"] for s in item.get("allowed_items", {}).get("L", [])]
            )
            
            # Cache the result
            await cache_set(cache_key_str, health_rule.__dict__, ttl=1800, prefix="health_rules")  # 30 min
            
            return health_rule
    
    async def get_menu_item(self, item_id: str) -> Optional[MenuItem]:
        """Get a specific menu item"""
        async with self.session.client(
            "dynamodb", 
            region_name=self.region_name,
            endpoint_url=self.endpoint_url
        ) as dynamodb:
            response = await dynamodb.get_item(
                TableName="menu_items",
                Key={"item_id": {"S": item_id}}
            )
            
            if "Item" not in response:
                return None
            
            item = response["Item"]
            suitable_for = item.get("suitable_for", {}).get("M", {})
            
            return MenuItem(
                item_id=item.get("item_id", {}).get("S", ""),
                item_name=item.get("item_name", {}).get("S", ""),
                calories=int(item.get("calories", {}).get("N", 0)),
                spice_level=item.get("spice_level", {}).get("S", ""),
                oil_level=item.get("oil_level", {}).get("S", ""),
                diet_type=item.get("diet_type", {}).get("S", ""),
                image_url=item.get("image_url", {}).get("S"),
                suitable_for={
                    "bmi_categories": [s["S"] for s in suitable_for.get("bmi_categories", {}).get("L", [])],
                    "medical_conditions": [s["S"] for s in suitable_for.get("medical_conditions", {}).get("L", [])]
                }
            )
    

    async def add_favorite(self, phone_number: str, item_id: str) -> str:
        """Add a favorite item for a user"""
        favorite_id = str(uuid.uuid4())

        # Get item name for response
        item = await self.get_menu_item(item_id)
        if not item:
            raise ValueError("Menu item not found")

        async with self.session.client(
            "dynamodb",
            region_name=self.region_name,
            endpoint_url=self.endpoint_url
        ) as dynamodb:
            await dynamodb.put_item(
                TableName="favorites",
                Item={
                    "favorite_id": {"S": favorite_id},
                    "phone_number": {"S": phone_number},
                    "item_id": {"S": item_id},
                    "item_name": {"S": item.item_name},
                    "added_at": {"S": datetime.utcnow().isoformat()},
                }
            )

        return favorite_id

    async def get_user_favorites(self, phone_number: str) -> List[Dict[str, Any]]:
        """Get favorite items for a user"""
        async with self.session.client(
            "dynamodb",
            region_name=self.region_name,
            endpoint_url=self.endpoint_url
        ) as dynamodb:
            response = await dynamodb.scan(
                TableName="favorites",
                FilterExpression="phone_number = :phone",
                ExpressionAttributeValues={":phone": {"S": phone_number}}
            )

            favorites = []
            for item in response.get("Items", []):
                favorites.append({
                    "favorite_id": item.get("favorite_id", {}).get("S", ""),
                    "phone_number": item.get("phone_number", {}).get("S", ""),
                    "item_id": item.get("item_id", {}).get("S", ""),
                    "item_name": item.get("item_name", {}).get("S", ""),
                    "added_at": item.get("added_at", {}).get("S", ""),
                })

            # Sort by added_at descending (most recent first)
            favorites.sort(key=lambda x: x.get("added_at", ""), reverse=True)

            return favorites

    async def remove_favorite(self, phone_number: str, item_id: str) -> bool:
        """Remove a favorite item for a user"""
        async with self.session.client(
            "dynamodb",
            region_name=self.region_name,
            endpoint_url=self.endpoint_url
        ) as dynamodb:
            # Find the favorite to delete
            response = await dynamodb.scan(
                TableName="favorites",
                FilterExpression="phone_number = :phone AND item_id = :item",
                ExpressionAttributeValues={
                    ":phone": {"S": phone_number},
                    ":item": {"S": item_id}
                }
            )

            items = response.get("Items", [])
            if not items:
                return False

            # Delete the favorite
            await dynamodb.delete_item(
                TableName="favorites",
                Key={
                    "favorite_id": {"S": items[0].get("favorite_id", {}).get("S", "")}
                }
            )

        return True

    @safe_write(max_attempts=3, base_delay=0.5, timeout=10.0)
    async def create_guest_session(self) -> Dict[str, Any]:
        """Create a new guest session with 30-minute expiry"""
        session_id = f"guest_session_{uuid.uuid4().hex[:12]}"
        expires_at = datetime.utcnow() + timedelta(minutes=30)
        
        async with self.session.client(
            "dynamodb", 
            region_name=self.region_name,
            endpoint_url=self.endpoint_url
        ) as dynamodb:
            await dynamodb.put_item(
                TableName="guest_sessions",
                Item={
                    "session_id": {"S": session_id},
                    "created_at": {"S": datetime.utcnow().isoformat()},
                    "expires_at": {"S": expires_at.isoformat()},
                    "is_active": {"BOOL": True}
                }
            )
        
        return {
            "session_id": session_id,
            "expires_at": expires_at
        }

    @safe_read(max_attempts=2, base_delay=0.2, timeout=5.0)
    async def validate_guest_session(self, session_id: str) -> bool:
        """Validate if guest session exists and is not expired"""
        try:
            async with self.session.client(
                "dynamodb", 
                region_name=self.region_name,
                endpoint_url=self.endpoint_url
            ) as dynamodb:
                response = await dynamodb.get_item(
                    TableName="guest_sessions",
                    Key={"session_id": {"S": session_id}}
                )
                
                if "Item" not in response:
                    return False
                
                item = response["Item"]
                expires_at = datetime.fromisoformat(item["expires_at"]["S"])
                is_active = item.get("is_active", {"BOOL": True})["BOOL"]
                
                return datetime.utcnow() < expires_at and is_active
                
        except Exception:
            return False

    @safe_critical(max_attempts=7, base_delay=0.1, timeout=5.0)
    async def get_menu_items_by_criteria(self, bmi_category: str, medical_condition: str, diet_type: str, spice_tolerance: str) -> List[MenuItem]:
        """Get menu items that match specific health criteria"""
        # Try cache first
        cache_key_str = cache_key("menu_items_criteria", bmi_category, medical_condition, diet_type, spice_tolerance)
        cached_items = await cache_get(cache_key_str, "menu_items")
        if cached_items:
            logger.debug(f"Cache hit for menu items criteria: {cache_key_str}")
            return [MenuItem(**item) for item in cached_items]
        
        async with self.session.client(
            "dynamodb", 
            region_name=self.region_name,
            endpoint_url=self.endpoint_url
        ) as dynamodb:
            # Scan for items matching diet type first
            response = await self._execute_with_client(
                "get_menu_items_by_criteria",
                dynamodb.scan,
                TableName="menu_items",
                FilterExpression="diet_type = :diet",
                ExpressionAttributeValues={":diet": {"S": diet_type}}
            )
            
            matching_items = []
            for item in response.get("Items", []):
                # Parse suitable_for data
                suitable_for = item.get("suitable_for", {}).get("M", {})
                bmi_categories = [s["S"] for s in suitable_for.get("bmi_categories", {}).get("L", [])]
                medical_conditions = [s["S"] for s in suitable_for.get("medical_conditions", {}).get("L", [])]
                
                # Check if item matches criteria
                bmi_match = not bmi_categories or bmi_category in bmi_categories
                medical_match = not medical_conditions or medical_condition in medical_conditions or "none" in medical_conditions
                spice_match = item.get("spice_level", {}).get("S", "") == spice_tolerance or spice_tolerance == "high"
                
                if bmi_match and medical_match and spice_match:
                    matching_items.append(MenuItem(
                        item_id=item.get("item_id", {}).get("S", ""),
                        item_name=item.get("item_name", {}).get("S", ""),
                        calories=int(item.get("calories", {}).get("N", 0)),
                        spice_level=item.get("spice_level", {}).get("S", ""),
                        oil_level=item.get("oil_level", {}).get("S", ""),
                        diet_type=item.get("diet_type", {}).get("S", ""),
                        image_url=item.get("image_url", {}).get("S"),
                        suitable_for={
                            "bmi_categories": bmi_categories,
                            "medical_conditions": medical_conditions
                        }
                    ))
            
            # Cache the result
            items_dict = [item.__dict__ for item in matching_items]
            await cache_set(cache_key_str, items_dict, ttl=900, prefix="menu_items")  # 15 min
            
            return matching_items

    @safe_read(max_attempts=3, base_delay=0.5, timeout=10.0)
    async def get_menu_items_by_diet_type(self, diet_type: str) -> List[MenuItem]:
        """Get menu items by diet type (fallback method)"""
        async with self.session.client(
            "dynamodb", 
            region_name=self.region_name,
            endpoint_url=self.endpoint_url
        ) as dynamodb:
            response = await dynamodb.scan(
                TableName="menu_items",
                FilterExpression="diet_type = :diet",
                ExpressionAttributeValues={":diet": {"S": diet_type}}
            )
            
            items = []
            for item in response.get("Items", []):
                suitable_for = item.get("suitable_for", {}).get("M", {})
                items.append(MenuItem(
                    item_id=item.get("item_id", {}).get("S", ""),
                    item_name=item.get("item_name", {}).get("S", ""),
                    calories=int(item.get("calories", {}).get("N", 0)),
                    spice_level=item.get("spice_level", {}).get("S", ""),
                    oil_level=item.get("oil_level", {}).get("S", ""),
                    diet_type=item.get("diet_type", {}).get("S", ""),
                    image_url=item.get("image_url", {}).get("S"),
                    suitable_for={
                        "bmi_categories": [s["S"] for s in suitable_for.get("bmi_categories", {}).get("L", [])],
                        "medical_conditions": [s["S"] for s in suitable_for.get("medical_conditions", {}).get("L", [])]
                    }
                ))
            
            return items

    async def cleanup_expired_sessions(self) -> int:
        """Clean up expired guest sessions (returns count of cleaned sessions)"""
        cleaned_count = 0
        
        async with self.session.client(
            "dynamodb", 
            region_name=self.region_name,
            endpoint_url=self.endpoint_url
        ) as dynamodb:
            # Scan for expired sessions
            response = await dynamodb.scan(
                TableName="guest_sessions",
                FilterExpression="expires_at < :now OR attribute_not_exists(is_active) OR is_active = :false",
                ExpressionAttributeValues={
                    ":now": {"S": datetime.utcnow().isoformat()},
                    ":false": {"BOOL": False}
                }
            )
            
            # Delete expired sessions
            for item in response.get("Items", []):
                await dynamodb.delete_item(
                    TableName="guest_sessions",
                    Key={"session_id": {"S": item["session_id"]["S"]}}
                )
                cleaned_count += 1
        
        return cleaned_count

    @safe_read(max_attempts=3, base_delay=0.5, timeout=10.0)
    async def list_users(self) -> List[UserResponse]:
        """List all users from the users table"""
        async with self.session.client(
            "dynamodb", 
            region_name=self.region_name,
            endpoint_url=self.endpoint_url
        ) as dynamodb:
            response = await self._execute_with_client(
                "list_users",
                dynamodb.scan,
                TableName="users"
            )
            
            users = []
            for item in response.get("Items", []):
                users.append(UserResponse(
                    user_id=item.get("user_id", {}).get("S", ""),
                    name=item.get("name", {}).get("S", ""),
                    phone_number=item.get("phone_number", {}).get("S", ""),
                    email=item.get("email", {}).get("S", ""),
                    age=int(item.get("age", {}).get("N", 0)),
                    gender=item.get("gender", {}).get("S", ""),
                    height_cm=float(item.get("height_cm", {}).get("N", 0)),
                    weight_kg=float(item.get("weight_kg", {}).get("N", 0)),
                    bmi=float(item.get("bmi", {}).get("N", 0)),
                    bmi_category=item.get("bmi_category", {}).get("S", ""),
                    diet_type=item.get("diet_type", {}).get("S", ""),
                    health_goal=item.get("health_goal", {}).get("S", ""),
                    medical_condition=item.get("medical_condition", {}).get("S", ""),
                    spice_tolerance=item.get("spice_tolerance", {}).get("S", ""),
                    created_at=item.get("created_at", {}).get("S", "")
                ))
            
            return users



