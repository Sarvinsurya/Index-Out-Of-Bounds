import React from 'react';
import { useAuth } from '../context/AuthContext';

const NotificationsPage = () => {
  const { user, notifications, loading, markNotificationRead, refreshNotifications } = useAuth();

  const handleMarkAsRead = async (notificationId) => {
    await markNotificationRead(notificationId);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'urgent': return '#dc3545';
      case 'high': return '#fd7e14';
      case 'normal': return '#0d6efd';
      case 'low': return '#6c757d';
      default: return '#0d6efd';
    }
  };

  return (
    <>
      <header className="app-header">
        <h2 className="page-subtitle">Your Notifications</h2>
        <button 
          onClick={refreshNotifications}
          className="button-secondary"
          style={{ marginLeft: 'auto' }}
        >
          🔄 Refresh
        </button>
      </header>
      <div className="notifications-container">
        {loading ? (
          <div className="loading-spinner">Loading notifications...</div>
        ) : notifications.length > 0 ? (
          <ul className="notification-list">
            {notifications.map(notification => (
              <li 
                key={notification.id} 
                className={`notification-item ${notification.is_read ? 'read' : 'unread'}`}
                style={{ 
                  borderLeft: `4px solid ${getPriorityColor(notification.priority)}`,
                  opacity: notification.is_read ? 0.7 : 1
                }}
              >
                <div className="notification-header">
                  <h4 className="notification-title">{notification.title}</h4>
                  <div className="notification-meta">
                    <span className="priority-badge" style={{ backgroundColor: getPriorityColor(notification.priority) }}>
                      {notification.priority.toUpperCase()}
                    </span>
                    <span className="notification-date">{formatDate(notification.created_at)}</span>
                  </div>
                </div>
                <p className="notification-message">{notification.message}</p>
                {!notification.is_read && (
                  <button 
                    onClick={() => handleMarkAsRead(notification.id)}
                    className="button-small"
                    style={{ marginTop: '8px' }}
                  >
                    Mark as Read
                  </button>
                )}
                {notification.is_read && (
                  <span className="read-indicator">✓ Read</span>
                )}
              </li>
            ))}
          </ul>
        ) : (
          <div className="no-notifications">
            <p>📭 You have no notifications yet.</p>
            <p>When someone schedules a meeting with you, you'll see it here!</p>
          </div>
        )}
      </div>
    </>
  );
};

export default NotificationsPage;