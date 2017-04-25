library(tidyr)
library(dplyr)
library(foreach)
library(data.table)
library(readr)


#making a string of sample files
experiments <- list.files()
experiments <- experiments[grep("emd.tsv", experiments)]

#reading the files and putting them in a list
all_experiments <-  foreach(file = experiments, .combine=bind_rows) %do% {
  file_content <- readr::read_tsv(file = file, col_names = c("attribute", "value"))
  spread(file_content, key = "attribute", value = "value")
}


#filtering columns with 90% missing values
#column_names <- colnames(all_experiments)

#for (i in column_names){
#  x <- (length(which(is.na(all_experiments[,i])))/745*100)
#  if (x >= 90){
#    all_experiments[,i] <- NULL
#  }
#}

write_tsv(all_experiments,path = "all_experiments.tsv", col_names = TRUE)
