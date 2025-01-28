// Import React and necessary hooks
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

// Import local components
import FormGroup from '../FormGroup/FormGroup';
import ToggleText from '../ToggleText/ToggleText';
import ForeignLoginButtons from '../ForeignLoginButtons/ForeignLoginButtons';
import AuthSeparator from '../AuthSeparator/AuthSeparator';
import PasswordCriteria from './PasswordCriteria/PasswordCriteria';
import CustomAlert from '../../../utils/Components/CustomAlert/CustomAlert';

// Import services and utilities
import { handleRegisterUser } from '../../../services/authHandlers';
import { useAuth } from '../../../utils/Contexts/AuthContext';
import isValidPassword from '../../../utils/functions/isValidPassword';
import isValidEmail from '../../../utils/functions/isValidEmail';

// Import CSS
import './RegisterForm.css';

// Define the props for the RegisterForm component
interface RegisterFormProps {
  email: string;
  setEmail: (email: string) => void;
  password: string;
  setPassword: (password: string) => void;
  toggleForm: () => void;
}

// Define the RegisterForm component
const RegisterForm: React.FC<RegisterFormProps> = ({ email, setEmail, password, setPassword, toggleForm }) => {
  // Get the navigate function from useNavigate hook
  const navigate = useNavigate();

  // Get the setIsAuthenticated function from useAuth hook
  const { setIsAuthenticated } = useAuth();

  const [error, setError] = useState<string | null>(null);

  // Define the onSubmit handler for the form
  const onSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    let errorMessage = '';
    if (!isValidEmail(email)) {
      errorMessage += 'Invalid email address. ';
    }
    if (!isValidPassword(password)) {
      errorMessage += 'Password does not meet the criteria.';
    }
    if (errorMessage) {
      setError(errorMessage.trim());
    } else {
      handleRegisterUser(event, email, password, navigate, setIsAuthenticated);
    }
  };

  // Render the register form
  return (
    <div className="register-form">
      <h2>Register</h2>
      <form onSubmit={onSubmit}>
        <FormGroup
          label="Email:"
          type="text"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          id="email"
          name="email"
        />
        <FormGroup
          label="Password:"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          id="password"
          name="password"
        />
        <PasswordCriteria password={password} />
        <button type="submit" className="auth-button">Register</button>
      </form>
      <AuthSeparator />
      <ForeignLoginButtons />
      <ToggleText toggleForm={toggleForm} text="Already have an account? Login" />
      {error && <CustomAlert message={error} onClose={() => setError(null)} />}
    </div>
  );
};

// Export the RegisterForm component as the default export
export default RegisterForm;
