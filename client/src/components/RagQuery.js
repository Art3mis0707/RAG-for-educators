import React, { useState } from 'react';
import axios from 'axios';

function RagQuery() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult('');
    try {
      const response = await axios.post('http://localhost:5004/api/rag', { query });
      setResult(response.data.result);
    } catch (err) {
      setError('Error running the query. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Inline styles for centering, dark theme, and font settings.
  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '80vh', // Adjust height as needed
    backgroundColor: '#121212',
    padding: '20px',
    color: '#fff',
    fontFamily: '"Century Schoolbook", serif' // Set font here
  };

  const formStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '15px',
    backgroundColor: '#1f1f1f',
    padding: '30px',
    borderRadius: '10px',
    boxShadow: '0 4px 10px rgba(0, 0, 0, 0.3)'
  };

  const inputStyle = {
    width: '400px',
    padding: '12px',
    borderRadius: '5px',
    border: '1px solid #333',
    backgroundColor: '#2c2c2c',
    color: '#fff'
  };

  const buttonStyle = {
    padding: '12px 24px',
    borderRadius: '5px',
    backgroundColor: '#1e90ff',
    color: '#fff',
    border: 'none',
    cursor: 'pointer',
    fontWeight: 'bold'
  };

  const resultStyle = {
    marginTop: '20px',
    width: '400px',
    backgroundColor: '#2e2e2e',
    color: '#fff',
    padding: '15px',
    borderRadius: '5px',
    whiteSpace: 'pre-wrap'
  };

  return (
    <div style={containerStyle}>
      <h1>Analyze your students' data in seconds!</h1>
      <form onSubmit={handleSubmit} style={formStyle}>
        <label htmlFor="query">Enter your query:</label>
        <input
          type="text"
          id="query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Type your query here..."
          style={inputStyle}
        />
        <button type="submit" style={buttonStyle}>
          {loading ? 'Processing...' : 'Run Query'}
        </button>
      </form>
      {error && <p style={{ color: '#ff6b6b' }}>{error}</p>}
      {result && (
        <div style={resultStyle}>
          <h3>Result:</h3>
          <p>{result}</p>
        </div>
      )}
    </div>
  );
}

export default RagQuery;
