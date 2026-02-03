import { motion } from 'framer-motion';

interface ProgressBarProps {
    currentStep: number;
    totalSteps: number;
}

/**
 * Animated Progress Bar
 * Shows user progress through multi-step questionnaire
 */
export const ProgressBar: React.FC<ProgressBarProps> = ({ currentStep, totalSteps }) => {
    const progress = (currentStep / totalSteps) * 100;

    return (
        <div className="w-full max-w-2xl mx-auto px-6 py-8">
            {/* Header info */}
            <div className="flex justify-between items-end mb-4">
                <div>
                    <span className="text-xs font-bold text-dosa-heat uppercase tracking-wider block mb-1">
                        Step {currentStep} of {totalSteps}
                    </span>
                    <h2 className="text-lg font-display text-white">
                        {currentStep === 1 && "Basic Details"}
                        {currentStep === 2 && "Body Metrics"}
                        {currentStep === 3 && "Diet Preference"}
                        {currentStep === 4 && "Medical History"}
                        {currentStep === 5 && "Health Metrics"}
                        {currentStep === 6 && "Fitness Goal"}
                    </h2>
                </div>
                <div className="text-right">
                    <span className="text-2xl font-bold text-white">{Math.round(progress)}%</span>
                </div>
            </div>

            {/* Segmented Progress Bar */}
            <div className="flex gap-2 h-3">
                {Array.from({ length: totalSteps }).map((_, index) => {
                    const stepNum = index + 1;
                    const isActive = stepNum === currentStep;
                    const isCompleted = stepNum < currentStep;

                    return (
                        <div key={index} className="flex-1 relative h-full bg-zinc-800 rounded-full overflow-hidden">
                            {/* Background for future steps */}
                            <div className="absolute inset-0 bg-zinc-800" />

                            {/* Completed Step Fill */}
                            {isCompleted && (
                                <motion.div
                                    initial={{ width: 0 }}
                                    animate={{ width: "100%" }}
                                    className="absolute inset-0 bg-gradient-to-r from-dosa-heat to-dosa-warm"
                                />
                            )}

                            {/* Active Step Fill & Pulse */}
                            {isActive && (
                                <>
                                    <motion.div
                                        initial={{ width: 0 }}
                                        animate={{ width: "100%" }}
                                        transition={{ duration: 0.5, ease: "easeOut" }}
                                        className="absolute inset-0 bg-gradient-to-r from-dosa-heat to-dosa-warm"
                                    />
                                    <motion.div
                                        className="absolute inset-0 bg-white/30"
                                        animate={{ opacity: [0, 0.5, 0] }}
                                        transition={{ duration: 1.5, repeat: Infinity }}
                                    />
                                </>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};
