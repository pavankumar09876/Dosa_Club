import { motion } from 'framer-motion';
import { useState } from 'react';
import { Form, App } from 'antd';
import {
    TrophyOutlined,
    RiseOutlined,
    FallOutlined,
} from '@ant-design/icons';
import { AnimatedButton } from '../../../components/AnimatedButton';

interface FitnessGoalQuestionProps {
    onNext: (data: Record<string, any>) => void;
    onBack: () => void;
}

/**
 * Fitness Goal & Spice Tolerance Question - Step 5 (Final)
 */
export const FitnessGoalQuestion: React.FC<FitnessGoalQuestionProps> = ({
    onNext,
    onBack,
}) => {
    const { message } = App.useApp();
    const [selectedGoal, setSelectedGoal] = useState<string>('');
    const [selectedSpice, setSelectedSpice] = useState<string>('');

    const handleSubmit = () => {
        if (!selectedGoal || !selectedSpice) {
            message.error('Please complete both selections');
            return;
        }

        onNext({ health_goal: selectedGoal, spice_tolerance: selectedSpice });
    };

    const fitnessGoals = [
        {
            value: 'weight_loss',
            label: 'Weight Loss',
            icon: <FallOutlined />,
            description: 'Lower calorie options',
        },
        {
            value: 'weight_gain',
            label: 'Weight Gain',
            icon: <RiseOutlined />,
            description: 'Higher calorie meals',
        },
        {
            value: 'balanced',
            label: 'Stay Balanced',
            icon: <TrophyOutlined />,
            description: 'Maintain current health',
        },
    ];

    const spiceLevels = [
        { value: 'low', label: 'Mild', emoji: '😌' },
        { value: 'medium', label: 'Medium', emoji: '🌶️' },
        { value: 'high', label: 'Spicy', emoji: '🔥' },
    ];

    return (
        <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ type: 'spring', damping: 25, stiffness: 120 }}
            className="max-w-4xl mx-auto px-6 py-12"
        >
            <div className="relative z-10 text-center mb-12">
                <h2 className="font-display font-bold text-4xl md:text-5xl text-white mb-4">
                    Final Preferences
                </h2>
                <p className="text-zinc-400 text-lg">
                    Almost done! Just two more quick questions
                </p>
            </div>

            <Form onFinish={handleSubmit} className="relative z-10 space-y-12">
                {/* Fitness Goal */}
                <div className="relative z-10">
                    <h3 className="text-white text-2xl font-semibold mb-6 text-center">
                        What's your health goal?
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {fitnessGoals.map((goal, index) => (
                            <motion.div
                                key={goal.value}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.1 * index, type: 'spring', damping: 20 }}
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={() => setSelectedGoal(goal.value)}
                                className={`
                  cursor-pointer p-6 rounded-2xl border-2 transition-all gpu-accelerated
                  ${selectedGoal === goal.value
                                        ? 'bg-dosa-heat/20 border-dosa-heat'
                                        : 'bg-zinc-900 border-zinc-800 hover:border-zinc-700'
                                    }
                `}
                            >
                                <div className="text-center">
                                    <div
                                        className={`text-4xl mb-3 ${selectedGoal === goal.value ? 'text-dosa-heat' : 'text-zinc-400'
                                            }`}
                                    >
                                        {goal.icon}
                                    </div>
                                    <h4 className="text-white font-semibold text-lg mb-1">
                                        {goal.label}
                                    </h4>
                                    <p className="text-zinc-500 text-sm">{goal.description}</p>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>

                {/* Spice Tolerance */}
                <div className="relative z-10">
                    <h3 className="text-white text-2xl font-semibold mb-6 text-center">
                        How spicy do you like it?
                    </h3>
                    <div className="grid grid-cols-3 gap-4 max-w-2xl mx-auto">
                        {spiceLevels.map((spice, index) => (
                            <motion.div
                                key={spice.value}
                                initial={{ opacity: 0, scale: 0.8 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ delay: 0.6 + 0.1 * index, type: 'spring', damping: 20 }}
                                whileHover={{ scale: 1.1 }}
                                whileTap={{ scale: 0.9 }}
                                onClick={() => setSelectedSpice(spice.value)}
                                className={`
                  cursor-pointer p-6 rounded-2xl border-2 transition-all gpu-accelerated
                  ${selectedSpice === spice.value
                                        ? 'bg-dosa-heat/20 border-dosa-heat'
                                        : 'bg-zinc-900 border-zinc-800 hover:border-zinc-700'
                                    }
                `}
                            >
                                <div className="text-center">
                                    <div className="text-5xl mb-2">{spice.emoji}</div>
                                    <p className="text-white font-medium">{spice.label}</p>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>

                {/* Navigation Buttons */}
                <div className="relative z-10 flex gap-4 pt-6">
                    <AnimatedButton type="button" variant="secondary" onClick={onBack} fullWidth>
                        Back
                    </AnimatedButton>
                    <AnimatedButton type="submit" variant="primary" fullWidth>
                        Get My Recommendation
                    </AnimatedButton>
                </div>
            </Form>
        </motion.div>
    );
};
