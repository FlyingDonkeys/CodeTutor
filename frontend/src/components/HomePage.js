import React, {Component} from 'react';
import {render} from "react-dom";
import ReactDOM from 'react-dom';
import { StrictMode } from 'react';
import CreateAccountPage from './CreateAccountPage';
import Helper from './Helper';

import { 
    BrowserRouter as Router, 
    Routes,
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
        <>
            <Routes>
                <Route exact path = "/" element = {<Helper/>}></Route>
                <Route path = "/create" element = {<CreateAccountPage/>}/>
            </Routes>
    
        </>
        );
    }
}