import { motion } from 'framer-motion';
import { ReactNode } from 'react';

interface PageTransitionProps {
    children: ReactNode;
}

/**
 * Page Transition Wrapper
 * Provides smooth fade + slide animations for route changes
 */
export const PageTransition: React.FC<PageTransitionProps> = ({ children }) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{
                type: 'spring',
                damping: 25,
                stiffness: 120,
                duration: 0.6,
            }}
            className="w-full"
        >
            {children}
        </motion.div>
    );
};
