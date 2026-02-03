import React from 'react';
import { Button, ButtonProps } from 'antd';
import { motion } from 'framer-motion';

interface BrandButtonProps extends Omit<ButtonProps, 'type' | 'ghost' | 'danger'> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  children: React.ReactNode;
  fullWidth?: boolean;
}

export const BrandButton: React.FC<BrandButtonProps> = ({
  variant = 'primary',
  children,
  fullWidth = false,
  ...props
}) => {
  const getButtonClass = () => {
    const baseClass = 'brand-animated-btn';
    const widthClass = fullWidth ? 'w-full' : '';
    return `${baseClass} ${widthClass}`;
  };

  const getButtonType = () => {
    switch (variant) {
      case 'primary':
      case 'danger':
        return 'primary';
      case 'secondary':
      case 'ghost':
      default:
        return 'default';
    }
  };

  const motionProps = {
    whileHover: { scale: 1.02 },
    whileTap: { scale: 0.98 },
    transition: {
      type: "spring",
      stiffness: 400,
      damping: 17
    }
  };

  return (
    <motion.div {...motionProps} className={fullWidth ? 'w-full' : ''}>
      <Button
        {...props}
        className={getButtonClass()}
        type={getButtonType()}
        danger={variant === 'danger'}
        ghost={variant === 'ghost'}
        style={{
          width: fullWidth ? '100%' : undefined,
        }}
      >
        {children}
      </Button>
    </motion.div>
  );
};

export default BrandButton;
