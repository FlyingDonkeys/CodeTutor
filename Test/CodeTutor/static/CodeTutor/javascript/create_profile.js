document.addEventListener("DOMContentLoaded", () => {
    console.log("Loading page")
    document.querySelector('#register_student_view').style.display = 'none';
    document.querySelector('#register_tutor_view').style.display = 'none';
    document.querySelector('#initial_view').style.display = 'block';

    document.querySelector("#student").onclick = () => load_form('student');

    document.querySelector("#tutor").onclick = () => load_form('tutor');

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
        display_choices();
    }
})

function display_choices() {
    document.querySelector('#register_student_view').style.display = 'none';
    document.querySelector('#register_tutor_view').style.display = 'none';
    document.querySelector('#initial_view').style.display = 'block';
}

function load_form(user_type){
    if (user_type === 'student') {
        document.querySelector('#register_student_view').style.display = 'block';
        document.querySelector('#register_tutor_view').style.display = 'none';
        document.querySelector('#initial_view').style.display = 'none' ;
    } else if (user_type === 'tutor') {
        document.querySelector('#register_student_view').style.display = 'none';
        document.querySelector('#register_tutor_view').style.display = 'block';
        document.querySelector('#initial_view').style.display = 'none' ;
    }
}