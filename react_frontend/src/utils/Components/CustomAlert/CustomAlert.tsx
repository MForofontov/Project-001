import React from 'react';
import './CustomAlert.css';

interface CustomAlertProps {
  message: string;
  onClose: () => void;
}

const CustomAlert: React.FC<CustomAlertProps> = ({ message, onClose }) => {
  return (
    <div className="custom-alert">
      <div className="custom-alert-content">
        <span>{message}</span>
        <button onClick={onClose} className="custom-alert-close">
          &times;
        </button>
      </div>
    </div>
  );
};

export default CustomAlert;