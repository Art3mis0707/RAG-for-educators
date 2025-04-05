import React, { useState } from 'react';

function Emails() {
  const [responseMsg, setResponseMsg] = useState('');

  const handleTriggerEmail = async () => {
    try {
      const response = await fetch('http://localhost:5004/api/send-emails', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      const data = await response.json();
      setResponseMsg(data.message);
    } catch (error) {
      console.error('Error triggering email process:', error);
      setResponseMsg('Failed to trigger email sending.');
    }
  };

  // Container style for centering the box and applying a dark theme
  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '80vh', // Adjust height as needed
    backgroundColor: '#121212',
    padding: '20px',
    color: '#fff',
    fontFamily: '"Century Schoolbook", serif'
  };

  // Box style for the main content area (matching RagQuery's form style)
  const boxStyle = {
    maxWidth: '800px',
    backgroundColor: '#1f1f1f',
    padding: '30px',
    borderRadius: '10px',
    boxShadow: '0 4px 10px rgba(0, 0, 0, 0.3)',
    textAlign: 'center'
  };

  // Button styling similar to RagQuery's button style
  const buttonStyle = {
    padding: '12px 24px',
    borderRadius: '5px',
    backgroundColor: '#1e90ff',
    color: '#fff',
    border: 'none',
    cursor: 'pointer',
    fontWeight: 'bold',
    marginTop: '1rem'
  };

  return (
    <div style={containerStyle}>
      <div style={boxStyle}>
        <h1>Personalized Course Materials</h1>
        <p>
          Our automated learning support system helps each student succeed by providing personalized study materials based on their test performance. After each assessment, the system analyzes how well students understood different topics and automatically sends them customized study resources via email. Rather than using a one-size-fits-all approach, students receive materials specifically chosen to match their current understanding of each topic. For example, if a student shows strong understanding in one area but needs more support in another, they'll receive different types of resources for each topic. This personalized approach ensures every student gets exactly the help they need to improve, delivered straight to their inbox. The system makes it easy for students to access relevant study materials without having to search through multiple resources or guess which materials might be most helpful for their situation.
        </p>
        <button style={buttonStyle} onClick={handleTriggerEmail}>
          Send Emails!
        </button>
        {responseMsg && <p style={{ marginTop: '1rem' }}>{responseMsg}</p>}
      </div>
    </div>
  );
}

export default Emails;
