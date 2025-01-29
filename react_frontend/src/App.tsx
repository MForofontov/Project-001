// Import React and necessary hooks
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate, useLocation } from 'react-router-dom';

// Import context providers and hooks
import { AuthProvider, useAuth } from './utils/Contexts/AuthContext';

// Import local components
import Header from './Components/Header/Header';
import Footer from './Components/Footer/Footer';
import HomePage from './Components/HomePage/HomePage';
import Auth from './Components/Auth/Auth';
import DashBoard from './Components/DashBoard/DashBoard';
import NotFound from './utils/Components/NotFound/NotFound';

// Import route utilities
import PrivateRoute from './utils/Routes/PrivateRoute';
import PublicRoute from './utils/Routes/PublicRoute';
import { initializeAnalytics, sendPageView } from './services/analytics';

// Import response interceptors
import { setupResponseInterceptorsRefreshToken } from './utils/ResponseInterceptors/setupResponseInterceptorsRefreshToken';

const App: React.FC = () => {
  useEffect(() => {
    // Initialize Google Analytics
    initializeAnalytics();
  }, []); // Dependency array ensures this effect runs only once


  return (
    <AuthProvider> {/* Provide authentication context to the entire app */}
      <Router> {/* Set up the router for navigation */}
        <AppContent /> {/* Render the AppContent component */}
      </Router>
    </AuthProvider>
  );
};

const AppContent: React.FC = () => {
  const [isSidebarVisible, setIsSidebarVisible] = useState<boolean>(false); // State to manage sidebar visibility
  const { setIsAuthenticated } = useAuth(); // Get the setIsAuthenticated function from AuthContext
  const location = useLocation();
  
  useEffect(() => {
    setupResponseInterceptorsRefreshToken((status: boolean) => {
      setIsAuthenticated(status); // Update authentication status using AuthContext
    });
  }, [setIsAuthenticated]); // Dependency array ensures this effect runs only once when setIsAuthenticated is stable

  useEffect(() => {
    // Send page view event to Google Analytics 4
    sendPageView({ hitType: 'pageview', page: window.location.pathname });
  }, [location]); // Dependency array ensures this effect runs on location change

  // Function to toggle sidebar visibility
  const toggleSidebar = () => {
    setIsSidebarVisible(!isSidebarVisible); // Toggle the sidebar visibility state
  };

  return (
    <>
      <Header toggleSidebar={toggleSidebar} /> {/* Render the Header component and pass the toggleSidebar function */}
      <Routes>
        <Route path="/" element={<HomePage />} /> {/* Add a home route */}
        <Route path="/authentication" element={<PublicRoute component={Auth} />} /> {/* Add a login route with a public route wrapper */}
        <Route path="/dashboard" element={<PrivateRoute component={DashBoard} isSidebarVisible={isSidebarVisible} />} /> {/* Add a dashboard route with a private route wrapper */}
        <Route path="/verify-email/:uidb64/:token" /> {/* Add a route for email verification */}
        {/* Add more routes as needed */}
        <Route path="/404" element={<NotFound />} /> {/* Route for the NotFound component */}
        <Route path="*" element={<Navigate to="/404" />} /> {/* Redirect to /404 for undefined paths */}
      </Routes>
      <Footer /> {/* Render the Footer component */}
    </>
  );
};

export default App;
