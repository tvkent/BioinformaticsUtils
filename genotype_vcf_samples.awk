#!/bin/bash
#convert vcf samples to 012 genotypes.
#return chr,pos,ref,alt,genotypes
#Tyler Kent 10 May 2017

BEGIN{OFS = "\t"}
{
	var=$1OFS$2OFS$3OFS$4
	geno=""
	for (i = 5; i<=NF; ++i){
		split($i,g,":")

		if( g[1] == "0/0" ){ geno="0" }
		else if( g[1] == "0/1" || g[1] == "1/0" ){ geno="1" }
		else if( g[1] == "1/1" ){ geno="2" }
		else if( g[1] == "./." ){ geno="." }

		var=var OFS geno
	}
	print var
}
