import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import { Link } from "@material-ui/core";
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import {InputAdornment} from "@material-ui/core";
import {IconButton} from "@material-ui/core";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import Person from "@mui/icons-material/Person";

import NavBar from "./Navbar";
const SignInPage = () => {
    const navigate = useHistory();
    const [userName, setuserName] = useState("");
    const [password, setpassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
const handleClickShowPassword = () => setShowPassword(!showPassword);
const handleMouseDownPassword = () => setShowPassword(!showPassword);
    const handleUserNameChanges = (e) => {
        setuserName(e.target.value);
        console.log("username:" + e.target.value);
    };
    const handlePassWordChanges = (e) => {
        setpassword(e.target.value);
        console.log("password:"+ e.target.value);
    };

    const handleAccountButtonPressed = () =>{
        if(!(/^[a-zA-Z]+$/.test(userName))|| (/\s/g.test(userName))) {
            alert("Username should only contain alphabets");
            return;
        }

        if(userName.length <8){
            alert("Username should be at least 8 letters long!");
            return;
        }
        if(password.length < 8){
            alert("password should be at least 8 letters long!");
            return;
        }

        if( (/\s/g.test(password))) {
            alert("password cannot contain white space!");
            return;
        }
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username: userName,
                password: password,
            }),
          };
          fetch("/api/get-student-username?username="+userName)

            .then((response) => {
                if(!response.ok) {

                    alert("Username is invalid!");

                    return;

                }else {

                    const data = response.json();

                    console.log(data);
                    
                    data.then((s) => {
                        console.log(s);
                        console.log(s.username); 
                        console.log(s.code); 
                        if(password == s.password){
                        
                        navigate.push("/profile/" + s.code);
                        return;
                        }
                        alert("Incorrect password!");
                    });
                }
            })
            //.then((data) => navigate("/profile/" + data.code));
    };
    return (
      <>
        <NavBar isHome = {false} text = {"Log In"}/>
        <Grid container spacing = {2} className="center">
        <Grid item xs = {6} style = {{minHeight:'100vh'}}>
            <div className="deco" style={{textAlign:'center'}}>
                <h4> Did you know that our system is designed according to pedagogy research? </h4>
            </div>
           
        </Grid>
        <Grid item xs={6}>
        <Grid item xs={12} align="left" style = {{paddingTop:'20px'}}>
            <FormControl>
                <TextField
                required
                variant = "outlined"
                onChange={(e) => handleUserNameChanges(e)}
                defaultValue={""}
                type = "text"
                InputProps={{ // <-- This is where the toggle button is added.
                    endAdornment: (
                    <InputAdornment position="end">
                    <IconButton
                    aria-label="person"
                    >
                    <Person/>
                    </IconButton>
                    </InputAdornment>
                    )
      }}
            />
            <FormHelperText >
                <div align="center">Enter an username</div>
            </FormHelperText>
            </FormControl>
      </Grid>

      <Grid item xs={12} align="left" style = {{paddingTop:'10px'}}>
            <FormControl>
                <TextField
                required
                variant = "outlined"
                //type="string"
                type={showPassword ? "text" : "password"} // <-- This is where the magic happens
                onChange={(e) => handlePassWordChanges(e)}
                InputProps={{ // <-- This is where the toggle button is added.
                endAdornment: (
                <InputAdornment position="end">
                <IconButton
                aria-label="toggle password visibility"
                onClick={handleClickShowPassword}
                onMouseDown={handleMouseDownPassword}
                >
                {showPassword ? <Visibility /> : <VisibilityOff />}
                </IconButton>
                </InputAdornment>
                )
  }}
                
                defaultValue={""}
            />
            <FormHelperText>
                <div align="center">Enter a password</div>
            </FormHelperText>
            </FormControl>
      </Grid>
      <Grid item xs={12} align="left" style = {{paddingTop:'5px'}}>
        <Button
          color="primary"
          variant="contained"
          onClick={handleAccountButtonPressed}
        >
          Sign In 
        </Button>
      </Grid>
      <Grid item xs={12} align="left" style = {{paddingTop:'5px'}}>
        <Button color="secondary" variant="contained" onClick={() => {navigate.push("/sign-in-tutor");}}>
          Log in as tutor
        </Button>
      </Grid>
    </Grid>
    </Grid>
    </>
    );
};

export default SignInPage;