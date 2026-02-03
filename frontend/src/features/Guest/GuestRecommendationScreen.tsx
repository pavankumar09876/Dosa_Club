import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { message, Spin } from 'antd';
import { PageTransition } from '../../components/PageTransition';
import { SuggestionResponse, GuestSessionResponse } from '../../types';
import { RecommendationDisplay } from '../Recommendation/components/RecommendationDisplay';

/**
 * Guest Recommendation Screen
 * Displays food recommendation for guest users
 */
export const GuestRecommendationScreen = () => {
    const navigate = useNavigate();
    const [suggestion, setSuggestion] = useState<SuggestionResponse | null>(null);
    const [sessionData, setSessionData] = useState<GuestSessionResponse | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Load suggestion and session data from sessionStorage
        const storedSuggestion = sessionStorage.getItem('guestSuggestion');
        const storedSession = sessionStorage.getItem('guestSessionData');

        if (storedSuggestion && storedSession) {
            try {
                setSuggestion(JSON.parse(storedSuggestion));
                setSessionData(JSON.parse(storedSession));
                setLoading(false);
            } catch (error) {
                message.error('Failed to load recommendation data');
                navigate('/mode-selection');
            }
        } else {
            message.error('No recommendation found. Please start again.');
            navigate('/mode-selection');
        }
    }, [navigate]);

    const handleStartOver = () => {
        // Clear guest session data
        sessionStorage.removeItem('guestSuggestion');
        sessionStorage.removeItem('guestSessionData');
        navigate('/');
    };

    if (loading) {
        return (
            <PageTransition>
                <div className="min-h-screen flex items-center justify-center bg-black text-white">
                    <div className="text-center">
                        <Spin size="large" />
                        <p className="mt-4">Loading your recommendation...</p>
                    </div>
                </div>
            </PageTransition>
        );
    }

    if (!suggestion || !sessionData) {
        return null; // Redirect handled in useEffect
    }

    return (
        <PageTransition>
            <div className="min-h-screen flex flex-col items-center justify-center px-6 py-12 bg-black text-white relative overflow-hidden">
                {/* Ambient Background */}
                <div className="absolute inset-0 opacity-20 pointer-events-none">
                    <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full filter blur-3xl animate-pulse-slow" />
                    <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-400/10 rounded-full filter blur-3xl animate-pulse-slow" />
                </div>

                <RecommendationDisplay
                    suggestion={suggestion}
                    sessionData={sessionData}
                    mode="guest"
                    onRestart={handleStartOver}
                    onExplore={() => navigate('/explore')}
                    onCreateAccount={() => navigate('/start')}
                />
            </div>
        </PageTransition>
    );
};
