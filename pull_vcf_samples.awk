#!/bin/bash
#pull chr,pos,ref,alt,samples from vcf file with no header

BEGIN{OFS = "\t"}
{	
	var=$1OFS$2OFS$4OFS$5
	for (i = 10; i<=NF; ++i){

		var=var OFS $i
	}
	print var
}
