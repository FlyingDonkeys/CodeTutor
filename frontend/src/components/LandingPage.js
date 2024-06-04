import React from 'react';
import NavBar from './Navbar';
import { Calendar, momentLocalizer, Views, DateLocalizer } from 'react-big-calendar';
import moment from 'moment';
import { Fragment, useState, useCallback, useMemo } from 'react'
import PropTypes from 'prop-types'

require('style-loader!css-loader!react-big-calendar/lib/css/react-big-calendar.css')
const localizer = momentLocalizer(moment);

const LandingPage = (props) => {
  const [myEvents, setEvents] = useState([])

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
      <NavBar loggedIn = {true}/>

      <div className="main-content">
        <div className="timetable">
          <h2>My Calendar</h2>
          <Calendar
            className="Timetable"
            localizer={localizer}
            style={{ height: '420px',background:'white' }}
            events={myEvents}
            onSelectEvent={handleSelectEvent}
            onSelectSlot={handleSelectSlot}
            selectable
          />
        </div>
        <div className="buttons">
          <button className="find-tutor-button">Find 1 to 1 Tutoring Session</button>
          <button className="my-requests-button">My Requests</button>
        </div>
      </div>
    </div>
  );
};
x
export default LandingPage;

