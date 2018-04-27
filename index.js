function searchName() {
	var restaurantName = $('#restaurantName').val().toLowerCase();
	var restaurantExists = (names.indexOf(restaurantName) > -1);
	localStorage.restaurantName = restaurantName;
	if (restaurantExists) {
		return true;
	} else {
		alert("Restaurant Unavailable")
		return false;
	}
}

function getNames() {
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function(){
  		if(xmlhttp.status == 200 && xmlhttp.readyState == 4) {
    		csv = xmlhttp.responseText;
    		var data = $.csv.toArrays(csv);
    		for (var i = 0; i < data.length; i++) {
    			names.push(data[i][1].toLowerCase());
    		}
  		}
	};
	xmlhttp.open("GET","http://localhost:8000/restaurant.csv",true);
	xmlhttp.send();
	console.log(names)
}

var names = [];
document.addEventListener('DOMContentLoaded', function() {
    getNames();
	}, false);
