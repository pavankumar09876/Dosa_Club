import { motion, useTransform, useSpring, useMotionValue } from 'framer-motion';
import { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Modal, Input } from 'antd';
import { MagneticButton } from './MagneticButton';
import { ContactModal } from './ContactModal';

/**
 * Abstract Hero Section - "Digital Gastronomy"
 * A purely code-driven, high-end visual experience.
 * No photos. Just math, colors, and motion.
 */
export const Hero = () => {
    const [isAdminModalParams, setIsAdminModalParams] = useState({ open: false });
    const [isContactModalOpen, setIsContactModalOpen] = useState(false);
    const navigate = useNavigate();
    const containerRef = useRef<HTMLDivElement>(null);

    // Mouse Physics
    const mouseX = useMotionValue(0);
    const mouseY = useMotionValue(0);

    // Smooth mouse response
    const springConfig = { damping: 20, stiffness: 100, mass: 0.5 };
    const springX = useSpring(mouseX, springConfig);
    const springY = useSpring(mouseY, springConfig);

    // Dynamic transforms for background and elements
    const moveBackgroundX = useTransform(springX, [-0.5, 0.5], ['-5%', '5%']);
    const moveBackgroundY = useTransform(springY, [-0.5, 0.5], ['-5%', '5%']);

    const tiltX = useTransform(springY, [-0.5, 0.5], [5, -5]);
    const tiltY = useTransform(springX, [-0.5, 0.5], [-5, 5]);

    useEffect(() => {
        const handleMouseMove = (e: MouseEvent) => {
            const { innerWidth, innerHeight } = window;
            mouseX.set((e.clientX / innerWidth) - 0.5);
            mouseY.set((e.clientY / innerHeight) - 0.5);
        };
        window.addEventListener('mousemove', handleMouseMove);
        return () => window.removeEventListener('mousemove', handleMouseMove);
    }, [mouseX, mouseY]);

    return (
        <div ref={containerRef} className="relative z-10 h-screen w-full flex flex-col overflow-hidden bg-dosa-black font-sans selection:bg-dosa-gold-500 selection:text-black">

            {/* 1. The Aurora Background (Code Generated) */}
            <motion.div
                style={{ x: moveBackgroundX, y: moveBackgroundY, scale: 1.1 }}
                className="absolute inset-0 z-0 pointer-events-none"
            >
                {/* Deep Base Layer */}
                <div className="absolute inset-0 bg-dosa-black" />

                {/* The "Aurora" - Moving Gradients */}
                <div className="absolute top-[-20%] left-[-10%] w-[70vw] h-[70vw] bg-dosa-emerald-900/30 rounded-full blur-[120px] animate-pulse-slow mix-blend-screen" />
                <div className="absolute bottom-[-20%] right-[-10%] w-[60vw] h-[60vw] bg-dosa-gold-600/10 rounded-full blur-[100px] animate-pulse-slow delay-700 mix-blend-screen" />
                <div className="absolute top-[40%] left-[30%] w-[40vw] h-[40vw] bg-teal-900/20 rounded-full blur-[80px] animate-pulse-slow delay-1000 mix-blend-overlay" />

                {/* Noise Texture for Film Grain Feel */}
                <div className="absolute inset-0 opacity-[0.04]" style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='1'/%3E%3C/svg%3E")` }} />
            </motion.div>

            {/* Navigation */}
            <nav className="relative z-50 flex items-center justify-between px-8 py-8 w-full max-w-[1600px] mx-auto">
                <div className="flex gap-2">
                    <div className="w-3 h-3 rounded-full bg-dosa-gold-500" />
                    <div className="w-3 h-3 rounded-full bg-dosa-emerald-500" />
                </div>
                <div className="hidden md:flex gap-12 text-xs font-bold text-zinc-500 tracking-[0.2em] uppercase">
                    {['Menu', 'Story', 'Reserve'].map((item) => (
                        <a key={item} href="#" className="hover:text-dosa-gold-500 transition-colors duration-300 relative group">
                            {item}
                            <span className="absolute -bottom-2 left-0 w-0 h-[1px] bg-dosa-gold-500 group-hover:w-full transition-all duration-300" />
                        </a>
                    ))}
                    <button
                        onClick={() => setIsContactModalOpen(true)}
                        className="hover:text-dosa-gold-500 transition-colors duration-300 relative group uppercase tracking-[0.2em]"
                    >
                        Contact
                        <span className="absolute -bottom-2 left-0 w-0 h-[1px] bg-dosa-gold-500 group-hover:w-full transition-all duration-300" />
                    </button>
                </div>
                <button onClick={() => setIsAdminModalParams({ open: true })} className="text-zinc-700 hover:text-white transition-colors">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
                </button>
            </nav>

            {/* Main Content Stage */}
            <main className="relative z-10 flex-grow flex flex-col items-center justify-center pointer-events-none">

                {/* 2. The Golden Swirl (The "Abstract Dosa") */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] pointer-events-auto">
                    <GoldenSwirl mouseX={springX} mouseY={springY} />
                </div>

                {/* 3. Typography & UI */}
                <div className="relative z-20 text-center space-y-8 pointer-events-auto mix-blend-hard-light">
                    <motion.div
                        initial={{ opacity: 0, y: 40 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] }}
                        style={{ rotateX: tiltX, rotateY: tiltY }}
                        className="perspective-1000"
                    >
                        <h1 className="font-display text-7xl md:text-9xl font-bold tracking-tighter leading-[0.85] drop-shadow-2xl">
                            <motion.span
                                className="block text-white"
                                animate={{
                                    color: ["#ffffff", "#fbbf24", "#ffffff"],
                                    textShadow: [
                                        "0 0 20px rgba(251, 191, 36, 0.5)",
                                        "0 0 40px rgba(251, 191, 36, 0.8)",
                                        "0 0 20px rgba(251, 191, 36, 0.5)"
                                    ]
                                }}
                                transition={{
                                    duration: 4,
                                    repeat: Infinity,
                                    ease: "easeInOut"
                                }}
                            >
                                THE DOSA
                            </motion.span>
                            <motion.span
                                className="block"
                                animate={{
                                    backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"],
                                }}
                                transition={{
                                    duration: 6,
                                    repeat: Infinity,
                                    ease: "linear",
                                }}
                                style={{
                                    backgroundSize: "200% 200%",
                                    backgroundClip: "text",
                                    WebkitBackgroundClip: "text",
                                    color: "transparent",
                                    backgroundImage: "linear-gradient(90deg, #fbbf24, #f59e0b, #d97706, #f59e0b, #fbbf24)"
                                }}
                            >
                                CLUB
                            </motion.span>
                        </h1>
                    </motion.div>

                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.8, duration: 1 }}
                        className="font-mono text-dosa-emerald-400/80 tracking-widest text-sm uppercase max-w-md mx-auto"
                    >
                        // South Indian Special Dosas
                    </motion.p>
                </div>
            </main>

            {/* Bottom Interaction Area */}
            <motion.div
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1.2, duration: 0.8 }}
                className="relative z-30 pb-16 w-full flex flex-col items-center gap-6"
            >
                <MagneticButton
                    onClick={() => navigate('/mode-selection')}
                    className="group relative px-10 py-4 bg-transparent border border-dosa-gold-500/30 text-dosa-gold-500 font-bold tracking-[0.2em] uppercase text-xs rounded-full overflow-hidden hover:border-dosa-gold-500 transition-colors backdrop-blur-sm"
                >
                    <div className="absolute inset-0 bg-dosa-gold-500 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-in-out" />
                    <span className="relative z-10 group-hover:text-black transition-colors duration-300">
                        Enter The Club
                    </span>
                </MagneticButton>
            </motion.div>

            {/* Admin PIN Modal */}
            <Modal
                title={null}
                open={isAdminModalParams.open}
                onCancel={() => setIsAdminModalParams({ open: false })}
                footer={null}
                centered
                width={320}
                className="game-modal"
                modalRender={(modal) => (
                    <div className="bg-zinc-900 border border-zinc-800 rounded-3xl overflow-hidden shadow-2xl">
                        {modal}
                    </div>
                )}
            >
                <div className="p-6 text-center space-y-6">
                    <div className="w-12 h-12 bg-zinc-800 rounded-full flex items-center justify-center mx-auto text-2xl">🔐</div>
                    <div>
                        <h3 className="text-white text-lg font-bold mb-1">Admin Access</h3>
                        <p className="text-zinc-500 text-sm">Enter security PIN</p>
                    </div>
                    <Input.Password
                        autoFocus
                        placeholder="••••"
                        maxLength={4}
                        size="large"
                        className="text-center text-2xl tracking-[0.5em] bg-zinc-950 border-zinc-800 text-white h-14 rounded-xl focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
                        onChange={(e) => {
                            const adminPin = import.meta.env.VITE_ADMIN_PIN || '1234';
                            if (e.target.value === adminPin) {
                                setIsAdminModalParams({ open: false });
                                navigate('/admin');
                            }
                        }}
                    />
                </div>
            </Modal>

            {/* Contact Modal */}
            <ContactModal
                visible={isContactModalOpen}
                onClose={() => setIsContactModalOpen(false)}
            />
        </div>
    );
};

