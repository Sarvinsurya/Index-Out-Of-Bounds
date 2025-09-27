import { React, useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

const FollowUpsPage = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [followUps, setFollowUps] = useState([]);
  const [nextMeeting, setNextMeeting] = useState(null);

  useEffect(() => {
    Promise.all([
      fetch('/follow_ups.json').then(res => res.json()),
      fetch('/meetings.json').then(res => res.json())
    ])
    .then(([followUpsData, meetingsData]) => {
      let initialFollowUps = followUpsData.items.map(item => ({
        ...item,
        status: item.status || 'Pending'
      }));

      // New: Sort the follow-ups by date in ascending order (oldest first)
      initialFollowUps.sort((a, b) => new Date(a.date) - new Date(b.date));

      setFollowUps(initialFollowUps);

      const now = new Date();
      const upcomingMeeting = meetingsData.meetings
        .sort((a, b) => new Date(a.startTime) - new Date(b.startTime))
        .find(meeting => new Date(meeting.startTime) > now);
      
      setNextMeeting(upcomingMeeting);
      setLoading(false);
    });
  }, []);

  const handleStatusChange = (followUpId, newStatus) => {
    const updatedFollowUps = followUps.map(item => {
      if (item.id === followUpId) {
        return { ...item, status: newStatus };
      }
      return item;
    });
    setFollowUps(updatedFollowUps);
  };

  const getEffectiveStatus = (item) => {
    const isPastDue = nextMeeting && new Date() > new Date(nextMeeting.startTime);
    if (item.status === 'Pending' && isPastDue) {
      return 'Overdue';
    }
    return item.status;
  };

  const getStatusClass = (status) => {
    return status.toLowerCase();
  };

  if (loading) {
    return <div className="loading-screen">Loading Follow Ups...</div>;
  }

  return (
    <>
      <header className="app-header">
        <h2 className="page-subtitle">Action Items & Follow Ups</h2>
      </header>
      <div className="follow-ups-container">
        <div className="follow-up-list">
          {followUps.map(item => {
            const effectiveStatus = getEffectiveStatus(item);
            return (
              <div key={item.id} className="follow-up-row">
                <div className="follow-up-task">
                  <p>{item.task}</p>
                  <p className="follow-up-date">
                    From Meeting on: {new Date(item.date + 'T00:00:00Z').toLocaleDateString('en-GB', { day: 'numeric', month: 'long' })}
                  </p>
                </div>
                <div className="follow-up-status">
                  <span className={`status ${getStatusClass(effectiveStatus)}`}>
                    {effectiveStatus}
                  </span>
                </div>
                <div className="follow-up-action">
                  <select 
                    value={item.status} 
                    onChange={(e) => handleStatusChange(item.id, e.target.value)}
                  >
                    <option value="Pending">Pending</option>
                    <option value="Done">Done</option>
                  </select>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
};

export default FollowUpsPage;