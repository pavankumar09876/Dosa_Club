import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { App } from 'antd';
import { PageTransition } from '../../components/PageTransition';
import { useUserData } from '../../context/UserContext';
import apiService from '../../services/api';
import { HealthPulseAnimation } from './HealthPulseAnimation';

/**
 * AI Processing Screen - Screen 3
 * Shows AI thinking animation while calling backend API
 */
export const ProcessingScreen = () => {
    const navigate = useNavigate();
    const { message } = App.useApp();
    const { userData } = useUserData();
    const [randomFact, setRandomFact] = useState('');

    useEffect(() => {
        const FACTS = [
            "Fermentation increases the bioavailability of nutrients in Dosa batter, making it easier to digest.",
            "Idli is considered one of the most nutritious breakfasts by the WHO due to its steaming process.",
            "Sambar is a complete protein source when paired with rice or idli, providing essential amino acids.",
            "Curry leaves are rich in iron and antioxidants, helping to improve hair health and digestion.",
            "Coconut chutney provides healthy fats (MCTs) that boost metabolism and provide quick energy.",
            "Rasam is known as a 'digestive soup' due to its tamarind base and digestive spices like pepper.",
            "Turmeric, a key ingredient in many dishes, contains curcumin which has powerful anti-inflammatory properties.",
            "Fenugreek seeds used in batter help regulate blood sugar levels and improve insulin sensitivity.",
            "Ragi Dosa is an excellent source of calcium and fiber, making it great for bone health.",
            "Eating with your hands connects you with your food and stimulates digestive enzymes via nerve endings.",
            "South Indian cuisine creates a balanced meal with all six tastes according to Ayurveda.",
            "Urad dal in batter is rich in protein, magnesium, and folic acid, essential for heart health.",
            "Ginger in chutneys acts as a natural immunity booster and helps combat nausea.",
            "Steamed foods like Idli retain more water-soluble vitamins than fried or boiled foods.",
            "Buttermilk serves as a natural probiotic, cooling the body and aiding in gut health.",
            "Tamarind is a rich source of antioxidants like polyphenols and helps in heart health.",
            "Drumsticks in Sambar are loaded with vitamins A, C, and K, along with essential minerals.",
            "Asafoetida (Hing) serves as a potent digestive aid, reducing bloating and gas.",
            "Traditional stone grinding preserves heat-sensitive nutrients in the batter better than modern blenders.",
            "Banana leaves used for serving add mild antioxidants to the warm food and are eco-friendly."
        ];
        setRandomFact(FACTS[Math.floor(Math.random() * FACTS.length)]);
    }, []);

    useEffect(() => {
        const fetchSuggestion = async () => {
            try {
                // Validate we have all required fields before making API call
                const requiredFields = [
                    'name',
                    'phone_number',
                    'age',
                    'height_cm',
                    'weight_kg',
                    'diet_type',
                    'medical_condition',
                    'health_goal',
                    'spice_tolerance'
                ];

                const missingFields = requiredFields.filter(field => !userData[field as keyof typeof userData]);

                if (missingFields.length > 0) {
                    console.error('Missing required fields:', missingFields);
                    message.error('Please complete all questions first.');
                    navigate('/start');
                    return;
                }

                // Minimum display time for better UX (show animation for at least 2 seconds)
                const minDisplayTime = new Promise((resolve) => setTimeout(resolve, 2000));

                // Call backend API
                const apiCall = apiService.getSuggestion(userData as any);

                // Wait for both to complete
                const [_, result] = await Promise.all([minDisplayTime, apiCall]);

                // Auto-navigate to recommendation screen after brief delay
                setTimeout(() => {
                    navigate('/recommendation', { state: { recommendation: result } });
                }, 800);
            } catch (error: any) {
                console.error('API Error:', error);

                // Handle 422 errors specifically
                if (error.response?.status === 422) {
                    message.error('Incomplete data. Please retake the questionnaire.');
                } else {
                    message.error(error.message || 'Unable to get recommendation. Please try again.');
                }

                // Navigate back to questions after error
                setTimeout(() => {
                    navigate('/questions');
                }, 2000);
            }
        };

        fetchSuggestion();
    }, [userData, navigate, message]);



    return (
        <PageTransition>
            <div className="min-h-screen bg-black flex items-center justify-center px-6">
                {/* Background gradient */}
                <div className="absolute inset-0 opacity-20">
                    <motion.div
                        animate={{
                            scale: [1, 1.2, 1],
                            opacity: [0.3, 0.5, 0.3],
                        }}
                        transition={{
                            duration: 3,
                            repeat: Infinity,
                            ease: 'easeInOut',
                        }}
                        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-dosa-heat rounded-full filter blur-3xl"
                    />
                </div>

                {/* Content */}
                <div className="relative z-10 text-center max-w-2xl">
                    {/* AI Health Core Animation */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ type: 'spring', damping: 20, stiffness: 100 }}
                        className="mb-12 flex justify-center" // increased margin and centered
                    >
                        <HealthPulseAnimation />
                    </motion.div>

                    {/* Text */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3, type: 'spring', damping: 25 }}
                    >
                        <h2 className="font-display font-bold text-4xl md:text-5xl text-white mb-6">
                            Analyzing Your Profile
                        </h2>

                        <motion.p
                            className="text-zinc-400 text-xl mb-8"
                            animate={{ opacity: [0.5, 1, 0.5] }}
                            transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
                        >
                            Our AI is finding the perfect food match for you...
                        </motion.p>

                        {/* Progress dots */}
                        <div className="flex justify-center gap-2">
                            {[0, 1, 2].map((index) => (
                                <motion.div
                                    key={index}
                                    className="w-3 h-3 rounded-full bg-dosa-heat"
                                    animate={{
                                        scale: [1, 1.5, 1],
                                        opacity: [0.3, 1, 0.3],
                                    }}
                                    transition={{
                                        duration: 1.5,
                                        repeat: Infinity,
                                        delay: index * 0.2,
                                        ease: 'easeInOut',
                                    }}
                                />
                            ))}
                        </div>
                    </motion.div>

                    {/* Fun fact while loading */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 1 }}
                        className="mt-16 bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 max-w-xl mx-auto"
                    >
                        <p className="text-zinc-500 text-sm italic">
                            💡 <span className="text-zinc-400 font-semibold not-italic">Did you know?</span> {randomFact}
                        </p>
                    </motion.div>
                </div>
            </div>
        </PageTransition>
    );
};
