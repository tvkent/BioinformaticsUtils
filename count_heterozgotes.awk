#!/bin/bash
#count number of heterozygotes at each site from 012 data
#return chr,pos,count,nonmissing,total
#Tyler Kent 10 May 2017

BEGIN{OFS = "\t"}
{
	var=$1OFS$2
	count=0
	nonmissing=0
	total=0

	for (i = 5; i<=NF; ++i){

		if( $i == "1" ){ count+=1 }
		if( $i != "." ){ nonmissing+=1 }

		total+=1

	}
	print var OFS count OFS nonmissing OFS total
}
