import React from 'react';
import NavBar from './Navbar';
import { Calendar, momentLocalizer, Views, DateLocalizer } from 'react-big-calendar';
import moment from 'moment';
import {useCallback} from 'react'
import { useState, useEffect } from 'react';
import { useHistory, matchPath } from 'react-router-dom';

require('style-loader!css-loader!react-big-calendar/lib/css/react-big-calendar.css')
const localizer = momentLocalizer(moment);

const LandingPage = (props) => {
  //Do get-Student request=> redirect student/tutor to the request page with the code and then request page with that code
  //get request of the sessions student had with tutor on the website by storing that data inside the db and then importing here as events 
  const [username, setusername] = useState("");
  const [profileImage, setProfileImage] = useState("");
  const location = useHistory();
  const [success, setSuccess] = useState(true);
  let next = "";
  if (props.isStudent) {
    next = "/dashboard/:param";
  } else {
    next = "/dashboard-tutor/:param";
  }
  const match = matchPath(location.location.pathname, {
      path: next,
      exact: true,
      strict: false,
  });

  const code = match === null ? " " : match.params.param;

 

  useEffect(() => {
      const getPersonDetails = async () => {
          try {
              let path = "";
              if(props.isStudent){
                path = "/api/get-student?code=";
              }else {
                path = "/api/get-tutor?code=";
              }
              const response = await fetch(path + code);
              if (!response.ok) {
                  console.error("Error fetching user details:", response.statusText);
                  setSuccess(false);
                  alert(response.statusText);
                  return;
              }
              const data = await response.json();
              console.log(data);
              setusername(data.username);
              //setTutorScore(data.tutorScore);
              console.log(data.image);
              setProfileImage(data.image); // Assuming profile_image is the key for the profile picture URL
          } catch (error) {
              console.error("Error fetching user details:", error);
              setSuccess(false);
          }
      };

      getPersonDetails();
  }, [code]);

  const [myEvents, setEvents] = useState([]);
  console.log(myEvents);
  

  const handleSelectSlot = useCallback(
    ({ start, end }) => {
      const title = window.prompt('New Event name')
      if (title) {
        setEvents((prev) => [...prev, { start, end, title }])
      }
    },
    [setEvents]
  );

  const handleSelectEvent = useCallback(
    (event) => window.alert(event.title),
    []
  );


  return (
    <div className="landing-page">
      <NavBar isStudent = {props.isStudent} loggedIn={true} profileImage={profileImage} code = {code} username = {username}/>
      {success? 
      <div className="main-content">
        <div className="timetable">
          <h2>My Calendar</h2>
          <Calendar
            className="Timetable"
            localizer={localizer}
            style={{ height: '420px', background: 'white' }}
            events={myEvents}
            onSelectEvent={handleSelectEvent}
            onSelectSlot={handleSelectSlot}
            selectable
          />
        </div>
        <div className="buttons">
          <a href={"/request/"+code} class="button-card find-tutor-button">
            <i class="fas fa-chalkboard-teacher"></i>
            <span>Find 1 to 1 Tutoring Session</span>
          </a>

          <a href={"/"} class="button-card my-requests-button">
            <i class="fas fa-list"></i>
            <span>My Requests</span>
          </a>
        </div>
      </div>
      :<>⚠︎ Dear user, please log in to access the dashboard ⚠︎</>}
    </div> 
  );
};

export default LandingPage;

