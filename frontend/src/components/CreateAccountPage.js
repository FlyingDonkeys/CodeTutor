import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import { Link } from "react-router-dom";
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";

const CreateAccountPage = () => {
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
                    alert("wrong username or password!");
                }else {
                    const data = response.json();
                    console.log(data);
                }
            })
            //.then((data) => navigate("/profile/" + data.code));
    };
    return (
        <Grid container spacing = {1}>
            <Grid item xs={12} align="center">
                <Typography component="h4" variant="h4">
                    Create An Account
                </Typography>
            </Grid>

        <Grid item xs={12} align="center">
            <FormControl>
                <TextField
                required
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
          Create A Room
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