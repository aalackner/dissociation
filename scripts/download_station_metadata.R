# I wanted to know whether I could get elevation from the station metadata
# turns out I can't, not very useful :(


library(tidyverse)
mvm_ids = read.csv("mvm_ids.csv")$mvm_id

## load set up variables and library for accessing the API
library(jsonlite)

my.token <- "PUJD93023KAS943HD"

/observations-service/v2/sample-sites/

get_samples <- function(folder, id) {
  
  # Try the operation and catch errors
  tryCatch({
    # Step 2: Define the pipeline (assuming into_table() and combine_col() are defined elsewhere)
    url.call <- paste0('https://miljodata.slu.se/api//observations-service/v2/sample-sites/'id,'?token=', my.token)
    json.path <- paste0(folder, "JSON\\", id, ".json" )
    
    full.samples<-fromJSON(url.call)
    
    ## Write as json to the folder
    write(toJSON(full.samples), file = json.path)
    
    return(full.samples)
  }, error = function(e) {
    # Step 3: If an error occurs, add the id and error message to the fail_table
    fail_table <<- rbind(fail_table, data.frame(mvm_id = id, comment = e$message))
    return(NA)
  })
}