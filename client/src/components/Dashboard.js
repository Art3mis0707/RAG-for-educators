import React from 'react';

function Dashboard() {
  // Container style to center the iframe and match the dark theme
  const containerStyle = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    backgroundColor: '#121212', // Matches your dark theme
    padding: '20px'
  };

  // Style for the embedded iframe
  const iframeStyle = {
    width: '90%',
    height: '90%',
    border: 'none',
    borderRadius: '15px',
    boxShadow: '0 4px 10px rgba(0, 0, 0, 0.3)'
  };

  return (
    <div style={containerStyle}>
      <iframe
        src="http://localhost:8501" // URL where your Streamlit app is running
        style={iframeStyle}
        title="Student Score Dashboard"
      ></iframe>
    </div>
  );
}

export default Dashboard;
