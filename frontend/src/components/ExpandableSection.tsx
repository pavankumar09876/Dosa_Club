import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import { InfoCircleOutlined } from '@ant-design/icons';

interface ExpandableSectionProps {
    title: string;
    children: React.ReactNode;
    defaultExpanded?: boolean;
}

/**
 * Expandable Section Component
 * Smooth height animation with spring physics
 */
export const ExpandableSection: React.FC<ExpandableSectionProps> = ({
    title,
    children,
    defaultExpanded = false,
}) => {
    const [isExpanded, setIsExpanded] = useState(defaultExpanded);

    return (
        <div className="border border-zinc-800 rounded-2xl overflow-hidden bg-zinc-900/50">
            {/* Header - Clickable */}
            <motion.button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full px-6 py-4 flex items-center justify-between hover:bg-zinc-800/50 transition-colors"
                whileHover={{ backgroundColor: 'rgba(39, 39, 42, 0.5)' }}
                whileTap={{ scale: 0.98 }}
            >
                <div className="flex items-center gap-3">
                    <InfoCircleOutlined className="text-dosa-warm text-xl" />
                    <span className="text-white font-semibold text-lg">{title}</span>
                </div>

                {/* Expand/Collapse Icon */}
                <motion.div
                    animate={{ rotate: isExpanded ? 180 : 0 }}
                    transition={{ type: 'spring', damping: 20, stiffness: 200 }}
                >
                    <svg
                        className="w-5 h-5 text-zinc-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M19 9l-7 7-7-7"
                        />
                    </svg>
                </motion.div>
            </motion.button>

            {/* Expandable Content */}
            <AnimatePresence initial={false}>
                {isExpanded && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{
                            height: { type: 'spring', damping: 30, stiffness: 150 },
                            opacity: { duration: 0.2 },
                        }}
                        className="overflow-hidden"
                    >
                        <div className="px-6 py-4 border-t border-zinc-800">{children}</div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};
