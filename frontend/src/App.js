import './App.css';

// pages
import HomePage from './pages/HomePage';
import PredictionPage from './pages/PredictionPage';

// react router components: main router in index.js
import { Routes, Route } from 'react-router-dom';

function App() {
  return (
    <div className="app">
      <Routes>
        <Route path="/" element={<HomePage />} />"
        <Route path="/prediction" element={<PredictionPage />} />
      </Routes>
    </div>
  );
}

export default App;