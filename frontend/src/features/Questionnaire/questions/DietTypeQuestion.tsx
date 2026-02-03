import { motion } from 'framer-motion';
import { useState } from 'react';
import { Form, message } from 'antd';
import { AnimatedButton } from '../../../components/AnimatedButton';

interface DietTypeQuestionProps {
    onNext: (data: Record<string, any>) => void;
    onBack: () => void;
}

/**
 * Diet Type Question - Step 3
 * Icon-based selection for diet preference
 */
export const DietTypeQuestion: React.FC<DietTypeQuestionProps> = ({ onNext, onBack }) => {
    const [form] = Form.useForm();
    const [selectedDiet, setSelectedDiet] = useState<string>('');

    const handleSubmit = () => {
        if (!selectedDiet) {
            message.error('Please select a diet type');
            return;
        }

        onNext({ diet_type: selectedDiet });
    };

    const dietOptions = [
        {
            value: 'veg',
            label: 'Vegetarian',
            emoji: '🥗',
            description: 'Plant-based foods only',
        },
        {
            value: 'egg',
            label: 'Eggetarian',
            emoji: '🥚',
            description: 'Veg + Eggs',
        },
        {
            value: 'non-veg',
            label: 'Non-Vegetarian',
            emoji: '🍗',
            description: 'All food types',
        },
    ];

    return (
        <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ type: 'spring', damping: 25, stiffness: 120 }}
            className="max-w-3xl mx-auto px-6 py-12"
        >
            <div className="relative z-10 text-center mb-12">
                <h2 className="font-display font-bold text-4xl md:text-5xl text-white mb-4">
                    Your Diet Preference
                </h2>
                <p className="text-zinc-400 text-lg">
                    We'll only suggest items that match your diet
                </p>
            </div>

            <Form form={form} onFinish={handleSubmit}>
                {/* Diet Type Selection - Large Icon Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
                    {dietOptions.map((option, index) => (
                        <motion.div
                            key={option.value}
                            initial={{ opacity: 0, y: 30 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.1 * index, type: 'spring', damping: 20 }}
                            whileHover={{ scale: 1.05, y: -5 }}
                            whileTap={{ scale: 0.95 }}
                            onClick={() => setSelectedDiet(option.value)}
                            className={`
                cursor-pointer p-8 rounded-3xl border-3 transition-all gpu-accelerated
                ${selectedDiet === option.value
                                    ? 'bg-dosa-heat/20 border-dosa-heat shadow-2xl shadow-dosa-heat/30'
                                    : 'bg-zinc-900 border-zinc-800 hover:border-zinc-700'
                                }
              `}
                        >
                            <div className="text-center">
                                <div className="text-6xl mb-4">{option.emoji}</div>
                                <h3 className="text-white font-display font-bold text-2xl mb-2">
                                    {option.label}
                                </h3>
                                <p className="text-zinc-400 text-sm">{option.description}</p>
                            </div>

                            {/* Selection indicator */}
                            {selectedDiet === option.value && (
                                <motion.div
                                    initial={{ scale: 0 }}
                                    animate={{ scale: 1 }}
                                    className="mt-4 flex justify-center"
                                >
                                    <div className="w-8 h-8 rounded-full bg-dosa-heat flex items-center justify-center">
                                        <svg
                                            className="w-5 h-5 text-black"
                                            fill="currentColor"
                                            viewBox="0 0 20 20"
                                        >
                                            <path
                                                fillRule="evenodd"
                                                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                                clipRule="evenodd"
                                            />
                                        </svg>
                                    </div>
                                </motion.div>
                            )}
                        </motion.div>
                    ))}
                </div>

                {/* Navigation Buttons */}
                <div className="flex gap-4">
                    <AnimatedButton type="button" variant="secondary" onClick={onBack} fullWidth>
                        Back
                    </AnimatedButton>
                    <AnimatedButton type="submit" variant="primary" fullWidth>
                        Next
                    </AnimatedButton>
                </div>
            </Form>
        </motion.div>
    );
};
