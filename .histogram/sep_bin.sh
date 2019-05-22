#!/bin/bash

# Separates authors that did and did not hit our 10,000 article limit.
# If the limit was hit, this goes and finds the true article count via binary search of user pages.

awk '{if($4 > 9500 && $7 > 395 && $4 <10500 ){} else{print $1,$2,$3,$4}}' count_consolidate.txt > no_bin_search.txt
awk '{if($4 > 9500 && $7 > 395 && $4 <10500 ){print $0}}' count_consolidate.txt > need_bin_search.txt
for i in `awk '{print $1","$2}' need_bin_search.txt`; do python count-single-authorpage.py $i; done > post_bin_search.txt
cat no_bin_search.txt post_bin_search.txt | sort -k 1,1n -k2,2n > final_count.txt
