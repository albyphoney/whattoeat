class Restaurant():
    def __init__(self, rest_id, rest_name, rest_items, rest_reviews, rest_review_ratings):
    	self.ID = rest_id
    	self.name = rest_name
    	self.items = rest_items
    	self.reviews = rest_reviews
    	self.review_ratings = rest_review_ratings

    def get_id(self):
    	"""Returns the restaurant ID"""
    	return self.ID
    
    def get_name(self):
    	"""Returns the restaurant name"""
    	return self.name
    
    def get_items(self):
    	"""Returns the restaurant items"""
    	return self.items

    #The reviews and review ratings indeces correspond to each other
    def get_review_comments(self):
    	"""Adds review to list of reviews for the restaurant"""
    	return self.reviews

    def get_review_ratings(self):
    	"""Adds review to list of reviews for the restaurant"""
    	return self.review_ratings




