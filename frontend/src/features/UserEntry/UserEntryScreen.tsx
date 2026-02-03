import { motion } from 'framer-motion';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input, Form, App, Modal } from 'antd';
import { UserOutlined, PhoneOutlined, MailOutlined, ArrowRightOutlined, EditOutlined } from '@ant-design/icons';
import { PageTransition } from '../../components/PageTransition';
import { AnimatedButton } from '../../components/AnimatedButton';
import { useUserData } from '../../context/UserContext';
import apiService from '../../services/api';
import { UserData } from '../../types';

/**
 * User Entry Screen - Screen 1
 * Collects basic user information: name, email, and phone number
 */
export const UserEntryScreen = () => {
    const navigate = useNavigate();
    const { message } = App.useApp();
    const { updateUserData } = useUserData();
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const [checkingUser, setCheckingUser] = useState(false);
    const [foundUser, setFoundUser] = useState<UserData | null>(null);
    const [modalVisible, setModalVisible] = useState(false);

    const checkUser = async (phone: string) => {
        if (!/^\d{10}$/.test(phone)) return;

        try {
            setCheckingUser(true);
            const user = await apiService.getUserProfile(phone);
            if (user) {
                setFoundUser(user);
                setModalVisible(true);
            }
        } catch (error) {
            // User not found, silent fail (treat as new user)
        } finally {
            setCheckingUser(false);
        }
    };

    const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const phone = e.target.value;
        if (phone.length === 10) {
            checkUser(phone);
        }
    };

    const handleContinueExisting = () => {
        if (foundUser) {
            updateUserData(foundUser);
            setModalVisible(false);
            // Go straight to processing if data seems complete, else questions
            if (foundUser.medical_condition && foundUser.health_goal) {
                navigate('/processing');
            } else {
                navigate('/questions');
            }
        }
    };

    const handleEditDetails = () => {
        if (foundUser) {
            // Pre-fill form
            form.setFieldsValue({
                name: foundUser.name,
                email: foundUser.email,
                phone_number: foundUser.phone_number
            });
            // Update context with what we have
            updateUserData(foundUser);
            setModalVisible(false);
            // Stay on screen to edit
        }
    };

    const handleSubmit = async (values: { name: string; email: string; phone_number: string }) => {
        try {
            setLoading(true);

            // Validate phone number format (10 digits)
            if (!/^\d{10}$/.test(values.phone_number)) {
                message.error('Please enter a valid 10-digit phone number');
                setLoading(false);
                return;
            }

            // Update user context
            updateUserData({
                name: values.name,
                email: values.email,
                phone_number: values.phone_number,
            });

            // Smooth transition to next screen
            await new Promise((resolve) => setTimeout(resolve, 300));
            navigate('/questions');
        } catch (error) {
            message.error('Something went wrong. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <PageTransition>
            <div className="min-h-screen flex items-center justify-center px-6 py-12 bg-black">
                {/* Subtle background gradient */}
                <div className="absolute inset-0 opacity-30">
                    <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-dosa-heat/10 rounded-full filter blur-3xl" />
                    <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-dosa-warm/10 rounded-full filter blur-3xl" />
                </div>

                {/* Content */}
                <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{
                        type: 'spring',
                        damping: 25,
                        stiffness: 120,
                        delay: 0.2,
                    }}
                    className="relative z-10 w-full max-w-md"
                >
                    {/* Header */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3, type: 'spring', damping: 20 }}
                        className="text-center mb-12"
                    >
                        <h1 className="font-display font-bold text-4xl md:text-5xl text-white mb-4">
                            Let's Get Started
                        </h1>
                        <p className="text-zinc-400 text-lg">
                            Tell us a bit about yourself
                        </p>
                    </motion.div>

                    {/* Form */}
                    <Form
                        form={form}
                        onFinish={handleSubmit}
                        layout="vertical"
                        className="space-y-6"
                    >
                        {/* Name Input */}
                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.4, type: 'spring', damping: 25 }}
                        >
                            <Form.Item
                                name="name"
                                rules={[
                                    { required: true, message: 'Please enter your name' },
                                    { min: 2, message: 'Name must be at least 2 characters' },
                                ]}
                            >
                                <Input
                                    prefix={<UserOutlined />}
                                    placeholder="Your Name"
                                    size="large"
                                    autoComplete="name"
                                />
                            </Form.Item>
                        </motion.div>

                        {/* Email Input */}
                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.45, type: 'spring', damping: 25 }}
                        >
                            <Form.Item
                                name="email"
                                rules={[
                                    { type: 'email', message: 'Please enter a valid email' },
                                    { required: false, message: 'Email is optional' }
                                ]}
                            >
                                <Input
                                    prefix={<MailOutlined />}
                                    placeholder="Email Address (Optional)"
                                    size="large"
                                    autoComplete="email"
                                />
                            </Form.Item>
                        </motion.div>

                        {/* Phone Input */}
                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.5, type: 'spring', damping: 25 }}
                        >
                            <Form.Item
                                name="phone_number"
                                rules={[
                                    { required: true, message: 'Please enter your phone number' },
                                    {
                                        pattern: /^\d{10}$/,
                                        message: 'Please enter a valid 10-digit phone number',
                                    },
                                ]}
                            >
                                <Input
                                    prefix={<PhoneOutlined />}
                                    placeholder="Phone Number (10 digits)"
                                    size="large"
                                    maxLength={10}
                                    autoComplete="tel"
                                    onChange={handlePhoneChange}
                                />
                            </Form.Item>
                        </motion.div>

                        {/* Submit Button */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.6, type: 'spring', damping: 20 }}
                        >
                            <AnimatedButton
                                type="submit"
                                variant="primary"
                                fullWidth
                                loading={loading || checkingUser}
                                className="flex items-center justify-center gap-2"
                            >
                                {loading ? 'Saving...' : (
                                    <>
                                        Continue <ArrowRightOutlined />
                                    </>
                                )}
                            </AnimatedButton>
                        </motion.div>
                    </Form>

                    {/* Privacy note */}
                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.8 }}
                        className="text-center text-sm text-zinc-600 mt-8"
                    >
                        Your information is safe and secure with us
                    </motion.p>
                </motion.div>
            </div>

            {/* Welcome Back Modal */}
            <Modal
                title={
                    <div className="text-center">
                        <span className="text-2xl">🎉</span>
                        <h3 className="text-xl font-bold mt-2">Welcome Back!</h3>
                    </div>
                }
                open={modalVisible}
                onCancel={() => setModalVisible(false)}
                footer={null}
                centered
                className="welcome-modal"
            >
                <div className="text-center space-y-6 py-4">
                    <div className="bg-zinc-100 p-4 rounded-xl">
                        <p className="text-zinc-500 text-sm mb-1">Found profile for</p>
                        <h4 className="text-lg font-bold text-dosa-heat">{foundUser?.name}</h4>
                        <p className="text-zinc-600">{foundUser?.email}</p>
                    </div>

                    <p className="text-zinc-600">
                        Would you like to use your saved details or update them?
                    </p>

                    <div className="flex flex-col gap-3">
                        <AnimatedButton
                            type="button"
                            variant="primary"
                            fullWidth
                            onClick={handleContinueExisting}
                            className="flex items-center justify-center gap-2"
                        >
                            Continue as {foundUser?.name} <ArrowRightOutlined />
                        </AnimatedButton>

                        <AnimatedButton
                            type="button"
                            variant="secondary"
                            fullWidth
                            onClick={handleEditDetails}
                            className="flex items-center justify-center gap-2"
                        >
                            <EditOutlined /> Update My Details
                        </AnimatedButton>
                    </div>
                </div>
            </Modal>
        </PageTransition>
    );
};
