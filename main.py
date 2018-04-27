from parse_reviews import parseRestaurantItems
from menu_review_filter import menu_filter,review_filter
from textblob import TextBlob
import csv

def track_menu_items(menu_distinct, word_to_menu, reviews_clean_wnl, review_ratings):
	menu_info = {}
	for menu_item in menu_distinct:
		menu_info[menu_item] = [0,0,0]   #0th index: count   1st index: yelp rating  2nd index: our sentiment rating
	#empty_info = menu_info.copy()
	for i in range(len(reviews_clean_wnl)):
		sentiment_info = {}
		#menu_info_copy = empty_info.copy()
		#print(menu_info_copy)
		seen_menu_items = set()
		review = reviews_clean_wnl[i]
		#print(review)
		for sentence in review:
			for hit_word in word_to_menu:
				search_word = " " + hit_word + " "
				menu_hit = word_to_menu[hit_word]
				if search_word in sentence: 
					if menu_hit not in seen_menu_items:
						seen_menu_items.add(menu_hit)
						menu_info[menu_hit][0] += 1
						menu_info[menu_hit][1] += review_ratings[i]
					polarity = TextBlob(sentence).sentiment.polarity
					if menu_hit in sentiment_info:
						sentiment_info[menu_hit] = max(sentiment_info[menu_hit], abs(polarity))
					else:
						sentiment_info[menu_hit] = polarity
		for menu_hit in sentiment_info:
			menu_info[menu_hit][2] += (sentiment_info[menu_hit] * 2) + 3
	for menu_item in menu_info:
		if menu_info[menu_item][0] != 0:
			menu_info[menu_item][1] = round(menu_info[menu_item][1] / menu_info[menu_item][0], 1)
			menu_info[menu_item][2] = round(menu_info[menu_item][2] / menu_info[menu_item][0], 1)
	return menu_info

restaurant_list = parseRestaurantItems()

for restaurant in restaurant_list:
	menu_distinct, word_to_menu = menu_filter(restaurant.items)
	reviews_clean_wnl = review_filter(restaurant.reviews)
	menu_info = track_menu_items(menu_distinct, word_to_menu, reviews_clean_wnl, restaurant.review_ratings)
	top_ten_ordered = sorted(menu_info.items(), key=lambda x: x[1], reverse=True)[:10]
	#top_ten_reviewed = sorted(menu_info.items(), key=lambda x: x[1][1], reverse=True)[:10]
	top_dishes = [x[0].replace(',', '') for x in top_ten_ordered]
	top_count = [x[1][0] for x in top_ten_ordered]
	top_yelp = [x[1][1] for x in top_ten_ordered]
	top_senti = [x[1][2] for x in top_ten_ordered]
	with open('restaurant.csv', 'a') as csvfile:
		restaurant_writer = csv.writer(csvfile)
		restaurant_writer.writerow([restaurant.get_id(), restaurant.get_name(), top_dishes, top_count, top_yelp, top_senti])
print("Complete")




