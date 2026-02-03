import { motion } from 'framer-motion';
import { useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Button, Progress, Input, Select, Radio } from 'antd';
import { ArrowLeftOutlined, ArrowRightOutlined } from '@ant-design/icons';

const { Option } = Select;

interface MobileQuestionnaireData {
    age?: number;
    gender?: string;
    height?: number;
    weight?: number;
    activity_level?: string;
    diet_type?: string;
    fitness_goal?: string;
    medical_conditions?: string[];
}

/**
 * Mobile Questionnaire Screen
 * Optimized questionnaire experience for mobile devices
 */
export const MobileQuestionnaireScreen = () => {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const sessionId = searchParams.get('session') || 'unknown';
    
    const [currentStep, setCurrentStep] = useState(0);
    const [questionnaireData, setQuestionnaireData] = useState<MobileQuestionnaireData>({});
    const [isSubmitting, setIsSubmitting] = useState(false);

    // Mobile-optimized questions configuration
    const mobileQuestions = [
        {
            key: 'age',
            title: 'What\'s your age?',
            icon: '🎂',
            render: () => (
                <div className="space-y-4">
                    <Input
                        type="number"
                        placeholder="Enter your age"
                        size="large"
                        value={questionnaireData.age || ''}
                        onChange={(e) => {
                            const value = e.target.value;
                            if (value) {
                                const numValue = parseInt(value);
                                if (!isNaN(numValue) && numValue >= 1 && numValue <= 120) {
                                    updateData('age', numValue);
                                }
                            }
                        }}
                        className="text-center text-lg h-14 bg-zinc-800 border-zinc-600 hover:border-zinc-500 focus:border-blue-500"
                        min={1}
                        max={120}
                        style={{ fontSize: '18px' }}
                    />
                </div>
            )
        },
        {
            key: 'gender',
            title: 'What\'s your gender?',
            icon: '👤',
            render: () => (
                <div className="space-y-4">
                    <Radio.Group
                        value={questionnaireData.gender}
                        onChange={(e) => updateData('gender', e.target.value)}
                        className="w-full"
                        size="large"
                    >
                        <div className="space-y-3">
                            <Radio.Button 
                                value="male" 
                                className="w-full h-14 text-center text-base flex items-center justify-center bg-zinc-800 border-zinc-600 hover:border-zinc-500"
                            >
                                👨 Male
                            </Radio.Button>
                            <Radio.Button 
                                value="female" 
                                className="w-full h-14 text-center text-base flex items-center justify-center bg-zinc-800 border-zinc-600 hover:border-zinc-500"
                            >
                                👩 Female
                            </Radio.Button>
                            <Radio.Button 
                                value="other" 
                                className="w-full h-14 text-center text-base flex items-center justify-center bg-zinc-800 border-zinc-600 hover:border-zinc-500"
                            >
                                🧑 Other
                            </Radio.Button>
                        </div>
                    </Radio.Group>
                </div>
            )
        },
        {
            key: 'height_weight',
            title: 'Height & Weight',
            icon: '📏',
            render: () => (
                <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-3">
                        <div>
                            <label className="text-zinc-400 text-sm mb-2 block">Height (cm)</label>
                            <Input
                                type="number"
                                placeholder="170"
                                size="large"
                                value={questionnaireData.height || ''}
                                onChange={(e) => {
                                    const value = e.target.value;
                                    if (value) {
                                        const numValue = parseInt(value);
                                        if (!isNaN(numValue) && numValue >= 100 && numValue <= 250) {
                                            updateData('height', numValue);
                                        }
                                    }
                                }}
                                className="text-center h-12 bg-zinc-800 border-zinc-600 hover:border-zinc-500 focus:border-blue-500"
                                min={100}
                                max={250}
                            />
                        </div>
                        <div>
                            <label className="text-zinc-400 text-sm mb-2 block">Weight (kg)</label>
                            <Input
                                type="number"
                                placeholder="70"
                                size="large"
                                value={questionnaireData.weight || ''}
                                onChange={(e) => {
                                    const value = e.target.value;
                                    if (value) {
                                        const numValue = parseInt(value);
                                        if (!isNaN(numValue) && numValue >= 30 && numValue <= 200) {
                                            updateData('weight', numValue);
                                        }
                                    }
                                }}
                                className="text-center h-12 bg-zinc-800 border-zinc-600 hover:border-zinc-500 focus:border-blue-500"
                                min={30}
                                max={200}
                            />
                        </div>
                    </div>
                </div>
            )
        },
        {
            key: 'diet_type',
            title: 'Dietary Preference',
            icon: '🥗',
            render: () => (
                <div className="space-y-4">
                    <Select
                        value={questionnaireData.diet_type}
                        onChange={(value) => updateData('diet_type', value)}
                        className="w-full"
                        size="large"
                        placeholder="Select your diet type"
                        style={{ height: '48px', backgroundColor: '#27272a', borderColor: '#52525b' }}
                    >
                        <Option value="vegetarian">🥗 Vegetarian</Option>
                        <Option value="vegan">🌱 Vegan</Option>
                        <Option value="eggetarian">🥚 Eggetarian</Option>
                        <Option value="non-vegetarian">🍗 Non-Vegetarian</Option>
                    </Select>
                </div>
            )
        },
        {
            key: 'fitness_goal',
            title: 'Fitness Goal',
            icon: '🎯',
            render: () => (
                <div className="space-y-4">
                    <Radio.Group
                        value={questionnaireData.fitness_goal}
                        onChange={(e) => updateData('fitness_goal', e.target.value)}
                        className="w-full"
                        size="large"
                    >
                        <div className="space-y-3">
                            <Radio.Button 
                                value="weight_loss" 
                                className="w-full h-14 text-center text-base flex items-center justify-center bg-zinc-800 border-zinc-600 hover:border-zinc-500"
                            >
                                ⬇️ Weight Loss
                            </Radio.Button>
                            <Radio.Button 
                                value="muscle_gain" 
                                className="w-full h-14 text-center text-base flex items-center justify-center bg-zinc-800 border-zinc-600 hover:border-zinc-500"
                            >
                                💪 Muscle Gain
                            </Radio.Button>
                            <Radio.Button 
                                value="maintenance" 
                                className="w-full h-14 text-center text-base flex items-center justify-center bg-zinc-800 border-zinc-600 hover:border-zinc-500"
                            >
                                ⚖️ Maintain Weight
                            </Radio.Button>
                            <Radio.Button 
                                value="general_fitness" 
                                className="w-full h-14 text-center text-base flex items-center justify-center bg-zinc-800 border-zinc-600 hover:border-zinc-500"
                            >
                                🏃 General Fitness
                            </Radio.Button>
                        </div>
                    </Radio.Group>
                </div>
            )
        }
    ];

    const updateData = (key: keyof MobileQuestionnaireData, value: any) => {
        setQuestionnaireData(prev => ({
            ...prev,
            [key]: value
        }));
    };

    const handleNext = () => {
        if (currentStep < mobileQuestions.length - 1) {
            setCurrentStep(currentStep + 1);
        } else {
            handleSubmitQuestionnaire();
        }
    };

    const handlePrevious = () => {
        if (currentStep > 0) {
            setCurrentStep(currentStep - 1);
        }
    };

    const handleSubmitQuestionnaire = async () => {
        setIsSubmitting(true);
        
        try {
            // Simulate API call to submit questionnaire
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Navigate to mobile recommendation page
            navigate(`/mobile/recommendation?session=${sessionId}`, {
                state: { questionnaireData }
            });
            
        } catch (error) {
            console.error('Error submitting questionnaire:', error);
        } finally {
            setIsSubmitting(false);
        }
    };

    const progress = ((currentStep + 1) / mobileQuestions.length) * 100;
    const currentQuestionKey = mobileQuestions[currentStep].key;
    
    // More lenient validation - check if value exists and is valid
    const isCurrentStepValid = () => {
        const value = questionnaireData[currentQuestionKey as keyof MobileQuestionnaireData];
        
        // For age, check if it's a valid number between 1 and 120
        if (currentQuestionKey === 'age') {
            return typeof value === 'number' && value >= 1 && value <= 120;
        }
        
        // For height and weight, check if they are valid numbers
        if (currentQuestionKey === 'height') {
            return typeof value === 'number' && value >= 100 && value <= 250;
        }
        
        if (currentQuestionKey === 'weight') {
            return typeof value === 'number' && value >= 30 && value <= 200;
        }
        
        // For other fields, check if value exists and is not empty
        return value !== undefined && value !== null && value !== '';
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-black via-zinc-900 to-zinc-800 text-white relative overflow-hidden">
            {/* Mobile Header */}
            <div className="sticky top-0 z-50 bg-black/90 backdrop-blur-xl border-b border-zinc-700">
                <div className="px-4 py-3">
                    <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-2">
                            <span className="text-lg">📱</span>
                            <span className="text-sm font-medium text-zinc-400">Mobile Quiz</span>
                        </div>
                        <div className="text-xs text-zinc-500">
                            Session: {sessionId.slice(-8)}
                        </div>
                    </div>
                    
                    {/* Progress Bar */}
                    <Progress 
                        percent={progress} 
                        showInfo={false}
                        strokeColor={{
                            '0%': '#3b82f6',
                            '100%': '#8b5cf6',
                        }}
                        trailColor="#374151"
                        strokeWidth={6}
                        className="mb-2"
                    />
                    
                    <div className="flex items-center justify-between text-xs text-zinc-400">
                        <span>Step {currentStep + 1} of {mobileQuestions.length}</span>
                        <span>{Math.round(progress)}% Complete</span>
                    </div>
                </div>
            </div>

            {/* Question Content */}
            <div className="px-4 py-6 pb-32 relative z-10">
                <motion.div
                    key={currentStep}
                    initial={{ x: 300, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    exit={{ x: -300, opacity: 0 }}
                    transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                    className="max-w-lg mx-auto"
                >
                    {/* Question Header */}
                    <div className="text-center mb-8">
                        <motion.div
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            transition={{ type: 'spring', stiffness: 200 }}
                            className="text-6xl mb-4"
                        >
                            {mobileQuestions[currentStep].icon}
                        </motion.div>
                        
                        <h2 className="text-2xl font-bold text-white mb-2">
                            {mobileQuestions[currentStep].title}
                        </h2>
                        
                        <div className="w-16 h-1 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full mx-auto"></div>
                    </div>

                    {/* Question Component */}
                    <div className="mb-8">
                        {mobileQuestions[currentStep].render()}
                    </div>

                    {/* Navigation Buttons */}
                    <div className="flex gap-3">
                        {currentStep > 0 && (
                            <Button
                                onClick={handlePrevious}
                                className="flex-1 bg-zinc-800 border-zinc-700 hover:bg-zinc-700 text-white h-14"
                                icon={<ArrowLeftOutlined />}
                                size="large"
                            >
                                Previous
                            </Button>
                        )}
                        
                        <Button
                            onClick={handleNext}
                            loading={isSubmitting}
                            disabled={!isCurrentStepValid()}
                            className={`flex-1 h-14 ${
                                currentStep === mobileQuestions.length - 1
                                    ? 'bg-gradient-to-r from-green-500 to-green-600 border-0 hover:from-green-600 hover:to-green-700'
                                    : 'bg-gradient-to-r from-blue-500 to-purple-500 border-0 hover:from-blue-600 hover:to-purple-600'
                            } text-white font-medium`}
                            icon={currentStep === mobileQuestions.length - 1 ? null : <ArrowRightOutlined />}
                            size="large"
                        >
                            {currentStep === mobileQuestions.length - 1 
                                ? isSubmitting ? 'Submitting...' : 'Get Recommendation'
                                : 'Next'
                            }
                        </Button>
                    </div>
                </motion.div>
            </div>

            {/* Mobile Footer */}
            <div className="fixed bottom-0 left-0 right-0 z-50 bg-black/90 backdrop-blur-xl border-t border-zinc-700 px-4 py-3">
                <div className="flex items-center justify-between text-xs text-zinc-500">
                    <div className="flex items-center gap-2">
                        <span>💙</span>
                        <span>Mobile Optimized</span>
                    </div>
                    <div>
                        <span>Tap to continue</span>
                    </div>
                </div>
            </div>
        </div>
    );
};
