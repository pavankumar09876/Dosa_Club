import { motion } from 'framer-motion';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { Button } from 'antd';
import { ArrowLeftOutlined, ShareAltOutlined } from '@ant-design/icons';

/**
 * Mobile Recommendation Screen
 * Displays personalized food recommendations on mobile devices
 */
export const MobileRecommendationScreen = () => {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const sessionId = searchParams.get('session') || 'unknown';
    
    const [recommendationData, setRecommendationData] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Get questionnaire data from navigation state
        const state = history.state;
        if (state?.questionnaireData) {
            // Simulate API call to get recommendation
            setTimeout(() => {
                setRecommendationData({
                    item_name: "Masala Dosa",
                    calories: 250,
                    spice_level: "medium",
                    diet_type: "vegetarian",
                    image_url: "/api/placeholder/300/200",
                    reason: "Perfect for your fitness goals and dietary preferences",
                    bmi_category: "Normal"
                });
                setIsLoading(false);
            }, 1500);
        } else {
            // No questionnaire data, redirect back
            navigate(`/mobile/quiz?session=${sessionId}`);
        }
    }, [sessionId, navigate]);

    const handleShare = async () => {
        if (navigator.share) {
            try {
                await navigator.share({
                    title: 'My Dosa Club Recommendation',
                    text: `I got recommended ${recommendationData?.item_name}! Check out your personalized recommendation.`,
                    url: window.location.href
                });
            } catch (error) {
                console.log('Error sharing:', error);
            }
        } else {
            // Fallback - copy to clipboard
            navigator.clipboard.writeText(window.location.href);
        }
    };

    if (isLoading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-black via-zinc-900 to-zinc-800 text-white flex items-center justify-center px-4">
                <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className="w-12 h-12 border-2 border-blue-500 border-t-transparent rounded-full"
                />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-black via-zinc-900 to-zinc-800 text-white">
            {/* Mobile Header */}
            <div className="sticky top-0 z-50 bg-black/80 backdrop-blur-xl border-b border-zinc-700">
                <div className="px-4 py-3">
                    <div className="flex items-center justify-between">
                        <Button
                            onClick={() => navigate(-1)}
                            className="bg-zinc-800 border-zinc-700 hover:bg-zinc-700 text-white"
                            icon={<ArrowLeftOutlined />}
                        >
                            Back
                        </Button>
                        <div className="flex items-center gap-2">
                            <span className="text-lg">📱</span>
                            <span className="text-sm font-medium text-zinc-400">Mobile Result</span>
                        </div>
                        <Button
                            onClick={handleShare}
                            className="bg-zinc-800 border-zinc-700 hover:bg-zinc-700 text-white"
                            icon={<ShareAltOutlined />}
                        />
                    </div>
                </div>
            </div>

            {/* Recommendation Content */}
            <div className="px-4 py-6 pb-20">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                    className="max-w-lg mx-auto space-y-6"
                >
                    {/* Success Header */}
                    <div className="text-center">
                        <motion.div
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            transition={{ type: 'spring', stiffness: 200 }}
                            className="text-6xl mb-4"
                        >
                            🎉
                        </motion.div>
                        
                        <h1 className="text-3xl font-bold text-white mb-2">
                            Your Perfect Match!
                        </h1>
                        
                        <p className="text-zinc-400">
                            Based on your health profile, we found the ideal dosa for you
                        </p>
                    </div>

                    {/* Recommendation Card */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.2 }}
                        className="bg-gradient-to-br from-zinc-900/90 to-zinc-800/90 backdrop-blur-2xl border border-zinc-700 rounded-2xl p-6"
                    >
                        <div className="text-center mb-4">
                            <div className="inline-flex items-center gap-2 bg-gradient-to-r from-green-500/20 to-blue-500/20 backdrop-blur-xl border border-green-500/30 rounded-full px-4 py-2 mb-4">
                                <span className="text-lg">⭐</span>
                                <span className="text-green-400 font-semibold text-sm">Best For You</span>
                            </div>
                            
                            <h2 className="text-2xl font-bold text-white mb-2">
                                {recommendationData.item_name}
                            </h2>
                            
                            <div className="flex justify-center gap-2 mb-4">
                                <span className="bg-orange-500/20 text-orange-400 px-3 py-1 rounded-full text-sm">
                                    🌶️ {recommendationData.spice_level}
                                </span>
                                <span className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-sm">
                                    🥗 {recommendationData.diet_type}
                                </span>
                                <span className="bg-blue-500/20 text-blue-400 px-3 py-1 rounded-full text-sm">
                                    ⚡ {recommendationData.calories} cal
                                </span>
                            </div>
                        </div>

                        {/* Food Image */}
                        <div className="mb-6">
                            <div className="relative">
                                <img
                                    src={recommendationData.image_url}
                                    alt={recommendationData.item_name}
                                    className="w-full h-48 object-cover rounded-xl"
                                />
                                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent rounded-xl" />
                            </div>
                        </div>

                        {/* Why This Section */}
                        <div className="bg-gradient-to-r from-green-500/10 via-blue-500/10 to-purple-500/10 rounded-xl p-4 border border-green-500/20">
                            <h3 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
                                <span>🎯</span> Why This is Perfect For You
                            </h3>
                            <p className="text-zinc-300 text-sm leading-relaxed">
                                {recommendationData.reason}
                            </p>
                            <div className="mt-3 text-xs text-zinc-400">
                                Ideal for <span className="text-green-400 font-medium">{recommendationData.bmi_category}</span> body type
                            </div>
                        </div>
                    </motion.div>

                    {/* Action Buttons */}
                    <div className="space-y-3">
                        <Button
                            onClick={() => navigate('/explore')}
                            className="w-full bg-gradient-to-r from-orange-500 to-orange-600 border-0 hover:from-orange-600 hover:to-orange-700 h-14 text-base font-semibold"
                        >
                            🍽️ Explore More Options
                        </Button>
                        
                        <Button
                            onClick={() => navigate(`/mobile/quiz?session=${sessionId}`)}
                            className="w-full bg-zinc-800 border-zinc-700 hover:bg-zinc-700 text-white h-14"
                        >
                            🔄 Retake Quiz
                        </Button>
                    </div>

                    {/* Trust Message */}
                    <div className="text-center">
                        <div className="inline-flex items-center gap-3 bg-zinc-800/50 backdrop-blur-sm rounded-full px-4 py-2">
                            <span className="text-lg">💚</span>
                            <div className="text-left">
                                <p className="text-white font-medium text-sm">AI-Powered Recommendation</p>
                                <p className="text-zinc-400 text-xs">Personalized just for you</p>
                            </div>
                        </div>
                    </div>
                </motion.div>
            </div>

            {/* Mobile Footer */}
            <div className="fixed bottom-0 left-0 right-0 bg-black/80 backdrop-blur-xl border-t border-zinc-700 px-4 py-3">
                <div className="flex items-center justify-between text-xs text-zinc-500">
                    <div className="flex items-center gap-2">
                        <span>💙</span>
                        <span>Mobile Optimized</span>
                    </div>
                    <div>
                        <span>Session: {sessionId.slice(-8)}</span>
                    </div>
                </div>
            </div>
        </div>
    );
};
