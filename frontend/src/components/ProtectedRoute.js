import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Sidebar from './Sidebar';

const ProtectedRoute = () => {
  const { user } = useAuth();

  if (!user) {
    // If no user is logged in, redirect to the login page
    return <Navigate to="/login" />;
  }

  // If user is logged in, render the main layout with the nested pages
  return (
    <div className="app-layout">
      <Sidebar />
      <div className="main-content">
        <Outlet /> {/* This will render the matched child route (HomePage, SchedulerPage, etc.) */}
      </div>
    </div>
  );
};

export default ProtectedRoute;