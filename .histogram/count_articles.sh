#!/bin/bash

filename=$1

awk ' BEGIN{SUM1 = 0; SUM2 = 0; SUM3 = 0; current_author="NULL"; current_author_num=0; last_page_num=0; last_page_count=0};
  {
    if( NR == 1) {current_author=$4; current_author_num=$2;}
    if( NF == 4 && NR != 1) {print current_author_num,current_author,SUM1,SUM2,SUM3,last_page_num,last_page_count; current_author=$4; current_author_num=$2; SUM1=0;SUM2=0;SUM3=0;last_page_num=0; last_page_count=0;  }
    else if ( NF == 3 )  {SUM1+=$1;SUM2+=$2;SUM3+=$3;last_page_num+=1;last_page_count=$1;}
  }
 END{print current_author_num,current_author,SUM1,SUM2,SUM3,last_page_num,last_page_count;} ' $filename 

