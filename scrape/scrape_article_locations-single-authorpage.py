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
DriveLocation = '/data/tmp_project_data/muck_rack'

prev_response_time = 0

import sys
author_page_num = int(sys.argv[1])

filename_info = DriveLocation + '/article_links_and_bylines_data_authorpage_'+ str(author_page_num) + '-info.txt'
f_info        = open(filename_info, "w")

for author_num in range(len(authors[author_page_num][1])):
   author_link = authors[author_page_num][1][author_num] ## author page #, name/link, author index

   filename = DriveLocation + '/article_links_and_bylines_data_authorpage_'+ str(author_page_num) + '_authornum_' + str(author_num) + '.txt'
   f = open(filename, "w")

   f_info.write(str(author_page_num) + ' ' + str(author_num) + ' ' + str(prev_response_time) + ' ' + str(author_link) + '\n')

   last_page = False
   count_articles = 0
   url = source + author_link + '/articles' + '?page=1'
   title_hash = {}
   while last_page == False and count_articles < 10000:
      time.sleep(prev_response_time)
      start_time = time.time()
      page = requests.get(url)
      prev_response_time = time.time() - start_time
      tree = html.fromstring(page.content)
      data = tree.xpath('//a[@data-title]')
      for el in data:
         title    = str(el.xpath('@data-title')[0])
         headline = str(el.xpath('@data-description')[0])
         article_source   = str(el.xpath('@data-source')[0])
         link     = str(el.xpath('@data-link')[0])
         info = [title, headline, article_source, link]
         if title not in title_hash:
            f.write(str(info) + '\n')
            title_hash[title] = 1
            count_articles += 1
      
      next_page = tree.xpath('//div[@class="endless_container"]//a/@href')
      if not next_page: # Next page is empty
         last_page = True
      else:
         url = source + next_page[0]

      f.flush()
      f_info.flush()

   f.close()

f_info.close()
