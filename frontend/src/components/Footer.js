import { Container } from "@material-ui/core";
import React, { useState } from "react";
import {Link} from "@material-ui/core";

export default function Footer() {
  return (
    // <div classNameName="bg1"><hr />
    //   <p style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#FFFFFF' }}> Images retrieved from various websites @Copyright 2023</p>
    //   <p style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#FFFFFF' }}> <b>Contact Us</b>: </p>
    //   <br />
    //   <br />
    // </div>

    <div className="bg-gray" style = {{background:'gray'}}>
      <Container className="footer-container">
        <footer className="py-3 mt-4">
          <ul className="nav justify-content-center border-bottom pb-3 mb-3">
        
            <li className="nav-item me-auto footer-item">
      
              <Link href="mailto:contact@codeTutor.org" className="nav-link px-2 text-muted">
                <i className="material-icons inline-icon">mail</i>&nbsp;
                <span>contact@codeTutor.org</span>
              </Link>
            </li>
          </ul>
          <p className="text-center" style={{color:'white'}}>© 2024 Code Tutor</p>
        </footer>
      </Container>
    </div>
  )
}