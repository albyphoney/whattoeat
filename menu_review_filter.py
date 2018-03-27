# import packages

import bs4 as bs
import nltk
from nltk.tokenize import sent_tokenize # tokenizes sentences
import re
from nltk.stem import PorterStemmer
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

eng_stopwords = stopwords.words('english')
wnl = WordNetLemmatizer()

#For menu_filter only
def find_pairs(noun, word_list):
    ret = []
    for word in word_list:
        ret.append(word + " " + noun)
    return ret

#For menu_filter only
def add_hit_word(word, menu_item, word_to_menu, menu_to_word, seen_word):
    #we already know this word isn't a hit word
    if word in seen_word:
        return
    #this word was hit word for one other menu item
    elif word in word_to_menu:
        other_menu_item = word_to_menu[word]
        menu_to_word[other_menu_item].remove(word)
        del word_to_menu[word]
        seen_word.add(word)
    #this word isn't a hit word for any menu item yet
    else:
        menu_to_word[menu_item].append(word)
        word_to_menu[word] = menu_item 

#For menu_filter only
def menu_cleaner(menu):
	num_items = len(menu)
	menu_distinct = []
	menu_clean = []
	seen = set()
	for i in range(0,num_items):
	    clean_item = cleaner(menu[i])
	    if clean_item not in seen:
	        seen.add(clean_item)
	        menu_distinct.append(menu[i])
	        menu_clean.append(clean_item)
	return menu_distinct, menu_clean

#For review_filter only
def reviews_cleaner(reviews):
	num_items = len(reviews)
	reviews_clean = []
	for i in range(0,num_items): 
	    clean_item = cleaner(reviews[i])
	    reviews_clean.append(clean_item)
	return reviews_clean

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return 'n'

def cleaner(item):
    '''
    Clean and preprocess an item.
    
    1. Remove HTML tags
    2. Use regex to remove all special characters (only keep letters)
    3. Make strings to lower case and tokenize / word split items
    4. Remove English stopwords
    5. Rejoin to one string
    '''
    
    #1. Remove HTML tags
    item = bs.BeautifulSoup(item,features='lxml').text
    
    #2. Use regex to find emoticons
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', item)
    
    #3. Remove punctuation
    item = re.sub("[^a-zA-Z]", " ",item)
    
    #4. Tokenize into words (all lower case)
    item = item.lower().split()
    
    #5. Remove stopwords
    eng_stopwords = set(stopwords.words("english"))
    extra_stopwords = ['lunch','dinner','large','small','medium','kids', "thai", "chinese", "italian", "mediterranean",
                      "french", "japanese", "spanish", "greek", "ethiopian", "indian"]
    eng_stopwords.update(extra_stopwords)
    item = [w for w in item if not w in eng_stopwords]
    
    #6. Join the item to one sentence
    item = ' '.join(item+emoticons)
    # add emoticons to the end
    return(item)

def menu_filter(menu):
	menu_distinct,menu_clean = menu_cleaner(menu)
	is_noun = lambda pos: pos[:2] == 'NN'
	word_to_menu = {}   #word: hit word, menu item
	menu_to_word = {}   #key: menu item, value: hit words
	seen_word = set()   #words that we've seen

	for i in range(len(menu_clean)):
	    menu_original = menu_distinct[i]
	    menu_item = menu_clean[i]
	    lemmatized_nouns = []
	    lemmatized_other = []
	    menu_to_word[menu_original] = []
	    token_tag = pos_tag(menu_item.split())
	    for pair in token_tag:
	        if is_noun(pair[1]):
	            res_noun = wnl.lemmatize(pair[0],pos=get_wordnet_pos(pair[1]))
	            lemmatized_nouns.append(res_noun)
	        else:
	            res_other = wnl.lemmatize(pair[0],pos=get_wordnet_pos(pair[1]))
	            lemmatized_other.append(res_other)
	    for noun in lemmatized_nouns:
	        add_hit_word(noun, menu_original, word_to_menu, menu_to_word, seen_word)
	        #pair nouns with noun
	        for noun_pair in find_pairs(noun, list(filter(lambda n: n != noun, lemmatized_nouns))):
	            add_hit_word(noun_pair, menu_original, word_to_menu, menu_to_word, seen_word)
	        #pair others with noun
	        for other_pair in find_pairs(noun, lemmatized_other):  
	            add_hit_word(other_pair, menu_original, word_to_menu, menu_to_word, seen_word)
	return menu_distinct, word_to_menu

def review_filter(reviews):
	reviews_clean = reviews_cleaner(reviews)
	reviews_clean_wnl = []
	for i in range(len(reviews_clean)):	    
	    wnl_stems = []
	    token_tag = pos_tag(reviews_clean[i].split())
	    #print(token_tag)
	    for pair in token_tag:
	        res = wnl.lemmatize(pair[0],pos=get_wordnet_pos(pair[1]))
	        wnl_stems.append(res)
	    reviews_clean_wnl.append(' '.join(wnl_stems))
	return reviews_clean_wnl


