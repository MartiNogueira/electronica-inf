import React, { useState } from 'react';
import { FaCar, FaUser, FaLock } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import Button from './Button';
import '../css/Login.css';

interface RegisterFormData {
  fullName: string;
  password: string;
  confirmPassword: string;
}

const Register: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<RegisterFormData>({
    fullName: '',
    password: '',
    confirmPassword: ''
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
    // Aquí iría la lógica para enviar los datos al backend
    console.log('Register data:', formData);
    // Por ahora, redirigimos a login
    navigate('/login');
  };

  return (
    <div className="container">
      <div className="content">
        <div className="logo">
          <FaCar size={32} color="#4F46E5" />
          <span>DriveIn</span>
        </div>
        
        <p className="slogan">
          Create your account
        </p>

        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <FaUser className="form-icon" />
            <input
              type="text"
              name="fullName"
              placeholder="Full Name"
              value={formData.fullName}
              onChange={handleChange}
              required
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
              required
            />
          </div>

          <div className="form-group">
            <FaLock className="form-icon" />
            <input
              type="password"
              name="confirmPassword"
              placeholder="Confirm Password"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
            />
          </div>

          <div className="button-container">
            <Button 
              title="Create Account" 
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

export default Register; 