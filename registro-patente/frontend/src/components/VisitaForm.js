import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const VisitaForm = () => {
  const [patente, setPatente] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/registro/visita', {
        patente
      });
      alert('Visita registrada con éxito');
      setPatente('');
    } catch (error) {
      console.error('Error al registrar visita', error);
    }
  };

  const formContainerStyle = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'flex-start',
    height: '100vh',
    paddingTop: '60px',
    backgroundColor: '#f0f2f5',
    fontFamily: 'Arial, sans-serif'
  };

  const formStyle = {
    display: 'flex',
    flexDirection: 'column',
    gap: '15px',
    border: '1px solid #ccc',
    borderRadius: '8px',
    padding: '30px',
    backgroundColor: '#ffffff',
    width: '320px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
  };

  const inputStyle = {
    padding: '10px',
    fontSize: '16px',
    borderRadius: '4px',
    border: '1px solid #ccc'
  };

  const buttonStyle = {
    padding: '10px',
    fontSize: '16px',
    backgroundColor: '#007bff', // azul como en propietario
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  };

  const linkStyle = {
    marginTop: '10px',
    textAlign: 'center',
    color: '#007bff',
    textDecoration: 'none'
  };

  return (
    <div style={formContainerStyle}>
      <form onSubmit={handleSubmit} style={formStyle}>
        <h2 style={{ textAlign: 'center' }}>Registro de Visita</h2>
        <input
          type="text"
          placeholder="Patente"
          value={patente}
          onChange={(e) => setPatente(e.target.value)}
          style={inputStyle}
        />
        <button type="submit" style={buttonStyle}>Registrar</button>
        <Link to="/" style={linkStyle}>← Volver al inicio</Link>
      </form>
    </div>
  );
};

export default VisitaForm;
