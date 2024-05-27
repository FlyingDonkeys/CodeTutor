import React, { useState, useEffect } from 'react';
import { matchPath } from 'react-router'
import { useLocation } from 'react-router-dom';
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import { Button } from '@material-ui/core';
import { Link } from 'react-router-dom';
import { useHistory } from 'react-router-dom';


const Profile = (props) => {
    
    const location = useHistory();
    console.log("location");

    console.log(location);
    console.log(location.location.pathname);
    const [success, setSuccess] = useState(true);
    const match = matchPath(
        location.location.pathname,
        { path: "/profile/:param",
          exact: true,
          strict:false,
         }
      );
    
    console.log(match);
    const code = match === null? " ":match.params.param;
    const nav = useHistory();
   
   return (<h1>Username: {code} </h1>
    
    );
};

export default Profile;
