#Tyler Kent
#22 Oct 2016
#Convert pairwise maf to column-fasta format

import argparse
import pandas as pd

def arguments():
	parser  = argparse.ArgumentParser(description="Loads pairwise maf and returns reference and aligned sequences each in columns")
	parser.add_argument("-i", "--input", help="path for input", required=True)
	parser.add_argument("-o","--output", help="path for output", required=True)
	parser.add_argument("-r","--reference", help="full reference sequence name, e.g. CR_scaffold1")
	args = parser.parse_args()
	return(args)

def lineloop(ref, lines):

	'''
	loop over all lines, with checks for score,
	ref seq, aligned seq, and sends pairs to be
	added to final DataFrame
	'''

	i = 0
	df = pd.DataFrame()

	for line in lines:

		if line[0]=='a' and i==0:
			i+=1

		elif i==1 and line[0]=='s':
			i+=1
			sline = line.split()

			if sline[1]==ref:
				refseq = sline[6]
				startbp = sline[2]
				numbp = sline[3]
			else:
				print('WARNING: first sequence does not match reference '+str(sline[1])+str(sline[2]))
				break

		elif i==2 and line[0]=='s':
			i=0
			sline = line.split()
			alignedseq = sline[6]

			dfupdate = build_df(refseq,startbp,alignedseq,numbp)
			df = df.append(dfupdate)

		elif i==0 and line[0]=='s':
			print('WARNING: sequence skipped. Possibly more than one aligned sequence')
	df.columns=['ref','aligned','pos']
	df = df[['pos','ref','aligned']]
	return(df)

def build_df(refseq,startbp,alignedseq,numbp):

	'''
	Take sequence info for each aligned block
	and combine into same DataFrame, return dfupdate.
	Removes gaps from reference.
	'''

	bp = [int(startbp)+n+1 for n in range(0,int(numbp))]
	bpseries = pd.Series(bp).astype(str)
	refseries = pd.Series(list(refseq))
	alignedseries = pd.Series(list(alignedseq))

	seqs = pd.concat([refseries,alignedseries], axis=1)
	seqs.columns=['ref','aligned']
	seqs = seqs[seqs.ref != '-']
	seqs = seqs.reset_index(drop=True)
	seqs['pos']=bpseries

	return(seqs)

##########################
# Begin
##########################

args = arguments()

#get file info
inpath = args.input
outpath = args.output

infile = open(inpath, 'r')
lines = infile.readlines()

dfout = lineloop(args.reference, lines)

outfile = open(outpath,'w')

dfout.to_csv(outpath,header=True,index=False,sep='\t')

outfile.close()
