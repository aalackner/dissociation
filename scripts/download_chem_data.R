library(tidyverse)
source("../src/sourcecode.R")

## first we load the list of mvm_ids 
## replace with your source

mvm_ids = read.csv("mvm_ids.csv")$mvm_id

## load set up variables and library for accessing the API
library(jsonlite)

my.token <- "PUJD93023KAS943HD"

# define folder where json's should be stored for potential future access
folder <- "01_mvm_miljödata/"

fail_table <- data.frame(
  mvm_id = integer(),
  comment = integer(),
  stringsAsFactors = FALSE
)

overview <- data.frame(
  mvm_id = integer(),
  comment = character(),
  stringsAsFactors = FALSE
)


## Now we loop through all the mvm_ids accessing the json file, saving the raw json in case I need to ever access the metadata. And then moving on to saving it as a csv per station.

for (id in mvm_ids){
  
  full.samples <- get_samples(folder, id)
  
  csv.path <- paste0(folder, "CSV/", id, ".csv" )
  
  
  ## run the JSON through the functions combine_col and into_table to generate a single csv file for each station.
  process_samples(full.samples, csv.path, id)
  
# Pause for 10 seconds in order to let the server also do other jobs
# remove this step if you want it to go faster
  Sys.sleep(10) 
}

print(fail_table)

fail_table %>% write.csv(., file = 'fails.csv')

overview %>% write.csv(., file = 'overview.csv')

folder.csv <- "01_mvm_miljödata/CSV/"

#  List all files in the folder
files_in_folder <- list.files(path = folder.csv, full.names = TRUE)

# Filter for .csv files
csv_files <- files_in_folder %>%
  keep(~ str_detect(.x, "\\.csv$"))  # Keep only .csv files

# Step 3: Read and bind all .csv files into a single tibble
csv_files %>%
  map_dfr(read_csv) %>% write.csv(.,file = paste0(folder, 'water_chem_complete.csv' ))