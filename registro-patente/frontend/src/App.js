import logo from './logo.svg';
import './App.css';

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import PropietarioForm from './components/PropietariosForm';
import VisitaForm from './components/VisitaForm';

function App() {
  return (

    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/propietario" element={<PropietarioForm />} />
        <Route path="/visita" element={<VisitaForm />} />
      </Routes>
    </Router>
  );
}

export default App;
