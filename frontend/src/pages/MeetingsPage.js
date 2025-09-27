import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

const MeetingsPage = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [upcomingMeeting, setUpcomingMeeting] = useState(null);

  useEffect(() => {
    fetch('/meetings.json')
      .then(res => res.json())
      .then(data => {
        const now = new Date();
        // Find the first meeting where the start time is in the future
        const nextMeeting = data.meetings
          .sort((a, b) => new Date(a.startTime) - new Date(b.startTime)) // Sort meetings by date
          .find(meeting => new Date(meeting.startTime) > now);
        
        setUpcomingMeeting(nextMeeting);
        setLoading(false);
      });
  }, []);

  const formatTime = (dateString) => {
    return new Date(dateString).toLocaleTimeString('en-IN', { hour: 'numeric', minute: 'numeric', hour12: true });
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const today = new Date();
    if (date.toDateString() === today.toDateString()) return 'Today';
    const tomorrow = new Date();
    tomorrow.setDate(today.getDate() + 1);
    if (date.toDateString() === tomorrow.toDateString()) return 'Tomorrow';
    return date.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' });
  };

  if (loading) {
    return <div className="loading-screen">Loading Meetings...</div>;
  }

  return (
    <>
      <header className="app-header">
        <h2 className="page-subtitle">Upcoming Meetings</h2>
      </header>
      <div className="meeting-container">
        {upcomingMeeting ? (
          <div className="meeting-card">
            <h3>{upcomingMeeting.title}</h3>
            <p className="meeting-date">{formatDate(upcomingMeeting.startTime)}</p>
            <p className="meeting-time">
              {formatTime(upcomingMeeting.startTime)} - {formatTime(upcomingMeeting.endTime)}
            </p>
            <button className="button-primary join-button">Join Now</button>
          </div>
        ) : (
          <div className="meeting-card no-meetings">
            <p>You have no upcoming meetings scheduled.</p>
          </div>
        )}
      </div>
    </>
  );
};

export default MeetingsPage;