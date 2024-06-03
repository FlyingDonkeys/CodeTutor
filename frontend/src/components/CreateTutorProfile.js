import React, { useState, useEffect } from 'react';
import { useHistory,matchPath} from 'react-router-dom';
import NavBar from './Navbar';
import { Button, FormControl, Select, MenuItem, Checkbox, ListItemText } from '@material-ui/core';

const CreateTutorProfilePage = (props) => {
    let history = useHistory();

    const [image, setImage] = useState(null);
    const [username, setuserName] = useState('');
    const [password, setpassword] = useState('');
    const [address, setAddress] = useState('');
    const [hourlyRate, setHourlyRate] = useState('');
    const [tutorDescription, setTutorDescription] = useState('');
    const [qualification, setQualification] = useState('');
    const [stuSubjects, setstuSubjects] = useState([]);
    const [subjects, setSubjects] = useState([]);
    const location = useHistory();

    useEffect(() => {
        const getSubjects = async() => {
            const response = await fetch("/api/subjects");
            if (!response.ok) {
                console.error("Failed to fetch subjects");
                return;
            }
            const data = await response.json();
            setSubjects(data);
        };
        getSubjects();
    }, []);

    const handleSubjectToggle = (subject) => {
        setstuSubjects((prevSubjects) => {
            if (prevSubjects.includes(subject)) {
                return prevSubjects.filter((s) => s.subject_name !== subject.subject_name);
            } else {
                return [...prevSubjects, subject];
            }
        });
    };

    const addNewTutor = async() => {
        if (!/^[a-zA-Z]+$/.test(username) || /\s/g.test(username)) {
            alert("Username should only contain alphabets and no spaces");
            return;
        }
        if (username.length < 8) {
            alert("Username should be at least 8 letters long!");
            return;
        }

        if (password.length < 8) {
            alert("Password should be at least 8 letters long!");
            return;
        }
        if (/\s/g.test(password)) {
            alert("Password cannot contain white space!");
            return;
        }

        if (!address) {
            alert("Location is required!");
            return;
        }

        if (stuSubjects.length === 0) {
            alert("At least one subject is required!");
            return;
        }

        if (!hourlyRate) {
            alert("Hourly rate is required!");
            return;
        }

        if (!tutorDescription) {
            alert("Tutor description is required!");
            return;
        }

        if (!qualification) {
            alert("Qualification is required!");
            return;
        }

        let formField = new FormData();
        formField.append('username', username);
        formField.append('password', password);
        formField.append('location', address);
        formField.append('hourly_rate', hourlyRate);
        formField.append('tutor_description', tutorDescription);
        //const qualification = qualification == null? "": qualification;
        formField.append('tutor_qualification', qualification);
    
        stuSubjects.forEach(subject => formField.append('subjects_taught', subject.subject_name));

        if (image !== null) {
            formField.append('image', image);
        }else formField.append('image', "");

        let cookieValue = null;
        console.log("HELLO HELLO COOKIES");
        console.log(cookieValue);
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, "csrftoken".length + 1) === ("csrftoken" + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring("csrftoken".length + 1));
                    console.log("csrftoken!")
                    console.log(cookieValue);
                    break;
                }
            }
        }
        console.log(cookieValue);
        const requestOptions = {
            method: "POST",
            headers: {'X-CSRFToken': cookieValue },
            body: formField,
        };

        if(!props.update){
            fetch("/api/create-tutor", requestOptions)
                .then((response) => response.json()).catch(e => {alert("Invalid Username"); return;})
                .then((data) => history.push("/profile-tutor/" + data.code));
        } else {
            
            
            const match = matchPath(location.location.pathname, {
                path: "/update-tutor/:param",
                exact: true,
                strict: false,
            });
        
            const code = match === null ? " " : match.params.param;
            fetch("/api/update-tutor?code="+code, requestOptions)
                .then((response) => response.json()).catch(e => {alert("Invalid Username"); return;})
                .then((data) => history.push("/profile-tutor/" + data.code));
        }
    };

    return (
        <>
            <NavBar isHome={false} text={"Create Tutor Account"} />
            <div className="container">
                <div className="w-75 mx-auto shadow p-5">
                    <div className="form-group">
                        <label>Profile Image (Optional)</label>
                        <input type="file" className="form-control" onChange={(e) => setImage(e.target.files[0])} />
                    </div>
                
                    <div className="form-group">
                        <label>Username</label>
                        <input
                            type="text"
                            className="form-control form-control-lg"
                            placeholder="Enter Your Username"
                            name="username"
                            value={username}
                            onChange={(e) => {
                                const value = e.target.value;
                                setuserName(value);
                            }}
                        />
                    </div>

                    <div className="form-group">
                        <label>Password</label>
                        <input
                            type="password"
                            className="form-control form-control-lg"
                            placeholder="Enter Your Password"
                            name="password"
                            value={password}
                            onChange={(e) => {
                                const value = e.target.value;
                                setpassword(value);
                            }}
                        />
                    </div>

                    <div className="form-group">
                        <label id="demo-simple-select-label">Location</label>
                        <select
                            id="demo-simple-select"
                            value={address}
                            onChange={(e) => setAddress(e.target.value)}
                            className="form-control form-control-lg"
                        >
                            <option value="N">North</option>
                            <option value="NE">North East</option>
                            <option value="E">East</option>
                            <option value="SE">South East</option>
                            <option value="S">South</option>
                            <option value="SW">South West</option>
                            <option value="W">West</option>
                            <option value="NW">North West</option>
                            <option value="C">Central</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label>Hourly Rate</label>
                        <input
                            type="number"
                            className="form-control form-control-lg"
                            placeholder="Enter Your Hourly Rate"
                            name="hourly_rate"
                            value={hourlyRate}
                            onChange={(e) => {
                                const value = e.target.value;
                                setHourlyRate(value);
                            }}
                        />
                    </div>

                    <div className="form-group">
                        <label>Tutor Description</label>
                        <textarea
                            className="form-control form-control-lg"
                            placeholder="Enter a Description"
                            name="tutor_description"
                            value={tutorDescription}
                            onChange={(e) => {
                                const value = e.target.value;
                                setTutorDescription(value);
                            }}
                        />
                    </div>

                    <div className="form-group">
                        <label>Qualification</label>
                        <select
                            className="form-control form-control-lg"
                            value={qualification}
                            onChange={(e) =>{ console.log(e.target.value);setQualification(e.target.value);}}
                        >
                            <option value="IB">IB</option>
                            <option value="diploma">Diploma</option>
                            <option value="undergraduate">Undergraduate</option>
                            <option value="Masters">Masters</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label id="subject-select-label">Subjects</label>
                        <FormControl className="form-control form-control-lg">
                            <Select
                                labelId="subject-select-label"
                                id="subject-select"
                                multiple
                                value={stuSubjects}
                                renderValue={(selected) => selected.map(subject => subject.subject_name).join(', ')}
                            >
                                {subjects.map((subject) => (
                                    <MenuItem key={subject.subject_name} value={subject}>
                                        <Checkbox
                                            checked={stuSubjects.some(s => s.subject_name === subject.subject_name)}
                                            onChange={() => handleSubjectToggle(subject)}
                                        />
                                        <ListItemText primary={subject.subject_name} />
                                    </MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </div>
                    <Button className="btn btn-primary btn-block" onClick={addNewTutor}>Submit</Button>
                </div>
            </div>
        </>
    );
};

export default CreateTutorProfilePage;
