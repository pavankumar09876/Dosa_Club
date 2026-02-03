// TypeScript type definitions for DosaClub

export interface UserData {
    name: string;
    phone_number: string;
    age?: number;
    email?: string;
    gender?: 'male' | 'female' | 'other';
    height_cm: number;
    weight_kg: number;
    diet_type: 'veg' | 'egg' | 'non-veg';
    health_goal: 'weight_loss' | 'weight_gain' | 'balanced';
    medical_condition: 'none' | 'diabetes' | 'bp' | 'acidity';
    spice_tolerance: 'low' | 'medium' | 'high';
}

export interface UserIntakeResponse {
    user_id: string;
    name: string;
    bmi: number;
    bmi_category: string;
    created_at: string;
}

export interface SuggestionResponse {
    health_summary: string;
    bmi_category: string;
    suggested_item: string;
    suggested_item_details?: MenuItem;
    similar_items?: MenuItem[];
    reason: string;
}

export interface MenuItem {
    item_id: string;
    item_name: string;
    calories: number;
    spice_level: 'low' | 'medium' | 'high';
    oil_level: 'low' | 'medium' | 'high';
    diet_type: 'veg' | 'egg' | 'non-veg';
    image_url?: string;
    suitable_for: {
        bmi_categories: string[];
        medical_conditions: string[];
    };
}

export interface ApiError {
    message: string;
    detail?: any;
}

// Guest Mode Types
export interface GuestSessionResponse {
    session_id: string;
    expires_at: string;
    message: string;
}

export interface GuestData {
    age: number;
    gender: 'male' | 'female' | 'other';
    height_cm: number;
    weight_kg: number;
    diet_type: 'veg' | 'egg' | 'non-veg';
    health_goal: 'weight_loss' | 'weight_gain' | 'balanced';
    medical_condition: 'none' | 'diabetes' | 'bp' | 'acidity';
    spice_tolerance: 'low' | 'medium' | 'high';
}

export interface GuestSuggestionRequest {
    session_id: string;
    health_data: GuestData;
}

// Enhanced Nutrition Types
export interface NutritionInfo {
    protein_g: number;
    carbohydrates_g: number;
    fat_g: number;
    fiber_g?: number;
    sugar_g?: number;
    sodium_mg?: number;
    cholesterol_mg?: number;
    vitamin_a_mcg?: number;
    vitamin_c_mg?: number;
    calcium_mg?: number;
    iron_mg?: number;
}

export type Allergen = 'gluten' | 'dairy' | 'nuts' | 'soy' | 'eggs' | 'fish' | 'shellfish' | 'peanuts' | 'sesame' | 'none';

export interface HealthBenefit {
    category: string;
    title: string;
    description: string;
    importance: 'low' | 'medium' | 'high';
}

export interface EnhancedMenuItem extends MenuItem {
    nutrition?: NutritionInfo;
    allergens: Allergen[];
    health_benefits: HealthBenefit[];
    preparation_time_minutes?: number;
    serving_size_g?: number;
}

export interface UserHistoryResponse {
    id: string;
    item_name: string;
    date: string;
    description: string;
}

export interface FavoriteResponse {
    item_id: string;
    item_name: string;
    image_url?: string;
    price?: number;
}

export type UserResponse = UserData;
