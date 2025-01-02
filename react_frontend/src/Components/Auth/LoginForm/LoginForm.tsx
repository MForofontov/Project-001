// Import necessary modules and components
import React from 'react';
import { useNavigate } from 'react-router-dom';

// Import local components
import FormGroup from '../FormGroup/FormGroup';
import ToggleText from '../ToggleText/ToggleText';
import ForeignLoginButtons from './ForeignLoginButtons/ForeignLoginButtons';

// Import services and utilities
import { handleLoginUser } from '../../../services/authHandlers';
import { useAuth } from '../../../utils/Contexts/AuthContext';

// Import CSS
import './LoginForm.css';

// Define the props for the LoginForm component
interface LoginFormProps {
  email: string;
  setEmail: (email: string) => void;
  password: string;
  setPassword: (password: string) => void;
  toggleForm: () => void;
}

// Define the LoginForm component
const LoginForm: React.FC<LoginFormProps> = ({ email, setEmail, password, setPassword, toggleForm }) => {
  // Get the navigate function from useNavigate hook
  const navigate = useNavigate();
  
  // Get the setIsAuthenticated function from useAuth hook
  const { setIsAuthenticated } = useAuth();

  // Define the onSubmit handler for the form
  const onSubmit = (event: React.FormEvent) => {
    // Call handleLoginUser with necessary arguments
    handleLoginUser(event, email, password, navigate, setIsAuthenticated);
  };

  // Render the login form
  return (
    <div className="login-form">
      <h2>Login</h2>
      <form onSubmit={onSubmit}>
        <FormGroup
          label="Email:"
          type="text"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          id="username"
          name="username"
        />
        <FormGroup
          label="Password:"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          id="password"
          name="password"
        />
        <button type="submit" className="auth-button">Login</button>
      </form>
      <ForeignLoginButtons />
      <ToggleText toggleForm={toggleForm} text="Don't have an account? Register" />
    </div>
  );
};

// Export the LoginForm component as the default export
export default LoginForm;
