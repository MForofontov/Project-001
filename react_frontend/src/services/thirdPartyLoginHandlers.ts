/**
 * Function to handle Google login by redirecting the user to the Google login URL.
 */
export const handleGoogleLogin = () => {
  // Redirect the user to the Google login URL
  window.location.href = 'http://localhost/user-management/api/v1/google/login/';
};

/**
 * Function to handle Facebook login by redirecting the user to the Facebook login URL.
 */
export const handleFacebookLogin = () => {
  // Redirect the user to the Facebook login URL
  window.location.href = 'http://localhost/user-management/api/facebook/login/';
};