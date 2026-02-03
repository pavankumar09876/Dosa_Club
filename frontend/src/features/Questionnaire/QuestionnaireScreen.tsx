import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import { PageTransition } from '../../components/PageTransition';
import { ProgressBar } from '../../components/ProgressBar';
import { useUserData } from '../../context/UserContext';

// Import individual question components
import { AgeQuestion } from './questions/AgeQuestion';
import { BodyMetricsQuestion } from './questions/BodyMetricsQuestion';
import { DietTypeQuestion } from './questions/DietTypeQuestion';
import { MedicalConditionQuestion } from './questions/MedicalConditionQuestion';
import { HealthMetricsQuestion } from './questions/HealthMetricsQuestion';
import { FitnessGoalQuestion } from './questions/FitnessGoalQuestion';

const TOTAL_STEPS = 6;

/**
 * Questionnaire Screen - Screen 2
 * Multi-step health questionnaire with one question per screen
 */
export const QuestionnaireScreen = () => {
    const [currentStep, setCurrentStep] = useState(1);
    const navigate = useNavigate();
    const { updateUserData } = useUserData();

    const handleNext = (data: Record<string, any>) => {
        updateUserData(data);

        if (currentStep < TOTAL_STEPS) {
            setCurrentStep((prev) => prev + 1);
        } else {
            // All questions completed, move to processing
            navigate('/processing');
        }
    };

    const handleBack = () => {
        if (currentStep > 1) {
            setCurrentStep((prev) => prev - 1);
        } else {
            navigate('/start');
        }
    };

    const renderQuestion = () => {
        switch (currentStep) {
            case 1:
                return <AgeQuestion onNext={handleNext} onBack={handleBack} />;
            case 2:
                return <BodyMetricsQuestion onNext={handleNext} onBack={handleBack} />;
            case 3:
                return <DietTypeQuestion onNext={handleNext} onBack={handleBack} />;
            case 4:
                return <MedicalConditionQuestion onNext={handleNext} onBack={handleBack} />;
            case 5:
                return <HealthMetricsQuestion onNext={handleNext} onBack={handleBack} />;
            case 6:
                return <FitnessGoalQuestion onNext={handleNext} onBack={handleBack} />;
            default:
                return null;
        }
    };

    return (
        <PageTransition>
            <div className="min-h-screen bg-black text-white">
                {/* Progress Bar */}
                <ProgressBar currentStep={currentStep} totalSteps={TOTAL_STEPS} />

                {/* Question Content with AnimatePresence for smooth transitions */}
                <AnimatePresence mode="wait">
                    <div key={currentStep}>{renderQuestion()}</div>
                </AnimatePresence>
            </div>
        </PageTransition>
    );
};
