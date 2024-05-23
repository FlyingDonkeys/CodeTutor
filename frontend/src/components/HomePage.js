import React, {Component} from 'react';
import {render} from "react-dom";
import ReactDOM from 'react-dom';
import { StrictMode } from 'react';
import Room from './Room';

import CreateRoomPage from './CreateRoomPage';
import { 
    BrowserRouter as Router, 
    Routes,
    Route,
    Link, 
    Redirect 
} from 'react-router-dom';
import RoomJoinPage from './RoomJoinPage';

export default class HomePage extends Component {
    constructor(props) {
        super(props);
    }
//path should have exact so anything that matches / will result in at least that rendering
    render() {
        return (
        <>
            <Routes>
                <Route exact path = "/"></Route>
                <Route path = "/join" element = {<RoomJoinPage/>}/>
                <Route path = "/create" element = {<CreateRoomPage/>}/>
                <Route path = "/room/:roomCode" element = {<Room/>}/>
            </Routes>

    
        </>
        );
    }
}

