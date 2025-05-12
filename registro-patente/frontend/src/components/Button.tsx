import React from 'react';
import { IconBaseProps } from 'react-icons';
import '../css/Button.css';

interface ButtonProps {
  title: string;
  icon?: React.ComponentType<IconBaseProps>;
  onClick?: () => void;
  variant?: 'primary' | 'secondary';
  className?: string;
  type?: 'button' | 'submit' | 'reset';
}

const Button: React.FC<ButtonProps> = ({
  title,
  icon: Icon,
  onClick,
  variant = 'primary',
  className,
  type = 'button'
}) => {
  return (
    <button
      type={type}
      onClick={onClick}
      className={`button button--${variant} ${className || ''}`}
    >
      {Icon && <Icon size={20} />}
      <span>{title}</span>
    </button>
  );
};

export default Button; 