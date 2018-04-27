function arrayToTable(tableData) {
	var table = $('<table></table>');
	$(tableData).each(function (i, rowData) {
		var row = $('<tr></tr>');
		$(rowData).each(function (j, cellData) {
			row.append($('<td>'+cellData+'</td>'));
		});
		table.append(row);
	});
	return table;
}

function getData(restaurantName) {
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function(){
  		if(xmlhttp.status == 200 && xmlhttp.readyState == 4){
    		csv = xmlhttp.responseText;
    		var data = $.csv.toArrays(csv);
    		for (var i = 0; i < data.length; i++) {
    			if (restaurantName.toLowerCase() === data[i][1].toLowerCase()) { 
    				$('#tableView').append(arrayToTable([data[i]]));
    			}
    		}
  		}
	};
	xmlhttp.open("GET","http://localhost:8000/restaurant.csv",true);
	xmlhttp.send();
}

document.addEventListener('DOMContentLoaded', function() {
    getData(localStorage.restaurantName);
    // getData('Versailles');
	}, false);
