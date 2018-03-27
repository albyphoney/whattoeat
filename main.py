from parse_reviews import parseRestaurantItems
from menu_review_filter import menu_filter,review_filter
import operator

#restaurant_list = [restaurant_list[1]] #remove this later

def count_menu_items(menu_distinct, word_to_menu, reviews_clean_wnl):
	menu_counts = {}
	for menu_item in menu_distinct:
		menu_counts[menu_item] = 0
	for review in reviews_clean_wnl:
		for hit_word in word_to_menu:
			search_word = " " + hit_word + " "
			if search_word in review:
				#print(hit_word)
				menu_counts[word_to_menu[hit_word]] += 1
	return menu_counts

restaurant_list = parseRestaurantItems()
for restaurant in restaurant_list:
	menu_distinct, word_to_menu = menu_filter(restaurant.items)
	#print(word_to_menu)
	#print(restaurant.reviews[0])
	reviews_clean_wnl = review_filter(restaurant.reviews)
	#print(reviews_clean_wnl)
	menu_counts = count_menu_items(menu_distinct, word_to_menu, reviews_clean_wnl)
	#print(menu_counts)
	top_ten = sorted(menu_counts.items(), key=operator.itemgetter(1))[-10:]
	print(top_ten)
	print("%n")
#print(menu_counts['Drunken Noodles Dinner'])



