// Import necessary modules and functions
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

// Create an axios instance for the user management service
const userManagementApi: AxiosInstance = axios.create({
  baseURL: 'https://localhost/user-management/api/v1/', // User Management API base URL
  timeout: 30000, // Request timeout of 30 seconds
  withCredentials: true, // Ensure cookies are sent with requests
  headers: {
    'Content-Type': 'application/json', // Default content type
  }
});

// Create an axios instance for the data processing service
const dataProcessingApi: AxiosInstance = axios.create({
  baseURL: 'http://localhost:8001/api/data_processing', // Data Processing API base URL
  timeout: 30000, // Request timeout of 30 seconds
  withCredentials: true, // Ensure cookies are sent with requests
  headers: {
    'Content-Type': 'application/json', // Default content type
  },
});

/**
 * Function to call the user management API with token refresh logic.
 * 
 * @param {AxiosRequestConfig} config - The Axios request configuration object.
 * @returns {Promise<AxiosResponse>} - A promise that resolves with the server response.
 * @throws {Error} - Throws an error if the API call fails.
 */
const callUserManagementAPI = async (config: AxiosRequestConfig): Promise<AxiosResponse> => {
  try {
    const response = await userManagementApi(config); // Make the API call
    return response; // Return the response
  } catch (error) {
    console.error('API Error:', error); // Log any errors that occur
    throw error; // Throw error if the API call fails
  }
};

/**
 * Function to call the data processing API.
 * 
 * @param {AxiosRequestConfig} config - The Axios request configuration object.
 * @returns {Promise<AxiosResponse>} - A promise that resolves with the server response.
 * @throws {Error} - Throws an error if the API call fails.
 */
const callDataProcessingAPI = async (config: AxiosRequestConfig): Promise<AxiosResponse> => {
  try {
    const response = await dataProcessingApi(config); // Make the API call
    return response; // Return the response
  } catch (error) {
    console.error('API Error:', error); // Log any errors that occur
    throw error; // Throw error if the API call fails
  }
};

// Export the axios instances and API call functions
export { userManagementApi, dataProcessingApi, callUserManagementAPI, callDataProcessingAPI };
