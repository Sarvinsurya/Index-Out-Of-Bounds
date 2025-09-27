import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { useData } from '../context/DataContext';
import InstantScheduleCard from '../components/InstantScheduleCard';
import KeyContextCard from '../components/KeyContextCard';
import AgendaCard from '../components/AgendaCard';
import FollowUpCard from '../components/FollowUpCard';
import AIStatusNotification from '../components/AIStatusNotification';

const HomePage = () => {
  const { user } = useAuth();
  const { 
    fetchAllData, 
    getCachedData, 
    isAnyLoading, 
    aiStatus, 
    showNotification, 
    setShowNotification 
  } = useData();
  
  // Local state for processed data
  const [scheduleData, setScheduleData] = useState(null);
  const [contextData, setContextData] = useState(null);
  const [agendaData, setAgendaData] = useState(null);
  const [followUpsData, setFollowUpsData] = useState(null);
  
  // Track navigation timing for smart caching
  const lastVisitRef = useRef(null);

  useEffect(() => {
    const loadData = async () => {
      // Detect if this is a quick navigation (user was here recently)
      const now = Date.now();
      const isQuickNavigation = lastVisitRef.current && (now - lastVisitRef.current) < 30000; // 30 seconds
      
      if (isQuickNavigation) {
        console.log('🚀 Quick navigation detected - using cached data');
      } else {
        console.log('🔄 Fresh page load - fetching data');
      }
      
      try {
        // Use the smart caching system
        const data = await fetchAllData(isQuickNavigation);
        
        if (data.schedule && data.schedule.suggested_time_ist) {
          // Process schedule data
          const istTimeStr = data.schedule.suggested_time_ist.replace(' IST', '');
          const startTime = new Date(istTimeStr + '+05:30');
          const endTime = new Date(startTime.getTime() + (data.schedule.meeting_duration || 60) * 60000);
          
          const processedScheduleData = {
            slots: [
              {
                start: startTime.toISOString(),
                end: endTime.toISOString()
              },
              ...(data.schedule.alternative_slots || []).map(slot => {
                if (!slot.ist_time && !slot.utc_time) return null;
                const altIstTime = slot.ist_time ? slot.ist_time.replace(' IST', '') : slot.utc_time.replace(' UTC', '');
                const altStart = new Date(altIstTime + (slot.ist_time ? '+05:30' : 'Z'));
                const altEnd = new Date(altStart.getTime() + 60 * 60000);
                return {
                  start: altStart.toISOString(),
                  end: altEnd.toISOString()
                };
              }).filter(slot => slot !== null)
            ]
          };
          
          setScheduleData(processedScheduleData);
        }
        
        if (data.context) {
          setContextData(data.context);
        }
        
        if (data.agenda) {
          setAgendaData(data.agenda);
        }
        
        if (data.followups) {
          setFollowUpsData(data.followups);
        }
        
      } catch (error) {
        console.error('❌ Error loading data:', error);
        
        // Try to use any cached data as fallback
        const cachedSchedule = getCachedData('scheduleData');
        const cachedContext = getCachedData('contextData');
        const cachedAgenda = getCachedData('agendaData');
        const cachedFollowups = getCachedData('followUpsData');
        
        if (cachedSchedule && cachedSchedule.suggested_time_ist) {
          // Process cached schedule data
          const istTimeStr = cachedSchedule.suggested_time_ist.replace(' IST', '');
          const startTime = new Date(istTimeStr + '+05:30');
          const endTime = new Date(startTime.getTime() + (cachedSchedule.meeting_duration || 60) * 60000);
          
          setScheduleData({
            slots: [{
              start: startTime.toISOString(),
              end: endTime.toISOString()
            }]
          });
        }
        if (cachedContext) setContextData(cachedContext);
        if (cachedAgenda) setAgendaData(cachedAgenda);
        if (cachedFollowups) setFollowUpsData(cachedFollowups);
      }
    };
    
    loadData();
    
    // Update last visit time when component unmounts
    return () => {
      lastVisitRef.current = Date.now();
    };
  }, [fetchAllData, getCachedData]);

  // Determine overall AI status for notification
  const getOverallAiStatus = () => {
    if (aiStatus === 'quota_exceeded') return 'quota_exceeded';
    if (aiStatus === 'invalid_key') return 'invalid_key';
    if (aiStatus === 'error') return 'error';
    return 'active';
  };

  // Loading states based on data availability and global loading
  const loading = {
    schedule: !scheduleData && isAnyLoading(),
    context: !contextData && isAnyLoading(),
    agenda: !agendaData && isAnyLoading(),
    followups: !followUpsData && isAnyLoading()
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>🤖 AI Meeting Buddy</h1>
        <p>Welcome back, {user?.name || 'User'}! Here's your intelligent meeting dashboard.</p>
      </div>

      {/* AI Status Notification */}
      {showNotification && (
        <AIStatusNotification 
          aiStatus={getOverallAiStatus()} 
          onClose={() => setShowNotification(false)} 
        />
      )}

      <div className="dashboard-grid">
        <InstantScheduleCard 
          scheduleData={scheduleData} 
          loading={loading.schedule}
        />
        <KeyContextCard 
          contextData={contextData} 
          loading={loading.context}
        />
        <AgendaCard 
          agendaData={agendaData} 
          loading={loading.agenda}
        />
        <FollowUpCard 
          followUpsData={followUpsData} 
          loading={loading.followups}
        />
      </div>
    </div>
  );
};

export default HomePage;