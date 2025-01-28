import React, { useState } from 'react';
import './FormGroup.css';
import TogglePasswordButton from './TogglePasswordButton/TogglePasswordButton';

interface FormGroupProps {
  label: string;
  type: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  id: string;
  name: string;
  validatePassword?: (value: string) => void
}

const FormGroup: React.FC<FormGroupProps> = ({ label, type, value, onChange, id, name }) => {
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);

  const togglePasswordVisibility = () => {
    setIsPasswordVisible(!isPasswordVisible);
  };

  return (
    <div className="form-group">
      <label htmlFor={id}>{label}</label>
      <div className="input-wrapper">
        <input
          value={value}
          onChange={onChange}
          type={type === 'password' && isPasswordVisible ? 'text' : type}
          id={id}
          name={name}
          required
        />
        {type === 'password' && (
          <TogglePasswordButton
            isPasswordVisible={isPasswordVisible}
            togglePasswordVisibility={togglePasswordVisibility}
          />
        )}
      </div>
    </div>
  );
};

export default FormGroup;