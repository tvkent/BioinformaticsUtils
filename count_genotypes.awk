#!/bin/bash
#count number of genotypes at each site from 012 data
#return chr,pos,homoref,homoalt,totalhomo,het,nonmissing,total
#Tyler Kent 10 May 2017

BEGIN{OFS = "\t"}
{
	var=$1OFS$2
	het=0
	ref=0
	alt=0
	nonmissing=0
	total=0

	for (i = 5; i<=NF; ++i){

		if( $i == "1" ){ het+=1 }
		if( $i != "." ){ nonmissing+=1 }
		if( $i == "0" ){ ref+=1 }
		if( $i == "2" ){ alt+=1 }
		total+=1

	}
	totalhomo=ref+alt
	print var OFS ref OFS alt OFS totalhomo OFS het OFS nonmissing OFS total
}
