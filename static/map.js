// Based on various pages on Google Maps Javascript API documentation except where noted otherwise

// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.

// Handle location updates
// From https://medium.com/risan/track-users-location-and-display-it-on-google-maps-41d1f850786e
const trackLocation = ({ onSuccess, onError = () => { } }) => {
    if ('geolocation' in navigator === false) {
      return onError(new Error('Geolocation is not supported by your browser.'));
    }
  
    // Use watchPosition for live updates
    return navigator.geolocation.watchPosition(onSuccess, onError);
  };
  
  var map;
  
  function initMap() {

      map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: 40.3471, lng: -74.6566},
          zoom: 17
      });
      locationMarker = new google.maps.Marker({
          map: map,
          icon: 'my_location.svg'
      });
  
      // Sets pins on map from static file
      plants = [
          {
              "lat": "40.3471",
              "lng": "-74.6566",
          },
          {
              "lat": "40.3468",
              "lng": "-74.6552",
          },
          {
              "lat": "40.3469",
              "lng": "-74.6566",
          },
          {
              "lat": "40.3472",
              "lng": "-74.6552",
          }
      ]
  
      for (var i = 0; i < plants.length; i++) {
          var lat = parseFloat(plants[i].lat);
          var lng = parseFloat(plants[i].lng);
  
          console.log(i, lat, lng);
          var marker = new google.maps.Marker({
              map: map,
              position: {
                  lat: lat,
                  lng: lng
              },
          });
      }
  
      // Call trackLocation
      // From https://medium.com/risan/track-users-location-and-display-it-on-google-maps-41d1f850786e
      trackLocation({
          onSuccess: ({ coords: { latitude: lat, longitude: lng } }) => {
              locationMarker.setPosition({ lat, lng });
          map.panTo({ lat, lng });
          },
          onError: err =>
              alert(`Error: ${getPositionErrorMessage(err.code) || err.message}`)
      });
  }