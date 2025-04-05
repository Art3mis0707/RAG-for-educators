import React, { useState } from 'react';

// Reusable AccordionItem component for each dropdown section
function AccordionItem({ title, description }) {
  const [isOpen, setIsOpen] = useState(false);

  // Toggle the open/closed state when the title is clicked
  const toggleOpen = () => {
    setIsOpen((prevOpen) => !prevOpen);
  };

  // Style for the header container including the rotating arrow
  const headerStyle = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    cursor: 'pointer',
    userSelect: 'none',
    transition: 'color 0.3s',
  };

  const titleStyle = {
    fontSize: '2.5rem',
    margin: '20px 10px 10px',
    borderBottom: '2px solid #1e90ff',
    display: 'inline-block',
    paddingBottom: '10px',
  };

  // Arrow style with rotation based on open state
  const arrowStyle = {
    fontSize: '2.5rem',
    transition: 'transform 0.3s ease',
    transform: isOpen ? 'rotate(90deg)' : 'rotate(0deg)',
  };

  const descriptionContainerStyle = {
    fontSize: '1.2rem',
    lineHeight: '1.8',
    maxWidth: '800px',
    margin: '10px auto 20px',
    transition: 'opacity 0.3s ease, max-height 0.3s ease',
    overflow: 'hidden',
    opacity: isOpen ? 1 : 0,
    maxHeight: isOpen ? '500px' : '0px',
  };

  return (
    <div>
      <div style={headerStyle} onClick={toggleOpen}>
        <h2 style={titleStyle}>{title}</h2>
        <span style={arrowStyle}>&#9654;</span>
      </div>
      <div style={descriptionContainerStyle}>
        {isOpen && <div>{description}</div>}
      </div>
    </div>
  );
}

function Home() {
  // Container style for centering content and applying the dark theme with Courier font
  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '60px 20px',
    textAlign: 'center',
    backgroundColor: '#121212',
    color: '#ffffff',
    minHeight: '100vh',
    fontFamily: '"Century Schoolbook", serif'
  };

  // Style for the main heading with a subtle text shadow
  const headingStyle = {
    fontSize: '3.5rem',
    marginBottom: '30px',
    letterSpacing: '1px',
    textShadow: '2px 2px 4px rgba(0, 0, 0, 0.5)',
  };

  // Style for paragraphs with increased line height for readability
  const paragraphStyle = {
    fontSize: '1.2rem',
    lineHeight: '1.8',
    maxWidth: '800px',
    margin: '0 auto 20px',
  };

  // Style for section titles (for Why Teachers Love TeachSmart)
  const sectionTitleStyle = {
    fontSize: '2.5rem',
    margin: '50px 0 20px',
    borderBottom: '2px solid #1e90ff',
    display: 'inline-block',
    paddingBottom: '10px',
  };

  // Style for quotes
  const quoteStyle = {
    fontStyle: 'italic',
    fontSize: '1.4rem',
    margin: '30px 0',
    borderLeft: '4px solid #1e90ff',
    paddingLeft: '20px',
  };

  // Style for quote authors
  const quoteAuthorStyle = {
    marginTop: '10px',
    fontWeight: 'bold',
    fontSize: '1.2rem',
  };

  return (
    <div style={containerStyle}>
      <h1 style={headingStyle}>Welcome to TeachSmart</h1>
      <p style={paragraphStyle}>
        Transform the way you support student success. TeachSmart gives you instant insights and automated personalization to help every student reach their potential.
      </p>
      <p style={{ ...paragraphStyle, fontWeight: 'bold', fontSize: '1.3rem' }}>
        Your Command Center for Student Achievement
      </p>

      {/* Collapsible Sections for Smart Analytics, Visual Insights, Automated Support */}
      <div style={{ marginTop: '50px', maxWidth: '800px' }}>
        <AccordionItem
          title="Smart Analytics"
          description="Ask natural questions about student performance and get instant, data-driven answers."
        />
        <AccordionItem
          title="Visual Insights"
          description="Track student progress through intuitive dashboards that highlight trends and patterns."
        />
        <AccordionItem
          title="Automated Support"
          description="Send personalized study materials based on each student's exam performance with just one click."
        />
      </div>

      {/* Collapsible How It Works Section */}
      <div style={{ marginTop: '60px', maxWidth: '800px' }}>
        <AccordionItem
          title="How It Works"
          description={
            <>
              <p>
                <strong>Upload your student assessment data</strong>
              </p>
              <p>
                Get immediate insights through natural language questions or visual dashboards.
              </p>
              <p>
                Automatically generate and send customized study resources to students who need extra support.
              </p>
            </>
          }
        />
      </div>

      {/* Why Teachers Love TeachSmart Section (remains static) */}
      <div style={{ marginTop: '60px', maxWidth: '800px' }}>
        <h2 style={sectionTitleStyle}>Why Teachers Love TeachSmart</h2>
        <p style={quoteStyle}>
          "I used to spend hours analyzing exam results and creating individual study plans. TeachSmart does this in minutes, letting me focus on what matters most - teaching."
        </p>
        <p style={quoteAuthorStyle}>Gayatri, High School Mathematics</p>
      </div>
    </div>
  );
}

export default Home;
