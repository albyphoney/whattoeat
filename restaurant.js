function appendToTable(table, rowData) {
	var row = $('<tr></tr>');
	$(rowData).each(function (j, cellData) {
		row.append($('<td>'+cellData+'</td>'));
	});
	table.append(row);
	return table;
}

function appendHeader(table, rowData) {
	var row = $('<tr></tr>');
	$(rowData).each(function (j, cellData) {
		row.append($('<th>'+cellData+'</th>'));
	});
	row.appendTo(table.find("thead"))
	// table.append(row);
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
    				//Parsing string
    				var dishes = data[i][2].split(',');
    				var count = data[i][3].split(',');
    				var yelp = data[i][4].split(',');
    				var senti = data[i][5].split(',');
    				for (var j = 0; j < dishes.length; j++) {
    					var clean_dish = dishes[j].replace(/[\[\]']+/g,"");
						var final_dish = clean_dish.replace(/\s{2,}/g," ");
						dishes[j] = final_dish

						var clean_count = count[j].replace(/[\[\]']+/g,"");
						count[j] = clean_count

						var clean_yelp = yelp[j].replace(/[\[\]']+/g,"");
						yelp[j] = clean_yelp

						var clean_senti = senti[j].replace(/[\[\]']+/g,"");
						senti[j] = clean_senti
    				}
    				var table = $('<table class="table table-striped table-hover"><thead></thead><tbody></tbody></table>');
    				$('#tableView').append(appendHeader(table, ['Dish Name', 'Total Yelp Reviews', 'Average Yelp Review', 'Average Sentiment Review']))
    				for (var k = 0; k < dishes.length; k++) {
    					$('#tableView').append(appendToTable(table, [dishes[k], count[k], yelp[k], senti[k]]));
    				}
    			}
    		}
  		}
	};
	xmlhttp.open("GET","http://localhost:8000/restaurant.csv",true);
	xmlhttp.send();
}

document.addEventListener('DOMContentLoaded', function() {
	$("#restaurantName").html(localStorage.restaurantName + "'s Top 10 Items");
    getData(localStorage.restaurantName);
    // getData('Versailles');
	}, false);
