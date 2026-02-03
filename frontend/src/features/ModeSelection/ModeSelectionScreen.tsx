import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { PageTransition } from '../../components/PageTransition';
import { CompassOutlined, HeartOutlined, ThunderboltOutlined } from '@ant-design/icons';

/**
 * Mode Selection Screen
 * Lets the user choose between direct menu exploration or the health questionnaire.
 */
export const ModeSelectionScreen = () => {
    const navigate = useNavigate();

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.2,
                delayChildren: 0.1,
            },
        },
    };

    const cardVariants = {
        hidden: { opacity: 0, y: 30 },
        visible: {
            opacity: 1,
            y: 0,
            transition: {
                type: 'spring',
                damping: 25,
                stiffness: 100,
            },
        },
    };

    return (
        <PageTransition>
            <div className="min-h-screen flex flex-col items-center justify-center px-6 py-12 bg-black text-white relative overflow-hidden">
                {/* Ambient Background */}
                <div className="absolute inset-0 opacity-20 pointer-events-none">
                    <div className="absolute top-0 left-1/4 w-96 h-96 bg-dosa-heat/10 rounded-full filter blur-3xl animate-pulse-slow" />
                    <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-dosa-glow/10 rounded-full filter blur-3xl animate-pulse-slow" />
                </div>

                <motion.div
                    variants={containerVariants}
                    initial="hidden"
                    animate="visible"
                    className="relative z-10 max-w-5xl w-full"
                >
                    {/* Header */}
                    <div className="text-center mb-12">
                        <motion.h1
                            variants={cardVariants}
                            className="font-display font-bold text-4xl md:text-5xl mb-4"
                        >
                            How would you like to proceed?
                        </motion.h1>
                        <motion.p
                            variants={cardVariants}
                            className="text-zinc-400 text-lg"
                        >
                            Choose the path that suits your appetite
                        </motion.p>
                    </div>

                    {/* Selection Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
                        {/* Option 1: Explore Menu */}
                        <motion.div
                            variants={cardVariants}
                            whileHover={{ scale: 1.03, y: -5 }}
                            whileTap={{ scale: 0.98 }}
                            onClick={() => navigate('/explore')}
                            className="group cursor-pointer relative p-8 md:p-12 rounded-3xl border border-zinc-800 bg-zinc-900/40 backdrop-blur-xl hover:bg-zinc-800/60 hover:border-dosa-glow/50 transition-all duration-300 shadow-2xl hover:shadow-dosa-glow/20"
                        >
                            <div className="mb-6 inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-zinc-800 group-hover:bg-dosa-glow/20 transition-colors duration-300">
                                <CompassOutlined className="text-3xl text-dosa-glow" />
                            </div>
                            <h3 className="text-2xl font-bold mb-3 group-hover:text-dosa-glow transition-colors duration-300">
                                Explore Food Menu
                            </h3>
                            <p className="text-zinc-400 group-hover:text-zinc-300 transition-colors duration-300">
                                Directly view our full menu and filter by your preferences.
                            </p>
                        </motion.div>

                        {/* Option 2: Health Recommendation */}
                        <motion.div
                            variants={cardVariants}
                            whileHover={{ scale: 1.03, y: -5 }}
                            whileTap={{ scale: 0.98 }}
                            onClick={() => navigate('/start')}
                            className="group cursor-pointer relative p-8 md:p-12 rounded-3xl border border-zinc-800 bg-zinc-900/40 backdrop-blur-xl hover:bg-zinc-800/60 hover:border-dosa-heat/50 transition-all duration-300 shadow-2xl hover:shadow-dosa-heat/20"
                        >
                            <div className="mb-6 inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-zinc-800 group-hover:bg-dosa-heat/20 transition-colors duration-300">
                                <HeartOutlined className="text-3xl text-dosa-heat" />
                            </div>
                            <h3 className="text-2xl font-bold mb-3 group-hover:text-dosa-heat transition-colors duration-300">
                                Get Health Recommendation
                            </h3>
                            <p className="text-zinc-400 group-hover:text-zinc-300 transition-colors duration-300">
                                Take a quick quiz to find the perfect dish for your body.
                            </p>
                        </motion.div>

                        {/* Option 3: Quick Guest Mode */}
                        <motion.div
                            variants={cardVariants}
                            whileHover={{ scale: 1.03, y: -5 }}
                            whileTap={{ scale: 0.98 }}
                            onClick={() => navigate('/guest/questions')}
                            className="group cursor-pointer relative p-8 md:p-12 rounded-3xl border border-zinc-800 bg-zinc-900/40 backdrop-blur-xl hover:bg-zinc-800/60 hover:border-purple-500/50 transition-all duration-300 shadow-2xl hover:shadow-purple-500/20"
                        >
                            <div className="mb-6 inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-zinc-800 group-hover:bg-purple-500/20 transition-colors duration-300">
                                <ThunderboltOutlined className="text-3xl text-purple-400" />
                            </div>
                            <h3 className="text-2xl font-bold mb-3 group-hover:text-purple-400 transition-colors duration-300">
                                Quick Guest Mode
                            </h3>
                            <p className="text-zinc-400 group-hover:text-zinc-300 transition-colors duration-300">
                                Skip registration and get instant recommendations.
                            </p>
                        </motion.div>
                    </div>
                </motion.div>
            </div>
        </PageTransition>
    );
};
