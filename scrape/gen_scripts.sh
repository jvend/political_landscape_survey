#!/bin/bash

# N.B loop is inclusive
for i in {111..121}
   do
      python scrape_article_locations-single-authorpage.py $i &
   done

