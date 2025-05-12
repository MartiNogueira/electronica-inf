import React from 'react';
import { FaCar, FaBell, FaExclamationTriangle, FaKey, FaEdit, FaHome, FaList, FaUser } from 'react-icons/fa';
import { IconType } from 'react-icons';
import { useNavigate } from 'react-router-dom';
import '../css/Home.css';

interface MenuItem {
  icon: IconType;
  title: string;
  onClick: () => void;
}

const Home: React.FC = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    navigate('/');
  };

  const menuItems: MenuItem[] = [
    { 
      icon: FaBell, 
      title: 'Notifications and Notices',
      onClick: () => console.log('Notifications clicked')
    },
    { 
      icon: FaExclamationTriangle, 
      title: 'Incidents',
      onClick: () => console.log('Incidents clicked')
    },
    { 
      icon: FaKey, 
      title: 'Authorize Entry',
      onClick: () => navigate('/authorize-entry')
    },
    { 
      icon: FaEdit, 
      title: 'Edit Authorizations',
      onClick: () => console.log('Edit Authorizations clicked')
    }
  ];

  const navItems: MenuItem[] = [
    {
      icon: FaHome,
      title: 'Home',
      onClick: () => console.log('Home clicked')
    },
    {
      icon: FaList,
      title: 'My Authorizations',
      onClick: () => console.log('My Authorizations clicked')
    },
    {
      icon: FaUser,
      title: 'Profile',
      onClick: () => console.log('Profile clicked')
    }
  ];

  return (
    <div className="container">
      <header className="header">
        <div className="logo">
          <FaCar size={24} className="text-accent" />
          <span>DriveIn</span>
        </div>
        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </header>

      <main className="main">
        <div className="grid">
          {menuItems.map((item, index) => (
            <button 
              key={index} 
              className="grid-button"
              onClick={item.onClick}
            >
              {React.createElement(item.icon, { size: 32, className: "text-accent" })}
              <span>{item.title}</span>
            </button>
          ))}
        </div>
      </main>

      <nav className="bottom-nav">
        {navItems.map((item, index) => (
          <button 
            key={index} 
            className="nav-button"
            onClick={item.onClick}
          >
            {React.createElement(item.icon, { size: 20 })}
            <span>{item.title}</span>
          </button>
        ))}
      </nav>
    </div>
  );
};

export default Home; 