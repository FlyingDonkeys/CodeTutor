import React from 'react';
//import '../../static/css/navbar.css'; // You can add custom styling in this CSS file

const NavBar = () => {
  return (
    <nav className="navbar shadow">
      <div className="logo">
        <img  style={{height:'50px'}} src="../../static/images/Favicon.ico" alt="Code Tutor Logo" />
      </div>
      <ul className="nav-links" >
        <li><a href="#find-tutor">Find a tutor</a></li>
        <li><a href="#become-tutor">Become a tutor</a></li>
        <li><a href="#how-it-works">How it works</a></li>
        <li><a style={{verticalAlign:'middle',fontSize:'large'}} href="/create">Sign Up</a></li>
        <li><a style={{verticalAlign:'middle',fontSize:'large'}} href="/login">Log In</a></li>
      </ul>
    </nav>
  );
};

export default NavBar;
