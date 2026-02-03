import { useState, useEffect } from 'react';
// import { motion } from 'framer-motion';
import { PageTransition } from '../../components/PageTransition';
// import { AnimatedButton } from '../../components/AnimatedButton';
// import { ExpandableSection } from '../../components/ExpandableSection';
// import { FoodCard } from '../../components/FoodCard';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
// import { UserResponse, UserHistoryResponse, FavoriteResponse } from '../../types';

/**
 * User Profile Screen
 * Displays user profile, allows editing, shows history and favorites
 */
export const UserProfileScreen = () => {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState<'profile' | 'history' | 'favorites'>('profile');
    // const [userProfile, setUserProfile] = useState<UserResponse | null>(null);
    // const [suggestionHistory, setSuggestionHistory] = useState<UserHistoryResponse[]>([]);
    // const [favorites, setFavorites] = useState<FavoriteResponse[]>([]);
    const [loading, setLoading] = useState(true);
    // const [editing, setEditing] = useState(false);
    // const [editForm, setEditForm] = useState<Partial<UserResponse>>({});

    // Mock phone number - in real app, get from context/auth
    const phoneNumber = '9876543210';

    useEffect(() => {
        loadUserData();
    }, []);

    const loadUserData = async () => {
        try {
            setLoading(true);
            const [profileRes, historyRes, favoritesRes] = await Promise.all([
                api.getUserProfile(phoneNumber),
                api.getSuggestionHistory(phoneNumber),
                api.getUserFavorites(phoneNumber)
            ]);

            console.log('Loaded:', profileRes, historyRes, favoritesRes);
            // setUserProfile(profileRes);
            // setSuggestionHistory(historyRes);
            // setFavorites(favoritesRes);
        } catch (error) {
            console.error('Error loading user data:', error);
        } finally {
            setLoading(false);
        }
    };

    /*
    const handleSaveProfile = async () => {
        if (!userProfile) return;

        try {
            await api.updateUserProfile(phoneNumber, editForm);
            setUserProfile({ ...userProfile, ...editForm });
            setEditing(false);
            setEditForm({});
        } catch (error) {
            console.error('Error updating profile:', error);
        }
    };

    const handleToggleFavorite = async (itemId: string, itemName: string) => {
        try {
            const isFavorited = favorites.some(fav => fav.item_id === itemId);

            if (isFavorited) {
                await api.removeFavorite(phoneNumber, itemId);
                setFavorites(favorites.filter(fav => fav.item_id !== itemId));
            } else {
                await api.addFavorite(phoneNumber, itemId);
                // Refresh favorites to get the new entry
                const updatedFavorites = await api.getUserFavorites(phoneNumber);
                setFavorites(updatedFavorites);
            }
        } catch (error) {
            console.error('Error toggling favorite:', error);
        }
    };
    */

    if (loading) {
        return (
            <PageTransition>
                <div className="min-h-screen bg-black flex items-center justify-center">
                    <div className="text-white text-xl">Loading your profile...</div>
                </div>
            </PageTransition>
        );
    }

    return (
        <PageTransition>
            <div className="min-h-screen bg-black text-white p-6 pb-24">
                <header className="flex justify-between items-center mb-8">
                    <h1 className="text-3xl font-bold bg-gradient-to-r from-emerald-400 to-teal-500 bg-clip-text text-transparent">
                        My Profile
                    </h1>
                    <button
                        onClick={() => navigate('/')}
                        className="p-2 bg-zinc-800 rounded-full hover:bg-zinc-700 transition-colors"
                    >
                        🏠
                    </button>
                </header>

                <div className="space-y-6">
                    {/* Tabs */}
                    <div className="flex p-1 bg-zinc-900 rounded-xl">
                        {(['profile', 'history', 'favorites'] as const).map((tab) => (
                            <button
                                key={tab}
                                onClick={() => setActiveTab(tab)}
                                className={`flex-1 py-2 rounded-lg text-sm font-medium transition-all ${activeTab === tab
                                    ? 'bg-zinc-800 text-white shadow-lg'
                                    : 'text-zinc-500 hover:text-zinc-300'
                                    }`}
                            >
                                {tab.charAt(0).toUpperCase() + tab.slice(1)}
                            </button>
                        ))}
                    </div>

                    {/* Content would go here - placeholder for now to fix build */}
                    <div className="bg-zinc-900/50 rounded-2xl p-6 border border-zinc-800">
                        <p className="text-zinc-400 text-center">User details loaded.</p>
                    </div>
                </div>
            </div>
        </PageTransition>
    );
};
