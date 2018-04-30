function home() {
	window.location.href="../index.html"
}

function appendToTable(table, rowData, i) {
	var row = $('<tr data-toggle="modal" data-target="#orderModal" data-id="'+ i.toString() + '"></tr>');
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
    				dishNames = dishes;
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
    				for (var l = 6; l < 16; l++) {
    					// Up to 3 reviews for dish l
    					var clean_reviews = data[i][l].replace(/[\[\]']+/g,"");
    					var final_reviews = clean_reviews.replace(/\s{2,}/g," ");
    					var split_reviews = final_reviews.split(',');
    					foodReviews.push(split_reviews);
    				}
    				for (var m = 16; m < 26; m++) {
    					var clean_word = data[i][m].replace(/[\[\]']+/g,"");
    					var final_word = clean_word.replace(/\s{2,}/g," ");
    					var split_words = final_word.split(', ');
    					for (var n = 0; n < split_words.length; n++) {
    						split_words[n] = split_words[n].split(' ');
    					}
    					hitWords.push(split_words);
    				}
    				console.log(hitWords);
    				var table = $('<table class="table table-striped table-hover"><thead></thead><tbody></tbody></table>');
    				$('#tableView').append(appendHeader(table, ['Dish Name', 'Total Yelp Reviews', 'Average Yelp Review', 'Average Sentiment Review']))
    				for (var k = 0; k < dishes.length; k++) {
    					$('#tableView').append(appendToTable(table, [dishes[k], count[k], yelp[k], senti[k]], k));
    				}
    			}
    		}
  		}
	};
	xmlhttp.open("GET","http://localhost:8000/restaurant.csv",true);
	xmlhttp.send();
}

$(function(){
    $('#orderModal').modal({
        keyboard: true,
        backdrop: "static",
        show:false,

    }).on('show.bs.modal', function(){
    	$("#modalTable").remove();
        var getIdFromRow = $(event.target).closest('tr').data('id');
        $('#dishName').html("Reviews for " + dishNames[getIdFromRow]);
        var modalTable = $('<table id="modalTable" class="table table-striped"><thead></thead><tbody></tbody></table>');
        for (var i = 0; i < foodReviews[getIdFromRow].length; i++) {
        	var row = $('<tr></tr>');
        	var reviewBody = foodReviews[getIdFromRow][i];
        	var wordsToBold = hitWords[getIdFromRow][i];
        	var boldedReview = makeBold(reviewBody, wordsToBold);
        	row.append($('<td>' + boldedReview + '</td>'));
        	modalTable.append(row);
        }
        $('#orderDetails').append(modalTable);
    });
});

function makeBold(input, wordsToBold) {
    return input.replace(new RegExp('(\\b)(' + wordsToBold.join('|') + ')(\\b)','ig'), '$1<b>$2</b>$3');
}

//foodReviews: each index is an of top 10 dishes for restaurant, each subarray is up to 3 reviews
var foodReviews = [];
var dishNames = [];
var hitWords = [];
document.addEventListener('DOMContentLoaded', function() {
	$("#restaurantName").html(localStorage.restaurantName + "'s Top 10 Items");
    getData(localStorage.restaurantName);
	}, false);
