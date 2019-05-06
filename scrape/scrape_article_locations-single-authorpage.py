import time
import numpy as np
from lxml import html
import requests
 
######################################################################################
# Article Link and Byline scrape from Muck Rack
######################################################################################

import pickle

authors = pickle.load( open( "MuckRack_authors.p", "rb" ) )

source = 'https://muckrack.com'
#DriveLocation = '/data/tmp_project_data/muck_rack'
#DriveLocation = '/home/jordan/VenderleyData/Muck_Rack_data/new-cap'
DriveLocation = '/data/tmp_project_data/muck_rack'

prev_response_time = 0
#for author_page_num in range(len(authors)):
#for author_page_num in range(70,len(authors)):

import sys
author_page_num = int(sys.argv[1])

filename_info = DriveLocation + '/article_links_and_bylines_data_authorpage_'+ str(author_page_num) + '-info.txt'
f_info        = open(filename_info, "w")

for author_num in range(len(authors[author_page_num][1])):
   author_link = authors[author_page_num][1][author_num] ## author page #, name/link, author index
   author_data = [author_num]

   filename = DriveLocation + '/article_links_and_bylines_data_authorpage_'+ str(author_page_num) + '_authornum_' + str(author_num) + '.txt'
   f = open(filename, "w")

   f_info.write(str(author_page_num) + ' ' + str(author_num) + ' ' + str(prev_response_time) + ' ' + str(author_link) + '\n')
   #print(str(author_page_num) + ' ' + str(author_num) + ' ' + str(prev_response_time) + ' ' + str(author_link))

   last_page = False
   url = source + author_link + '/articles' + '?page=1'

   count = 1
   while last_page == False and count <= 400:
      time.sleep(prev_response_time)
      start_time = time.time()
      page = requests.get(url)
      prev_response_time = time.time() - start_time
      tree = html.fromstring(page.content)
      
      article_names    = tree.xpath('//h4[@class="news-story-title"]//a/text()')
      article_links    = tree.xpath('//h4[@class="news-story-title"]//a/@href')
      
      article_bylines = tree.xpath('//div[contains(@class,"news-story-body")]')
      for i in range(len(article_bylines)):
         article_bylines[i] = article_bylines[i].text_content() # later use .split()
      author_data.append([article_names,article_links,article_bylines])
      f_info.write('     ' + str(len(article_names)) + ' ' + str(len(article_links)) + ' ' + str(len(article_bylines)) + '\n')
      #print('     ' + str(len(article_names)) + ' ' + str(len(article_links)) + ' ' + str(len(article_bylines)))
      
      next_page = tree.xpath('//div[@class="endless_container"]//a/@href')
      if not next_page: # Next page is empty
         last_page = True
      else:
         url = source + next_page[0]

      f.write(str(author_data) + '\n')
      #f_info.flush()
      count = count + 1

   f.close()

f_info.close()
