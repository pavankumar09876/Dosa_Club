import { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { App } from 'antd';
import { useUserData } from '../../context/UserContext';
import { PageTransition } from '../../components/PageTransition';
import { RecommendationDisplay } from './components/RecommendationDisplay';
import { SuggestionResponse } from '../../types';

/**
 * User Recommendation Screen
 * Displays AI recommendation for logged-in/registered users
 */
export const RecommendationScreen = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { message } = App.useApp();
    const { userData } = useUserData();
    const suggestion = location.state?.recommendation as SuggestionResponse | undefined;

    useEffect(() => {
        if (!suggestion) {
            message.warning('Recommendation session expired or invalid.');
            navigate('/start');
        }
    }, [suggestion, navigate, message]);

    const handleStartOver = () => {
        navigate('/');
    };

    if (!suggestion) {
        return null; // Redirect handled in useEffect
    }

    return (
        <PageTransition>
            <div className="min-h-screen flex flex-col items-center justify-center px-4 py-8 bg-black text-white relative overflow-hidden">
                {/* Ambient Background Elements */}
                <div className="absolute inset-0 pointer-events-none overflow-hidden">
                    <div className="absolute -top-1/2 -left-1/2 w-[100vw] h-[100vw] bg-purple-900/10 rounded-full filter blur-[120px] animate-pulse-slow" />
                    <div className="absolute -bottom-1/2 -right-1/2 w-[100vw] h-[100vw] bg-orange-900/10 rounded-full filter blur-[120px] animate-pulse-slow delay-1000" />
                </div>

                <RecommendationDisplay
                    suggestion={suggestion}
                    mode="user"
                    onRestart={handleStartOver}
                    onExplore={() => navigate('/explore')}
                    userName={userData.name}
                />
            </div>
        </PageTransition>
    );
};
