import React, { useState, useEffect } from 'react';
import { useHistory, matchPath } from 'react-router-dom';
import NavBar from './Navbar';
import { Button } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { Typography } from '@material-ui/core';



const useStyles = makeStyles((theme) => ({
    container: {
        maxWidth: '1200px',
        margin: '0 auto',
        padding: theme.spacing(2),
    },
    profileSection: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: theme.spacing(4),
        backgroundColor: '#f9f9f9',
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        marginBottom: theme.spacing(4),
    },
    profileImage: {
        width: '150px',
        height: '150px',
        borderRadius: '50%',
        objectFit: 'cover',
        marginBottom: theme.spacing(2),
    },
    profileName: {
        fontSize: '1.5rem',
        fontWeight: 'bold',
        marginBottom: theme.spacing(1),
    },
    profileButton: {
        marginTop: theme.spacing(2),
        backgroundColor: '#f5f5f5',
        '&:hover': {
            backgroundColor: '#e0e0e0',
        },
    },
    aboutSection: {
        padding: theme.spacing(4),
        backgroundColor: '#f9f9f9',
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    },
    aboutText: {
        fontSize: '1rem',
    },
    joinedDate: {
        display: 'flex',
        alignItems: 'center',
        marginTop: theme.spacing(2),
    },
    joinedDateIcon: {
        marginRight: theme.spacing(1),
    },
}));

const Profile = (props) => {
    const classes = useStyles();
    const [username, setusername] = useState("");
    const [isStudent, setisStudent] = useState(props.isStudent);
    const [joinedDate, setjoinedDate] = useState("");
    const [stuLocation, setstuLocation] = useState("");
    const [profileImage, setProfileImage] = useState("");
    const location = useHistory();
    const [success, setSuccess] = useState(true);


    const match = matchPath(location.location.pathname, {
        path: "/profile/:param",
        exact: true,
        strict: false,
    });

    const code = match === null ? " " : match.params.param;

    useEffect(() => {

        const getPersonDetails = async () => {
            try {
                const response = await fetch("/api/get-student?code=" + code);
                if (!response.ok) {
                    console.error("Error fetching details:", response.statusText);
                    setSuccess(false);
                }
                const data = await response.json();
                console.log(data);
                setusername(data.username);
                setisStudent(true);
                setjoinedDate(data.date_joined);
                setstuLocation(data.location);
                //console.log("../../.." + data.image);
                //const t = "../../.."+data.image
                setProfileImage(data.image); // Assuming profile_image is the key for the profile picture URL
            } catch (error) {
                console.error("Error fetching user details:", error);
                setSuccess(false);
            }
        };

        getPersonDetails();
    }, [code]);

    return (
        <>
            <NavBar isHome={false} text={"Profile Page"} isLoggedIn={true} />
            {success ? (
                <div className={classes.container}>
                    <div className={classes.profileSection}>
                        <img
                            src={"../../.." + profileImage || "../../static/images/Hero.png"} // Use a default image if profileImage is empty
                            alt="Profile"
                            className={classes.profileImage}
                        />
                        <Typography className={classes.profileName}>{username}</Typography>
                        <Button
                            variant="contained"
                            className={classes.profileButton}
                            href={`/update/${code}`}
                        >
                            Edit my Profile
                        </Button>
                    </div>
                    <div className={classes.aboutSection}>
                        <Typography className={classes.aboutText}>About me</Typography>
                        <div className={classes.joinedDate}>
                            <span className={classes.joinedDateIcon}>📅</span>
                            <Typography>Joined {new Date(joinedDate).toLocaleDateString()}</Typography>
                        </div>
                    </div>
                </div>
            ) : (
                <p>⚠︎ Dear Student, please log in before updating your profile ⚠︎</p>
            )}
        </>
    );
};

export default Profile;
