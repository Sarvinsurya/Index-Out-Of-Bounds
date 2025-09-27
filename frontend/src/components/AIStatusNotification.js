import React from 'react';

const AIStatusNotification = ({ aiStatus, fallbackUsed, onClose }) => {
  // COMMENTED OUT: Hide all fallback notifications from user
  // if (aiStatus === "active" && !fallbackUsed) {
  //   return null; // Don't show notification when everything is working fine
  // }
  
  // Always return null to hide all notifications
  return null;

  const getNotificationContent = () => {
    if (aiStatus === "quota_exceeded") {
      return {
        title: "🚨 AI Quota Exceeded",
        message: "OpenAI API quota exceeded. Add payment method at platform.openai.com/settings/organization/billing to restore AI functionality. Using smart fallback algorithms for now.",
        type: "warning",
        icon: "⚠️"
      };
    } else if (aiStatus === "invalid_key") {
      return {
        title: "🔑 Invalid API Key",
        message: "OpenAI API key is invalid or expired. Get a new key at platform.openai.com/api-keys. Using intelligent fallback systems.",
        type: "error",
        icon: "🔑"
      };
    } else if (aiStatus === "error") {
      return {
        title: "🔧 AI Service Unavailable", 
        message: "AI processing is temporarily unavailable. Using intelligent fallback systems to ensure continued functionality.",
        type: "error",
        icon: "🛠️"
      };
    } else if (fallbackUsed) {
      return {
        title: "🔄 Fallback Mode Active",
        message: "Using enhanced business logic instead of AI ranking. Results remain reliable and optimized.",
        type: "info", 
        icon: "ℹ️"
      };
    }
  };

  const notification = getNotificationContent();
  
  if (!notification) return null;

  return (
    <div className={`ai-status-notification ${notification.type}`}>
      <div className="notification-content">
        <div className="notification-header">
          <span className="notification-icon">{notification.icon}</span>
          <h4 className="notification-title">{notification.title}</h4>
          <button className="close-button" onClick={onClose}>×</button>
        </div>
        <p className="notification-message">{notification.message}</p>
        <div className="notification-details">
          <small>💡 Tip: The AI Meeting Buddy continues to work with intelligent business logic even when AI services are limited.</small>
        </div>
      </div>
    </div>
  );
};

export default AIStatusNotification;
