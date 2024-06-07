
document.addEventListener('DOMContentLoaded', function() {

    // The buttons should enable the webapp to display the correct forms to the user
    document.querySelector('#register_student_button').onclick = () => load_form('student');
    document.querySelector('#register_tutor_button').onclick = () => load_form('tutor');
    document.querySelector('#log_in_button').onclick = () => log_in();
    document.querySelector('#log_out_button').onclick = () => log_out();

    // By default, user should be in the log_in view
    log_in();
})


function log_out() {
    document.querySelector('#register_student_view').style.display = 'none';
    document.querySelector('#register_tutor_view').style.display = 'none';
    document.querySelector('#log_in_view').style.display = 'block' ;
}


// Only show the client the login view
function log_in() {
    document.querySelector('#register_student_view').style.display = 'none';
    document.querySelector('#register_tutor_view').style.display = 'none';
    document.querySelector('#log_in_view').style.display = 'block' ;
}


// Only show the client the registration views
function load_form(user_type) {
    if (user_type === 'student') {
        document.querySelector('#register_student_view').style.display = 'block';
        document.querySelector('#register_tutor_view').style.display = 'none';
        document.querySelector('#log_in_view').style.display = 'none' ;
    } else if (user_type === 'tutor') {
        document.querySelector('#register_student_view').style.display = 'none';
        document.querySelector('#register_tutor_view').style.display = 'block';
        document.querySelector('#log_in_view').style.display = 'none' ;
    }
}


