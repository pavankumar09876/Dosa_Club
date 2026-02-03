import { motion } from 'framer-motion';
import { Form, InputNumber, App } from 'antd';
import { AnimatedButton } from '../../../components/AnimatedButton';

interface BodyMetricsQuestionProps {
    onNext: (data: Record<string, any>) => void;
    onBack: () => void;
}

/**
 * Height & Weight Question - Step 2
 */
export const BodyMetricsQuestion: React.FC<BodyMetricsQuestionProps> = ({
    onNext,
    onBack,
}) => {
    const { message } = App.useApp();
    const [form] = Form.useForm();

    const handleSubmit = (values: { height_cm: number; weight_kg: number }) => {
        if (!values.height_cm || !values.weight_kg) {
            message.error('Please enter both height and weight');
            return;
        }

        if (values.height_cm < 100 || values.height_cm > 250) {
            message.error('Height must be between 100 and 250 cm');
            return;
        }

        if (values.weight_kg < 20 || values.weight_kg > 300) {
            message.error('Weight must be between 20 and 300 kg');
            return;
        }

        onNext({ height_cm: values.height_cm, weight_kg: values.weight_kg });
    };

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
                    Body Metrics
                </h2>
                <p className="text-zinc-400 text-lg">
                    We'll calculate your BMI to suggest healthier options
                </p>
            </div>

            <Form form={form} onFinish={handleSubmit} layout="vertical" className="relative z-10 space-y-8">
                {/* Height Input */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="relative z-10"
                >
                    <Form.Item
                        label={<span className="text-white text-lg">Height (cm)</span>}
                        name="height_cm"
                        rules={[{ required: true, message: 'Please enter your height' }]}
                    >
                        <InputNumber
                            placeholder="175"
                            size="large"
                            min={100}
                            max={250}
                            className="w-full bg-zinc-900 border-zinc-800 text-white text-2xl"
                            controls={false}
                        />
                    </Form.Item>
                </motion.div>

                {/* Weight Input */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="relative z-10"
                >
                    <Form.Item
                        label={<span className="text-white text-lg">Weight (kg)</span>}
                        name="weight_kg"
                        rules={[{ required: true, message: 'Please enter your weight' }]}
                    >
                        <InputNumber
                            placeholder="70"
                            size="large"
                            min={20}
                            max={300}
                            className="w-full bg-zinc-900 border-zinc-800 text-white text-2xl"
                            controls={false}
                        />
                    </Form.Item>
                </motion.div>

                {/* Info Card */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.4 }}
                    className="relative z-10 bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6"
                >
                    <p className="text-zinc-400 text-sm text-center">
                        💡 Your BMI will be calculated automatically and used to recommend foods
                        suitable for your health profile
                    </p>
                </motion.div>

                {/* Navigation Buttons */}
                <div className="relative z-10 flex gap-4 pt-6">
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
