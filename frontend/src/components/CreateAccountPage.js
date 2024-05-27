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

const CreateAccountPage = () => {
    const navigate = useHistory();
    const [userName, setuserName] = useState("");
    const [password, setpassword] = useState("");
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
          fetch("/api/create-student", requestOptions)
            .then((response) => {
                if(!response.ok){
                    alert("Username has been taken!");
                    return;
                }else {
                    const data = response.json();
                    console.log(data);
                    console.log(data.code);
                    data.then((s) => {navigate("/profile/" + s.code);});
                }
            })
            //.then((data) => navigate("/profile/" + data.code));
    };
    return (
        
        <Grid container spacing = {1} className="center">
            <Grid item xs={12} align="center">
                <Typography component="h4" variant="h4">
                    Create An Account
                </Typography>
            </Grid>

        <Grid item xs={12} align="center">
            <FormControl>
                <TextField
                required
                variant = "outlined"
                onChange={(e) => handleUserNameChanges(e)}
                defaultValue={""}
                inputProps={{
                style: { textAlign: "left" },
                }}
            />
            <FormHelperText>
                <div align="center">Enter an username</div>
            </FormHelperText>
            </FormControl>
      </Grid>

      <Grid item xs={12} align="center">
            <FormControl>
                <TextField
                required
                variant = "outlined"
                //type="string"
                onChange={(e) => handlePassWordChanges(e)}
                defaultValue={""}
                inputProps={{
                style: { textAlign: "left" },
                }}
            />
            <FormHelperText>
                <div align="center">Enter a password</div>
            </FormHelperText>
            </FormControl>
      </Grid>
      <Grid item xs={12} align="center">
        <Button
          color="primary"
          variant="contained"
          onClick={handleAccountButtonPressed}
        >
          Create An Account
        </Button>
      </Grid>
      <Grid item xs={12} align="center">
        <Button color="secondary" variant="contained" to="/" component={Link}>
          Back
        </Button>
      </Grid>
    </Grid>
    );
};

export default CreateAccountPage;