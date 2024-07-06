console.log("profile page is loaded!");

document.addEventListener('DOMContentLoaded', function(){

    load_profile();
    
});

document.addEventListener('DOMContentLoaded', function(){

    document.querySelector('#showButton').onclick = showMap;
    
});


function load_profile() {
    console.log("loading student profile");
    //check if user is student or tutor over here 
    fetch(`/load_user_profile`)
        .then(response=> response.json())
        .then(user => {
            console.log(user);
            generate_profile(user);
            if(user.is_student){
                generate_map(user);
            }
            if(!user.is_student){
                alert("hiding the button!");
                hideButton();
            }
        });

}
function hideButton(){
    document.querySelector('#showButton').style.display = 'none';
}
let counter = 0;
function showMap() {
    document.querySelector('#map').style.display = counter%2== 0? 'block': 'none';
    counter ++;
}

function generate_profile(user){
const profile = document.createElement('div');

    
    let url = user.user.profile_picture_url === null ? 'https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg'
                                                            : user.user.profile_picture_url;
    //if isStudent, show location, else do not show
    profile.className = 'post';

    profile.innerHTML = null;

if (user.is_student) {
    profile.innerHTML += `
    <div class="profile-head"  id="User${user.user.id}">
               <div class="row vh-40">
                   <div class="col-xl-6 text-center mx-auto align-self-center ">
                        <div class="imgcover mb-4">
                            <img src="${url}" style="width:250px; height:250px; object-fit: cover;"alt="No Image" class="rounded-pill bg-white p-2 shadow">
                        </div>
                        <b class="fs-6">Hello I am,  ${user.user.username}</b>
                        <h1 class="fw-bold mb-4 fs-1">Student</h1>
                        <p> Location: ${user.user.location}</p>
                        <p> Postal Code: ${user.user.postal_code}</p> 
                        <p> Finding Tutor: ${user.user.finding_tutor}</p> 
                    </div>
               </div>
            </div>`;    
} else {
    profile.innerHTML += `
    <div class="profile-head"  id="User ${user.user.id}">
               <div class="row vh-35">
                   <div class="col-xl-6 text-center mx-auto align-self-center ">
                        <div class="imgcover mb-4">
                            <img src="${url}" style="width:250px; height:250px; object-fit: cover;"alt="No Image" class="rounded-pill bg-white p-2 shadow">
                        </div>
                        <b class="fs-6">Hello I am,  ${user.user.username}</b>
                        <h1 class="fw-bold mb-4 fs-1">Tutor</h1>
                        <p> ${user.user.description}</p>    
                        <a href = "subscribe"
                        <button class="btn btn-outline-primary fw-bolder fs-7 px-4 py-2 mt-3 rounded-pill">Subsribe</button>
                        </a>
                    </div>
               </div>
            </div>`;
}

document.querySelector('#student_list').append(profile);
}


function generate_map(user){
//may have included GoogleMaps API multiple times 
$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + user.google_api_key + "&libraries=places") 
.done(function() {
    //convert postal code to actual address that gets fed into google maps
    var geocoder = new google.maps.Geocoder();
    
    geocoder.geocode({
        'address': user.user.postal_code.toString(),
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