/**
 * The Golden Swirl - Code Generated Abstract Art
 * Draws a mesmerizing spiral representing the dosa batter spreading.
 */
const GoldenSwirl = ({ mouseX, mouseY }: { mouseX: any, mouseY: any }) => {
    // Generate spiral path data mathematically
    const spiralPath = useDerivedSpiralPath();

    // Parallax effect for the swirl using simple rotation/tilt based on mouse
    const rotate = useTransform(mouseX, [-0.5, 0.5], [-15, 15]);
    const tilt = useTransform(mouseY, [-0.5, 0.5], [10, -10]);

    return (
        <motion.div style={{ rotate, rotateX: tilt }} className="w-full h-full preserve-3d">
            <svg viewBox="0 0 100 100" className="w-full h-full overflow-visible opacity-80 mix-blend-screen">
                <defs>
                    <linearGradient id="goldGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#FCD34D" stopOpacity="0" />
                        <stop offset="50%" stopColor="#D4AF37" stopOpacity="1" />
                        <stop offset="100%" stopColor="#B8860B" stopOpacity="0" />
                    </linearGradient>
                    <filter id="glow">
                        <feGaussianBlur stdDeviation="1.5" result="coloredBlur" />
                        <feMerge>
                            <feMergeNode in="coloredBlur" />
                            <feMergeNode in="SourceGraphic" />
                        </feMerge>
                    </filter>
                </defs>

                {/* 3 Layer Spiral for depth */}
                {[0, 1, 2].map((i) => (
                    <motion.path
                        key={i}
                        d={spiralPath}
                        fill="none"
                        stroke="url(#goldGradient)"
                        strokeWidth={0.3 - (i * 0.05)}
                        strokeLinecap="round"
                        filter="url(#glow)"
                        initial={{ pathLength: 0, opacity: 0 }}
                        animate={{
                            pathLength: 1,
                            opacity: 1 - (i * 0.2),
                            rotateZ: i * 120 // Offset rotation to create complex weave
                        }}
                        transition={{
                            duration: 3 + i,
                            ease: "easeInOut",
                            repeat: Infinity,
                            repeatType: "reverse"
                        }}
                        style={{
                            scale: 1 - (i * 0.1) // create depth
                        }}
                    />
                ))}
            </svg>
        </motion.div>
    );
};

// Helper to generate a nice spiral SVG path string
const useDerivedSpiralPath = () => {
    // Archimedean spiral approximation using cubic bezier curves concept or just high res points
    // For simplicity and smoothness in SVG, a multi-turn curve
    // M center -> spiral out
    return "M 50 50 m 0 0 c 2 0 4 3 5 5 s -2 6 -5 7 s -8 -2 -9 -6 s 3 -10 9 -11 s 14 3 15 10 s -3 16 -12 17 s -20 -4 -21 -14 s 5 -22 17 -23 s 26 6 27 18 s -7 28 -22 29";
};

export default Hero;
