console.log("tutor list page is loaded!")

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
    document.querySelector("#submit").onclick = () => load_profiles_by_score(document.querySelector("#lowest_rate").value,
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
    fetch(`/load_tutor_profiles?start=${start}&end=${end}`)
        .then(response => response.json()) // We have a Json object here of 10 tutors
        .then(tutors => {
            console.log("list of tutors below")
            console.log(tutors); // Verify that the tutors json objects have been passed in
            tutors.forEach(tutor => {
                add_tutor(tutor);
            });
            // Update counter to load the next 10 posts
            counter+=quantity;
        })
        .finally(() => {
            console.log("All tutors loaded");
            document.querySelector("#tutor_list").style.display = "block"
        });
}


// Used to implement filter function

function load_specific_profiles(subject) {

    // User may choose to load all profiles again
    if (subject === "All") {
        load()
        return null
    }

    // Check if load is being called
    console.log(`Loading tutor profiles who require ${subject}`)

    // Note that the start should be reset
    const start = counter;
    const end = start + quantity - 1;
    // Get new posts and add posts
    fetch(`/load_tutor_profiles?start=${start}&end=${end}`)
        .then(response => response.json()) // We have a Json object here of 10 tutors
        .then(tutors => {
            console.log(tutors)
            return tutors.filter(tutor => tutor.subjects_taught.includes(subject));
        })
        .then(tutors => {
            console.log("middle")
            console.log(tutors); // Verify that the tutors json objects have been passed in
            tutors.forEach(tutor => {
                // For filter feature, we have to take profiles teaching specific subjects
                add_tutor(tutor)
            });
            // Update counter to load the next 10 posts
            counter+=quantity;
        })
        .finally(() => {
            console.log(`Tutors teaching ${subject} loaded`)
            document.querySelector("#tutor_list").style.display = "block"
        });
}


