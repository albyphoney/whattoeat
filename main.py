from parse_reviews import parseRestaurantItems
from menu_review_filter import menu_filter,review_filter
import operator



def count_menu_items(menu_distinct, word_to_menu, reviews_clean_wnl):
	menu_counts = {}
	for menu_item in menu_distinct:
		menu_counts[menu_item] = 0
	for review in reviews_clean_wnl:
		seen_menu_items = set()
		for hit_word in word_to_menu:
			search_word = " " + hit_word + " "
			menu_hit = word_to_menu[hit_word]
			if search_word in review and menu_hit not in seen_menu_items:
				seen_menu_items.add(menu_hit)
				menu_counts[menu_hit] += 1
				# if word_to_menu[hit_word] == "Hot and Crusty":
				# 	print(review)
				# 	print(hit_word)
	return menu_counts

restaurant_list = parseRestaurantItems()
restaurant_list = restaurant_list #remove this later
for restaurant in restaurant_list:
	menu_distinct, word_to_menu = menu_filter(restaurant.items)
	reviews_clean_wnl = review_filter(restaurant.reviews)
	menu_counts = count_menu_items(menu_distinct, word_to_menu, reviews_clean_wnl)
	top_ten = sorted(menu_counts.items(), key=operator.itemgetter(1))[-10:]
	print(top_ten)
	print("%n")
#print(menu_counts['Drunken Noodles Dinner'])



