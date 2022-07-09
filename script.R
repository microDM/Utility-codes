setwd('/MyVolume/temp/sahabram/ANI')

indata <- read.table(file = 'myway/ANI.txt.matrix',sep = '\t',header = T,check.names = F)

library(reshape2)
indata.m <- na.omit(melt(indata))
indata.m$value <- round(indata.m$value,digits = 2)
library(ggplot2)
ggplot(data = indata.m,mapping = aes(x = Organism,y = variable,fill=value)) + geom_tile(color = "white") + theme_bw() + scale_fill_distiller(palette = 'RdYlBu',name='Ortho-ANI') + theme_minimal() + theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust = 1)) + coord_fixed() + geom_text(aes(Organism,variable, label = value), color = "black", size = 4) + theme(
  axis.title.x = element_blank(),
  axis.title.y = element_blank(),
  panel.grid.major = element_blank(),
  panel.border = element_blank(),
  panel.background = element_blank(),
  axis.ticks = element_blank(),
  legend.justification = c(1, 0),
  legend.position = c(1, 0.5),
  legend.direction = "horizontal")+
  guides(fill = guide_colorbar(barwidth = 7, barheight = 1,
                               title.position = "top", title.hjust = 0.5))

