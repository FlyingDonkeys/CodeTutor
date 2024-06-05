import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { StrictMode } from 'react';
import HomePage from './HomePage';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Redirect
} from 'react-router-dom';

export default class App extends Component {
  constructor(props) {
    super(props);
    console.log(100); // This should log to the console
  }

  render() {

    return (
      <Router>
        <HomePage />
      </Router>
    )
  }
}

ReactDOM.render(
  <StrictMode>
    <App />
  </StrictMode>,
  document.getElementById('app')
)
