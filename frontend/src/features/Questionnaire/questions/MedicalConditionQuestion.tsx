import { motion } from 'framer-motion';
import { useState } from 'react';
import { Form, App } from 'antd';
import {
    HeartOutlined,
    MedicineBoxOutlined,
    FireOutlined,
    CheckCircleOutlined,
} from '@ant-design/icons';
import { AnimatedButton } from '../../../components/AnimatedButton';

interface MedicalConditionQuestionProps {
    onNext: (data: Record<string, any>) => void;
    onBack: () => void;
}

/**
 * Medical Condition Question - Step 4
 */
export const MedicalConditionQuestion: React.FC<MedicalConditionQuestionProps> = ({
    onNext,
    onBack,
}) => {
    const { message } = App.useApp();
    const [selectedCondition, setSelectedCondition] = useState<string>('');

    const handleSubmit = () => {
        if (!selectedCondition) {
            message.error('Please select a medical condition');
            return;
        }

        onNext({ medical_condition: selectedCondition });
    };

    const conditions = [
        {
            value: 'none',
            label: 'None',
            icon: <CheckCircleOutlined />,
            description: 'No known conditions',
        },
        {
            value: 'diabetes',
            label: 'Diabetes',
            icon: <MedicineBoxOutlined />,
            description: 'Low sugar recommendations',
        },
        {
            value: 'bp',
            label: 'Blood Pressure',
            icon: <HeartOutlined />,
            description: 'Low sodium options',
        },
        {
            value: 'acidity',
            label: 'Acidity',
            icon: <FireOutlined />,
            description: 'Mild food suggestions',
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
                    Any Health Conditions?
                </h2>
                <p className="text-zinc-400 text-lg">
                    We'll ensure food suggestions are safe for you
                </p>
            </div>

            <Form onFinish={handleSubmit}>
                {/* Condition Selection Cards */}
                <div className="relative z-10 grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
                    {conditions.map((condition, index) => (
                        <motion.div
                            key={condition.value}
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{
                                delay: 0.1 * index,
                                type: 'spring',
                                damping: 20,
                                stiffness: 150,
                            }}
                            whileHover={{ scale: 1.05, y: -5 }}
                            whileTap={{ scale: 0.95 }}
                            onClick={() => setSelectedCondition(condition.value)}
                            className={`
                cursor-pointer p-6 rounded-2xl border-2 transition-all gpu-accelerated
                ${selectedCondition === condition.value
                                    ? 'bg-dosa-heat/20 border-dosa-heat shadow-lg shadow-dosa-heat/30'
                                    : 'bg-zinc-900 border-zinc-800 hover:border-zinc-700'
                                }
              `}
                        >
                            <div className="text-center">
                                <div
                                    className={`text-4xl mb-3 ${selectedCondition === condition.value
                                        ? 'text-dosa-heat'
                                        : 'text-zinc-400'
                                        }`}
                                >
                                    {condition.icon}
                                </div>
                                <h4 className="text-white font-semibold mb-1">{condition.label}</h4>
                                <p className="text-zinc-500 text-xs">{condition.description}</p>
                            </div>
                        </motion.div>
                    ))}
                </div>

                {/* Info Notice */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5 }}
                    className="relative z-10 bg-zinc-900/50 border border-zinc-800 rounded-xl p-4 mb-8"
                >
                    <p className="text-zinc-400 text-sm text-center">
                        🔒 Your health data is private and used only for personalized recommendations
                    </p>
                </motion.div>

                {/* Navigation Buttons */}
                <div className="relative z-10 flex gap-4">
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
