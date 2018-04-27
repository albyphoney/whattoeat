from parse_reviews import parseRestaurantItems
from menu_review_filter import menu_filter,review_filter
import csv

def track_menu_items(menu_distinct, word_to_menu, reviews_clean_wnl, review_ratings):
	menu_info = {}
	for menu_item in menu_distinct:
		menu_info[menu_item] = [0,0]   #0th index: count   1st index: yelp rating
	for i in range(len(reviews_clean_wnl)):
		seen_menu_items = set()
		review = reviews_clean_wnl[i]
		for hit_word in word_to_menu:
			search_word = " " + hit_word + " "
			menu_hit = word_to_menu[hit_word]
			if search_word in review and menu_hit not in seen_menu_items:
				seen_menu_items.add(menu_hit)
				menu_info[menu_hit][0] += 1
				menu_info[menu_hit][1] += review_ratings[i]
	for menu_item in menu_info:
		if menu_info[menu_item][0] != 0:
			menu_info[menu_item][1] = round(menu_info[menu_item][1] / menu_info[menu_item][0], 1)
	return menu_info

restaurant_list = parseRestaurantItems()
#restaurant_list = restaurant_list[0] #remove this later
for restaurant in restaurant_list:
	menu_distinct, word_to_menu = menu_filter(restaurant.items)
	reviews_clean_wnl = review_filter(restaurant.reviews)
	menu_info = track_menu_items(menu_distinct, word_to_menu, reviews_clean_wnl, restaurant.review_ratings)
	top_ten_ordered = sorted(menu_info.items(), key=lambda x: x[1], reverse=True)[:10]
	#top_ten_reviewed = sorted(menu_info.items(), key=lambda x: x[1][1], reverse=True)[:10]
	with open('restaurant.csv', 'a') as csvfile:
		restaurant_writer = csv.writer(csvfile)
		restaurant_writer.writerow([restaurant.get_id(), restaurant.get_name(), top_ten_ordered])
	print(top_ten_ordered)
	print("%n")




