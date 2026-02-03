import { Modal, Button, Typography, Space, Divider } from 'antd';
import {
    InstagramOutlined,
    FacebookOutlined,
    XOutlined,
    MailOutlined,
    PhoneOutlined,
    GlobalOutlined
} from '@ant-design/icons';
import { motion } from 'framer-motion';

const { Title, Text, Link } = Typography;

interface ContactModalProps {
    visible: boolean;
    onClose: () => void;
}

export const ContactModal = ({ visible, onClose }: ContactModalProps) => {
    const containerVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: {
            opacity: 1,
            y: 0,
            transition: {
                staggerChildren: 0.1
            }
        }
    };

    const itemVariants = {
        hidden: { opacity: 0, x: -20 },
        visible: { opacity: 1, x: 0 }
    };

    return (
        <Modal
            open={visible}
            onCancel={onClose}
            footer={null}
            centered
            width={500}
            className="contact-modal"
            title={null}
            closeIcon={<span className="text-white/50 hover:text-white text-xl">×</span>}
            styles={{
                content: {
                    backgroundColor: 'rgba(20, 20, 20, 0.95)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '24px',
                    padding: '32px'
                }
            }}
        >
            <motion.div
                variants={containerVariants}
                initial="hidden"
                animate="visible"
                className="text-center"
            >
                <div className="w-16 h-16 bg-dosa-heat/10 rounded-full flex items-center justify-center mx-auto mb-6">
                    <GlobalOutlined className="text-3xl text-dosa-heat" />
                </div>

                <Title level={2} className="!text-white font-display mb-2">Get in Touch</Title>
                <Text className="text-zinc-400 text-lg block mb-8">
                    We'd love to hear from you. Connect with us on social media or reach out directly.
                </Text>

                <div className="space-y-4 text-left">
                    <motion.div variants={itemVariants}>
                        <a
                            href="https://www.instagram.com/thedosaclub_denton/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="bg-zinc-800/50 hover:bg-zinc-800 border border-white/5 hover:border-dosa-heat/50 rounded-xl p-4 flex items-center gap-4 transition-all group"
                        >
                            <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-purple-500 to-pink-500 flex items-center justify-center text-white">
                                <InstagramOutlined className="text-xl" />
                            </div>
                            <div>
                                <h4 className="text-white font-bold m-0 group-hover:text-dosa-heat transition-colors">Instagram</h4>
                                <span className="text-zinc-500 text-sm">@TheDosaClub</span>
                            </div>
                        </a>
                    </motion.div>

                    <motion.div variants={itemVariants}>
                        <a
                            href="https://facebook.com"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="bg-zinc-800/50 hover:bg-zinc-800 border border-white/5 hover:border-dosa-heat/50 rounded-xl p-4 flex items-center gap-4 transition-all group"
                        >
                            <div className="w-10 h-10 rounded-full bg-[#1877F2] flex items-center justify-center text-white">
                                <FacebookOutlined className="text-xl" />
                            </div>
                            <div>
                                <h4 className="text-white font-bold m-0 group-hover:text-dosa-heat transition-colors">Facebook</h4>
                                <span className="text-zinc-500 text-sm">The Dosa Club Official</span>
                            </div>
                        </a>
                    </motion.div>

                    <motion.div variants={itemVariants}>
                        <a
                            href="https://twitter.com"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="bg-zinc-800/50 hover:bg-zinc-800 border border-white/5 hover:border-dosa-heat/50 rounded-xl p-4 flex items-center gap-4 transition-all group"
                        >
                            <div className="w-10 h-10 rounded-full bg-black border border-white/10 flex items-center justify-center text-white">
                                <XOutlined className="text-xl" />
                            </div>
                            <div>
                                <h4 className="text-white font-bold m-0 group-hover:text-dosa-heat transition-colors">X (Twitter)</h4>
                                <span className="text-zinc-500 text-sm">@TheDosaClub</span>
                            </div>
                        </a>
                    </motion.div>
                </div>

                <Divider className="border-white/10 my-8">Or Contact Directly</Divider>

                <div className="grid grid-cols-2 gap-4">
                    <motion.a
                        variants={itemVariants}
                        href="mailto:hello@dosaclub.com"
                        className="bg-zinc-800/30 hover:bg-zinc-800 rounded-xl p-4 flex flex-col items-center gap-2 transition-all hover:scale-105"
                    >
                        <MailOutlined className="text-2xl text-dosa-warm" />
                        <span className="text-zinc-300 text-sm">hello@dosaclub.com</span>
                    </motion.a>

                    <motion.a
                        variants={itemVariants}
                        href="tel:+19405550123"
                        className="bg-zinc-800/30 hover:bg-zinc-800 rounded-xl p-4 flex flex-col items-center gap-2 transition-all hover:scale-105"
                    >
                        <PhoneOutlined className="text-2xl text-dosa-warm" />
                        <span className="text-zinc-300 text-sm">+1 (940) 555-0123</span>
                    </motion.a>
                </div>

            </motion.div>
        </Modal>
    );
};
