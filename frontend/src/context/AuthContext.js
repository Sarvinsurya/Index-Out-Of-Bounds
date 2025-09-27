import React, { createContext, useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// The two mock users we have
const MOCK_USERS = {
  vendor: { type: 'vendor', name: 'Zoho (Chennai)' },
  distributor: { type: 'distributor', name: 'Germany' },
};

// Create the context
const AuthContext = createContext(null);

// Create the provider component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Fetch notifications from database
  const fetchNotifications = async (userType) => {
    if (!userType) return;
    
    setLoading(true);
    try {
      const response = await fetch(`/api/notifications/${userType}`);
      const data = await response.json();
      
      if (response.ok) {
        setNotifications(data.notifications || []);
      } else {
        console.error('Error fetching notifications:', data.detail);
        setNotifications([]);
      }
    } catch (error) {
      console.error('Error fetching notifications:', error);
      setNotifications([]);
    } finally {
      setLoading(false);
    }
  };

  // Mark notification as read
  const markNotificationRead = async (notificationId) => {
    try {
      const response = await fetch(`/api/notifications/${notificationId}/mark-read`, {
        method: 'POST'
      });
      
      if (response.ok) {
        // Update local state
        setNotifications(prev => 
          prev.map(notification => 
            notification.id === notificationId 
              ? { ...notification, is_read: true, read_at: new Date().toISOString() }
              : notification
          )
        );
      }
    } catch (error) {
      console.error('Error marking notification as read:', error);
    }
  };

  const login = (userType) => {
    const userToLogin = MOCK_USERS[userType];
    if (userToLogin) {
      setUser(userToLogin);
      // Fetch notifications for the logged-in user
      fetchNotifications(userType);
      navigate('/'); // Redirect to home page after login
    }
  };

  const logout = () => {
    setUser(null);
    setNotifications([]);
    navigate('/login'); // Redirect to login page after logout
  };

  // Refresh notifications (useful for polling)
  const refreshNotifications = () => {
    if (user?.type) {
      fetchNotifications(user.type);
    }
  };

  // Auto-refresh notifications every 30 seconds when user is logged in
  useEffect(() => {
    if (!user?.type) return;

    const interval = setInterval(() => {
      fetchNotifications(user.type);
    }, 30000); // 30 seconds

    return () => clearInterval(interval);
  }, [user?.type]);

  const value = { 
    user, 
    login, 
    logout, 
    notifications, 
    loading,
    markNotificationRead,
    refreshNotifications
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Create a custom hook to easily use the context
export const useAuth = () => {
  return useContext(AuthContext);
};