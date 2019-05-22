########################################################################
# Build Corpus 

import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
import ast

from gensim import corpora
from gensim.corpora import Dictionary

LOC = '/data/tmp_project_data/muck_rack/authorpages/'
filename_base = 'article_links_and_bylines_data_authorpage_'
lemmatizer = WordNetLemmatizer()

# Need to map tags: cf https://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
tag_map = defaultdict(lambda : wordnet.NOUN)
tag_map['J'] = wordnet.ADJ
tag_map['V'] = wordnet.VERB
tag_map['R'] = wordnet.ADV

def lemmatize_file(current_file):
   with open(current_file) as f:
      lines = f.read().splitlines()
   
   lemmas = []
   for line in lines:
      x = ast.literal_eval(line)
      title_and_headline = x[0] + ". " + x[1]
      title_and_headline_tokened = word_tokenize(title_and_headline)
      parsed_title_and_headline = [el.lower() for el in title_and_headline_tokened if el.isalpha()] #lowercase
      stop_words = set(stopwords.words('english')) 
      parsed_title_and_headline = [el for el in parsed_title_and_headline if not el in stop_words]
      text_pos = pos_tag(parsed_title_and_headline)
      title_and_headline_lemma = []
      for token, tag in text_pos:
         lemma = lemmatizer.lemmatize(token, tag_map[tag[0]])
         title_and_headline_lemma.append(lemma)
      lemmas.append(title_and_headline_lemma)
      #print(lemmas)

   return lemmas

loaded_dct = Dictionary.load("LDA_dct.dct")

import pickle
authors = pickle.load( open( "../MuckRack_authors.p", "rb" ) )

corpus = []
for authorpage_num in range(len(authors)-1):
   authors_per_page = len(authors[authorpage_num][0])
   for author_num in range(authors_per_page):
      print(authorpage_num, author_num)
      filepath = LOC + 'authorpage_' + str(authorpage_num) + '/' + filename_base + str(authorpage_num) + '_authornum_' + str(author_num) + '.txt'
      current_lemmas = lemmatize_file(filepath)
      for lemma in current_lemmas:
         corpus.append(loaded_dct.doc2bow(lemma))

corpora.MmCorpus.serialize('corpus.mm', corpus)

