import { useState } from 'react';
import { Button, Form, Input, Select, Slider, Card, Typography, Divider } from 'antd';
import { ArrowLeftOutlined, ArrowRightOutlined } from '@ant-design/icons';
import { motion } from 'framer-motion';

const { Title, Text } = Typography;
const { Option } = Select;

interface HealthMetricsQuestionProps {
    onNext: (data: Record<string, any>) => void;
    onBack: () => void;
}

export const HealthMetricsQuestion: React.FC<HealthMetricsQuestionProps> = ({
    onNext,
    onBack,
}) => {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (values: any) => {
        setLoading(true);
        
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Pass health metrics data (mock - not integrated with backend)
        onNext({
            healthMetrics: {
                bloodPressure: values.bloodPressure,
                heartRate: values.heartRate,
                bloodSugar: values.bloodSugar,
                cholesterol: values.cholesterol,
                sleepHours: values.sleepHours,
                stressLevel: values.stressLevel,
                waterIntake: values.waterIntake,
                exerciseFrequency: values.exerciseFrequency,
            }
        });
        
        setLoading(false);
    };

    const containerVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: { 
            opacity: 1, 
            y: 0,
            transition: {
                duration: 0.6,
                staggerChildren: 0.1
            }
        }
    };

    const itemVariants = {
        hidden: { opacity: 0, x: -20 },
        visible: { opacity: 1, x: 0 }
    };

    return (
        <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="max-w-2xl mx-auto px-4 py-8 relative"
            style={{ zIndex: 1 }}
        >
            <motion.div variants={itemVariants}>
                <Title level={2} className="text-white text-center mb-4">
                    Health Metrics
                </Title>
                <Text className="text-gray-400 text-center block mb-8">
                    Please provide your current health measurements (This is for demonstration purposes only)
                </Text>
            </motion.div>

            <Card className="bg-gray-900 border-gray-800">
                <Form
                    form={form}
                    layout="vertical"
                    onFinish={handleSubmit}
                    requiredMark={false}
                >
                    <motion.div variants={itemVariants}>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                            <Form.Item
                                label={<Text className="text-gray-300">Blood Pressure</Text>}
                                name="bloodPressure"
                                rules={[{ required: true, message: 'Please enter blood pressure' }]}
                            >
                                <Input
                                    placeholder="120/80 mmHg"
                                    className="bg-gray-800 border-gray-700 text-white"
                                />
                            </Form.Item>

                            <Form.Item
                                label={<Text className="text-gray-300">Heart Rate (bpm)</Text>}
                                name="heartRate"
                                rules={[{ required: true, message: 'Please enter heart rate' }]}
                            >
                                <Input
                                    type="number"
                                    placeholder="72"
                                    className="bg-gray-800 border-gray-700 text-white"
                                />
                            </Form.Item>
                        </div>
                    </motion.div>

                    <motion.div variants={itemVariants}>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                            <Form.Item
                                label={<Text className="text-gray-300">Blood Sugar (mg/dL)</Text>}
                                name="bloodSugar"
                                rules={[{ required: true, message: 'Please enter blood sugar level' }]}
                            >
                                <Input
                                    type="number"
                                    placeholder="90"
                                    className="bg-gray-800 border-gray-700 text-white"
                                />
                            </Form.Item>

                            <Form.Item
                                label={<Text className="text-gray-300">Cholesterol (mg/dL)</Text>}
                                name="cholesterol"
                                rules={[{ required: true, message: 'Please enter cholesterol level' }]}
                            >
                                <Input
                                    type="number"
                                    placeholder="180"
                                    className="bg-gray-800 border-gray-700 text-white"
                                />
                            </Form.Item>
                        </div>
                    </motion.div>

                    <motion.div variants={itemVariants}>
                        <Form.Item
                            label={<Text className="text-gray-300">Sleep Hours per Night</Text>}
                            name="sleepHours"
                            rules={[{ required: true, message: 'Please select sleep hours' }]}
                        >
                            <Slider
                                min={4}
                                max={12}
                                marks={{
                                    4: '4h',
                                    6: '6h',
                                    8: '8h',
                                    10: '10h',
                                    12: '12h'
                                }}
                                className="text-white"
                                styles={{
                                    track: { backgroundColor: '#374151' },
                                    tracks: { backgroundColor: '#374151' },
                                    handle: { 
                                        backgroundColor: '#FB923C',
                                        borderColor: '#FB923C',
                                        zIndex: 10
                                    },
                                    rail: { backgroundColor: '#1F2937' }
                                }}
                            />
                        </Form.Item>
                    </motion.div>

                    <motion.div variants={itemVariants}>
                        <Form.Item
                            label={<Text className="text-gray-300">Stress Level</Text>}
                            name="stressLevel"
                            rules={[{ required: true, message: 'Please select stress level' }]}
                        >
                            <Select
                                placeholder="Select your stress level"
                                className="bg-gray-800 border-gray-700 text-white"
                                dropdownStyle={{
                                    backgroundColor: '#1F2937',
                                    border: '1px solid #374151',
                                    zIndex: 1050
                                }}
                                popupClassName="health-metrics-select-dropdown"
                            >
                                <Option value="low">Low</Option>
                                <Option value="moderate">Moderate</Option>
                                <Option value="high">High</Option>
                                <Option value="very-high">Very High</Option>
                            </Select>
                        </Form.Item>
                    </motion.div>

                    <motion.div variants={itemVariants}>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                            <Form.Item
                                label={<Text className="text-gray-300">Water Intake (liters/day)</Text>}
                                name="waterIntake"
                                rules={[{ required: true, message: 'Please enter water intake' }]}
                            >
                                <Input
                                    type="number"
                                    step="0.1"
                                    placeholder="2.5"
                                    className="bg-gray-800 border-gray-700 text-white"
                                />
                            </Form.Item>

                            <Form.Item
                                label={<Text className="text-gray-300">Exercise Frequency</Text>}
                                name="exerciseFrequency"
                                rules={[{ required: true, message: 'Please select exercise frequency' }]}
                            >
                                <Select
                                    placeholder="How often do you exercise?"
                                    className="bg-gray-800 border-gray-700 text-white"
                                    dropdownStyle={{
                                        backgroundColor: '#1F2937',
                                        border: '1px solid #374151',
                                        zIndex: 1050
                                    }}
                                    popupClassName="health-metrics-select-dropdown"
                                >
                                    <Option value="never">Never</Option>
                                    <Option value="rarely">Rarely (1-2 times/month)</Option>
                                    <Option value="sometimes">Sometimes (1-2 times/week)</Option>
                                    <Option value="often">Often (3-4 times/week)</Option>
                                    <Option value="daily">Daily</Option>
                                </Select>
                            </Form.Item>
                        </div>
                    </motion.div>

                    <Divider className="border-gray-700" />

                    <motion.div variants={itemVariants}>
                        <div className="flex justify-between items-center">
                            <Button
                                icon={<ArrowLeftOutlined />}
                                onClick={onBack}
                                className="bg-gray-800 border-gray-700 text-white"
                                size="large"
                            >
                                Back
                            </Button>

                            {/* <Space>
                                <Text className="text-gray-500 text-sm">
                                    Mock Form - Not integrated with backend
                                </Text>
                            </Space> */}

                            <Button
                                type="primary"
                                htmlType="submit"
                                icon={<ArrowRightOutlined />}
                                loading={loading}
                                className="bg-orange-500 border-orange-500 text-white"
                                size="large"
                            >
                                Continue
                            </Button>
                        </div>
                    </motion.div>
                </Form>
            </Card>
        </motion.div>
    );
};
