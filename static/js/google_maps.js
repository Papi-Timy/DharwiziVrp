
$.getScript( "https://maps.googleapis.com/maps/api/js?key=AIzaSyCa_lcyCRbSOMqRcnrv6WnlY1vVk1rrofY&libraries=places") 
.done(function( script, textStatus ) {
    google.maps.event.addDomListener(window, "load", initMap)

})


function initMap() {
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer;
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 7,
        center: { lat: 41.85, lng: -87.65 }
    });
    directionsDisplay.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsDisplay);

}

function calculateAndDisplayRoute(directionsService, directionsDisplay) {
  directionsService.route({
      origin: origin,
      destination: destination,
      waypoints: waypts,
      optimizeWaypoints: true,
      travelMode: google.maps.TravelMode.DRIVING,
  }, function(response, status) {
    if (status === 'OK') {
      directionsDisplay.setDirections(response);


    } else {

      alert('Directions request failed due to ' + status);
      // window.location.assign("/route")
    }
  });
}


