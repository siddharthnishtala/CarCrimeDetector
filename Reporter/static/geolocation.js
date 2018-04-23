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
    img.src = "http://maps.googleapis.com/maps/api/staticmap?center=" + latitude + "," + longitude + "&zoom=17&size=300x300&sensor=false";

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



function urlRefresh(){
	var x= document.getElementById("dropdown").value;
	if (window.location.href.indexOf('?')==-1)
		window.location.href=window.location.href+"?value="+x;
	else if(window.location.href.indexOf('&value=')==-1)
		window.location.href=window.location.href+"&value="+x;
	else
		window.location.href=window.location.href.substring(0, window.location.href.indexOf('&value='))+"&value="+x;
	
}

$( document ).ready(function() {
   
	function sort(hours){
	var i, x, rowDate, rowTime, day, time;
	
	table = document.getElementById("table");
	rows = table.getElementsByTagName("tr");
	
	for(i=1; i<(rows.length); i++ ){
		
		x=rows[i].getElementsByTagName("td")[1];
		rowDate= x.innerHTML.split(/[\s,:]+/);
		
		if((rowDate[5]=="p.m.")&&(parseInt(rowDate[3])<12)){
			rowTime= ((parseInt(rowDate[3])+12)*100)+parseInt(rowDate[4]);
		}
		else if((rowDate[5]!="p.m.")&&(parseInt(rowDate[3])==12))
			rowTime= parseInt(rowDate[4]);
		else
			rowTime= (parseInt(rowDate[3])*100)+parseInt(rowDate[4]);
		
		var currentDate= new Date();
		day= currentDate.getDate();
		time= currentDate.getHours()*100+currentDate.getMinutes();
		
		if(time>hours){
			if(rowTime<(time-hours)||(day!=parseInt(rowDate[1]))){
				table.deleteRow(i);
				i--;
			}
				
		}
		else{
			if((rowTime>(time+2400-hours)&&(day-1!=(parseInt(rowDate[1]))))||((rowTime<(time+2400-hours)&&(day!=(parseInt(rowDate[1])))))){
				table.deleteRow(i);
				i--;
			}
		}
	}
}
	
	var query= window.location.href.substring(window.location.href.indexOf('value='));
	var val= query.split(/[=]/);
	//alert(val[1]);
	var decide= parseInt(val[1]);
	switch (decide){
		case 15: 
			document.getElementById("dropdown").selectedIndex = "0";
			sort(15);
			break;
		case 100:
			document.getElementById("dropdown").selectedIndex = "1";
			sort(100);
			break;
		case 600:
			document.getElementById("dropdown").selectedIndex = "2";
			sort(600);
			break;
		case 1200:
			document.getElementById("dropdown").selectedIndex = "3";
			sort(1200);
			break;
		case 2400:
			document.getElementById("dropdown").selectedIndex = "4";
			sort(2400);
			break;
		case -1:
			document.getElementById("dropdown").selectedIndex = "5";
			break;
		default:
			break;
	}
});



//var url = window.location.search;
//url = url.replace("?", ''); // remove the ?
//alert(url);
