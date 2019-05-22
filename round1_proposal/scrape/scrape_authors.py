import time
import numpy as np
from lxml import html
import requests
 
######################################################################################
# Author scrape from Muck Rack
######################################################################################
All_author_info = []

retry = True
for page_num in range(1,123):
   retry = True
   print(page_num)
   url = 'https://muckrack.com/beat/politics?page=' + str(page_num)
   try:
      response = requests.get(url)
      tree = html.fromstring(response.content)
      author_names = tree.xpath('//div[@class="col-md-3"]//a/text()')
      author_links = tree.xpath('//div[@class="col-md-3"]//a/@href')
      print(len(author_names),len(author_links))
      if len(author_names) == len(author_links): 
         author_info  = [author_names,author_links]
         print(author_info)
         All_author_info.append(author_info)
         time.sleep(random.normalvariate(2,1)) # sleep for avg 2+-1 s
         retry = False
      else:
         retry = True
   except:
      retry = True
   
   if retry == True: page_num = page_num - 1 
   

import pickle
pickle.dump(All_author_info, open("MuckRack_authors.p", "wb"))
