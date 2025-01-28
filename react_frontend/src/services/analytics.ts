import ReactGA from 'react-ga4';

/**
 * Initializes Google Analytics with the provided tracking ID.
 * 
 * The tracking ID is retrieved from the environment variables.
 * Ensure that the environment variable REACT_APP_GOOGLE_ANALYTICS_ID is set.
 */
export const initializeAnalytics = () => {
  // Retrieve the Google Analytics tracking ID from environment variables
  const trackingId = process.env.REACT_APP_GOOGLE_ANALYTICS_ID;
  
  if (trackingId) {
    // Initialize Google Analytics with the tracking ID
    ReactGA.initialize(trackingId);
  } else {
    console.error('Google Analytics tracking ID is not set in environment variables.');
  }
};

/**
 * Sends data to Google Analytics.
 * 
 * @param {Record<string, any>} payload - The data to be sent to Google Analytics. This should be an object
 *                  containing the event details such as hitType, eventCategory, eventAction, etc.
 */
export const sendDataForAnalytics = (payload: Record<string, any>) => {
  ReactGA.send(payload);
};