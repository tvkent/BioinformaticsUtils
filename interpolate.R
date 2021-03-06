# USE: Rscript interpolate.R <positions> <genmap> > <outfile>

#library(magrittr,quietly = T)
library(tidyverse,quietly = T,warn.conflicts = F)
library(stats,quietly = T)
library(data.table,quietly = T,warn.conflicts = F)
options(scipen = 999, digits = 22)

args <- commandArgs(TRUE)

#read in positions for window midpoints, and recombination map
pos<-read.table(args[1])
map<-read.table(args[2])

#remove positions smaller and greater than min/max map pos
#minpos <- min(map$V2)
#maxpos <- max(map$V2)
#spos <- data.frame(position=pos[pos$V1 > minpos & pos$V1 < maxpos,])
#subpos <- rbind(spos,maxpos)
#calc monotonic interpolation
interp<-splinefun(map$V2,map$V3,method='monoH.FC')
chpos<- pos %>% mutate(gen=interp(x=V1)) %>% rename(pos = V1)

setDT(chpos)
chpos[,rate:=(shift(gen,1,type="lead")-gen)/(shift(pos,1,type="lead")-pos)]
setcolorder(chpos,c("pos","rate","gen"))

setDF(chpos)
#reset genetic position to make first site 0, and add last site as same rate as second to last
chpos <- chpos %>% mutate(gen=gen + abs(dplyr::first(gen))) %>% mutate(rate = ifelse(is.na(rate), nth(rate,-2), rate))
#chpos <- as_tibble(chpos) %>% add_row(pos=max(map$V2),rate=dplyr::last(chpos$rate),gen=dplyr::last(chpos$gen))
setDF(chpos)
chpos$pos <- as.character(chpos$pos)

#output to stdout
write.table(na.omit(chpos),'',quote = F, row.names = F, col.names = F)
