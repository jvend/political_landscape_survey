import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from collections import defaultdict

topic_filename = "topics.txt"
#dict_filename  = "LDA_dct.dct"


#lemmatizer = WordNetLemmatizer()
#tag_map = defaultdict(lambda : wordnet.NOUN)
#tag_map['J'] = wordnet.ADJ
#tag_map['V'] = wordnet.VERB
#tag_map['R'] = wordnet.ADV
#
#stop_words = set(stopwords.words('english'))

def Get_Topics(topic_filename):
   lemmatizer = WordNetLemmatizer()
   tag_map = defaultdict(lambda : wordnet.NOUN)
   tag_map['J'] = wordnet.ADJ
   tag_map['V'] = wordnet.VERB
   tag_map['R'] = wordnet.ADV
   
   stop_words = set(stopwords.words('english'))

   def parse_seed(seed):
      current_seed = word_tokenize(seed)
      parsed_seed  = [el.lower() for el in current_seed if el.isalpha()]
      parsed_seed  = [el for el in parsed_seed if not el in stop_words]
      seed_pos     = pos_tag(parsed_seed)
      seed_lemma   = [] 
      for token, tag in seed_pos:
         lemma = lemmatizer.lemmatize(token, tag_map[tag[0]])
         seed_lemma.append(lemma)
      return seed_lemma
   
   ###################################################################################
   ### Lemmatize topics.txt
   
   def Import_topics(topic_filename):
      
      with open(topic_filename) as f:
         lines = f.read().splitlines()
      
      titles = []
      lemmas_primary = []
      lemmas_secondary = []

      for line in lines:
         title = line.split(":")[0]
         titles.append(title)

         line = line.split(":")[1]
         priority_seeds = line.split(";")[0]
         secondary_seeds = line.split(";")[1]

         priority_seeds  = priority_seeds.split(",")
         secondary_seeds = secondary_seeds.split(",")

         priority_seed_lemmas = []
         for seed in priority_seeds:
            priority_seed_lemmas.append(parse_seed(seed))
         lemmas_primary.append(priority_seed_lemmas)

         secondary_seed_lemmas = []
         for seed in secondary_seeds:
            secondary_seed_lemmas.append(parse_seed(seed))
         lemmas_secondary.append(secondary_seed_lemmas)

         
         #print(title)
         #print(priority_seed_lemmas)
         #print(secondary_seed_lemmas)
         #print()
            
      return titles, lemmas_primary, lemmas_secondary 
   
   titles, lemmas_primary, lemmas_secondary = Import_topics(topic_filename)
   

   return titles, lemmas_primary, lemmas_secondary 

#Get_Topics(topic_filename)
