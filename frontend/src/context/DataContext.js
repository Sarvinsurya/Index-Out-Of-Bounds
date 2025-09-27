import React, { createContext, useContext, useState, useCallback } from 'react';

const DataContext = createContext();

// Cache configuration
const CACHE_DURATION = 2 * 60 * 1000; // 2 minutes in milliseconds
const QUICK_CACHE_DURATION = 30 * 1000; // 30 seconds for quick navigation

export const DataProvider = ({ children }) => {
  // State for cached data
  const [cache, setCache] = useState({
    scheduleData: { data: null, timestamp: null, loading: false, promise: null },
    contextData: { data: null, timestamp: null, loading: false, promise: null },
    agendaData: { data: null, timestamp: null, loading: false, promise: null },
    followUpsData: { data: null, timestamp: null, loading: false, promise: null },
  });

  // Global loading and notification states
  const [globalLoading, setGlobalLoading] = useState(false);
  const [aiStatus, setAiStatus] = useState('active');
  const [showNotification, setShowNotification] = useState(false);

  // Check if cached data is still valid
  const isCacheValid = useCallback((cacheEntry, quickNavigation = false) => {
    if (!cacheEntry.data || !cacheEntry.timestamp) return false;
    
    const now = Date.now();
    const maxAge = quickNavigation ? QUICK_CACHE_DURATION : CACHE_DURATION;
    return (now - cacheEntry.timestamp) < maxAge;
  }, []);

  // Generic fetch function with caching
  const fetchWithCache = useCallback(async (endpoint, cacheKey, quickNavigation = false) => {
    const cacheEntry = cache[cacheKey];
    
    // Return cached data if valid
    if (isCacheValid(cacheEntry, quickNavigation) && !cacheEntry.loading) {
      console.log(`📦 Using cached data for ${cacheKey}`);
      return cacheEntry.data;
    }

    // Prevent duplicate requests - wait for existing promise
    if (cacheEntry.loading && cacheEntry.promise) {
      console.log(`⏳ Request already in progress for ${cacheKey} - waiting for completion`);
      try {
        return await cacheEntry.promise;
      } catch (error) {
        console.log(`⚠️ Existing request failed for ${cacheKey}, returning cached data`);
        return cacheEntry.data;
      }
    }

    // Create the fetch promise with timeout
    const fetchPromise = (async () => {
      try {
        console.log(`🌐 Fetching fresh data for ${cacheKey} from ${endpoint}`);
        
        // Create AbortController for timeout
        const controller = new AbortController();
          const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout for better reliability
        
        const response = await fetch(endpoint, {
          signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Update cache with new data
        setCache(prev => ({
          ...prev,
          [cacheKey]: {
            data,
            timestamp: Date.now(),
            loading: false,
            promise: null
          }
        }));

        // Handle AI status notifications - COMMENTED OUT to hide fallback notifications from user
        // if (data.ai_status && data.ai_status !== 'active') {
        //   setAiStatus(data.ai_status);
        //   setShowNotification(true);
        // }

        return data;
      } catch (error) {
        console.error(`❌ Error fetching ${cacheKey}:`, error);
        
        // Check if it's a timeout error
        if (error.name === 'AbortError') {
          console.log(`⏰ Request timed out for ${cacheKey}, using fallback data`);
          
          // Provide fallback data based on cache key
          let fallbackData = {};
          if (cacheKey === 'followUpsData') {
            fallbackData = {
              pending_actions: [],
              completed_actions: [],
              overdue_items: [],
              action_completion_rate: 0.0,
              next_review_date: "2025-10-15",
              ai_status: "timeout",
              fallback_used: true
            };
          } else if (cacheKey === 'agendaData') {
            fallbackData = {
              meeting_topics: [],
              discussion_points: [],
              time_allocations: {},
              preparation_notes: [],
              ai_status: "timeout",
              fallback_used: true
            };
          }
          
          // Update cache with fallback data
          setCache(prev => ({
            ...prev,
            [cacheKey]: {
              data: fallbackData,
              timestamp: Date.now(),
              loading: false,
              promise: null
            }
          }));
          
          return fallbackData;
        }
        
        // Reset loading state but keep existing data
        setCache(prev => ({
          ...prev,
          [cacheKey]: { 
            ...prev[cacheKey], 
            loading: false, 
            promise: null 
          }
        }));
        
        // Return cached data if available, even if stale
        return cacheEntry.data;
      }
    })();

    // Set loading state with promise
    setCache(prev => ({
      ...prev,
      [cacheKey]: { 
        ...prev[cacheKey], 
        loading: true, 
        promise: fetchPromise 
      }
    }));

    return await fetchPromise;
  }, [cache, isCacheValid]);

  // Specific fetch functions
  const fetchScheduleData = useCallback((quickNavigation = false) => {
    return fetchWithCache('/api/meeting/schedule', 'scheduleData', quickNavigation);
  }, [fetchWithCache]);

  const fetchContextData = useCallback((quickNavigation = false) => {
    return fetchWithCache('/api/meeting/context', 'contextData', quickNavigation);
  }, [fetchWithCache]);

  const fetchAgendaData = useCallback((quickNavigation = false) => {
    return fetchWithCache('/api/meeting/agenda', 'agendaData', quickNavigation);
  }, [fetchWithCache]);

  const fetchFollowUpsData = useCallback((quickNavigation = false) => {
    return fetchWithCache('/api/meeting/followups', 'followUpsData', quickNavigation);
  }, [fetchWithCache]);

  // Fetch all data with intelligent caching
  const fetchAllData = useCallback(async (quickNavigation = false) => {
    setGlobalLoading(true);
    
    try {
      // Fetch all data in parallel, using cache when appropriate
      const [schedule, context, agenda, followups] = await Promise.all([
        fetchScheduleData(quickNavigation),
        fetchContextData(quickNavigation),
        fetchAgendaData(quickNavigation),
        fetchFollowUpsData(quickNavigation)
      ]);

      return { schedule, context, agenda, followups };
    } finally {
      setGlobalLoading(false);
    }
  }, [fetchScheduleData, fetchContextData, fetchAgendaData, fetchFollowUpsData]);

  // Clear cache (for manual refresh)
  const clearCache = useCallback(() => {
    console.log('🗑️ Clearing all cached data');
    setCache({
      scheduleData: { data: null, timestamp: null, loading: false, promise: null },
      contextData: { data: null, timestamp: null, loading: false, promise: null },
      agendaData: { data: null, timestamp: null, loading: false, promise: null },
      followUpsData: { data: null, timestamp: null, loading: false, promise: null },
    });
  }, []);

  // Get cached data without fetching
  const getCachedData = useCallback((cacheKey) => {
    return cache[cacheKey]?.data;
  }, [cache]);

  // Check if any data is loading
  const isAnyLoading = useCallback(() => {
    return Object.values(cache).some(entry => entry.loading) || globalLoading;
  }, [cache, globalLoading]);

  const value = {
    // Data fetching functions
    fetchAllData,
    fetchScheduleData,
    fetchContextData,
    fetchAgendaData,
    fetchFollowUpsData,
    
    // Cache management
    clearCache,
    getCachedData,
    
    // State
    cache,
    globalLoading,
    isAnyLoading,
    
    // AI Status
    aiStatus,
    showNotification,
    setShowNotification,
    
    // Utilities
    isCacheValid
  };

  return (
    <DataContext.Provider value={value}>
      {children}
    </DataContext.Provider>
  );
};

export const useData = () => {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error('useData must be used within a DataProvider');
  }
  return context;
};

export default DataContext;
