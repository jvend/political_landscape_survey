import time
import numpy as np
from lxml import html
import requests
 
######################################################################################
# Binary Search for Counting Article Number
######################################################################################

import pickle

authors = pickle.load( open( "MuckRack_authors.p", "rb" ) )
source = 'https://muckrack.com'
prev_response_time = 0

import sys
author_data     = sys.argv[1]
author_page_num = int(author_data.split(",")[0])
author_num      = int(author_data.split(",")[1])
#author_page_num  = int(sys.argv[1])
#author_num       = int(sys.argv[2])

author_link = authors[author_page_num][1][author_num] ## author page #, name/link, author index

last_page  = False
init_iters = True
depth = 14
current_page = 2**depth
url = source + author_link + '/articles' + '?page=' + str(current_page)

while last_page == False:
   #time.sleep(prev_response_time)
   start_time = time.time()
   page = requests.get(url)
   prev_response_time = time.time() - start_time
   tree = html.fromstring(page.content)
   
   next_page = tree.xpath('//div[@class="endless_container"]//a/@href')
   if not next_page: # Next page is empty
      last_page = True
      # Now count articles on this page
      articles_on_last_page = len(tree.xpath('//h4[@class="news-story-title"]//a/text()'))
   else:
      next_page = int(next_page[0].split('=')[1])
      if next_page == 2 and current_page != 1: # page exceeds available
         init_iters = False
         depth-=1
         current_page = current_page - 2**depth
      else:
         if init_iters == True:
            depth+=1 
            current_page*=2 # need to increase depth and bound
         else:
            init_iters = False
            depth-=1
            current_page = current_page + 2**depth
   url = source + author_link + '/articles' + '?page=' + str(current_page)

total_articles = 25*(current_page-1) + articles_on_last_page
#print( author_page_num, author_num, author_link, current_page, total_articles )
print( author_page_num, author_num, author_link, total_articles )
