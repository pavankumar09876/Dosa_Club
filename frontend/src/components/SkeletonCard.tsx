import { motion } from 'framer-motion';

/**
 * Skeleton Card Component
 * Loading placeholder for food cards
 */
export const SkeletonCard = () => {
    return (
        <div className="p-6 rounded-3xl bg-zinc-900 border-2 border-zinc-800">
            {/* Shimmer effect */}
            <div className="relative overflow-hidden">
                <motion.div
                    className="absolute inset-0 bg-gradient-to-r from-transparent via-zinc-800/50 to-transparent"
                    animate={{
                        x: ['-100%', '200%'],
                    }}
                    transition={{
                        duration: 1.5,
                        repeat: Infinity,
                        ease: 'linear',
                    }}
                />

                {/* Title skeleton */}
                <div className="h-7 bg-zinc-800 rounded-lg mb-4 w-3/4" />

                {/* Tags skeleton */}
                <div className="flex gap-2 mb-4">
                    <div className="h-6 bg-zinc-800 rounded-full w-20" />
                    <div className="h-6 bg-zinc-800 rounded-full w-16" />
                    <div className="h-6 bg-zinc-800 rounded-full w-14" />
                </div>

                {/* Learn more skeleton */}
                <div className="h-4 bg-zinc-800 rounded w-24" />
            </div>
        </div>
    );
};
