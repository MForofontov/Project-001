import React from 'react';
import './PasswordCriteria.css';

interface PasswordCriteriaProps {
  password: string;
}

// Define the PasswordCriteria component
const PasswordCriteria: React.FC<PasswordCriteriaProps> = ({ password }) => {
  const criteria = [
    { text: 'At least 8 characters', test: (pw: string) => pw.length >= 8 },
    { text: 'At least one uppercase letter', test: (pw: string) => /[A-Z]/.test(pw) },
    { text: 'At least one lowercase letter', test: (pw: string) => /[a-z]/.test(pw) },
    { text: 'At least one number', test: (pw: string) => /\d/.test(pw) },
    { text: 'At least one special character', test: (pw: string) => /[!@#$%^&*(),.?":{}|<>]/.test(pw) },
  ];

  if (password.length === 0) {
    return null;
  }

  return (
    <ul className="password-criteria">
      {criteria.map((criterion, index) => (
        <li key={index} className={criterion.test(password) ? 'valid' : 'invalid'}>
          {criterion.text}
        </li>
      ))}
    </ul>
  );
};

export default PasswordCriteria;