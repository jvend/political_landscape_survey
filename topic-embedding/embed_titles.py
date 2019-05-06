########################################################################
# Check articles

import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import ast
import gensim
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary = True,limit=500000)


LOC = '/Users/jvenderley/Documents/coding/data/article_titles/'
filename_base = 'article_titles_authorpage_'

def get_title_vecs(current_file):
   with open(current_file) as f:
      lines = f.read().splitlines()
   
   titles = []
   for line in lines:
      #print(line)
      x = ast.literal_eval(line)
      for i in range(0,len(x))
      #print(x)
      #for i in range(1,len(x)):
      #   for j in range(0,len(x[i][0])):
      #      #print(x[i][0][j])
      #      title = x[i][0][j]
      #      #print(title)
      #      title_tokens = word_tokenize(title)
      #      parsed_title = [el.lower() for el in title_tokens if el.isalpha()]
      #      stop_words = set(stopwords.words('english'))
      #      parsed_title = [el for el in parsed_title if not el in stop_words]
      #      titles.append(parsed_title)

   titles = [item for sublist in titles for item in sublist]
   return titles


#mytitle = get_title_words(filepath)
#print(mytitle)

title_dict = {}

import pickle

authors = pickle.load( open( "../article_links_and_bylines/MuckRack_authors.p", "rb" ) )
for authorpage_num in range(len(authors)-1):
   authors_per_page = len(authors[authorpage_num][0])
   for author_num in range(authors_per_page):
      print(authorpage_num, author_num)
      filepath = LOC + 'article_titles_authorpage_' + str(authorpage_num) + '/' + filename_base + str(authorpage_num) + '_authornum_' + str(author_num) + '.txt'
      #print(filepath)
      #current_titles = get_title_words(filepath)
      current_titles = get_title_words(filepath)

      for item in current_titles:
         if item in title_dict:
            title_dict[item] += 1
         else:
            title_dict[item] = 1
      
pickle.dump(title_dict, open("title_word_freq.p", "wb"))
