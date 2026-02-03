import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input, App } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import { PageTransition } from '../../components/PageTransition';
import { FoodCard } from '../../components/FoodCard';
import { SkeletonCard } from '../../components/SkeletonCard';
import { AnimatedButton } from '../../components/AnimatedButton';
import { apiService } from '../../services/api';
import { MenuItem } from '../../types';

/**
 * Menu Explorer Screen - Screen 5
 * Browse all menu items with filters
 */
export const MenuExplorerScreen = () => {
    const navigate = useNavigate();
    const { message } = App.useApp();
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedFilter, setSelectedFilter] = useState<string>('all');
    const [allMenuItems, setAllMenuItems] = useState<MenuItem[]>([]);
    const [filteredItems, setFilteredItems] = useState<MenuItem[]>([]);

    // Fetch menu items on mount
    useEffect(() => {
        const fetchMenuItems = async () => {
            try {
                setLoading(true);
                const items = await apiService.getMenuItems();
                setAllMenuItems(items);
                setFilteredItems(items);
            } catch (error) {
                console.error('Failed to fetch menu items:', error);
                message.error('Failed to load menu items');
                setAllMenuItems([]);
                setFilteredItems([]);
            } finally {
                setLoading(false);
            }
        };

        fetchMenuItems();
    }, []);

    // Apply filters when selectedFilter or search changes
    useEffect(() => {
        if (!allMenuItems.length) return;

        let filtered = [...allMenuItems];

        // Apply search filter first
        if (searchQuery.trim()) {
            filtered = filtered.filter(item =>
                item.item_name.toLowerCase().includes(searchQuery.toLowerCase())
            );
        }

        // Then apply category filter
        switch (selectedFilter) {
            case 'low-cal':
                // Low calorie: <= 250 calories
                filtered = filtered.filter(item => item.calories <= 250);
                break;
            case 'high-cal':
                // High calorie: > 250 calories
                filtered = filtered.filter(item => item.calories > 250);
                break;
            case 'mild':
                // Mild spice
                filtered = filtered.filter(item => item.spice_level === 'low');
                break;
            case 'medium':
                // Medium spice
                filtered = filtered.filter(item => item.spice_level === 'medium');
                break;
            case 'all':
            default:
                // 'all' - keep current filtered results (already has search applied)
                break;
        }

        setFilteredItems(filtered);
    }, [selectedFilter, searchQuery, allMenuItems]);

    const filters = [
        { label: 'All', value: 'all' },
        { label: 'Low Calorie', value: 'low-cal' },
        { label: 'High Calorie', value: 'high-cal' },
        { label: 'Mild Spice', value: 'mild' },
        { label: 'Medium Spice', value: 'medium' },
    ];

    return (
        <PageTransition>
            <div className="min-h-screen bg-black text-white px-6 py-12">
                <div className="max-w-7xl mx-auto">
                    {/* Header with Back Button */}
                    <div className="relative mb-6">
                        {/* Back Button - Top Left */}
                        <motion.button
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                            onClick={() => navigate('/')}
                            className="absolute left-0 top-1/2 -translate-y-1/2 p-3 rounded-full bg-zinc-800/50 hover:bg-zinc-700 text-zinc-400 hover:text-white transition-all z-20"
                        >
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                            </svg>
                        </motion.button>

                        <motion.div
                            initial={{ opacity: 0, y: -20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="relative z-10 text-center"
                        >
                            <h1 className="font-display font-bold text-4xl md:text-5xl mb-4">
                                Explore Our Dosa-Club Menu
                            </h1>
                            <p className="text-zinc-400 text-lg">
                                Browse through our healthy South Indian food selection
                            </p>
                            <p className="text-zinc-500 text-sm mt-2">
                                {filteredItems.length} item{filteredItems.length !== 1 ? 's' : ''} available
                            </p>
                        </motion.div>
                    </div>

                    {/* Search Bar */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 }}
                        className="relative z-10 max-w-2xl mx-auto mb-6"
                    >
                        <Input
                            id="menu-search"
                            name="search"
                            prefix={<SearchOutlined />}
                            placeholder="Search for dishes..."
                            size="large"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            allowClear
                        />
                    </motion.div>

                    {/* Filter Bar */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                        className="relative z-10 flex flex-wrap gap-3 justify-center mb-8"
                    >
                        {filters.map((filter, index) => (
                            <motion.button
                                key={filter.value}
                                initial={{ opacity: 0, scale: 0.8 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ delay: 0.3 + index * 0.05, type: 'spring', damping: 20 }}
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={() => setSelectedFilter(filter.value)}
                                className={`
                  px-6 py-3 rounded-full font-medium transition-all gpu-accelerated
                  ${selectedFilter === filter.value
                                        ? 'bg-dosa-heat text-black shadow-lg shadow-dosa-heat/30'
                                        : 'bg-zinc-900 text-zinc-300 border border-zinc-800 hover:border-zinc-700'
                                    }
                `}
                            >
                                {filter.label}
                            </motion.button>
                        ))}
                    </motion.div>

                    {/* Menu Grid */}
                    {loading ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {Array.from({ length: 9 }).map((_, index) => (
                                <SkeletonCard key={index} />
                            ))}
                        </div>
                    ) : filteredItems.length === 0 ? (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="text-center py-12"
                        >
                            <p className="text-zinc-400 text-lg mb-4">
                                No items found for the selected filter
                            </p>
                            <AnimatedButton onClick={() => setSelectedFilter('all')}>
                                Show All Items
                            </AnimatedButton>
                        </motion.div>
                    ) : (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: 0.4 }}
                            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                        >
                            {filteredItems.map((item, index) => (
                                <motion.div
                                    key={item.item_id}
                                    initial={{ opacity: 0, y: 30 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{
                                        delay: 0.5 + index * 0.05,
                                        type: 'spring',
                                        damping: 20,
                                        stiffness: 100,
                                    }}
                                >
                                    <FoodCard
                                        itemName={item.item_name}
                                        calories={item.calories}
                                        spiceLevel={item.spice_level}
                                        dietType={item.diet_type}
                                        imageUrl={item.image_url}
                                    />
                                </motion.div>
                            ))}
                        </motion.div>
                    )}
                </div>
            </div>
        </PageTransition>
    );
};
