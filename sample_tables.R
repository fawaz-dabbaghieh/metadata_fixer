library(tidyr)
library(dplyr)
library(foreach)
library(data.table)
library(readr)

#making a string of sample files
samples <- list.files()
samples <- samples[grep("smd.txt", samples)]

#reading the files and putting them in a list

all_samples <-  foreach(file = samples, .combine=bind_rows) %do% {
  file_content <- read_tsv(file = file, col_names = c("attribute", "value"))
  spread(file_content, key = "attribute", value = "value")
}

#filtering columns with 90% missing values
#column_names <- colnames(all_samples)

#for (i in column_names){
#  x <- (length(which(is.na(all_samples[,i])))/132*100)
#  if (x >= 90){
#    all_samples[,i] <- NULL
#  }
#}
write_tsv(all_samples,path = "all_samples.tsv", col_names = TRUE)
