import React from 'react';
import { handleGoogleLogin, handleFacebookLogin } from '../../../services/thirdPartyLoginHandlers';
import { FacebookLoginButton, GoogleLoginButton } from 'react-social-login-buttons';
import './ForeignLoginButtons.css';

const ForeignLoginButtons: React.FC = () => {
  return (
    <div className="foreign-login-buttons">
      <GoogleLoginButton onClick={handleGoogleLogin} />
      <FacebookLoginButton onClick={handleFacebookLogin} />
    </div>
  );
};

export default ForeignLoginButtons;