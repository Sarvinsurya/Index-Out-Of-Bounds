import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useData } from '../context/DataContext';

const SchedulerPage = () => {
  const { user, addNotification } = useAuth();
  const { state: navState } = useLocation();
  const { 
    fetchScheduleData, 
    fetchContextData, 
    getCachedData, 
    isAnyLoading 
  } = useData();

  // --- State for Data Fetching ---
  const [scheduleData, setScheduleData] = useState(null);
  const [contextData, setContextData] = useState(null);

  // --- State for Form Logic ---
  const [mode, setMode] = useState('discovery');
  const [date, setDate] = useState('');
  const [duration, setDuration] = useState('60');
  const [title, setTitle] = useState('');
  const [timeSlot, setTimeSlot] = useState('');
  const [availableSlots, setAvailableSlots] = useState([]);
  const [selectedSlot, setSelectedSlot] = useState('');
  const [hasSearched, setHasSearched] = useState(false);

  // Effect to fetch required data using the caching system
  useEffect(() => {
    const loadData = async () => {
      console.log('📅 SchedulerPage: Loading data with caching system');
      
      try {
        // Use cached data with quick navigation detection (within 30 seconds)
        const isQuickNavigation = true; // Scheduler page benefits from aggressive caching
        
        // Try to get cached data first for instant display
        const cachedSchedule = getCachedData('scheduleData');
        const cachedContext = getCachedData('contextData');
        
        if (cachedSchedule && cachedContext) {
          console.log('📦 SchedulerPage: Using cached data for instant display');
          setScheduleData(cachedSchedule);
          setContextData(cachedContext);
        }
        
        // Fetch fresh data (will use cache if valid)
        const [schedule, context] = await Promise.all([
          fetchScheduleData(isQuickNavigation),
          fetchContextData(isQuickNavigation)
        ]);
        
        if (schedule) setScheduleData(schedule);
        if (context) setContextData(context);
        
      } catch (error) {
        console.error('❌ SchedulerPage: Error loading data:', error);
        
        // Fallback to any cached data
        const cachedSchedule = getCachedData('scheduleData');
        const cachedContext = getCachedData('contextData');
        
        if (cachedSchedule) setScheduleData(cachedSchedule);
        if (cachedContext) setContextData(cachedContext);
      }
    };
    
    loadData();
  }, [fetchScheduleData, fetchContextData, getCachedData]);

  // Effect to set up the form's initial state after data has been fetched
  useEffect(() => {
    // Only run this logic after the initial data has loaded
    if (scheduleData && contextData) {
      if (navState?.startTime) {
        // USE CASE 1: Navigated from Home page (Prefilled Mode)
        setMode('prefilled');
        setDate(new Date(navState.startTime).toISOString().split('T')[0]);
        setTitle(navState.title || '');
        setTimeSlot(`${formatTime(navState.startTime)} - ${formatTime(navState.endTime)}`);
      } else {
        // USE CASE 2: Navigated from Sidebar (Discovery Mode)
        setMode('discovery');
        setTitle(contextData?.title || 'Follow-up Meeting');
        
        // Set the date to the first available slot date, or today if no slots
        if (scheduleData?.slots && scheduleData.slots.length > 0) {
          // Use the date from the first available slot
          const firstSlotDate = scheduleData.slots[0].start.split('T')[0];
          setDate(firstSlotDate);
        } else {
          // Fallback to today if no slots available
          const today = new Date();
          const yyyy = today.getFullYear();
          const mm = String(today.getMonth() + 1).padStart(2, '0');
          const dd = String(today.getDate()).padStart(2, '0');
          setDate(`${yyyy}-${mm}-${dd}`);
        }
      }
    }
  }, [scheduleData, contextData, navState]); // Re-run if any of these change

  // --- Helper Functions ---
  const formatTime = (dateString) => {
    if (!dateString) {
      console.warn('No date string provided to formatTime');
      return 'Invalid time';
    }
    try {
      return new Date(dateString).toLocaleTimeString('en-IN', { hour: 'numeric', minute: 'numeric', hour12: true });
    } catch (error) {
      console.error('Error formatting time:', error, dateString);
      return 'Invalid time';
    }
  };

  const handleFindSlots = (e) => {
    e.preventDefault();
    setHasSearched(true);
    setSelectedSlot('');
    
    // Check if we have all required data
    if (!date || !duration || !scheduleData) {
      console.warn('Missing required data for slot search:', { date, duration, scheduleData });
      setAvailableSlots([]);
      return;
    }
    
    // Check if scheduleData has slots array
    if (!scheduleData.slots || !Array.isArray(scheduleData.slots)) {
      console.warn('No slots data available in scheduleData:', scheduleData);
      setAvailableSlots([]);
      return;
    }
    
    try {
      const foundSlots = scheduleData.slots.filter(slot => {
        // Additional safety checks for slot data
        if (!slot || !slot.start || !slot.end) {
          console.warn('Invalid slot data:', slot);
          return false;
        }
        
        if (slot.start.split('T')[0] !== date) return false;
        const slotDuration = (new Date(slot.end) - new Date(slot.start)) / (60 * 1000);
        return slotDuration >= parseInt(duration, 10);
      });
      setAvailableSlots(foundSlots);
    } catch (error) {
      console.error('Error filtering slots:', error);
      setAvailableSlots([]);
    }
  };

  const formatSlotForDisplay = (slot) => {
    if (!slot || !slot.start || !slot.end) {
      console.warn('Invalid slot data for formatting:', slot);
      return 'Invalid slot';
    }
    return `${formatTime(slot.start)} - ${formatTime(slot.end)}`;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    let finalTimeSlot;
    if (mode === 'prefilled') {
      finalTimeSlot = timeSlot;
    } else {
      if (!selectedSlot) { 
        alert('Please select a time slot.'); 
        return; 
      }
      const fullSlot = availableSlots.find(slot => slot.start === selectedSlot);
      if (!fullSlot) { 
        alert('Error: Slot not found.'); 
        return; 
      }
      finalTimeSlot = formatSlotForDisplay(fullSlot);
    }

    try {
      // Send meeting request to backend
      const response = await fetch('/api/meeting/schedule-meeting', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: title,
          date: date,
          time_slot: finalTimeSlot,
          duration: parseInt(duration),
          sender_type: user.type,
          sender_name: user.name
        })
      });

      const result = await response.json();

      if (response.ok) {
        alert(`Meeting Request Sent Successfully!\n\nRecipient: ${result.recipient}\nTitle: ${title}\nDate: ${date}\nTime: ${finalTimeSlot}`);
      } else {
        alert(`Error: ${result.detail || 'Failed to send meeting request'}`);
      }
    } catch (error) {
      console.error('Error scheduling meeting:', error);
      alert('Error: Failed to send meeting request. Please try again.');
    }
  };

  // Render a loading state while fetching data
  if (!scheduleData || !contextData || isAnyLoading()) {
    return <div className="loading-screen">Loading Scheduler...</div>;
  }

  return (
    <>
      <header className="app-header">
        <h2 className="page-subtitle">Schedule a New Meeting</h2>
      </header>
      <div className="scheduler-container">
        <form className="scheduler-form" onSubmit={handleSubmit}>
          {/* Form fields */}
          <div className="form-group">
            <label htmlFor="title">Meeting Title</label>
            <input type="text" id="title" value={title} onChange={(e) => setTitle(e.target.value)} />
          </div>
          <div className="form-group">
            <label htmlFor="date">Date</label>
            <input type="date" id="date" value={date} onChange={(e) => setDate(e.target.value)} disabled={mode === 'prefilled'}/>
          </div>

          {mode === 'prefilled' ? (
            <div className="form-group">
              <label htmlFor="timeSlot">Time Slot</label>
              <input type="text" id="timeSlot" value={timeSlot} readOnly />
            </div>
          ) : (
            <div className="form-group">
              <label htmlFor="duration">Duration (in minutes)</label>
              <input type="number" id="duration" value={duration} onChange={(e) => setDuration(e.target.value)} placeholder="e.g., 60"/>
            </div>
          )}

          {mode === 'discovery' && (
            <>
              <button type="button" className="button-primary" onClick={handleFindSlots}>
                Find Available Slots
              </button>
              {hasSearched && (
                <div className="form-group" style={{ marginTop: '1.5rem' }}>
                  <label htmlFor="slots">Select a Time Slot</label>
                  <select id="slots" value={selectedSlot} onChange={(e) => setSelectedSlot(e.target.value)}>
                    <option value="" disabled>{availableSlots.length > 0 ? `${availableSlots.length} slots found...` : 'No slots available.'}</option>
                    {availableSlots.map((slot, index) => (<option key={index} value={slot.start}>{formatSlotForDisplay(slot)}</option>))}
                  </select>
                </div>
              )}
            </>
          )}

          {(mode === 'prefilled' || selectedSlot) && (
            <button type="submit" className="button-primary">Send Request</button>
          )}
        </form>
      </div>
    </>
  );
};

export default SchedulerPage;