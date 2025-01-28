import React from 'react';
import './TogglePasswordButton.css';

interface TogglePasswordButtonProps {
  isPasswordVisible: boolean;
  togglePasswordVisibility: () => void;
}

const TogglePasswordButton: React.FC<TogglePasswordButtonProps> = ({ isPasswordVisible, togglePasswordVisibility }) => {
  return (
    <button type="button" onClick={togglePasswordVisibility} className="toggle-password-button">
      {isPasswordVisible ? 'Hide' : 'Show'}
    </button>
  );
};

export default TogglePasswordButton;