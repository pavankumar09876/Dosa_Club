import { motion } from 'framer-motion';
import { useState } from 'react';
import { Form, message } from 'antd';
import { AnimatedButton } from '../../../components/AnimatedButton';

interface SpiceLevelQuestionProps {
    onNext: (data: Record<string, any>) => void;
    onBack: () => void;
}

/**
 * Spice Level Question
 * Icon-based selection for spice tolerance
 */
export const SpiceLevelQuestion: React.FC<SpiceLevelQuestionProps> = ({ onNext, onBack }) => {
    const [form] = Form.useForm();
    const [selectedLevel, setSelectedLevel] = useState<string>('');

    const handleSubmit = () => {
        if (!selectedLevel) {
            message.error('Please select your spice tolerance');
            return;
        }
        onNext({ spice_tolerance: selectedLevel });
    };

    const spiceOptions = [
        {
            value: 'low',
            label: 'Low',
            emoji: '🌶️',
            description: 'Mild flavors, no heat',
            color: 'text-green-400'
        },
        {
            value: 'medium',
            label: 'Medium',
            emoji: '🌶️🌶️',
            description: 'Balanced kick',
            color: 'text-orange-400'
        },
        {
            value: 'high',
            label: 'High',
            emoji: '🌶️🌶️🌶️',
            description: 'Bring the heat!',
            color: 'text-red-500'
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
                    Spice Tolerance
                </h2>
                <p className="text-zinc-400 text-lg">
                    How much heat can you handle?
                </p>
            </div>

            <Form form={form} onFinish={handleSubmit}>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
                    {spiceOptions.map((option, index) => (
                        <motion.div
                            key={option.value}
                            initial={{ opacity: 0, y: 30 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.1 * index, type: 'spring', damping: 20 }}
                            whileHover={{ scale: 1.05, y: -5 }}
                            whileTap={{ scale: 0.95 }}
                            onClick={() => setSelectedLevel(option.value)}
                            className={`
                                cursor-pointer p-8 rounded-3xl border-3 transition-all gpu-accelerated
                                ${selectedLevel === option.value
                                    ? 'bg-dosa-heat/20 border-dosa-heat shadow-2xl shadow-dosa-heat/30'
                                    : 'bg-zinc-900 border-zinc-800 hover:border-zinc-700'
                                }
                            `}
                        >
                            <div className="text-center">
                                <div className="text-5xl mb-4 leading-relaxed h-16 flex items-center justify-center">
                                    {option.emoji}
                                </div>
                                <h3 className={`font-display font-bold text-2xl mb-2 ${selectedLevel === option.value ? 'text-white' : option.color}`}>
                                    {option.label}
                                </h3>
                                <p className="text-zinc-400 text-sm">{option.description}</p>
                            </div>

                            {selectedLevel === option.value && (
                                <motion.div
                                    initial={{ scale: 0 }}
                                    animate={{ scale: 1 }}
                                    className="mt-4 flex justify-center"
                                >
                                    <div className="w-8 h-8 rounded-full bg-dosa-heat flex items-center justify-center">
                                        <svg className="w-5 h-5 text-black" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                    </div>
                                </motion.div>
                            )}
                        </motion.div>
                    ))}
                </div>

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
