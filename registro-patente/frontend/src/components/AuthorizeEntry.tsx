import React, { useState } from 'react';
import { FaUser, FaCar, FaArrowLeft } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import '../css/AuthorizeEntry.css';

interface AuthorizeEntryFormData {
  firstName: string;
  lastName: string;
  licensePlate: string;
}

const AuthorizeEntry: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<AuthorizeEntryFormData>({
    firstName: '',
    lastName: '',
    licensePlate: ''
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
    console.log('Authorize Entry data:', formData);
    // Aquí iría la lógica para enviar los datos al backend
    navigate('/home');
  };

  return (
    <div className="container">
      <header className="header">
        <button className="back-button" onClick={() => navigate('/home')}>
          <FaArrowLeft size={20} />
          <span>Back</span>
        </button>
        <h1>Authorize Entry</h1>
      </header>

      <main className="main">
        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <FaUser className="form-icon" />
            <input
              type="text"
              name="firstName"
              placeholder="First Name"
              value={formData.firstName}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <FaUser className="form-icon" />
            <input
              type="text"
              name="lastName"
              placeholder="Last Name"
              value={formData.lastName}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <FaCar className="form-icon" />
            <input
              type="text"
              name="licensePlate"
              placeholder="License Plate"
              value={formData.licensePlate}
              onChange={handleChange}
              required
            />
          </div>

          <button type="submit" className="submit-button">
            Authorize Entry
          </button>
        </form>
      </main>
    </div>
  );
};

export default AuthorizeEntry; 