import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { message } from 'antd';
import { PageTransition } from '../../components/PageTransition';
import { apiService } from '../../services/api';
import { GuestData, GuestSessionResponse, GuestSuggestionRequest } from '../../types';
import { AgeQuestion } from '../Questionnaire/questions/AgeQuestion';
import { BodyMetricsQuestion } from '../Questionnaire/questions/BodyMetricsQuestion';
import { DietTypeQuestion } from '../Questionnaire/questions/DietTypeQuestion';
import { FitnessGoalQuestion } from '../Questionnaire/questions/FitnessGoalQuestion';
import { MedicalConditionQuestion } from '../Questionnaire/questions/MedicalConditionQuestion';
import { HealthMetricsQuestion } from '../Questionnaire/questions/HealthMetricsQuestion';
import { SpiceLevelQuestion } from '../Questionnaire/questions/SpiceLevelQuestion';

/**
 * Guest Questionnaire Screen
 * Health questionnaire for guest users using shared reusable components
 */
export const GuestQuestionnaireScreen = () => {
    const navigate = useNavigate();
    const [currentStep, setCurrentStep] = useState(0);
    const [loading, setLoading] = useState(false);
    const [sessionData, setSessionData] = useState<GuestSessionResponse | null>(null);
    const [formData, setFormData] = useState<Partial<GuestData>>({});

    // Create guest session on component mount
    useEffect(() => {
        const createSession = async () => {
            try {
                setLoading(true);
                const session = await apiService.createGuestSession();
                setSessionData(session);

                // Set session expiry warning
                const expiryTime = new Date(session.expires_at);
                const timeUntilExpiry = expiryTime.getTime() - Date.now();

                if (timeUntilExpiry > 0) {
                    setTimeout(() => {
                        message.warning('Your guest session will expire in 5 minutes');
                    }, timeUntilExpiry - 5 * 60 * 1000);
                }

                setLoading(false);
            } catch (error) {
                message.error('Failed to create guest session');
                navigate('/mode-selection');
            }
        };

        createSession();
    }, [navigate]);

    const handleStepNext = async (stepData: Partial<GuestData>) => {
        const updatedData = { ...formData, ...stepData };
        setFormData(updatedData);

        if (currentStep === 4) { // Last step (Medical Condition)
            await handleSubmit(updatedData as GuestData);
        } else {
            setCurrentStep(prev => prev + 1);
        }
    };

    const handleStepBack = () => {
        if (currentStep === 0) {
            navigate('/mode-selection');
        } else {
            setCurrentStep(prev => prev - 1);
        }
    };

    const handleSubmit = async (completeData: GuestData) => {
        if (!sessionData) {
            message.error('Session expired. Please start again.');
            navigate('/mode-selection');
            return;
        }

        try {
            setLoading(true);

            // Merge form data with defaults to ensure all required fields are present
            const healthData: GuestData = {
                age: completeData.age || formData.age || 25,
                gender: completeData.gender || formData.gender || 'other',
                height_cm: completeData.height_cm || formData.height_cm || 170,
                weight_kg: completeData.weight_kg || formData.weight_kg || 70,
                diet_type: completeData.diet_type || formData.diet_type || 'veg',
                health_goal: completeData.health_goal || formData.health_goal || 'balanced',
                medical_condition: completeData.medical_condition || formData.medical_condition || 'none',
                spice_tolerance: completeData.spice_tolerance || formData.spice_tolerance || 'medium',
                ...completeData // Override with any provided data
            };

            // Debug: Log the data being sent
            console.log('Guest Session Data:', sessionData);
            console.log('Form Data:', formData);
            console.log('Complete Health Data:', completeData);
            console.log('Final Health Data:', healthData);

            const suggestionRequest: GuestSuggestionRequest = {
                session_id: sessionData.session_id,
                health_data: healthData
            };

            console.log('Suggestion Request:', suggestionRequest);

            const suggestion = await apiService.getGuestSuggestion(suggestionRequest);

            console.log('Suggestion Response:', suggestion);

            // Store suggestion data and navigate to recommendation
            sessionStorage.setItem('guestSuggestion', JSON.stringify(suggestion));
            sessionStorage.setItem('guestSessionData', JSON.stringify(sessionData));

            navigate('/guest/recommendation');
        } catch (error: any) {
            console.error('Guest Suggestion Error:', error);
            
            // Try to provide a fallback response
            if (error?.response?.status === 500 || error?.response?.status === 404) {
                // Server error - provide fallback suggestion
                const fallbackSuggestion = {
                    health_summary: "Based on your profile, we recommend a balanced diet approach.",
                    bmi_category: "normal",
                    suggested_item: "Plain Dosa",
                    suggested_item_details: null,
                    similar_items: [],
                    reason: "Safe, nutritious option suitable for your health profile."
                };
                
                sessionStorage.setItem('guestSuggestion', JSON.stringify(fallbackSuggestion));
                sessionStorage.setItem('guestSessionData', JSON.stringify(sessionData));
                navigate('/guest/recommendation');
                return;
            }
            
            if (error?.detail?.includes('Invalid or expired guest session')) {
                message.error('Session expired. Please start again.');
                navigate('/mode-selection');
            } else if (error?.response?.data) {
                // Handle API error response
                const errorMessage = error.response.data.detail || error.response.data.message || 'Failed to get recommendation';
                message.error(errorMessage);
            } else if (error?.message) {
                // Handle network or other errors
                message.error(`Error: ${error.message}`);
            } else {
                // Generic error
                message.error('Failed to get recommendation. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    if (loading && !sessionData && currentStep === 0) {
        return (
            <PageTransition>
                <div className="min-h-screen flex items-center justify-center bg-black text-white">
                    <div className="text-center">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-400 mx-auto mb-4"></div>
                        <p>Setting up your guest session...</p>
                    </div>
                </div>
            </PageTransition>
        );
    }

    if (loading && currentStep === 6) {
        return (
            <PageTransition>
                <div className="min-h-screen flex items-center justify-center bg-black text-white">
                    <div className="text-center">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-400 mx-auto mb-4"></div>
                        <p>Generating your personalized recommendation...</p>
                    </div>
                </div>
            </PageTransition>
        );
    }

    const renderCurrentStep = () => {
        const commonProps = {
            onBack: handleStepBack,
        };

        switch (currentStep) {
            case 0:
                return (
                    <AgeQuestion
                        {...commonProps}
                        onNext={(data) => handleStepNext(data as Partial<GuestData>)}
                    />
                );
            case 1:
                return (
                    <BodyMetricsQuestion
                        {...commonProps}
                        onNext={(data) => handleStepNext(data as Partial<GuestData>)}
                    />
                );
            case 2:
                // Note: GuestDietTypeQuestion vs DietTypeQuestion? 
                // DietTypeQuestion is "Step 3" in folder
                return (
                    <DietTypeQuestion
                        {...commonProps}
                        onNext={(data) => handleStepNext(data as Partial<GuestData>)}
                    />
                );
            case 3:
                return (
                    <MedicalConditionQuestion
                        {...commonProps}
                        onNext={(data) => handleStepNext(data as Partial<GuestData>)}
                    />
                );
            case 4:
                return (
                    <HealthMetricsQuestion
                        {...commonProps}
                        onNext={(data) => handleStepNext(data as Partial<GuestData>)}
                    />
                );
            case 5:
                return (
                    <SpiceLevelQuestion
                        {...commonProps}
                        onNext={(data) => handleStepNext(data as Partial<GuestData>)}
                    />
                );
            case 6:
                return (
                    <FitnessGoalQuestion
                        {...commonProps}
                        onNext={(data) => handleSubmit(data as GuestData)}
                    />
                );
            default:
                return null;
        }
    };

    return (
        <PageTransition>
            <div className="min-h-screen bg-black text-white relative overflow-hidden">
                {/* Ambient Background */}
                <div className="absolute inset-0 opacity-20 pointer-events-none">
                    <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full filter blur-3xl animate-pulse-slow" />
                    <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-400/10 rounded-full filter blur-3xl animate-pulse-slow" />
                </div>

                <div className="relative z-10 min-h-screen flex flex-col">
                    {/* Header / Progress Indicator could go here if needed, but components have their own headers */}
                    <div className="p-6">
                        <div className="flex justify-between items-center max-w-6xl mx-auto">
                            <div className="text-zinc-500 text-sm">Guest Mode</div>
                            {sessionData && (
                                <div className="text-purple-400 text-sm">
                                    Expires: {new Date(sessionData.expires_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                </div>
                            )}
                        </div>
                        {/* Simple Progress Bar */}
                        <div className="max-w-xl mx-auto mt-4 h-1 bg-zinc-800 rounded-full overflow-hidden">
                            <motion.div
                                className="h-full bg-purple-500"
                                initial={{ width: 0 }}
                                animate={{ width: `${((currentStep + 1) / 7) * 100}%` }}
                                transition={{ duration: 0.3 }}
                            />
                        </div>
                    </div>

                    <div className="flex-1 flex items-center justify-center">
                        <AnimatePresence mode="wait">
                            <motion.div
                                key={currentStep}
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                transition={{ duration: 0.3 }}
                                className="w-full"
                            >
                                {renderCurrentStep()}
                            </motion.div>
                        </AnimatePresence>
                    </div>
                </div>
            </div>
        </PageTransition>
    );
};
