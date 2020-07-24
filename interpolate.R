# USE: Rscript interpolate.R <positions> <genmap> > <outfile>

library(magrittr,quietly = T)
library(dplyr,quietly = T,warn.conflicts = F)
library(stats,quietly = T)
library(data.table,quietly = T)
options(scipen = 999)

args <- commandArgs(TRUE)

#read in positions for window midpoints, and recombination map
pos<-read.table(args[1])
map<-read.table(args[2])

#remove positions smaller and greater than min/max map pos
minpos <- min(map$V2)
maxpos <- max(map$V2)
spos <- data.frame(position=pos[pos$V1 > minpos & pos$V1 < maxpos,])
subpos <- rbind(spos,maxpos)
#calc monotonic interpolation
interp<-splinefun(map$V2,map$V3,method='monoH.FC')
chpos<- subpos %>% mutate(gen=interp(x=subpos$position))

setDT(chpos)
chpos[,rate:=(shift(gen,1,type="lead")-gen)/(shift(position,1,type="lead")-position)]
setcolorder(DT,c("position","rate","gen"))
setDF(chpos)

#output to stdout
write.table(na.omit(chpos),'',quote = F, row.names = F,col.names = F)
