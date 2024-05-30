import React, {Component} from 'react';
import {render} from "react-dom";
import ReactDOM from 'react-dom';
import { StrictMode } from 'react';
import SignInPage from './SignInPage';
import Helper from './Helper';
import Profile from './Profile';
import CreateProfilePage from './CreateAccountPage';
import CreateTutorProfilePage from './CreateTutorProfile';
import ProfileTutor from './ProfileTutor';

import { 
    BrowserRouter as Router, 
    Switch,
    Route,
    Link, 
    Redirect 
} from 'react-router-dom';


export default class HomePage extends Component {
    constructor(props) {
        super(props);
    }
//path should have exact so anything that matches / will result in at least that rendering
    render() {
        return (
        <div className="content">
            <Switch>
                <Route exact path = "/" component = {Helper}></Route>
                <Route path = "/sign-in" component = {SignInPage}/>
                <Route path = "/profile/:code" isStudent = {true} component = {Profile}/>
                <Route path = "/sign-up" update = {false} component = {CreateProfilePage}/>
                <Route path = "/update" update = {true} component = {CreateProfilePage}/>
                
                <Route path = "/sign-in-tutor" isStudent = {false} component = {SignInPage}/>
                <Route path = "/profile-tutor/:code" isStudent = {false} component = {ProfileTutor}/>
                <Route path = "/sign-up-tutor" update = {false} component = {CreateTutorProfilePage}/>
                <Route path = "/update-tutor" update = {true} component = {CreateTutorProfilePage}/>
            </Switch>
    
        </div>
        );
    }
}