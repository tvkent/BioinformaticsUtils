#!/bin/bash
#pipeline for getting 012 genotype calls from vcf files
#Tyler Kent 10 May 2017

#run with: bash get_vcf_genotypes.sh vcf output

vcfpath=$1
outpath=$2

if [[ $vcfpath =~ \.gz$ ]]; then 

zgrep -v '#' $vcfpath | awk -f pull_vcf_samples.awk | awk -f genotype_vcf_samples.awk > $outpath

else

grep -v '#' $vcfpath | awk -f pull_vcf_samples.awk | awk -f genotype_vcf_samples.awk > $outpath

fi
