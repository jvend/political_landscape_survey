########################################################################
# Check articles

import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
import ast

LOC = '/data/tmp_project_data/muck_rack/authorpages/'
filename_base = 'article_links_and_bylines_data_authorpage_'
output_LOC  = '/data/tmp_project_data/topic_filter/'
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

   return lines, lemmas

######################################################################################### Get Topics
topic_filename  = "topics.txt"
from parse_topics import Get_Topics
topic_titles, topic_seeds_primary, topic_seeds_secondary = Get_Topics(topic_filename)
topic_seeds = [topic_seeds_primary, topic_seeds_secondary]

hash_all = {}
for i in range(2):
   for topic_num, topic in enumerate(topic_seeds[i]):
      for seed_num, seed in enumerate(topic):
         if len(seed) > 0:
            if seed[0] not in hash_all:
               hash_all[seed[0]] = [[topic_num,seed_num,seed,i]]
            else:
               hash_all[seed[0]].append([topic_num,seed_num,seed,i])


'''
We use a two-level scheme as a first-order approach for picking out topics that will
be used to train a supervised topic classifier. Each topic has been given primary and
secondary seeds. If a primary seed is in the document, that document is immediately
classified under the corresponding topic. If the unique secondary seed count exceeds
the user-specified threshold (default = 2), the document is classified under the 
corresponding topic. Topics are not mutually exclusive.
'''

def check_for_topic(lemma):
   rel_topics = {}
   counter = {}
   second_seed_instance_num = 2
   relevant_topic_nums_list = []
   for word_num, word in enumerate(lemma):
      if word in hash_all:
         for topic_seed_pair in hash_all[word]:
            seed_length = len(topic_seed_pair[2])
            seed_priority = topic_seed_pair[3]
            seed_flag = False

            if seed_length == 1:
               seed_flag = True
            elif len(lemma) - (1+word_num) >= seed_length - 1:
               remaining_seed_words = seed_length - 1
               for j in range(remaining_seed_words):
                  if lemma[word_num+j+1] == topic_seed_pair[2][j+1]:
                     seed_flag = True
                  else:
                     seed_flag = False
                     break

            if seed_flag == True and seed_priority == 0:            
               rel_topics[topic_seed_pair[0]] = 1
            elif seed_flag == True and seed_priority == 1:
               if topic_seed_pair[0] not in counter:
                  counter[topic_seed_pair[0]] = {topic_seed_pair[1]:1}
               else:     
                  if topic_seed_pair[1] not in counter[topic_seed_pair[0]]:
                     counter[topic_seed_pair[0]][topic_seed_pair[1]] = 1 
                  else:     
                     counter[topic_seed_pair[0]][topic_seed_pair[1]] += 1
   for key in counter:
      if len(counter[key].keys()) >= second_seed_instance_num:
         rel_topics[key] = 1
   for key in rel_topics:
      relevant_topic_nums_list.append(key)

   return relevant_topic_nums_list

##  ##Benchmark/Testing
##  test_filepath = "test_check_for_topic.txt"
##  lines, current_lemmas = lemmatize_file(test_filepath)
##  #print(lines)
##  #print(current_lemmas)
##  for lemma_num,lemma in enumerate(current_lemmas):
##     print(lines[lemma_num])
##     print(lemma)
##     relevant_topics = check_for_topic(lemma)
##     for topic in relevant_topics:
##        print(topic_titles[topic])
##     print()

import pickle
authors = pickle.load( open( "../MuckRack_authors.p", "rb" ) )

out_files = []
for topic_num in range(len(topic_seeds[0])):
   output_path =  output_LOC + "topic_" + str(topic_num) + ".txt"
   out_files.append(open(output_path, "w"))

for authorpage_num in range(len(authors)-1):
   authors_per_page = len(authors[authorpage_num][0])
   for author_num in range(authors_per_page):
#for authorpage_num in range(0,1):
#   for author_num in range(2,3):
      print(authorpage_num, author_num, flush=True)
      filepath = LOC + 'authorpage_' + str(authorpage_num) + '/' + filename_base + str(authorpage_num) + '_authornum_' + str(author_num) + '.txt'
      lines, current_lemmas = lemmatize_file(filepath)

      for lemma_num,lemma in enumerate(current_lemmas):
         relevant_topics = check_for_topic(lemma)
         for topic in relevant_topics:
            out_files[topic].write(str(lines[lemma_num]) + '\n')

for outputfile in out_files:
   outputfile.close()
