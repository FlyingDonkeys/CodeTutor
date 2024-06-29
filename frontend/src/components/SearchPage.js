
import React from 'react';
import NavBar from './Navbar';

const SearchFilterPage = (props) => {
  return (
    <div className="search-filter-page">
      <NavBar isHome={false} />
      <div className="main-content">
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
      </div>
    </div>
  );
};

export default SearchFilterPage;
