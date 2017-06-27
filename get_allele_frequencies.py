import argparse
import numpy as np
import pandas as pd
import multiprocessing as mp

def arguments():
	parser  = argparse.ArgumentParser(description="Loads VCF and returns allele frequencies for every site.")
	parser.add_argument("-i", "--input", help="path for input", required=True)
	parser.add_argument("-o","--output", help="path for output", required=True)
	parser.add_argument("-p","--processes",help="number of processes (cores) to run job on",default=10, type=int)
	parser.add_argument("-c","--chunksize",help="size of chunks to read and write",default=5, type=int)
	args = parser.parse_args()
	return(args)

def allele_freqs(df):

	'''
	df will be pool-processed over -p cores.
	split df into a descriptive df and genotype df
	descriptive df will be handled as pandas DF, while
	the genotype df will be parsed and handled as a numpy
	array to calc 2 frequencies and allele counts.
	will return single merged df with 
	ref, alt, reffreq, altfreq, refcount, altcount, indivs
	columns.
	'''

	info = df[[0,1,3,4]]
	info.columns = ['ch','pos','ref','alt']

	genos = df.loc[:,9:].astype(str)
	genos = genos.apply(lambda x: x.str.split(':').str[0], axis=1)
	firstgenos = genos.apply(lambda x: x.str.split('/').str[0], axis=1)
	secondgenos = genos.apply(lambda x: x.str.split('/').str[1], axis=1)
	firstpd = firstgenos
	secondpd = secondgenos

	firstgenos[firstgenos=='.']=np.nan
	secondgenos[secondgenos=='.']=np.nan
	firstgenos = firstgenos.values
	secondgenos = secondgenos.values
	firstgenos = firstgenos.astype(float)
	secondgenos = secondgenos.astype(float)

	totgenos = np.add(firstgenos,secondgenos)

	altfreq = (np.nanmean(totgenos, axis=1))/2
	reffreq = 1 - altfreq
	
	notmissing = np.isfinite(totgenos)
	indivs = np.sum(notmissing, axis=1)

	firstcounts = firstpd.apply(pd.Series.value_counts, axis=1).fillna(0)
	secondcounts = secondpd.apply(pd.Series.value_counts, axis=1).fillna(0)

	if '0' in firstcounts.columns.values:
		firstzeros = firstcounts['0'].astype(int)
	else:
		firstzeros = np.zeros_like(indivs).astype(int)
	if '1' in firstcounts.columns.values:
		firstones = firstcounts['1'].astype(int)
	else:
		firstones = np.zeros_like(indivs).astype(int)
	if '0' in secondcounts.columns.values:
		secondzeros = secondcounts['0'].astype(int)
	else:
		secondzeros = np.zeros_like(indivs).astype(int)
	if '1' in secondcounts.columns.values:
		secondones = secondcounts['1'].astype(int)
	else:
		secondones = np.zeros_like(indivs).astype(int)

	refcount = np.add(firstzeros,secondzeros)
	altcount = np.add(firstones,secondones)

	freqmatrix = np.column_stack((reffreq, altfreq, refcount, altcount, indivs))
	freqdf = pd.DataFrame(freqmatrix, columns=['reffreq','altfreq','refcount','altcount','indivs'])
	freqdf[['refcount','altcount','indivs']] = freqdf[['refcount','altcount','indivs']].astype(int)

	total = pd.concat([info,freqdf], axis = 1)

	return(total)

####################
# Begin Script
####################

args = arguments()

#get infile info
input = args.input

#get outpath info
outpath = args.output

reader = pd.read_table(input, sep='\t', chunksize=args.chunksize, iterator = True, comment='#', header=None)
pool = mp.Pool(args.processes)

iter = 1
prelist = []
for df in reader:
	pre = pool.apply_async(allele_freqs, [df])
	prelist.append(pre)
for p in prelist:
	result = p.get()

	#result = pool.apply_async(allele_freqs, [df]).get()
	if iter==1:
		result.to_csv(outpath,header=True,index=False,sep='\t')
	else:
		result.to_csv(outpath,header=False,index=False,mode='a',sep='\t')
	iter+=1
