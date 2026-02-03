import { motion, useMotionValue, useSpring, useTransform } from 'framer-motion';
import { MouseEvent, useState } from 'react';

interface MagneticButtonProps {
    children: React.ReactNode;
    onClick?: () => void;
    className?: string;
}

/**
 * Magnetic CTA Button Component
 * Premium spring-based magnetic hover effect with soft glow
 */
export const MagneticButton = ({ children, onClick, className = '' }: MagneticButtonProps) => {
    const [isHovered, setIsHovered] = useState(false);

    const x = useMotionValue(0);
    const y = useMotionValue(0);

    // Smooth spring physics for magnetic effect
    const springConfig = { damping: 20, stiffness: 150, mass: 0.5 };
    const xSpring = useSpring(x, springConfig);
    const ySpring = useSpring(y, springConfig);

    // Scale and glow intensity based on hover
    const scale = useTransform(() => (isHovered ? 1.05 : 1));
    const glowOpacity = useTransform(() => (isHovered ? 0.6 : 0.3));

    const handleMouseMove = (e: MouseEvent<HTMLButtonElement>) => {
        const rect = e.currentTarget.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        // Magnetic pull towards cursor (subtle, not aggressive)
        const deltaX = (e.clientX - centerX) * 0.15;
        const deltaY = (e.clientY - centerY) * 0.15;

        x.set(deltaX);
        y.set(deltaY);
    };

    const handleMouseLeave = () => {
        setIsHovered(false);
        x.set(0);
        y.set(0);
    };

    return (
        <motion.button
            onMouseMove={handleMouseMove}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={handleMouseLeave}
            onClick={onClick}
            style={{
                x: xSpring,
                y: ySpring,
                scale,
            }}
            className={`relative px-10 py-5 rounded-full font-display font-semibold text-lg text-black
                 bg-gradient-to-r from-dosa-heat via-dosa-warm to-dosa-glow
                 shadow-2xl overflow-hidden gpu-accelerated
                 focus:outline-none focus:ring-2 focus:ring-dosa-warm focus:ring-offset-2 focus:ring-offset-black ${className}`}
        >
            {/* Animated glow layer */}
            <motion.div
                className="absolute inset-0 rounded-full"
                style={{
                    background: 'radial-gradient(circle, rgba(255, 107, 53, 0.4) 0%, transparent 70%)',
                    filter: 'blur(20px)',
                    opacity: glowOpacity,
                }}
            />

            {/* Shimmer effect on hover */}
            <motion.div
                className="absolute inset-0 rounded-full"
                initial={{ x: '-100%' }}
                animate={isHovered ? { x: '100%' } : { x: '-100%' }}
                transition={{ duration: 0.8, ease: 'easeInOut' }}
                style={{
                    background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent)',
                }}
            />

            {/* Button text */}
            <span className="relative z-10">{children}</span>
        </motion.button>
    );
};
