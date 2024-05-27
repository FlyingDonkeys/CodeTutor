import React, {Component} from 'react';
import {render} from "react-dom";
import ReactDOM from 'react-dom';
import { StrictMode } from 'react';
import CreateAccountPage from './CreateAccountPage';
import Helper from './Helper';
import Profile from './Profile';
import NavBar from './Navbar';

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
                <Route path = "/create" component = {CreateAccountPage}/>
                <Route path = "/profile/:code" component = {Profile}/>
            </Switch>
    
        </div>
        );
    }
}