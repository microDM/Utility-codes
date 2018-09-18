#!/usr/bin/env Rscript
arguments <- commandArgs(trailingOnly = TRUE)
if(length(arguments) < 3){
  cat("This script assume that your class labels are in \"class\" column. All other columns will be considered as features. \n Usage: csvToLibSVM.R inputFilename positiveClassName outputFilename\n")
} else if (length(arguments) ==3){
  data <- read.table(file = arguments[1],header = T,sep = ",")
  class.labels <- as.character(data$class)
  temp <- vector()
  for (i in class.labels) {
    if(i == arguments[2]){
      temp <- c(temp,"1")
    }else{
      temp <- c(temp,"-1")
    }
  }
  class.labels <- temp
  rm(temp)
  data$class <- NULL
  data <- na.omit(data)
  for (i in 1:length(class.labels)) {
     t <- paste(1:length(data[i,]),data[i,],sep = ":")
     data[i,] <- t
   }
 data <- cbind(class.labels,data)
# head(data)
 write.table(x = data,file = arguments[3],quote = F,sep = " ",row.names = F,col.names = F)
}