from restaurant import Restaurant
import json
from pprint import pprint

#Returns a list of Restaurant objects that contains the restaurant ID, name, items, and reviews.
def parseRestaurantItems():
	rest_info = json.load(open('data/test_restaurants.json'))
	rest_reviews = json.load(open('data/test_reviews.json'))
	restaurant_list = []
	for i in range(len(rest_info)):
		# Creates list of item NAMES to be stored in the restaurant object
		item_names = []
		items_list = rest_info[i]['items']
		for item in items_list:
			item_names.append(item['name'])

		review_list = rest_reviews[i]['reviews']

		#Creates a list of item REVIEWS to be stored in the restaurant object
		review_comments = []
		for review in review_list:
			review_comments.append(review['comment'])

		#Creates a list of item REVIEWS to be stored in the restaurant object
		review_ratings = []
		for review in review_list:
			review_ratings.append(review['rating'])

		# Adds Restaurant object to a list of all restaurants
		restaurant_list.append(Restaurant(rest_info[i]['id'], rest_info[i]['name'], item_names, review_comments, review_ratings))

		return restaurant_list
		
parseRestaurantItems()
