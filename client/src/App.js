import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './components/Home';
import Dashboard from './components/Dashboard'; // Now our Dashboard component uses the iframe
import Emails from './components/Emails';
import RagQuery from './components/RagQuery';
import Upload from './components/UploadDoc';

function App() {
  // Inline style for the navigation bar using Courier font, centered horizontally
  const navStyle = {
    fontFamily: '"Courier New", Courier, monospace',
    display: 'flex',
    justifyContent: 'center',
    gap: '20px',
    padding: '20px',
    backgroundColor: '#1f1f1f'
  };

  // Inline style for the main container with centered text
  const containerStyle = {
    fontFamily: '"Courier New", Courier, monospace',
    padding: '20px',
    textAlign: 'center'
  };

  return (
    <Router>
      <nav className="navbar" style={navStyle}>
        <Link to="/">Home</Link>
        <Link to="/rag">Smart Analytics</Link>
        <Link to="/dashboard">Visual Insights</Link>
        <Link to="/emails">Automated Support</Link>
        <Link to="/upload">Upload Document</Link>


      </nav>
      <div className="container" style={containerStyle}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/emails" element={<Emails />} />
          <Route path="/rag" element={<RagQuery />} />
          <Route path="/upload" element={<Upload />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
