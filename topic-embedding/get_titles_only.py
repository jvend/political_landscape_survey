########################################################################
# Get Titles

import numpy as np
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import ast

LOC_OLD = '/Volumes/VENDERLEY_8/Muck_Rack_data/article_links_and_bylines_tailed/'
LOC_NEW = '/Volumes/VENDERLEY_8/Muck_Rack_data/article_titles/'
filename_base_old = 'article_links_and_bylines_data_authorpage_'
filename_base_new = 'article_titles_authorpage_'

def get_title_words(filename_in,filename_out):
   with open(filename_in) as f:
      lines = f.read().splitlines()
   
   outfile = open(filename_out, "w")
   #titles = []
   for line in lines:
      x = ast.literal_eval(line)
      for i in range(1,len(x)):
         for j in range(0,len(x[i][0])):
            #print(x[i][0][j])
            title = x[i][0][j]
            #print(title)
            title_tokens = word_tokenize(title)
            parsed_title = [el.lower() for el in title_tokens if el.isalpha()]
            stop_words = set(stopwords.words('english'))
            parsed_title = [el for el in parsed_title if not el in stop_words]
            outfile.write(str(parsed_title))
            #titles.append(parsed_title)
            #print(parsed_title)
   
   outfile.close()
   #titles = [item for sublist in titles for item in sublist]
   #return titles


authors = pickle.load( open( "../article_links_and_bylines/MuckRack_authors.p", "rb" )     )
for authorpage_num in range(len(authors)-1):
   authors_per_page = len(authors[authorpage_num][0])
   for author_num in range(authors_per_page):
      #print(authorpage_num, author_num)
      filepath_in  = LOC_OLD + 'authorpage_' + str(authorpage_num) + '/' + filename_base_old + str(authorpage_num) + '_authornum_' + str(author_num) + '.txt'
      filepath_out = LOC_NEW + 'article_titles_authorpage_' + str(authorpage_num) + '/' + filename_base_new + str(authorpage_num) + '_authornum_' + str(author_num) + '.txt'
      #print(filepath_in)
      #print(filepath_out)
      get_title_words(filepath_in,filepath_out)

