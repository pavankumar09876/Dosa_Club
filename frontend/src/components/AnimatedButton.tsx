import { motion } from 'framer-motion';
// import { ButtonHTMLAttributes } from 'react';

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement>;
type MotionButtonProps = Omit<ButtonProps, 'onAnimationStart' | 'onDragStart' | 'onDragEnd' | 'onDrag' | 'ref'>;

interface AnimatedButtonProps extends MotionButtonProps {
    variant?: 'primary' | 'secondary';
    loading?: boolean;
    fullWidth?: boolean;
    children: React.ReactNode;
}

/**
 * Animated Button Component
 * Reusable button with spring hover animations and loading states
 */
export const AnimatedButton: React.FC<AnimatedButtonProps> = ({
    children,
    variant = 'primary',
    loading = false,
    fullWidth = false,
    disabled,
    className = '',
    ...props
}) => {
    const baseClasses = `
    relative px-10 py-5 rounded-xl font-display font-semibold text-lg
    transition-all duration-300 gpu-accelerated
    focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-black
    disabled:opacity-50 disabled:cursor-not-allowed
    ${fullWidth ? 'w-full' : ''}
  `;

    const variantClasses = {
        primary: `
      bg-gradient-to-r from-dosa-heat via-dosa-warm to-dosa-glow
      text-black shadow-2xl hover:shadow-dosa-heat/50
      focus:ring-dosa-warm
    `,
        secondary: `
      bg-zinc-800 text-white border-2 border-zinc-700
      hover:bg-zinc-700 hover:border-zinc-600
      focus:ring-zinc-600
    `,
    };

    return (
        <motion.button
            whileHover={{ scale: disabled || loading ? 1 : 1.02 }}
            whileTap={{ scale: disabled || loading ? 1 : 0.98 }}
            transition={{
                type: 'spring',
                damping: 20,
                stiffness: 300,
            }}
            className={`${baseClasses} ${variantClasses[variant]} ${className}`}
            disabled={disabled || loading}
            {...props}
        >
            {loading ? (
                <span className="flex items-center justify-center gap-2">
                    <svg
                        className="animate-spin h-5 w-5"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                    >
                        <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                        />
                        <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        />
                    </svg>
                    Loading...
                </span>
            ) : (
                children
            )}
        </motion.button>
    );
};
