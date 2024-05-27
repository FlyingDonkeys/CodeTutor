import React from 'react';
import NavBar from './Navbar'; // Import the NavBar component
//import '../../static/css/homepage.css'; // You can add custom styling in this CSS file
import { Link } from 'react-router-dom/cjs/react-router-dom';
import InfoCard from './Card';
import { Grid } from '@material-ui/core';
import Footer from './Footer';

const Helper = () => {
  return (
    <>
    <div className="parallax">
    <NavBar/>
       <div style={{display: 'flex', justifyContent: 'center' }}>
        <h1 style = {{alignSelf: 'center', color:'white',display:'flex'}}>
            Finding a tutor? Find Code-Tutor!
        </h1>
       </div>
    </div>


      <div style = {{display:'flex', justifyContent:'center',paddingTop:'5%'}}>
      <h1>
        What is Code Tutor? 
      </h1>
      </div>

      <div style = {{display:'flex', justifyContent:'center', marginLeft:'10%', marginRight:'10%'}}>
      <p>
      A dynamic tuition agency website that not only facilitates the discovery and connection between tutors and students but also incorporates a data-driven model to categorize tutors based on the actual academic performance of their students
      </p>
      </div>

      <div style={{display: 'flex', justifyContent: 'center'}}>
      <div style={{ backgroundColor: "#fffefa" }}>
        <Grid container spacing = {1}>
            <Grid item xs = {4}>
              <InfoCard header = {"placeHolder"} description={"Description"} />
            </Grid>
            <Grid item xs = {4}>
              <InfoCard header = {"placeHolder"} description={"Description"}/>
            </Grid>
            <Grid item xs = {4}>
              <InfoCard header = {"placeHolder"} description={"Description"}/>
            </Grid>
        </Grid>
      </div>
      </div>

      <div id = "how-it-works" style = {{display:'flex', justifyContent:'center',paddingTop:'5%'}}>
      <h1>
        How it works 
      </h1>
      </div>

      <div style = {{display:'flex', justifyContent:'center', marginLeft:'10%', marginRight:'10%'}}>
      <p>
        Simply sign up and start searching for the most suitable tutor on the website!
      </p>
      </div>

      <div style={{display: 'flex', justifyContent: 'center'}}>
      <div style={{ backgroundColor: "#fffefa" }}>
        <Grid container spacing = {1}>
            <Grid item xs = {4}>
              <InfoCard header = {"placeHolder"} description={"Description"} />
            </Grid>
            <Grid item xs = {4}>
              <InfoCard header = {"placeHolder"} description={"Description"}/>
            </Grid>
            <Grid item xs = {4}>
              <InfoCard header = {"placeHolder"} description={"Description"}/>
            </Grid>
        </Grid>
      </div>
      </div>

      <div id = "become-tutor" style = {{display:'flex', justifyContent:'center',paddingTop:'5%'}}>
      <h1>
       Become a tutor
      </h1>
      </div>

      <div style = {{display:'flex', justifyContent:'center', marginLeft:'10%', marginRight:'10%'}}>
      <p>
       Start teaching by signing up as a part time tutor! 
      </p>
      </div>

      <div style={{display: 'flex', justifyContent: 'center'}}>
      <div style={{ backgroundColor: "#fffefa" }}>
        <Grid container spacing = {1}>
            <Grid item xs = {4}>
              <InfoCard header = {"placeHolder"} description={"Description"} />
            </Grid>
            <Grid item xs = {4}>
              <InfoCard header = {"placeHolder"} description={"Description"}/>
            </Grid>
            <Grid item xs = {4}>
              <InfoCard header = {"placeHolder"} description={"Description"}/>
            </Grid>
        </Grid>
      </div>
      </div>

      <div id = "find-tutor" style = {{display:'flex', justifyContent:'center',paddingTop:'5%'}}>
      <h1>
       Find a tutor
      </h1>
      </div>

      <div style = {{display:'flex', justifyContent:'center', marginLeft:'10%', marginRight:'10%'}}>
      <p>
       Need an experienced tutor for a specific subject? 
      </p>
      </div>

      <div style={{display: 'flex', justifyContent: 'center'}}>
      <div style={{ backgroundColor: "#fffefa" }}>
        <Grid container spacing = {1}>
            <Grid item xs = {4}>
              <InfoCard header = {"placeHolder"} description={"Description"} />
            </Grid>
            <Grid item xs = {4}>
              <InfoCard header = {"placeHolder"} description={"Description"}/>
            </Grid>
            <Grid item xs = {4}>
              <InfoCard header = {"placeHolder"} description={"Description"}/>
            </Grid>
        </Grid>
      </div>
      </div>
      <Footer/>
    </>
  );
};

export default Helper;
