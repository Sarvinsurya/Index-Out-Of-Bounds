import React from 'react';
import { useAuth } from '../context/AuthContext';
import { FaBuilding, FaGlobeEurope} from 'react-icons/fa';

const LoginPage = () => {
  const { login } = useAuth();

  return (
    <div className="login-page-background">
      <div className="login-container">
        <div className="login-box">
          <div className="login-header">
            <h1>AI Meeting Buddy</h1>
          </div>
          <p>Select your role to Login</p>
          
          <div className="role-selection-container">
            {/* Vendor Card */}
            <div className="role-card" onClick={() => login('vendor')}>
              <FaBuilding className="role-icon" />
              <div className="role-text">
                <h2>Vendor</h2>
                <p>Zoho (Chennai)</p>
              </div>
            </div>

            {/* Distributor Card */}
            <div className="role-card" onClick={() => login('distributor')}>
              <FaGlobeEurope className="role-icon" />
              <div className="role-text">
                <h2>Distributor</h2>
                <p>Germany</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;