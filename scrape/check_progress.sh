#!/bin/bash

DataLoc='/data/tmp_project_data/muck_rack'
for i in `ls $DataLoc | grep 'info'`; do

author_page_num=`echo $i | awk 'BEGIN { FS = "authorpage_"}; {print $2}' | awk 'BEGIN{FS = "-"};{print $1}'`
file_count=`ls $DataLoc | grep ${author_page_num}_authornum | wc | awk '{print $1}'`

echo $author_page_num $file_count

done

echo ""
echo "Check currently running:"
ps aux | head -1
ps aux | grep "scrape" | grep -v grep
