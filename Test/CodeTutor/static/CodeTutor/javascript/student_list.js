console.log("student list page is loaded!")

// Note that the infinite scroll feature should be different according to whether user is loading
// all profiles or only specific profiles
let loading_all_profiles = true
let subject_to_be_loaded = ""


window.onscroll = () => {
    // If user scrolls to the end, load more profiles
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        if (loading_all_profiles) {
            load();
        } else {
            load_specific_profiles(subject_to_be_loaded)
        }
    }
}

// Start with first profile
let counter = 0;

// Load 10 profiles at a time
const quantity = 10;

// When DOM loads, render the first 10 profiles
document.addEventListener('DOMContentLoaded', function () {

    load()
    // Other eventlisteners such as change of profile display upon hover etc
    load_subjects()

    // Attach logic to process clicking of filter form submit button
    document.querySelector("#submit").onclick = () => load_profiles_by_rate(document.querySelector("#lowest_rate").value,
                                                                                     document.querySelector("#highest_rate").value)


    // Have some logic to give errors if user types in invalid input
    const alertPlaceholder = document.getElementById('liveAlertPlaceholder')
});

// Load next set of posts
function load() {
    // Check if load is being called
    console.log("Loading new profiles")

    // Ensure that we are loading all profiles
    loading_all_profiles = true

    // Set start and end profile numbers
    const start = counter;
    const end = start + quantity - 1;

    // Get new posts and add posts
    fetch(`/load_student_profiles?start=${start}&end=${end}`)
        .then(response => response.json()) // We have a Json object here of 10 students
        .then(students => {
            console.log("adding students")
            console.log(students); // Verify that the students json objects have been passed in
            students.forEach(student => {
                if (student.is_finding_tutor) { // Only display students actively finding tutors
                    add_student(student)
                }
            });
            // Update counter to load the next 10 posts
            counter+=quantity;
        })
        .finally(() => {
            console.log("All students loaded");
            document.querySelector("#student_list").style.display = "block"
        });
}

