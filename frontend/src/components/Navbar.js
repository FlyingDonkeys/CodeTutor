import React from 'react';
//import '../../static/css/navbar.css'; // You can add custom styling in this CSS file
//import { Container } from '@material-ui/core';
const NavBar = (props) => {
  return (
    <nav className="navbar shadow">
      <div className="logo">
        <a href = "/">
        <img  style={{height:'50px'}} src="../../static/images/Favicon.ico" alt="Code Tutor Logo"/>
        </a>
      </div>
      {props.isHome ? 
      <ul className="nav-links" >
        <li><a href="#find-tutor">Find a tutor</a></li>
        <li><a href="#become-tutor">Become a tutor</a></li>
        <li><a href="#how-it-works">How it works</a></li>
        <li><a href="/sign-up">Sign Up As Student</a></li>
        <li><a href="/sign-up-tutor">Sign Up As Tutor</a></li>
        <li><a style={{verticalAlign:'middle',fontSize:'large'}} href="/sign-in">Log In</a></li>
      </ul>
      : <div style = {{color:'white',transform:'translate(-50%, 0)'}}><h1>{props.text}</h1></div>
      }
      {props.loggedIn? 
      <div className="user-info">
      <p>Jason Student</p>
      <button className="logout-button">Log Out</button>
      </div>:<></>}
    </nav>
  );
};

export default NavBar;
