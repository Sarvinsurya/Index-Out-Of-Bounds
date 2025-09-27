import React from 'react';
import { useNavigate } from 'react-router-dom';

const InstantScheduleCard = ({ scheduleData, contextData, loading = false }) => {
  const navigate = useNavigate();

  // Show loading state
  if (loading) {
    return (
      <div className="card">
        <h3>🕒&nbsp; Instant Schedule</h3>
        <div className="card-content">
          <div className="loading-spinner">⏰ Finding optimal time slots...</div>
        </div>
      </div>
    );
  }

  const findNextAvailableSlot = () => {
    if (!scheduleData || !scheduleData.slots) return null;
    const now = new Date();
    const availabilityStarts = new Date(now.getTime() + 30 * 60 * 1000);
    const nextSlot = scheduleData.slots.find(slot => {
      const slotStart = new Date(slot.start);
      const slotEnd = new Date(slot.end);
      const durationMs = slotEnd.getTime() - slotStart.getTime();
      const oneHourMs = 60 * 60 * 1000;
      return slotStart > availabilityStarts && durationMs >= oneHourMs;
    });
    return nextSlot;
  };

  const formatTime = (date) => date.toLocaleString('en-IN', { hour: 'numeric', minute: 'numeric', hour12: true, timeZone: 'Asia/Kolkata' });
  const formatDate = (date) => {
    const today = new Date(); 
    if (date.toDateString() === today.toDateString()) return 'Today';
    const tomorrow = new Date(); 
    tomorrow.setDate(today.getDate() + 1); 
    if (date.toDateString() === tomorrow.toDateString()) return 'Tomorrow';
    return date.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'short' });
  };
  
  const handleScheduleClick = () => {
    if (!nextSlot) return;

    const meetingTitle = contextData?.title || 'Follow-up Meeting';

    navigate('/scheduler', { 
      state: { 
        startTime: nextSlot.start,
        endTime: nextSlot.end,
        title: meetingTitle,
      } 
    });
  };

  const nextSlot = findNextAvailableSlot();

  return (
    <div className="card">
      <h3>🕒&nbsp; Instant Schedule</h3>
      <div className="card-content">
        {nextSlot ? (
          <div className="schedule-info">
            <p>Next available slot is:</p>
            <div className="time">{formatTime(new Date(nextSlot.start))} - {formatTime(new Date(nextSlot.end))}</div>
            <div className="date">{formatDate(new Date(nextSlot.start))}</div>
            <button className="button-primary" onClick={handleScheduleClick}>
              Schedule Now
            </button>
          </div>
        ) : (
          <p>No available slots found for the near future.</p>
        )}
      </div>
    </div>
  );
};

export default InstantScheduleCard;