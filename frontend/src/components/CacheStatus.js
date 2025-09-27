import React from 'react';

const CacheStatus = ({ isUsingCache, lastUpdated }) => {
  if (!isUsingCache) return null;

  const timeAgo = lastUpdated ? Math.floor((Date.now() - lastUpdated) / 1000) : 0;
  
  const formatTimeAgo = (seconds) => {
    if (seconds < 60) return `${seconds}s ago`;
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    return `${hours}h ago`;
  };

  return (
    <div className="cache-status">
      <span className="cache-indicator">
        📦 Using cached data ({formatTimeAgo(timeAgo)})
      </span>
    </div>
  );
};

export default CacheStatus;
