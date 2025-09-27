import React from 'react';
import { Routes, Route } from 'react-router-dom';
import './App.css';

// Import pages and protected route component
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import SchedulerPage from './pages/SchedulerPage';
import MeetingsPage from './pages/MeetingsPage';
import FollowUpsPage from './pages/FollowUpsPage';
import NotificationsPage from './pages/NotificationsPage';
import UploadTranscriptPage from './pages/UploadTranscriptPage';
import ProtectedRoute from './components/ProtectedRoute';

// Import context providers
import { DataProvider } from './context/DataContext';

function App() {
  return (
    <DataProvider>
      <Routes>
        {/* Public route for login */}
        <Route path="/login" element={<LoginPage />} />

        {/* Protected routes for the main app */}
        <Route element={<ProtectedRoute />}>
          {/* These routes can only be accessed after login */}
          <Route path="/" element={<HomePage />} />
          <Route path="/meetings" element={<MeetingsPage />} />
          <Route path="/scheduler" element={<SchedulerPage />} />
          <Route path="/follow-ups" element={<FollowUpsPage />} />
          <Route path="/notifications" element={<NotificationsPage />} />
          <Route path="/upload-transcript" element={<UploadTranscriptPage />} />
        </Route>
      </Routes>
    </DataProvider>
  );
}

export default App;