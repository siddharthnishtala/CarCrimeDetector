function geoFindMe() {
  var output = document.getElementById("out");
  var url;

  if (!navigator.geolocation){
    output.innerHTML = "<p>Geolocation is not supported by your browser</p>";
    return;
  }

  function success(position) {
    var latitude  = position.coords.latitude.toString();
    var longitude = position.coords.longitude.toString();
    url= '/home/location?lat='+latitude+"&long="+longitude;
    output.innerHTML = '<p>Latitude is </p>';

    var img = new Image();
    img.src = "https://maps.googleapis.com/maps/api/staticmap?center=" + latitude + "," + longitude + "&zoom=17&size=300x300&sensor=false";

    output.appendChild(img);
    window.location.href= url;
  }

  function error() {
    output.innerHTML = "Unable to retrieve your location";
  }

  output.innerHTML = "<p>Locating…</p>";

  navigator.geolocation.getCurrentPosition(success, error);

//  window.location.href= "/home/location?lat="
}
