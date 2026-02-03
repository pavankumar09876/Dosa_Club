import { motion } from 'framer-motion';
import { ThunderboltOutlined, InfoCircleOutlined, HeartOutlined } from '@ant-design/icons';
import { useState } from 'react';
import { NutritionDetails } from './NutritionDetails';
import { EnhancedMenuItem } from '../types';

interface FoodCardProps {
    itemName: string;
    calories?: number;
    spiceLevel?: 'low' | 'medium' | 'high';
    dietType?: 'veg' | 'egg' | 'non-veg';
    featured?: boolean;
    onClick?: () => void;
    // Image from API
    imageUrl?: string;
    // Enhanced nutrition props
    nutrition?: EnhancedMenuItem['nutrition'];
    healthBenefits?: EnhancedMenuItem['health_benefits'];
    allergens?: EnhancedMenuItem['allergens'];
    servingSize?: number;
    // Health recommendation props
    showHealthRecommendation?: boolean;
}

/**
 * Food Card Component
 * Displays food item with image from API and animations
 */
export const FoodCard: React.FC<FoodCardProps> = ({
    itemName,
    calories,
    spiceLevel,
    dietType,
    featured = false,
    onClick,
    imageUrl,
    nutrition,
    healthBenefits = [],
    allergens = [],
    servingSize,
    showHealthRecommendation = false,
}) => {
    const [showNutrition, setShowNutrition] = useState(false);
    const [imageError, setImageError] = useState(false);
    
    const spiceEmoji = {
        low: '😌',
        medium: '🌶️',
        high: '🔥',
    };

    const dietEmoji = {
        veg: '🥗',
        egg: '🥚',
        'non-veg': '🍗',
    };

    return (
        <>
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                whileHover={{ scale: 1.02, y: -5 }}
                whileTap={{ scale: 0.98 }}
                transition={{ type: 'spring', damping: 20, stiffness: 200 }}
                onClick={onClick}
                className={`
        relative rounded-3xl border-2 cursor-pointer gpu-accelerated overflow-hidden flex flex-col h-full
        ${featured
                    ? 'bg-gradient-to-br from-dosa-heat/20 to-dosa-warm/10 border-dosa-heat shadow-2xl shadow-dosa-heat/30'
                    : 'bg-zinc-900 border-zinc-800 hover:border-zinc-700'
                }
    `}
            >
             {/* Image Section */}
            <div className="h-48 w-full overflow-hidden bg-zinc-800">
                {!imageError && imageUrl ? (
                    <img
                        src={imageUrl}
                        alt={itemName}
                        className="w-full h-full object-cover transition-transform duration-500 hover:scale-110"
                        onError={() => setImageError(true)}
                        loading="lazy"
                    />
                ) : (
                    <div className="w-full h-full flex items-center justify-center bg-zinc-800">
                        <div className="text-center">
                            <div className="text-4xl mb-2">🍽️</div>
                            <p className="text-zinc-400 text-sm">No image available</p>
                        </div>
                    </div>
                )}
            </div>
                {/* Featured Badge */}
                {featured && (
                    <motion.div
                        initial={{ scale: 0, rotate: -12 }}
                        animate={{ scale: 1, rotate: 0 }}
                        transition={{ type: 'spring', damping: 15, stiffness: 200, delay: 0.2 }}
                        className="absolute top-2 right-2 bg-dosa-heat text-black px-4 py-1 rounded-full font-bold text-sm shadow-lg z-10"
                    >
                        ⭐ Recommended
                    </motion.div>
                )}

                {/* Content Section */}
                <div className="p-6 flex-1 flex flex-col">
                    {/* Food Item Name */}
                    <h3 className="font-display font-bold text-2xl text-white mb-4 line-clamp-2">{itemName}</h3>

                    {/* Food Details */}
                    <div className="flex flex-wrap items-center gap-3 mb-auto">
                        {/* Calories */}
                        {calories && (
                            <div className="flex items-center gap-1 bg-zinc-800 px-3 py-1 rounded-full">
                                <ThunderboltOutlined className="text-dosa-warm text-sm" />
                                <span className="text-zinc-300 text-sm font-medium">{calories} cal</span>
                            </div>
                        )}

                        {/* Spice Level */}
                        {spiceLevel && (
                            <div className="flex items-center gap-1 bg-zinc-800 px-3 py-1 rounded-full">
                                <span>{spiceEmoji[spiceLevel]}</span>
                                <span className="text-zinc-300 text-sm font-medium capitalize">
                                    {spiceLevel}
                                </span>
                            </div>
                        )}

                        {/* Diet Type */}
                        {dietType && (
                            <div className="flex items-center gap-1 bg-zinc-800 px-3 py-1 rounded-full">
                                <span>{dietEmoji[dietType]}</span>
                                <span className="text-zinc-300 text-sm font-medium capitalize">
                                    {dietType}
                                </span>
                            </div>
                        )}

                        {/* Nutrition Info Button */}
                        {(nutrition || healthBenefits.length > 0 || allergens.length > 0) && (
                            <button
                                onClick={(e) => {
                                    e.stopPropagation();
                                    setShowNutrition(true);
                                }}
                                className="flex items-center gap-1 bg-blue-600/20 hover:bg-blue-600/30 px-3 py-1 rounded-full transition-colors"
                            >
                                <InfoCircleOutlined className="text-blue-400 text-sm" />
                                <span className="text-blue-400 text-sm font-medium">Nutrition</span>
                            </button>
                        )}

                        {/* Health Recommendation Button */}
                        {showHealthRecommendation && (
                            <button
                                onClick={(e) => {
                                    e.stopPropagation();
                                    // Navigate to health quiz or recommendation
                                    window.location.href = '/questions';
                                }}
                                className="flex items-center gap-1 bg-green-600/20 hover:bg-green-600/30 px-3 py-1 rounded-full transition-colors"
                            >
                                <HeartOutlined className="text-green-400 text-sm" />
                                <span className="text-green-400 text-sm font-medium">Health Tip</span>
                            </button>
                        )}
                    </div>

                    {/* Hover indicator */}
                    <motion.div
                        className="text-zinc-500 text-sm flex items-center gap-2 mt-4 pt-4 border-t border-zinc-800/50"
                        whileHover={{ x: 5 }}
                        transition={{ type: 'spring', damping: 20 }}
                    >
                        <span>Learn more</span>
                        <svg
                            className="w-4 h-4"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M9 5l7 7-7 7"
                            />
                        </svg>
                    </motion.div>
                </div>
            </motion.div>

            {/* Nutrition Details Modal */}
            <NutritionDetails
                visible={showNutrition}
                onClose={() => setShowNutrition(false)}
                itemName={itemName}
                nutrition={nutrition}
                healthBenefits={healthBenefits}
                allergens={allergens}
                calories={calories || 0}
                servingSize={servingSize}
            />
        </>
    );
};
