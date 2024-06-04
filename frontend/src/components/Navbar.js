import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Button } from '@material-ui/core';
import {Typography} from '@material-ui/core';
//import '../../static/css/navbar.css'; // You can add custom styling in this CSS file
//import { Container } from '@material-ui/core';
const useStyles = makeStyles((theme) => ({
  
  profileSection: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    paddingRight: theme.spacing(2),
  },
  profileImage: {
    width: 40,
    height: 40,
    borderRadius: '50%',
    marginRight: theme.spacing(1),
    objectFit: 'cover',
  },
  profileName: {
    marginRight: theme.spacing(1),
    fontWeight: 'bold',
    color:'white',
  },
}));

const NavBar = (props) => {
  const classes = useStyles();
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
      
        <div className={classes.profileSection}>
        <ul className="nav-links" >
        <li><a href="/dashboard">DashBoard</a></li>
        <li><a href="/sign-out">Sign Out</a></li>
        </ul>
        <a href = {"/profile" + props.code}>
          <img
            src={"../../.."+props.profileImage|| "../../static/images/Hero.png"} // Use a default image if profileImage is empty
                alt="Profile"
                className={classes.profileImage}
                ></img></a>
                <Typography className={classes.profileName}>{props.username || "Jason" }</Typography>

            </div>
            :<></>}
    </nav>
  );
};

export default NavBar;
