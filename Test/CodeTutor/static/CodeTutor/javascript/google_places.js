
$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places") 
.done(function( script, textStatus ) {
    google.maps.event.addDomListener(window, "load", initAutoComplete)
})


let autocomplete;

function initAutoComplete(){
   autocomplete = new google.maps.places.Autocomplete(
       document.getElementById('id-google-address'),
       {
           types: ['address'],
           //default in this app is "SG"
           componentRestrictions: {'country': ['sg']},
       })

   autocomplete.addListener('place_changed', onPlaceChanged);
}


function onPlaceChanged (){

    var place = autocomplete.getPlace();
    if (!place.geometry){
        document.getElementById('id-google-address').placeholder = "*Begin typing address";
    }
    else{
        
        for (var i = 0; i < place.address_components.length; i++) {
            for (var j = 0; j < place.address_components[i].types.length; j++) {
                if (place.address_components[i].types[j] == "postal_code") {
                    $('#id_post_code').val(place.address_components[i].long_name)   
                }
            }
        }
    }
}