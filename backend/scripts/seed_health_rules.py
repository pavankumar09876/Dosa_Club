"""
Enhanced Health Rules Seeder with Maximum Probability Matching.

Creates health rules based on actual menu items for better matching.
Uses specific item IDs instead of generic preferences for higher accuracy.
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load .env file from backend root explicitly
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

import aioboto3
from app.core.config import settings
from datetime import datetime
from seed_data import MENU_ITEMS


def print_banner():
    print("=" * 80)
    print("DOSA CLUB - ENHANCED HEALTH RULES SEEDER")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"DynamoDB Endpoint: {settings.dynamodb_endpoint or 'AWS (Real Service)'}")
    print("-" * 80)


def analyze_menu_items():
    """Analyze menu items to create probability-based health rules."""
    
    # Categorize items by health properties
    low_calorie_items = []
    medium_calorie_items = []
    high_calorie_items = []
    
    low_oil_items = []
    medium_oil_items = []
    high_oil_items = []
    
    low_spice_items = []
    medium_spice_items = []
    high_spice_items = []
    
    diabetic_friendly = []
    bp_friendly = []
    acidity_friendly = []
    
    for item in MENU_ITEMS:
        calories = item['calories']
        spice = item['spice_level']
        oil = item['oil_level']
        name = item['item_name']
        
        # Calorie categorization
        if calories < 150:
            low_calorie_items.append(name)
        elif calories < 250:
            medium_calorie_items.append(name)
        else:
            high_calorie_items.append(name)
        
        # Oil categorization
        if oil == 'low':
            low_oil_items.append(name)
        elif oil == 'medium':
            medium_oil_items.append(name)
        else:
            high_oil_items.append(name)
        
        # Spice categorization
        if spice == 'low':
            low_spice_items.append(name)
        elif spice == 'medium':
            medium_spice_items.append(name)
        else:
            high_spice_items.append(name)
        
        # Medical condition categorization
        suitable_conditions = item['suitable_for']['medical_conditions']
        
        if 'diabetes' in suitable_conditions and calories < 200:
            diabetic_friendly.append(name)
        
        if 'bp' in suitable_conditions and oil == 'low':
            bp_friendly.append(name)
        
        if 'acidity' in suitable_conditions and spice in ['low', 'medium']:
            acidity_friendly.append(name)
    
    return {
        'low_calorie': low_calorie_items,
        'medium_calorie': medium_calorie_items,
        'high_calorie': high_calorie_items,
        'low_oil': low_oil_items,
        'medium_oil': medium_oil_items,
        'high_oil': high_oil_items,
        'low_spice': low_spice_items,
        'medium_spice': medium_spice_items,
        'high_spice': high_spice_items,
        'diabetic_friendly': diabetic_friendly,
        'bp_friendly': bp_friendly,
        'acidity_friendly': acidity_friendly
    }


def create_max_probability_health_rules(categories):
    """Create health rules with maximum probability matching."""
    
    health_rules = []
    
    # Normal BMI + No condition - Maximum variety
    health_rules.append({
        "rule_id": "normal_none_max",
        "bmi_category": "normal",
        "medical_condition": "none",
        "allowed_items": categories['medium_calorie'][:15],  # Top 15 medium calorie items
        "description": "Maximum variety: balanced calorie items for healthy individuals",
        "priority": 1
    })
    
    # Normal BMI + Diabetes - Focus on low calorie, low sugar items
    diabetic_items = [item for item in categories['diabetic_friendly'] if item in categories['low_calorie']]
    health_rules.append({
        "rule_id": "normal_diabetes_max",
        "bmi_category": "normal",
        "medical_condition": "diabetes",
        "allowed_items": diabetic_items[:10] if diabetic_items else categories['low_calorie'][:10],
        "description": "Maximum probability: low calorie, diabetic-friendly items",
        "priority": 1
    })
    
    # Normal BMI + BP - Focus on low oil items
    health_rules.append({
        "rule_id": "normal_bp_max",
        "bmi_category": "normal",
        "medical_condition": "bp",
        "allowed_items": categories['bp_friendly'][:12] if categories['bp_friendly'] else categories['low_oil'][:12],
        "description": "Maximum probability: low oil, heart-friendly items",
        "priority": 1
    })
    
    # Normal BMI + Acidity - Focus on low spice items
    acidity_items = [item for item in categories['acidity_friendly'] if item in categories['low_spice']]
    health_rules.append({
        "rule_id": "normal_acidity_max",
        "bmi_category": "normal",
        "medical_condition": "acidity",
        "allowed_items": acidity_items[:10] if acidity_items else categories['low_spice'][:10],
        "description": "Maximum probability: low spice, mild items for acidity",
        "priority": 1
    })
    
    # Underweight + No condition - High calorie items
    health_rules.append({
        "rule_id": "underweight_none_max",
        "bmi_category": "underweight",
        "medical_condition": "none",
        "allowed_items": categories['high_calorie'][:15],
        "description": "Maximum probability: high calorie items for weight gain",
        "priority": 1
    })
    
    # Underweight + Diabetes - Balanced approach
    balanced_diabetic = [item for item in categories['diabetic_friendly'] if item in categories['medium_calorie']]
    health_rules.append({
        "rule_id": "underweight_diabetes_max",
        "bmi_category": "underweight",
        "medical_condition": "diabetes",
        "allowed_items": balanced_diabetic[:8] if balanced_diabetic else categories['medium_calorie'][:8],
        "description": "Maximum probability: balanced calories with diabetic safety",
        "priority": 1
    })
    
    # Underweight + BP - High calorie but low oil
    high_cal_low_oil = [item for item in categories['high_calorie'] if item in categories['low_oil']]
    health_rules.append({
        "rule_id": "underweight_bp_max",
        "bmi_category": "underweight",
        "medical_condition": "bp",
        "allowed_items": high_cal_low_oil[:8] if high_cal_low_oil else categories['medium_calorie'][:8],
        "description": "Maximum probability: high calorie, low oil for weight gain",
        "priority": 1
    })
    
    # Underweight + Acidity - High calorie, low spice
    high_cal_low_spice = [item for item in categories['high_calorie'] if item in categories['low_spice']]
    health_rules.append({
        "rule_id": "underweight_acidity_max",
        "bmi_category": "underweight",
        "medical_condition": "acidity",
        "allowed_items": high_cal_low_spice[:8] if high_cal_low_spice else categories['medium_calorie'][:8],
        "description": "Maximum probability: high calorie, low spice for weight gain",
        "priority": 1
    })
    
    # Overweight + No condition - Low calorie items
    health_rules.append({
        "rule_id": "overweight_none_max",
        "bmi_category": "overweight",
        "medical_condition": "none",
        "allowed_items": categories['low_calorie'][:15],
        "description": "Maximum probability: low calorie items for weight management",
        "priority": 1
    })
    
    # Overweight + Diabetes - Strict control
    strict_diabetic = [item for item in categories['diabetic_friendly'] if item in categories['low_calorie']]
    health_rules.append({
        "rule_id": "overweight_diabetes_max",
        "bmi_category": "overweight",
        "medical_condition": "diabetes",
        "allowed_items": strict_diabetic[:10] if strict_diabetic else categories['low_calorie'][:10],
        "description": "Maximum probability: very low calorie, diabetic-safe items",
        "priority": 1
    })
    
    # Overweight + BP - Low calorie and low oil
    low_cal_low_oil = [item for item in categories['low_calorie'] if item in categories['low_oil']]
    health_rules.append({
        "rule_id": "overweight_bp_max",
        "bmi_category": "overweight",
        "medical_condition": "bp",
        "allowed_items": low_cal_low_oil[:12] if low_cal_low_oil else categories['low_calorie'][:12],
        "description": "Maximum probability: low calorie, low oil for heart health",
        "priority": 1
    })
    
    # Overweight + Acidity - Low calorie and low spice
    low_cal_low_spice = [item for item in categories['low_calorie'] if item in categories['low_spice']]
    health_rules.append({
        "rule_id": "overweight_acidity_max",
        "bmi_category": "overweight",
        "medical_condition": "acidity",
        "allowed_items": low_cal_low_spice[:12] if low_cal_low_spice else categories['low_calorie'][:12],
        "description": "Maximum probability: low calorie, low spice for acidity",
        "priority": 1
    })
    
    # Obese + No condition - Very restricted
    very_low_cal = [item for item in categories['low_calorie'] if item in categories['low_oil']]
    health_rules.append({
        "rule_id": "obese_none_max",
        "bmi_category": "obese",
        "medical_condition": "none",
        "allowed_items": very_low_cal[:10] if very_low_cal else categories['low_calorie'][:10],
        "description": "Maximum probability: very low calorie, low oil items",
        "priority": 1
    })
    
    # Obese + Diabetes - Most restricted
    obese_diabetic = [item for item in categories['diabetic_friendly'] if item in categories['low_calorie'] and item in categories['low_oil']]
    health_rules.append({
        "rule_id": "obese_diabetes_max",
        "bmi_category": "obese",
        "medical_condition": "diabetes",
        "allowed_items": obese_diabetic[:8] if obese_diabetic else categories['low_calorie'][:8],
        "description": "Maximum probability: strictest diabetic control",
        "priority": 1
    })
    
    # Obese + BP - Very restricted
    obese_bp = [item for item in categories['bp_friendly'] if item in categories['low_calorie']]
    health_rules.append({
        "rule_id": "obese_bp_max",
        "bmi_category": "obese",
        "medical_condition": "bp",
        "allowed_items": obese_bp[:8] if obese_bp else very_low_cal[:8],
        "description": "Maximum probability: very low calorie, heart-friendly",
        "priority": 1
    })
    
    # Obese + Acidity - Most restricted
    obese_acidity = [item for item in categories['acidity_friendly'] if item in categories['low_calorie'] and item in categories['low_spice']]
    health_rules.append({
        "rule_id": "obese_acidity_max",
        "bmi_category": "obese",
        "medical_condition": "acidity",
        "allowed_items": obese_acidity[:8] if obese_acidity else categories['low_calorie'][:8],
        "description": "Maximum probability: very light, mild items only",
        "priority": 1
    })
    
    return health_rules


async def seed_enhanced_health_rules():
    """Seed enhanced health rules into DynamoDB."""
    
    print_banner()
    
    # Analyze menu items first
    print("Analyzing menu items for optimal health rules...")
    categories = analyze_menu_items()
    
    print(f"Menu Item Analysis:")
    print(f"  Low Calorie Items: {len(categories['low_calorie'])}")
    print(f"  Medium Calorie Items: {len(categories['medium_calorie'])}")
    print(f"  High Calorie Items: {len(categories['high_calorie'])}")
    print(f"  Low Oil Items: {len(categories['low_oil'])}")
    print("-" * 80)
    
    # Create enhanced health rules
    health_rules = create_max_probability_health_rules(categories)
    
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
        for rule in health_rules:
            # Convert allowed_items list to DynamoDB format
            allowed_items_list = [{"S": item} for item in rule["allowed_items"]]
            
            await ddb.put_item(
                TableName="health_rules",
                Item={
                    "rule_id": {"S": rule["rule_id"]},
                    "bmi_category": {"S": rule["bmi_category"]},
                    "medical_condition": {"S": rule["medical_condition"]},
                    "allowed_items": {"L": allowed_items_list},
                    "description": {"S": rule["description"]},
                    "priority": {"N": str(rule["priority"])}
                }
            )
            print(f"Created enhanced rule: {rule['rule_id']}")
            print(f"  Items: {len(rule['allowed_items'])} allowed items")
            print(f"  Description: {rule['description']}")
            print()
    
    print(f"Successfully seeded {len(health_rules)} enhanced health rules!")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(seed_enhanced_health_rules())