//determine whether to display the map or not     
let count = 0;
function map_button(code){
    //alert("please scroll to the top");
    if(count%2 == 0){
    window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    generate_map(code);
}
function generate_map(code){
    //may have included GoogleMaps API multiple times 
    $.getScript( "https://maps.googleapis.com/maps/api/js?key=" + 'AIzaSyC128zZlCt6WN8ygaNo0DtpDi0DL8s0SIM'+ "&libraries=places") 
    .done(function() {
        count+=1;
        //convert postal code to actual address that gets fed into google maps
        var geocoder = new google.maps.Geocoder();
        
        geocoder.geocode({
            'address': code.toString(),
            componentRestrictions: {
                country: 'SG'
            }
            }
        ,  
        function(results, status) {
       
        if (status == google.maps.GeocoderStatus.OK) {
            lat = results[0].geometry.location.lat();
            lng = results[0].geometry.location.lng();
            //options to feed into the map 
            var options = {
                zoom: 15,
                center: new google.maps.LatLng(lat, lng),
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            //Create the new map at div on html
            map = new google.maps.Map(document.getElementById("map"), options);
            //logic to determine whether to show map or not
            
            if(count%2 == 1){
                document.getElementById("map").style.display = "block";
                document.getElementById("map").style.height = "250px";
                console.log("scroll to top");

            }else{
                document.getElementById("map").style.display = "None";
                document.getElementById("map").style.height = "0px";
            }
            //Make the marker
            new google.maps.Marker({
                position:new google.maps.LatLng(lat,lng),
                map:map
            });
            
        }else {
            alert("Geocode was not successful for the following reason: " + status);
        }
    });
    });
    }


// Used to implement filter function

function load_specific_profiles(subject, min, max) {

    // User may choose to load all profiles again
    if (subject === "All") {
        load()
        return null
    }

    // Check if load is being called
    console.log(`Loading student profiles who require ${subject}`)

    // Note that the start should be reset
    const start = counter;
    const end = start + quantity - 1;
    // Get new posts and add posts
    fetch(`/load_student_profiles?start=${start}&end=${end}`)
        .then(response => response.json()) // We have a Json object here of 10 students
        .then(students => {
            console.log(students)
            return students.filter(student => student.subjects_required.includes(subject));
        })
        .then(students => {
            console.log("middle")
            console.log(students); // Verify that the students json objects have been passed in
            students.forEach(student => {
                // For filter feature, we have to take profiles requiring specific subjects
                if (student.is_finding_tutor) {
                    add_student(student)
                }
            });
            // Update counter to load the next 10 posts
            counter+=quantity;
        })
        .finally(() => {
            console.log(`Students requiring ${subject} loaded`)
            document.querySelector("#student_list").style.display = "block"
        });
}


function add_student(student) {
    //Create new student profile object for viewing
    //only if student is finding tutor
    if(student.is_finding_tutor){
        const profile = document.createElement('div');

    // Note that each student may have multiple subjects required
    let subjects_required = "";
    student.subjects_required.forEach(subject => {
        subjects_required += subject + ", ";
    });

    // Get the profile pictures urls of the users
    let url = student.profile_picture_url === null ? 'https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg'
                                                            : student.profile_picture_url;

    profile.className = 'post';
    profile.innerHTML = `<div class="container" id="Student ${student.id}">
                            <div class="row">
                                <div class="col-3">
                                    <!-- Profile picture functionality in Django to be implemented -->
                                    <div class="imgcover mb-4">
                                    <img src="${url}" style="width:250px; height:250px; object-fit: cover;"alt="No Image" class="rounded-pill bg-white p-2 shadow">
                                </div>
                                </div>
                                <div class="col-9">

                                    <div class="row mb-1">
                                    <div class="col-md-3 py-1">
                                        <h5 class="fw-bold">Name:</h5>
                                    </div>
                                        <div class="col-md-3 py-1">
                                            ${student.username}
                                        </div>
                                    </div>  
                                    <div class="row mb-1">
                                    <div class="col-md-3 py-1">
                                    <h5 class="fw-bold">Location:</h5>
                                </div>
                                    <div class="col-md-3 py-1">
                                        ${student.location}
                                    </div>
                                    </div>
                                    <div class="row mb-1">
                                    <div class="col-md-3 py-1">
                                    <h5 class="fw-bold">Subjects:</h5>
                                </div>
                                    <div class="col-md-3 py-1">
                                        ${subjects_required}
                                    </div>
                                    </div>
                                    <div class="row mb-1">
                                    <div class="col-md-3 py-1">
                                    <h5 class="fw-bold">Offered Rate:</h5>
                                </div>
                                    <div class="col-md-3 py-1">
                                        $${student.offered_rate}
                                    </div>
                                    </div>
                                    <div class="row mb-1">
                          
                                        <div class="col-2">
                                            <!-- Logic to apply for tuition job not done -->
                                            <a href="apply/${student.username}" role="button">
                                            <button class="btn btn-outline-primary fw-bolder fs-7 px-4 py-2 mt-3 rounded-pill">Apply as Tutor</button>
                                            </a>
                                        </div>

                                    <div class="col-2">
                                        <!-- Logic to show google map -->
                                        <button class="btn btn-outline-primary fw-bolder fs-7 px-4 py-2 mt-3 rounded-pill" onclick="map_button(${student.postal_code})">Show Location</button>
                                    </div>
                                    </div>
                                </div>
                            </div>
                      </div>
                      <hr>`

    // Add post to DOM
    document.querySelector('#the_actual_list').append(profile);
 }
}


function load_subjects() {
    // Check if load_subjects is being called
    console.log("Loading subjects in dropdown bar")

    // Get new posts and add posts
    fetch(`/load_subjects`)
        .then(response => response.json())
        .then(subjects => {
            // Verify if list of subjects has been passed in correctly
            console.log(subjects)
            subjects.forEach(
                subject => add_subject(subject.subject_name)
            )
        })
        .finally(() =>{
            add_subject("All")
            console.log("Subjects added")
        })
}


function add_subject(subject){
    console.log(`Adding ${subject}`)
    // Create the option with the subject as the name
    const the_subject = document.createElement('li')

    // When the list element is clicked, we want to dynamically load revelant student profiles
    the_subject.onclick = () => {
        loading_all_profiles = false // Ensure we are loading specific profiles
        subject_to_be_loaded = subject // Give context to global variable to indicate subject to be loaded
        counter = 0 // Reset counter
        document.querySelector("#the_actual_list").innerHTML = `` // Remove previously loaded profiles
        document.querySelector("#button_text").innerHTML = subject // Aesthetic stuff
        load_specific_profiles(subject, -1, -1)
    }
    the_subject.innerHTML = `<a class="dropdown-item" href="#">${subject}</a>`

    // Add option to dropdown
    document.querySelector('#subject_list').append(the_subject)
}


function load_profiles_by_rate(min, max) {
    console.log(`Filtering by rates, minimum = ${min}, maximum = ${max}`)

    // Javascript logic to show warning upon invalid input
    const appendAlert = (message, type) => {
        const wrapper = document.createElement('div')
        wrapper.innerHTML = [
            `<div class="alert alert-${type} alert-dismissible" role="alert">`,
            `   <div>${message}</div>`,
            '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
            '</div>'
        ].join('')

        alertPlaceholder.append(wrapper)
    }

    const alertTrigger = document.getElementById('liveAlertBtn')
    if (alertTrigger) {
        alertTrigger.addEventListener('click', () => {
        appendAlert('Nice, you triggered this alert message!', 'danger')
        })
    }

    // Convert min and max to numbers
    min = parseFloat(min);
    max = parseFloat(max);

    // Handle invalid operations
    if (isNaN(min) || isNaN(max)) {
        appendAlert('Please fill in both minimum and maximum value fields!', 'danger')
    } else if (min > max) {
        appendAlert('Minimum rate must not be higher than maximum!', 'danger');
    } else if (min <= 0 || max <= 0) {
        appendAlert("Entered rates must both be positive values!", 'danger')
    } else if (min > 1000 || max > 1000) {
        appendAlert("Your entered rates are too high!", 'danger')
    } else {
            // Check if load is being called
            console.log(`Loading student profiles whose offered rates are between ${min} and ${max}`)

            // Ensure that we are loading specific profiles only
            loading_all_profiles = false
            counter = 0 // Reset counter
            document.querySelector("#the_actual_list").innerHTML = `` // Remove previously loaded profiles

            // Note that the start should be reset
            const start = counter;
            const end = start + quantity - 1;
            // Get new posts and add posts
            fetch(`/load_student_profiles?start=${start}&end=${end}`)
                .then(response => response.json()) // We have a Json object here of 10 students
                .then(students => {
                    console.log(students);
                    return students.filter(student => student.offered_rate >= min && student.offered_rate <= max);
                })
                .then(students => {
                    console.log("middle")
                    console.log(students); // Verify that the students json objects have been passed in
                    students.forEach(student => {
                        // For filter feature, we have to take profiles requiring specific subjects
                        if (student.is_finding_tutor) {
                            add_student(student)
                        }
                    });
                    // Update counter to load the next 10 posts
                    counter+=quantity;
                })
                .finally(() => {
                    console.log(`Students offering rates between ${min} and ${max} loaded`)
                    document.querySelector("#student_list").style.display = "block"
                });
    }
}

