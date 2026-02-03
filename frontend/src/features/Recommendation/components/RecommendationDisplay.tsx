import React from 'react';
import { motion } from 'framer-motion';
import { Button, Tag, Typography, Progress } from 'antd';
import {
    ReloadOutlined,
    ArrowRightOutlined,
    FireOutlined,
    SafetyCertificateOutlined,
    ThunderboltOutlined
} from '@ant-design/icons';
import { SuggestionResponse, GuestSessionResponse } from '../../../types';
import { FoodCard } from '../../../components/FoodCard';
const { Title, Paragraph } = Typography;

interface RecommendationDisplayProps {
    suggestion: SuggestionResponse;
    sessionData?: GuestSessionResponse | null;
    mode: 'guest' | 'user';
    onRestart: () => void;
    onExplore: () => void;
    onCreateAccount?: () => void;
    userName?: string;
}

export const RecommendationDisplay: React.FC<RecommendationDisplayProps> = ({
    suggestion,
    mode,
    onRestart,
    onExplore,
    onCreateAccount,
    userName
}) => {
    const { suggested_item, suggested_item_details, reason, health_summary, similar_items } = suggestion;

    // Animation variants
    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1,
                delayChildren: 0.2
            }
        }
    };

    const itemVariants = {
        hidden: { y: 20, opacity: 0 },
        visible: {
            y: 0,
            opacity: 1,
            transition: { type: "spring", stiffness: 100 }
        }
    };

    return (
        <motion.div
            className="w-full max-w-6xl mx-auto z-10 p-4"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
        >
            {/* Header Section */}
            <motion.div variants={itemVariants} className="text-center mb-12">
                <Tag color="gold" className="mb-4 px-3 py-1 text-sm rounded-full border-none bg-yellow-500/20 text-yellow-300">
                    AI POWERED RECOMMENDATION
                </Tag>
                <Title level={1} className="!text-white font-display text-4xl md:text-6xl mb-2">
                    {userName ? (
                        <>
                            {userName}'s <span className="text-dosa-heat">Perfect Match</span>
                        </>
                    ) : (
                        <>
                            Your <span className="text-dosa-heat">Perfect Match</span>
                        </>
                    )}
                </Title>
                <Paragraph className="text-zinc-400 text-lg max-w-2xl mx-auto">
                    Based on your preferences, hunger level, and health goals, we've selected the ultimate choice for you.
                </Paragraph>
            </motion.div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
                {/* Left Column: Visual & Core Item Info */}
                <motion.div variants={itemVariants} className="relative group">
                    <div className="absolute inset-0 bg-dosa-heat/20 blur-[100px] rounded-full opacity-50 group-hover:opacity-75 transition-opacity" />

                    {/* Main Card */}
                    <div className="relative bg-zinc-900/40 backdrop-blur-xl border border-white/10 rounded-[2.5rem] p-8 overflow-hidden shadow-2xl">
                        {/* Image Placeholder or Actual Image */}
                        <div className="aspect-square w-full rounded-3xl overflow-hidden mb-6 relative">
                            <motion.img
                                src={suggested_item_details?.image_url || "https://images.unsplash.com/photo-1630384060421-cb20d0e0649d?auto=format&fit=crop&q=80&w=1000"}
                                alt={suggested_item}
                                className="w-full h-full object-cover"
                                whileHover={{ scale: 1.05 }}
                                transition={{ duration: 0.5 }}
                            />
                            <div className="absolute top-4 right-4 bg-black/60 backdrop-blur-md text-white px-4 py-2 rounded-full font-bold flex items-center gap-2">
                                <FireOutlined className="text-dosa-heat" />
                                {suggested_item_details?.calories || 350} cal
                            </div>
                        </div>

                        <div className="space-y-4">
                            <div className="flex justify-between items-start">
                                <h2 className="text-3xl font-bold text-white font-display">
                                    {suggested_item}
                                </h2>
                                <div className="flex gap-2">
                                    {suggested_item_details?.diet_type === 'veg' && (
                                        <span className="text-2xl" title="Vegetarian">🌱</span>
                                    )}
                                    {suggested_item_details?.spice_level === 'high' && (
                                        <span className="text-2xl" title="Spicy">🔥</span>
                                    )}
                                </div>
                            </div>

                            {/* Tags */}
                            <div className="flex flex-wrap gap-2">
                                <Tag className="bg-zinc-800 border-zinc-700 text-zinc-300 px-3 py-1 m-0 rounded-full">
                                    {suggested_item_details?.spice_level?.toUpperCase()} SPICE
                                </Tag>
                                <Tag className="bg-zinc-800 border-zinc-700 text-zinc-300 px-3 py-1 m-0 rounded-full">
                                    {suggested_item_details?.diet_type?.toUpperCase()}
                                </Tag>
                            </div>
                        </div>
                    </div>
                </motion.div>

                {/* Right Column: Reasoning & Stats */}
                <motion.div variants={itemVariants} className="space-y-6">
                    {/* The "Why" Box */}
                    <div className="bg-gradient-to-br from-zinc-800/80 to-zinc-900/80 backdrop-blur-md border-l-4 border-dosa-heat rounded-r-2xl p-6 shadow-lg">
                        <div className="flex items-center gap-2 mb-3 text-dosa-heat">
                            <ThunderboltOutlined className="text-xl" />
                            <span className="font-bold text-sm tracking-wider uppercase">AI Reasoning</span>
                        </div>
                        <p className="text-zinc-200 text-lg leading-relaxed italic">
                            "{reason}"
                        </p>
                    </div>

                    {/* Health Summary Box */}
                    <div className="bg-zinc-900/60 border border-white/5 rounded-2xl p-6">
                        <div className="flex items-center gap-2 mb-4 text-green-400">
                            <SafetyCertificateOutlined className="text-xl" />
                            <span className="font-bold text-sm tracking-wider uppercase">Health Insight</span>
                        </div>
                        <p className="text-zinc-300 mb-6">
                            {health_summary}
                        </p>

                        {/* Mock Macros (If we had real data we'd use it) */}
                        <div className="grid grid-cols-3 gap-4 text-center">
                            <div className="bg-black/30 rounded-xl p-3">
                                <div className="text-xs text-zinc-500 mb-1">PROTEIN</div>
                                <div className="text-xl font-bold text-white">12g</div>
                                <Progress percent={60} showInfo={false} strokeColor="#10b981" trailColor="#3f3f46" size="small" className="mt-2" />
                            </div>
                            <div className="bg-black/30 rounded-xl p-3">
                                <div className="text-xs text-zinc-500 mb-1">CARBS</div>
                                <div className="text-xl font-bold text-white">45g</div>
                                <Progress percent={40} showInfo={false} strokeColor="#f59e0b" trailColor="#3f3f46" size="small" className="mt-2" />
                            </div>
                            <div className="bg-black/30 rounded-xl p-3">
                                <div className="text-xs text-zinc-500 mb-1">FATS</div>
                                <div className="text-xl font-bold text-white">8g</div>
                                <Progress percent={25} showInfo={false} strokeColor="#ef4444" trailColor="#3f3f46" size="small" className="mt-2" />
                            </div>
                        </div>
                    </div>

                    {/* Action Area */}
                    <div className="pt-6 space-y-8">
                        <Button
                            type="primary"
                            size="large"
                            icon={<FireOutlined />}
                            className="w-full h-14 text-lg font-bold bg-gradient-to-r from-orange-500 to-red-600 border-none hover:translate-y-1 transform transition-all duration-300 shadow-lg shadow-orange-500/30"
                            onClick={() => console.log('Order placed')}
                        >
                            Select This Item
                        </Button>

                        <div className="grid grid-cols-2 gap-4 translate-y-2">
                            <button
                                onClick={onExplore}
                                className="h-12 px-6 text-white border border-white/20 rounded-lg hover:border-dosa-heat hover:text-dosa-heat hover:translate-y-1 transform transition-all duration-300 cursor-pointer bg-transparent flex items-center justify-center gap-2"
                            >
                                <ArrowRightOutlined />
                                Explore Menu
                            </button>
                            <button
                                onClick={onRestart}
                                className="h-12 px-6 text-white border border-white/20 rounded-lg hover:border-dosa-heat hover:text-dosa-heat hover:translate-y-1 transform transition-all duration-300 cursor-pointer bg-transparent flex items-center justify-center gap-2"
                            >
                                <ReloadOutlined />
                                Start Over
                            </button>
                        </div>

                        {mode === 'guest' && onCreateAccount && (
                            <div className="mt-6 text-center pt-6 border-t border-white/10">
                                <p className="text-zinc-400 mb-2 text-sm">Want to save your preferences?</p>
                                <Button
                                    type="link"
                                    className="text-dosa-heat hover:text-white p-0"
                                    onClick={onCreateAccount}
                                >
                                    Create a Free Account
                                </Button>
                            </div>
                        )}
                    </div>
                </motion.div>
            </div>

            {/* Similar Items Section */}
            {similar_items && similar_items.length > 0 && (
                <motion.div variants={itemVariants} className="mt-24">
                    <Title level={3} className="!text-white font-display mb-8 px-4 border-l-4 border-dosa-heat">
                        Similar Delights
                    </Title>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {similar_items.map((item) => (
                            <FoodCard
                                key={item.item_id}
                                itemName={item.item_name}
                                calories={item.calories}
                                spiceLevel={item.spice_level}
                                dietType={item.diet_type}
                                imageUrl={item.image_url}
                                onClick={() => {
                                    // Handle viewing this item logic - maybe swap main view?
                                    // For now just console log
                                    console.log('View similar:', item.item_name);
                                }}
                            />
                        ))}
                    </div>
                </motion.div>
            )}
        </motion.div>
    );
};
