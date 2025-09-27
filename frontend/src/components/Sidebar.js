import React from 'react';
import { NavLink } from 'react-router-dom';
import { FaHome, FaCalendarAlt, FaSignOutAlt,  FaFileUpload, FaVideo, FaCheckCircle, FaBell  } from 'react-icons/fa';
import {useAuth} from '../context/AuthContext';
import '../App.css';

const Sidebar = () => {
  const { user, logout, notifications} = useAuth();

   // Calculate unread notification count for the current user
   const notificationCount = notifications.filter(n => !n.is_read).length;
  return (
    <nav className="sidebar">
      <div className="sidebar-header">
        <h3>AI Meeting Buddy</h3>
      </div>
      <ul className="nav-list">
        <li className="nav-item">
          <NavLink to="/" end>
            <FaHome />
            Home
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/scheduler">
            <FaCalendarAlt />
            Scheduler
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/meetings">
            <FaVideo /> Meetings
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/follow-ups">
            <FaCheckCircle /> Follow Ups
          </NavLink>
        </li>
        <li className="nav-item">
          {/* Updated NavLink for Notifications */}
          <NavLink to="/notifications">
            <FaBell /> 
            Notifications
            {/* Badge appears if there are new notifications */}
            {notificationCount > 0 && (
              <span className="notification-badge">{notificationCount}</span>
            )}
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/upload-transcript">
            <FaFileUpload /> Upload Transcript
          </NavLink>
        </li>
        <li className="nav-item logout-item">
          <button className="logout-button" onClick={logout}>
            <FaSignOutAlt />
            Logout
          </button>
        </li> 
      </ul>
    </nav>
  );
};

export default Sidebar;