function add_tutor(tutor) {
    // Create new tutor profile object for viewing by student
    const profile = document.createElement('div');

    // Note that each tutor may have multiple subjects taught
    let subjects_taught = "";
    tutor.subjects_taught.forEach(subject => {
        subjects_taught += subject + ", ";
    });

    // Get the profile pictures urls of the users
    let url = tutor.profile_picture_url === null ? 'https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg'
                                                            : tutor.profile_picture_url;

    // Want to make the profiles stand out depending on tutorscore, similar to chunithm rating system
    let tutorscorehtml = ``;
    if (tutor.tutor_score >= 9) {
        tutorscorehtml = `<div class="col-3 rainbow rainbow_text_animated">
                            ${tutor.tutor_score}
                          </div>`;
    } else if (tutor.tutor_score < 9 && tutor.tutor_score >= 8.5) {
        tutorscorehtml = `<div class="col-3" style="color: goldenrod; font-size: 25px">
                            ${tutor.tutor_score}
                          </div>`;
    } else if (tutor.tutor_score < 8.5 && tutor.tutor_score >= 8) {
        tutorscorehtml = `<div class="col-3" style="color: gold; font-size: 25px">
                            ${tutor.tutor_score}
                          </div>`;
    } else if (tutor.tutor_score < 8 && tutor.tutor_score >= 7) {
        tutorscorehtml = `<div class="col-3" style="color: silver; font-size: 25px">
                            ${tutor.tutor_score}
                          </div>`;
    } else if (tutor.tutor_score < 7 && tutor.tutor_score >= 6) {
        tutorscorehtml = `<div class="col-3" style="color: saddlebrown; font-size: 25px">
                            ${tutor.tutor_score}
                          </div>`;
    } else {
        tutorscorehtml = `<div class="col-3" style="color: red; font-size: 25px">
                            ${tutor.tutor_score}
                          </div>`;
    }


    profile.className = 'post';
    profile.innerHTML = `<div class="container" id="Student ${tutor.id}">
                            <div class="row">
                                <div class="col-3">
                                    <!-- Profile picture functionality in Django to be implemented -->
                                    <img style='height: 100%; width: 100%; object-fit: contain;' src="${url}" alt="No Image">
                                </div>
                                <div class="col-9">
                                    <div class="row mb-1">
                                        <div class="col-3">
                                            <h4>Username: <h4>
                                        </div>
                                        <div class="col-3">
                                            ${tutor.username}
                                        </div>
                                    </div>
                                    <div class="row mb-1">
                                        <div class="col-3">
                                            <h4>Subjects Taught: <h4>
                                        </div>
                                        <div class="col-3">
                                            ${subjects_taught}
                                        </div>
                                    </div>
                                    <div class="row mb-1">
                                        <div class="col-3">
                                            <h4>Tutor Description: <h4>
                                        </div>
                                        <div class="col-3">
                                            ${tutor.tutor_description}
                                        </div>
                                    </div>
                                    <div class="row mb-1">
                                        <div class="col-3">
                                            <h4>TutorScore: </h4>
                                        </div>
                                        ${tutorscorehtml}
                                    </div>
                                    <div class="row mb-1">
                                        <div class="col-3">
                                            <h4>Students Taught: <h4>
                                        </div>
                                        <div class="col-3">
                                            ${tutor.students_taught}
                                        </div>
                                    </div>
                                    <div class="row mb-1">
                                        <div class="col-3">
                                            <h4>Hourly Rate: <h4>
                                        </div>
                                        <div class="col-3">
                                            $${tutor.hourly_rate}/hr
                                        </div>
                                    </div>
                                    <div class="row mb-1">
                                        <div class="col-4"><!-- To centralise --></div>
                                        <div class="col-2">
                                            <!-- Logic for student to apply for this tutor not done -->
                                            <!-- May mimic the form tutors use to apply for a student -->
                                            <!-- Note that the url provided here doesnt actually exist -->
                                            <!-- Maybe you could help with it -->
                                            <a class="btn btn-primary" href="hire_tutor/${tutor.username}" role="button">Hire this Tutor</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                      </div>
                      <hr>`

    // Add post to DOM
    document.querySelector('#the_actual_list').append(profile);
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

    // When the list element is clicked, we want to dynamically load relevant tutor profiles
    the_subject.onclick = () => {
        loading_all_profiles = false // Ensure we are loading specific profiles
        subject_to_be_loaded = subject // Give context to global variable to indicate subject to be loaded
        counter = 0 // Reset counter
        document.querySelector("#the_actual_list").innerHTML = `` // Remove previously loaded profiles
        document.querySelector("#button_text").innerHTML = subject // Aesthetic stuff
        load_specific_profiles(subject)
    }
    the_subject.innerHTML = `<a class="dropdown-item" href="#">${subject}</a>`

    // Add option to dropdown
    document.querySelector('#subject_list').append(the_subject)
}


function load_profiles_by_score(min, max) {
    console.log(`Filtering by tutorscore, minimum = ${min}, maximum = ${max}`)

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
            fetch(`/load_tutor_profiles?start=${start}&end=${end}`)
                .then(response => response.json()) // We have a Json object here of 10 tutors
                .then(tutors => {
                    console.log(tutors);
                    return tutors.filter(tutor => tutor.tutor_score >= min && tutor.tutor_score <= max);
                })
                .then(tutors => {
                    console.log("middle")
                    console.log(tutors); // Verify that the tutors json objects have been passed in

                    // Update counter to load the next 10 posts
                    counter+=quantity;

                    // Add tutors
                    tutors.forEach(tutor => add_tutor(tutor));
                })
                .finally(() => {
                    console.log(`Tutors with TutorScore between ${min} and ${max} loaded`)
                    document.querySelector("#tutor_list").style.display = "block"
                });
    }
}


// Tutors with high ratings to have a more appealing tutor score display
const style = document.createElement('style');
style.innerHTML = `
    #shadowBox {
        background-color: rgb(0, 0, 0);
        background-color: rgba(0, 0, 0, 0.2);
        border: 3px solid;
    }

    .rainbow {
        text-decoration: underline;
        font-size: 25px;
        font-family: monospace;
    }

    .rainbow_text_animated {
        background: linear-gradient(to right, #6666ff, #0099ff, #00ff00, #ff3399, #6666ff);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: rainbow_animation 6s ease-in-out infinite;
        background-size: 400% 100%;
    }

    @keyframes rainbow_animation {
        0%, 100% {
            background-position: 0 0;
        }

        50% {
            background-position: 100% 0;
        }
    }
`;
document.head.appendChild(style);


