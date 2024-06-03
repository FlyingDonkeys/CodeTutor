import React from 'react';
import './LandingPage.css';

const LandingPage = () => {
  return (
    <div className="landing-page">
      <header className="header">
        <div className="logo">
          <img src="path_to_logo_image" alt="Code Tutor Logo" />
        </div>
        <nav className="navbar">
          <ul>
            <li>Dashboard</li>
            <li>Find a tutor</li>
            <li>How it works</li>
          </ul>
        </nav>
        <div className="user-info">
          <p>Jason Student</p>
          <button className="logout-button">Log Out</button>
        </div>
      </header>
      <main className="main-content">
        <div className="timetable">
          <h2>My Time Table</h2>
          <img src="path_to_timetable_image" alt="Timetable" />
        </div>
        <div className="buttons">
          <button className="find-tutor-button">Find 1 to 1 Tutoring Session</button>
          <button className="my-requests-button">My Requests</button>
        </div>
      </main>
    </div>
  );
};

export default LandingPage;
