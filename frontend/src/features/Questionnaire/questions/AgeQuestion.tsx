import { motion } from 'framer-motion';
import { useState } from 'react';
import { Form, Input, message } from 'antd';
import { UserOutlined, ManOutlined, WomanOutlined } from '@ant-design/icons';
import { AnimatedButton } from '../../../components/AnimatedButton';

interface AgeQuestionProps {
    onNext: (data: Record<string, any>) => void;
    onBack: () => void;
}

/**
 * Age & Gender Question - Step 1
 */
export const AgeQuestion: React.FC<AgeQuestionProps> = ({ onNext, onBack }) => {
    const [form] = Form.useForm();
    const [selectedGender, setSelectedGender] = useState<string>('');

    const handleSubmit = (values: { age: number; gender: string }) => {
        if (!values.age || !values.gender) {
            message.error('Please complete all fields');
            return;
        }

        if (values.age < 1 || values.age > 120) {
            message.error('Age must be between 1 and 120');
            return;
        }

        onNext({ age: values.age, gender: values.gender });
    };

    const genderOptions = [
        { value: 'male', label: 'Male', icon: <ManOutlined /> },
        { value: 'female', label: 'Female', icon: <WomanOutlined /> },
        { value: 'other', label: 'Other', icon: <UserOutlined /> },
    ];

    return (
        <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ type: 'spring', damping: 25, stiffness: 120 }}
            className="max-w-2xl mx-auto px-6 py-12"
        >
            <div className="relative z-10 text-center mb-12">
                <h2 className="font-display font-bold text-4xl md:text-5xl text-white mb-4">
                    Tell us about you
                </h2>
                <p className="text-zinc-400 text-lg">
                    This helps us personalize your recommendations
                </p>
            </div>

            <Form form={form} onFinish={handleSubmit} layout="vertical" className="space-y-8">
                {/* Age Input */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                >
                    <Form.Item
                        label={<span className="text-white text-lg">What's your age?</span>}
                        name="age"
                        rules={[{ required: true, message: 'Please enter your age' }]}
                    >
                        <Input
                            type="number"
                            placeholder="Enter your age"
                            size="large"
                            min={1}
                            max={120}
                            className="bg-zinc-900 border-zinc-800 text-white text-2xl py-4"
                        />
                    </Form.Item>
                </motion.div>

                {/* Gender Selection - Icon Cards */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                >
                    <Form.Item
                        label={<span className="text-white text-lg">Select your gender</span>}
                        name="gender"
                        rules={[{ required: true, message: 'Please select your gender' }]}
                    >
                        <div className="grid grid-cols-3 gap-4">
                            {genderOptions.map((option) => (
                                <motion.div
                                    key={option.value}
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                    onClick={() => {
                                        form.setFieldsValue({ gender: option.value });
                                        setSelectedGender(option.value);
                                    }}
                                    className={`
                    cursor-pointer p-6 rounded-2xl border-2 transition-all gpu-accelerated
                    ${selectedGender === option.value
                                            ? 'bg-dosa-heat/20 border-dosa-heat'
                                            : 'bg-zinc-900 border-zinc-800 hover:border-zinc-700'
                                        }
                  `}
                                >
                                    <div className="text-center">
                                        <div className="text-4xl mb-3">{option.icon}</div>
                                        <div className="text-white font-medium">{option.label}</div>
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    </Form.Item>
                </motion.div>

                {/* Navigation Buttons */}
                <div className="flex gap-4 pt-6">
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
