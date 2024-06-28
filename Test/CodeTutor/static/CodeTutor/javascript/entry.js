
document.addEventListener('DOMContentLoaded', function() {

    // The buttons should enable the webapp to display the correct forms to the user
    document.querySelector('#register_student_button').onclick = () => load_form('student');
    document.querySelector('#register_tutor_button').onclick = () => load_form('tutor');
    document.querySelector('#login_button').onclick = () => log_in();
    console.log("DOM content reloaded");

    // By default, user should be in the log_in view, unless there are form errors
    const studentformHasErrors = document.querySelector('#student_form_has_errors').value;
    const tutorformHasErrors = document.querySelector('#tutor_form_has_errors').value;

    // A small detail here, but Python returns true while javascript true is actually True,
    // so we gotta compare with 'True' instead
    if (studentformHasErrors === 'True') {
        load_form('student');
    } else if (tutorformHasErrors === 'True') {
        load_form('tutor');
    } else {
        log_in();
    }
})


// Only show the client the login view
function log_in() {
    document.querySelector('#register_student_view').style.display = 'none';
    document.querySelector('#register_tutor_view').style.display = 'none';
    document.querySelector('#login_view').style.display = 'block' ;
}


// Only show the client the registration views
function load_form(user_type) {
    if (user_type === 'student') {
        document.querySelector('#register_student_view').style.display = 'block';
        document.querySelector('#register_tutor_view').style.display = 'none';
        document.querySelector('#login_view').style.display = 'none' ;
    } else if (user_type === 'tutor') {
        document.querySelector('#register_student_view').style.display = 'none';
        document.querySelector('#register_tutor_view').style.display = 'block';
        document.querySelector('#login_view').style.display = 'none' ;
    }
}


