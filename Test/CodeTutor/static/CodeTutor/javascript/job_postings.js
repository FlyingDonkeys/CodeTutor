console.log("student list page is loaded!")

window.onscroll = () => {
    // If user scrolls to the end, load more profiles
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        load();
    }
}

// Start with first profile
let counter = 1;

// Load 10 profiles at a time
const quantity = 10;

// When DOM loads, render the first 10 profiles
document.addEventListener('DOMContentLoaded', function () {
    load()
    // Other eventlisteners such as change of profile display upon hover etc
});

// Load next set of posts
function load() {
    // Check if load is being called
    console.log("Loading new profiles")

    // Set start and end profile numbers
    const start = counter;
    const end = start + quantity - 1;

    // Get new posts and add posts
    fetch(`/load_student_profiles?start=${start}&end=${end}`)
        .then(response => response.json()) // We have a Json object here of the student model
        .then(students => {
            console.log(students); // Verify that the students json objects have been passed in
            students.forEach(student => {
                if (student.is_finding_tutor) { // Only display students actively finding tutors
                    add_student(student)
                }
            });
            console.log("All students loaded");
            // Update counter to load the next 10 posts
            counter+=quantity;
        })
        .finally(() => {
            // Display header once profiles are done, this shld be fast process
            document.querySelector('#heading').style.display = 'block';
        });

}

function add_student(student) {
    // Create new student profile object for viewing
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
                                    <img style='height: 100%; width: 100%; object-fit: contain;' src="${url}" alt="No Image">
                                </div>
                                <div class="col-9">
                                    <div class="row mb-1">
                                        <div class="col-3">
                                            <h4>Username: <h4>
                                        </div>
                                        <div class="col-3">
                                            ${student.username}
                                        </div>
                                    </div>
                                    <div class="row mb-1">
                                        <div class="col-3">
                                            <h4>Location: <h4>
                                        </div>
                                        <div class="col-3">
                                            ${student.location}
                                        </div>
                                    </div>
                                    <div class="row mb-1">
                                        <div class="col-3">
                                            <h4>Subjects Required: <h4>
                                        </div>
                                        <div class="col-3">
                                            ${subjects_required}
                                        </div>
                                    </div>
                                    <div class="row mb-1">
                                        <div class="col-4"><!-- To centralise --></div>
                                        <div class="col-2">
                                            <!-- Logic to apply for tuition job not done -->
                                            <a class="btn btn-primary" href="logout" role="button">Apply as Tutor</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                      </div>
                      <hr>`

    // Add post to DOM
    document.querySelector('#student_list').append(profile);
}

