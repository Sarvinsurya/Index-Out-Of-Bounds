import React from 'react';

const AgendaCard = ({ agendaData, loading = false }) => {
  // Show loading state
  if (loading) {
    return (
      <div className="card">
        <h3>📝&nbsp; AI Generated Agenda</h3>
        <div className="card-content">
          <div className="loading-spinner">🤖 AI generating personalized agenda...</div>
          <div className="loading-progress">
            <div>✅ Analyzing past meetings</div>
            <div>🔄 Processing sales data</div>
            <div>⏳ Creating agenda items</div>
          </div>
        </div>
      </div>
    );
  }

  if (!agendaData || !agendaData.agenda_items || agendaData.agenda_items.length === 0) {
    return (
      <div className="card">
        <h3>📝&nbsp; AI Generated Agenda</h3>
        <div className="card-content">
          <p>No agenda available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h3>📝&nbsp; AI Generated Agenda</h3>
      <div className="card-content">
        <div className="agenda-header">
          <h4>{agendaData.agenda_title}</h4>
          <p className="duration">Duration: {agendaData.estimated_duration} minutes</p>
        </div>
        <ol className="agenda-list">
          {agendaData.agenda_items.map((item, index) => (
            <li key={index} className="agenda-item">
              <div className="agenda-time">{item.time}</div>
              <div className="agenda-content">
                <strong>{item.topic}</strong>
                <p>{item.description}</p>
                <span className={`priority ${item.priority}`}>{item.priority} priority</span>
              </div>
            </li>
          ))}
        </ol>
        {agendaData.discussion_priorities && agendaData.discussion_priorities.length > 0 && (
          <div className="priorities">
            <h5>🎯 Key Priorities:</h5>
            <ul>
              {agendaData.discussion_priorities.map((priority, index) => (
                <li key={index}>{priority}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default AgendaCard;