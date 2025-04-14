# Project-001

## Overview
**Project-001** is a microservices-based web application designed to manage user accounts, process music files, and provide a seamless user experience through a React-based frontend. The application is built using modern technologies and follows best practices for scalability, security, and maintainability.

The project consists of three main components:
1. **User Management Service**: Handles user authentication, registration, and profile management.
2. **Data Processing Service**: Processes uploaded music files and performs analysis.
3. **React Frontend**: Provides a user-friendly interface for interacting with the backend services.

---

## Features
- **User Authentication**: Secure login, registration, and email verification using JWT.
- **Music File Processing**: Upload and analyze music files with asynchronous task handling.
- **Dashboard**: A React-based dashboard for managing user data and viewing analysis results.
- **Prometheus Monitoring**: Metrics collection for performance monitoring.
- **Dockerized Deployment**: All services are containerized for easy deployment and scaling.

---

## Technologies Used

### **Backend**
- **Django**: Python web framework used for the backend services.
  - **Django REST Framework (DRF)**: For building RESTful APIs.
  - **Django Prometheus**: For exposing metrics to Prometheus.
  - **SimpleJWT**: For secure authentication using JSON Web Tokens.
- **PostgreSQL**: Database for storing user and music file data.
- **Celery**: For handling asynchronous tasks (e.g., music file processing).
- **Redis**: Message broker for Celery.

### **Frontend**
- **React**: JavaScript library for building the user interface.
  - **Vite**: Fast build tool for modern web projects.
  - **TypeScript**: For type-safe development.
  - **MUI**: Component library for building a responsive and accessible UI.
  - **shadcn/ui**: Utility-first component library integrated with Tailwind CSS.

### **DevOps**
- **Docker**: Containerization of all services for consistent environments.
- **Docker Compose**: Orchestration of multi-container applications.
- **Prometheus**: Monitoring and alerting toolkit.
- **Grafana**: Visualization of metrics collected by Prometheus.

## How to Run the Project

### Prerequisites
- **Node.js** (v18 or higher)
- **Docker** and **Docker Compose**
- **.env** file

## Environment Variables
The project uses environment variables for configuration. Create a .env file in the root directory with the following variables

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/Project-001.git
   cd Project-001
2. Start the services using Docker Compose:
    docker-compose up --build
3. Access the application:
    - **Frontend**: http://localhost:5173
    - **User Management API**: http://localhost:8000
    - **Data Processing API**: http://localhost:8001