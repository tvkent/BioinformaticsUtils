#Tyler Kent
#24 Oct 2016
#Convert 2 column chromosome-pos format to bed3

import argparse
import pandas as pd

def arguments():
    parser  = argparse.ArgumentParser(description="Converts 2 column chromosome-pos format to bed3")
    parser.add_argument("-i", "--input", help="path for input .sites file", required=True)
    parser.add_argument("-o","--output", help="path for output .bed file", required=True)
    args = parser.parse_args()
    return(args)

def convert(lines):

    '''
    Will check for chromosome constancy among sites within a
    potential block, so no chromosome arguments needed. input
    is two columns, with one site per line in the second column.
    Output will be the range from (site1, endsite+1)
    '''

    sites = {}
    beddf = pd.DataFrame(columns=['#CHROM','START','END'])

    for line in lines:

        sline = line.split()
        chrom = sline[0]
        pos = int(sline[1])

        '''else check if largest key in dictionary is current key-1
        also check if still on same chromosome
        if not next site or is next chromosome, print
        existing dictionary info, clear sites dict, and add to
        empty dict'''

        if sites:
            if chrom in sites:
                last = int(pos) - 1

                if max(sites[chrom])==last:
                    sites[chrom].append(int(pos))
                else:
                    beddf = get_segment(sites,beddf)
                    sites = {}
                    sites = {chrom:[int(pos)]}

            else:
                beddf = get_segment(sites,beddf)
                sites = {}
                sites = {chrom:[int(pos)]}

        #check if sites dict is empty, if so simply add
        if not sites:
            sites = {chrom:[int(pos)]}
	
    beddf = get_segment(sites,beddf)

    return(beddf)

def get_segment(sites,beddf):

    '''
    take dictionary of sites, make start pos as
    min(items), end pos as max(items)+1, and chrom
    as key. add this series to beddf, return beddf
    '''
    [(keys,values)] = sites.items()
    start = min(values)
    end = max(values)+1
    chrom = keys
    newline = pd.Series([chrom,start,end],index=['#CHROM','START','END'])
    beddf = beddf.append(newline,ignore_index=True)

    return(beddf)

def printtofile(bed,outpath):

    '''
    Print full DF to file
    '''

    bed.to_csv(outpath,header=True,index=False,sep='\t')

################
# Begin script
################

args = arguments()

#infile info
inpath = args.input
infile = open(inpath,'r')
lines = infile.readlines()

bed = convert(lines)

bed[['START','END']]=bed[['START','END']].astype(int)
printtofile(bed,args.output)
