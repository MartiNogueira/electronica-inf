import React from 'react';
import { FaCar } from 'react-icons/fa';
import Button from './Button';
import '../css/Login.css';
import {useNavigate} from "react-router-dom";

const Welcome: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="container">
      <div className="content">
        <div className="logo">
          <FaCar size={48} color="#4F46E5" />
          <span>DriveIn</span>
        </div>
        
        <p className="slogan">
          Your smart parking solution
        </p>

        <div className="button-container">
          <Button 
            title="Login" 
            variant="primary"
            onClick={() => navigate('/login')}
          />
          <Button 
            title="Register" 
            variant="secondary"
            onClick={() => navigate('/register')}
          />
        </div>
      </div>
    </div>
  );
};

export default Welcome; 