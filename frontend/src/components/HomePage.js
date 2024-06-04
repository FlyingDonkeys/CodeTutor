import React, { Component } from 'react';
import { render } from "react-dom";
import ReactDOM from 'react-dom';
import { StrictMode } from 'react';
import SignInPage from './SignInPage';
import Helper from './Helper';
import Profile from './Profile';
import CreateProfilePage from './CreateAccountPage';
import CreateTutorProfilePage from './CreateTutorProfile';
import ProfileTutor from './ProfileTutor';
import LandingPage from './LandingPage';
import SearchFilterPage from './SearchPage';

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

    render() {
        return (
            <div className="content">
                <Switch>
                    <Route exact path="/" component={Helper}></Route>
                    <Route
                        path="/sign-in"
                        render={(props) => <SignInPage {...props} isStudent={true} />}
                    />
                    <Route
                        path="/profile/:code"
                        render={(props) => <Profile {...props} isStudent={true} />}
                    />
                    <Route
                        path="/sign-up"
                        render={(props) => <CreateProfilePage {...props} update={false} />}
                    />
                    <Route
                        path="/update"
                        render={(props) => <CreateProfilePage {...props} update={true} />}
                    />
                    <Route
                        path="/sign-in-tutor"
                        render={(props) => <SignInPage {...props} isStudent={false} />}
                    />
                    <Route
                        path="/profile-tutor/:code"
                        render={(props) => <ProfileTutor {...props} isStudent={false} />}
                    />
                    <Route
                        path="/sign-up-tutor"
                        render={(props) => <CreateTutorProfilePage {...props} update={false} />}
                    />
                    <Route
                        path="/update-tutor"
                        render={(props) => <CreateTutorProfilePage {...props} update={true} />}
                    />

                    <Route
                        path="/dashboard"
                        render={(props) => <LandingPage {...props} isStudent = {true} />}
                    />

                    <Route
                        path="/dashboard-tutor"
                        render={(props) => <LandingPage {...props} isStudent = {false} />}
                    />

                    <Route
                        path="/request/:code"
                        render={(props) => <SearchFilterPage {...props} isStudent={true} />}
                    />
                    
                    <Route
                        path="/request-tutor/:code"
                        render={(props) => <SearchFilterPage {...props} isStudent={flase} />}
                    />
                </Switch>
            </div>
        );
    }
}
