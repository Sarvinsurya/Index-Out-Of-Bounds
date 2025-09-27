import React from 'react';

const FollowUpCard = ({ followUpsData, loading = false }) => {
  // Show loading state
  if (loading) {
    return (
      <div className="card">
        <h3>✅&nbsp; Follow up from last meet</h3>
        <div className="card-content">
          <div className="loading-spinner">📋 Analyzing action items from previous meetings...</div>
          <div className="loading-progress">
            <div>🔍 Scanning meeting transcripts</div>
            <div>📊 Tracking task status</div>
            <div>⏰ Checking deadlines</div>
          </div>
        </div>
      </div>
    );
  }

  // Check if we have any follow-up data
  const hasPendingActions = followUpsData?.pending_actions?.length > 0;
  const hasCompletedActions = followUpsData?.completed_actions?.length > 0;
  const hasOverdueItems = followUpsData?.overdue_items?.length > 0;
  
  if (!followUpsData || (!hasPendingActions && !hasCompletedActions && !hasOverdueItems)) {
    return (
      <div className="card">
        <h3>✅&nbsp; Follow up from last meet</h3>
        <div className="card-content">
          <p>No follow-ups available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h3>
        ✅&nbsp; Follow up from last meet
      </h3>
      <div className="card-content">
        <div className="completion-rate">
          <h4>📊 Completion Rate: {Math.round(followUpsData.action_completion_rate)}%</h4>
          <p>Next Review: {followUpsData.next_review_date}</p>
        </div>
        
        {hasOverdueItems && (
          <div className="overdue-section">
            <h5>⚠️ Overdue Items ({followUpsData.overdue_items.length})</h5>
            {followUpsData.overdue_items.map((item, index) => (
              <div key={index} className="follow-up-item overdue">
                <p className="task-text">{item.task || item.description}</p>
                <span className="status overdue">overdue</span>
              </div>
            ))}
          </div>
        )}
        
        {hasPendingActions && (
          <div className="pending-section">
            <h5>📋 Pending Actions ({followUpsData.pending_actions.length})</h5>
            {followUpsData.pending_actions.map((item, index) => (
              <div key={index} className="follow-up-item pending">
                <p className="task-text">{item.task || item.description}</p>
                <span className="status pending">pending</span>
              </div>
            ))}
          </div>
        )}
        
        {hasCompletedActions && (
          <div className="completed-section">
            <h5>✅ Recently Completed ({followUpsData.completed_actions.length})</h5>
            {followUpsData.completed_actions.map((item, index) => (
              <div key={index} className="follow-up-item completed">
                <p className="task-text">{item.task || item.description}</p>
                <span className="status completed">done</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default FollowUpCard;