import React, { useState, useEffect } from 'react';
import { matchPath } from 'react-router';
import { useLocation } from 'react-router-dom';

const Room = () => {
    const [votesToSkip, setVotesToSkip] = useState(2);
    const [guestCanPause, setGuestCanPause] = useState(false);
    const [isHost, setIsHost] = useState(false);
    const location = useLocation();
    const [success, setSuccess] = useState(true);
    const match = matchPath(
        { path: "/room/:param" },
        location.pathname,
      );
    
      const roomCode = match === null? " ":match.params.param;

    useEffect(() => {
        const getRoomDetails = async () => {
            try {
                const response = await fetch("/api/get-room?code=" + roomCode);
                if(!response.ok){
                    console.error("Error fetching room details:", error);
                    setSuccess(false);
                }
                const data = await response.json();
                setVotesToSkip(data.votes_to_skip);
                setGuestCanPause(data.guest_can_pause);
                setIsHost(data.is_host);
            } catch (error) {
                console.error("Error fetching room details:", error);
                setSuccess(false);
            }
        };

        getRoomDetails();
    }, [roomCode]);
if(success){
    return (
        <div>
            <h3>Room: {roomCode}</h3>
            <p>Votes: {votesToSkip}</p>
            <p>Guest Can Pause: {guestCanPause}</p>
            <p>Host: {isHost}</p>
        </div>
    );
}
return (<h1>Room does not exist!</h1>)
};

export default Room;
