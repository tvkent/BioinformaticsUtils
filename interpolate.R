# USE: Rscript interpolate.R <positions> <genmap> > <outfile>

library(magrittr,quietly = T)
library(dplyr,quietly = T,warn.conflicts = F)
library(stats,quietly = T)

args <- commandArgs(TRUE)

#read in positions for window midpoints, and recombination map
pos<-read.table(args[1])
map<-read.table(args[2])

#calc monotonic interpolation
interp<-splinefun(map$V2,map$V3,method='monoH.FC')
chpos<- pos %>% mutate(gen=interp(x=pos$V1))

#output to stdout
write.table(chpos,'',quote = F, row.names = F,col.names = F)
