import React, { useState } from 'react';
import { FaCar, FaEnvelope, FaLock } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import Button from './Button';
import '../css/Login.css';

interface LoginFormData {
  email: string;
  password: string;
}

const Login: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<LoginFormData>({
    email: '',
    password: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Por ahora, redirigimos directamente a home sin validación
    navigate('/home');
  };

  return (
    <div className="container">
      <div className="content">
        <div className="logo">
          <FaCar size={32} color="#4F46E5" />
          <span>DriveIn</span>
        </div>
        
        <p className="slogan">
          Sign in to your account
        </p>

        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <FaEnvelope className="form-icon" />
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <FaLock className="form-icon" />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
            />
          </div>

          <div className="button-container">
            <Button 
              title="Sign In" 
              variant="primary"
              type="submit"
            />
            <Button 
              title="Back" 
              variant="secondary"
              onClick={() => navigate('/')}
            />
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login; 