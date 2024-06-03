
import React from 'react';
import './SearchFilterPage.css';

const SearchFilterPage = () => {
  return (
    <div className="search-filter-page">
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
        <div className="search-bar">
          <input type="text" placeholder="Search" />
          <button className="search-button">Search</button>
        </div>
        <div className="filters">
          <button className="filter-button">Computer Science</button>
          <button className="filter-button">Price:  200</button>
          <button className="filter-button">Location: Any</button>
        </div>
        <div className="tutor-results">
          <div className="tutor-card">
            <img src="path_to_tutor_image" alt="Tutor" />
            <div className="tutor-info">
              <p>Name: Leon</p>
              <p>Intro: I am currently a senior developer working in Meta...</p>
              <p>Rating: ⭐⭐⭐⭐⭐</p>
              <p>Price: $100/h</p>
              <button className="request-button">Send Lesson Request</button>
            </div>
          </div>
          {/* Repeat the above block for each tutor result */}
        </div>
      </main>
    </div>
  );
};

export default SearchFilterPage;
