// Home.js o App.js
import React from 'react';
import { useNavigate } from 'react-router-dom';

function Home() {
  const navigate = useNavigate();

  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'flex-start',
    alignItems: 'center',
    height: '80vh',
    paddingTop: '100px',
    backgroundColor: '#f5f5f5',
    fontFamily: 'Arial, sans-serif'
  };
  

  const titleStyle = {
    fontSize: '2rem',
    marginBottom: '2rem',
    color: '#333'
  };

  const buttonStyle = {
    padding: '10px 20px',
    margin: '10px',
    fontSize: '1rem',
    borderRadius: '5px',
    border: 'none',
    backgroundColor: '#007bff',
    color: '#fff',
    cursor: 'pointer'
  };

  return (
    <div style={containerStyle}>
      <h1 style={titleStyle}>ACCESO AL BARRIO</h1>
      <div>
        <button style={buttonStyle} onClick={() => navigate('/propietario')}>PROPIETARIO</button>
        <button style={buttonStyle} onClick={() => navigate('/visita')}>VISITA</button>
      </div>
    </div>
  );
}

export default Home;
