"""
Seed data for DosaClub menu items.

Contains comprehensive list of dosa, uthappam, idly, vada, and other items
with estimated nutritional and suitability information.
"""

MENU_ITEMS = [
    {
        "item_name": "Plain Dosa",
        "calories": 150,
        "spice_level": "low",
        "oil_level": "low",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight", "obese"],
            "medical_conditions": ["none", "diabetes", "bp", "acidity"]
        }
    },
    {
        "item_name": "Masala Dosa",
        "calories": 320,
        "spice_level": "medium",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "diabetes", "bp"]
        }
    },
    {
        "item_name": "Kal Dosa",
        "calories": 180,
        "spice_level": "low",
        "oil_level": "low",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight", "obese"],
            "medical_conditions": ["none", "diabetes", "bp", "acidity"]
        }
    },
    {
        "item_name": "Onion Chilli Dosa",
        "calories": 200,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Chennai Podi Onion Chilli Dosa",
        "calories": 250,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Chennai Podi Onion Chilli Masala Dosa",
        "calories": 350,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Pure Ghee Dosa",
        "calories": 280,
        "spice_level": "low",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none", "diabetes", "bp", "acidity"]
        }
    },
    {
        "item_name": "Ghee Masala Dosa",
        "calories": 400,
        "spice_level": "medium",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none", "diabetes", "bp"]
        }
    },
    {
        "item_name": "Ghee Masala Dosa with Upma",
        "calories": 450,
        "spice_level": "medium",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none", "diabetes", "bp"]
        }
    },
    {
        "item_name": "Butter Dosa",
        "calories": 250,
        "spice_level": "low",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "diabetes", "bp", "acidity"]
        }
    },
    {
        "item_name": "Butter Masala Dosa",
        "calories": 380,
        "spice_level": "medium",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none", "diabetes", "bp"]
        }
    },
    {
        "item_name": "Butter Masala Dosa with Upma",
        "calories": 430,
        "spice_level": "medium",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none", "diabetes", "bp"]
        }
    },
    {
        "item_name": "Mysore Plain Dosa",
        "calories": 220,
        "spice_level": "medium",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Mysore Masala Dosa",
        "calories": 340,
        "spice_level": "medium",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Andhra Karam Dosa",
        "calories": 240,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Andhra Karam Masala Dosa",
        "calories": 360,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Double Egg Dosa",
        "calories": 300,
        "spice_level": "medium",
        "oil_level": "medium",
        "diet_type": "egg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Upma Dosa",
        "calories": 280,
        "spice_level": "medium",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight", "obese"],
            "medical_conditions": ["none", "diabetes", "bp", "acidity"]
        }
    },
    {
        "item_name": "Rameshwaram Masala Dosa",
        "calories": 380,
        "spice_level": "high",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Rameshwaram Podi Ghee Roast",
        "calories": 320,
        "spice_level": "high",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Rameshwaram Butter Roast Dosa",
        "calories": 300,
        "spice_level": "high",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Rameshwaram Butter Masala Dosa",
        "calories": 420,
        "spice_level": "high",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Rameshwaram Ghee Roast Dosa",
        "calories": 340,
        "spice_level": "high",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Rameshwaram Ghee Masala Dosa",
        "calories": 460,
        "spice_level": "high",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Schezwan Dosa",
        "calories": 260,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Schezwan Masala Dosa",
        "calories": 380,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Schezwan Butter Masala Dosa",
        "calories": 420,
        "spice_level": "high",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Schezwan Mysore Masala Dosa",
        "calories": 400,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Schezwan Corn & Cheese Dosa",
        "calories": 350,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Cheese Dosa",
        "calories": 280,
        "spice_level": "medium",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Chilli Cheese Onion Dosa",
        "calories": 320,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Cheese Corn Dosa",
        "calories": 310,
        "spice_level": "medium",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Vegetable Spring Dosa",
        "calories": 290,
        "spice_level": "medium",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight", "obese"],
            "medical_conditions": ["none", "diabetes", "bp", "acidity"]
        }
    },
    {
        "item_name": "Mumbai Style Street Dosa",
        "calories": 330,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Paneer Burji Dosa",
        "calories": 380,
        "spice_level": "medium",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Pizza Dosa",
        "calories": 400,
        "spice_level": "medium",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Chicken Keema Dosa",
        "calories": 420,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "non-veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Mutton Keema Dosa",
        "calories": 450,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "non-veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "70mm Dosa",
        "calories": 160,
        "spice_level": "low",
        "oil_level": "low",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight", "obese"],
            "medical_conditions": ["none", "diabetes", "bp", "acidity"]
        }
    },
    {
        "item_name": "Plain Rava Dosa",
        "calories": 180,
        "spice_level": "low",
        "oil_level": "low",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight", "obese"],
            "medical_conditions": ["none", "diabetes", "bp", "acidity"]
        }
    },
    {
        "item_name": "Rava Masala Dosa",
        "calories": 340,
        "spice_level": "medium",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "diabetes", "bp"]
        }
    },
    {
        "item_name": "Rava Onion Chilli Dosa",
        "calories": 220,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Rava Onion Chilli Masala Dosa",
        "calories": 380,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Rava Mysore Dosa",
        "calories": 240,
        "spice_level": "medium",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Rava Mysore Masala Dosa",
        "calories": 360,
        "spice_level": "medium",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Rava Andhra Karam Dosa",
        "calories": 260,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Rava Andhra Karam Masala Dosa",
        "calories": 380,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Rava Cheese Dosa",
        "calories": 300,
        "spice_level": "medium",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Rava Cheese Onion Chilli Dosa",
        "calories": 340,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Rava Cheese Onion Chilli Masala Dosa",
        "calories": 420,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Plain Uthappam",
        "calories": 200,
        "spice_level": "low",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight", "obese"],
            "medical_conditions": ["none", "diabetes", "bp", "acidity"]
        }
    },
    {
        "item_name": "Onion Garlic Uthappam",
        "calories": 240,
        "spice_level": "medium",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp", "acidity"]
        }
    },
    {
        "item_name": "Pizza Uthappam",
        "calories": 320,
        "spice_level": "medium",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Onion Tomato Chilli Uthappam",
        "calories": 260,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Chilli Cheese Garlic Uthappam",
        "calories": 300,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Podi Onion Uthappam",
        "calories": 280,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Vegetable Uthappam",
        "calories": 250,
        "spice_level": "medium",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight", "obese"],
            "medical_conditions": ["none", "diabetes", "bp", "acidity"]
        }
    },
    {
        "item_name": "Idly",
        "calories": 120,
        "spice_level": "low",
        "oil_level": "low",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight", "obese"],
            "medical_conditions": ["none", "diabetes", "bp", "acidity"]
        }
    },
    {
        "item_name": "Podi Idly Fry",
        "calories": 180,
        "spice_level": "high",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp"]
        }
    },
    {
        "item_name": "Ghee Idly",
        "calories": 160,
        "spice_level": "low",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight", "obese"],
            "medical_conditions": ["none", "diabetes", "bp", "acidity"]
        }
    },
    {
        "item_name": "Ghee Karam Idly",
        "calories": 190,
        "spice_level": "high",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Butter Idly",
        "calories": 150,
        "spice_level": "low",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight", "obese"],
            "medical_conditions": ["none", "diabetes", "bp", "acidity"]
        }
    },
    {
        "item_name": "Vada",
        "calories": 200,
        "spice_level": "medium",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp", "acidity"]
        }
    },
    {
        "item_name": "Idly Sambar",
        "calories": 180,
        "spice_level": "medium",
        "oil_level": "low",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight", "obese"],
            "medical_conditions": ["none", "diabetes", "bp", "acidity"]
        }
    },
    {
        "item_name": "Vada Sambar",
        "calories": 260,
        "spice_level": "medium",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "bp", "acidity"]
        }
    },
    {
        "item_name": "Bezawada Chitti Punugulu",
        "calories": 220,
        "spice_level": "high",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none"]
        }
    },
    {
        "item_name": "Chocolate Dosa",
        "calories": 350,
        "spice_level": "low",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "diabetes", "bp", "acidity"]
        }
    },
    {
        "item_name": "Butter Cone Dosa",
        "calories": 280,
        "spice_level": "low",
        "oil_level": "high",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight"],
            "medical_conditions": ["none", "diabetes", "bp", "acidity"]
        }
    },
    {
        "item_name": "Kids Cheese Dosa",
        "calories": 250,
        "spice_level": "low",
        "oil_level": "medium",
        "diet_type": "veg",
        "suitable_for": {
            "bmi_categories": ["underweight", "normal", "overweight", "obese"],
            "medical_conditions": ["none", "diabetes", "bp", "acidity"]
        }
    }
]
