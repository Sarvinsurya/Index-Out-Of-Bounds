import React from 'react';

const KeyContextCard = ({ contextData, loading = false }) => {
  // Show loading state
  if (loading) {
    return (
      <div className="card">
        <h3>📊&nbsp; Key Context</h3>
        <div className="card-content">
          <div className="loading-spinner">🔄 Analyzing relationship data...</div>
        </div>
      </div>
    );
  }

  // Gracefully handle the case where data might not be loaded yet
  if (!contextData) {
    return (
      <div className="card">
        <h3>📊&nbsp; Key Context</h3>
        <div className="card-content">
          <p>No context data available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h3>📊&nbsp; Key Context</h3>
      <div className="card-content">
        {/* Trust Score Header */}
        <div className="trust-score-header">
          <div className="trust-score-main">
            <span className="trust-label">Trust Score</span>
            <span className="trust-value">{contextData.trust_score || 0}/10</span>
          </div>
          <div className="relationship-status">
            <span className="status-badge">{contextData.relationship_status || 'Unknown'}</span>
          </div>
        </div>

        {/* Last Meeting Summary */}
        <div className="meeting-summary">
          <h5>📅 Last Meeting ({contextData.last_meeting_date || 'N/A'})</h5>
          <div className="meeting-summary-content">
            {contextData.last_meeting_summary ? (
              contextData.last_meeting_summary.split('\n').map((line, index) => (
                <div key={index} className="summary-line">
                  {line.trim()}
                </div>
              ))
            ) : (
              <div className="summary-line">No meeting summary available</div>
            )}
          </div>
        </div>

        {/* Key Insights */}
        {contextData.key_insights && contextData.key_insights.length > 0 && (
          <div className="key-insights">
            <h5>💡 Key Insights</h5>
            <ul className="insights-list">
              {contextData.key_insights.map((insight, index) => (
                <li key={index} className="insight-item">
                  {insight}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Sales Highlights */}
        {contextData.sales_highlights && contextData.sales_highlights.length > 0 && (
          <div className="sales-highlights">
            <h5>📈 Sales Highlights</h5>
            {contextData.sales_highlights.map((highlight, index) => (
              <div key={index} className="highlight-item">
                <div className="product-name">{highlight.product}</div>
                <div className="performance-info">
                  <span className="performance">{highlight.performance}</span>
                  <span className={`trend ${highlight.trend}`}>
                    {highlight.trend === 'positive' ? '📈' : highlight.trend === 'negative' ? '📉' : '➡️'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default KeyContextCard;