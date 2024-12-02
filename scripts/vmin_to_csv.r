library(openxlsx)
library(tidyverse)
library(glue)

# Define the function
process_split_data <- function(split_number, output_folder, tab_folder = "results/vmin") {
  
  # List all files that match the specified pattern
  list_files <- list.files(tab_folder, pattern = glue::glue("^split_{split_number}"), full.names = TRUE)
  
  # Read the corresponding Excel file
  excel_file_path <- glue::glue("input/split/Charge_density_split_{split_number}.xlsx")
  excel <- read.xlsx(excel_file_path) %>% select(sample_id, mvm_id)
  
  # Define the function to read tab-delimited files with a custom header
  read_tab_with_custom_header <- function(file_path) {
    header_data <- read_delim(file_path, delim = "\t", col_names = FALSE, n_max = 2, skip = 1)
    combined_header <- paste0(as.character(header_data[1, ]))
    
    data <- read_delim(file_path, delim = "\t", col_names = combined_header, skip = 3) %>%
      mutate(charge_diff = (`Sum of cations` - `Sum of anions`) / (`Sum of cations` + `Sum of anions`) * 100) 
    
    return(data)
  }
  
  # Extract the adom.doc value (after __)
  adom_docs <- str_extract(list_files, "__(.*)") %>%
    str_remove_all("__") %>%
    str_remove("_.*")
  
  # Initialize an empty list to store data frames
  data_frames <- list()
  
  # Read in each file, modify column names, and store in the list
  for (i in seq_along(list_files)) {
    file_path <- list_files[i]
    df <- read_tab_with_custom_header(file_path)
    
    # Debugging: print the data frame and the adom_doc
    # print(glue("Data frame from file: {basename(file_path)}"))
    # print(df)

    # Add the data frame to the list
    data_frames[[i]] <- df %>% bind_cols(excel)  %>% mutate(adom_doc = adom_docs[i]) # %>% select(sample_id, charge_diff,adom_doc)
  }
  
  # Combine all data frames by columns
  all_data <- bind_rows(data_frames)
  
  final_data <- all_data %>% group_by(sample_id) %>% mutate(charge_diff_abs = abs(charge_diff)) %>% slice_min(order_by = charge_diff_abs, n = 1) %>% ungroup() %>% select(-charge_diff_abs)

  # Create output file name and save the final data frame as a CSV file
  output_file_name <- glue::glue("{output_folder}/charge_dif_{split_number}.csv")
  write.csv(final_data, file = output_file_name, row.names = FALSE)
  
  # Return the final data frame (optional)
  return(final_data)
}

# Example of how to call the function
# process_split_data(split_number = 5, output_folder = "C:/sim/Anna/Output")


# Example of how to call the function
process_split_data(split_number = 1, output_folder = "results/charge_difference")
process_split_data(split_number = 5, output_folder = "results/charge_difference")
process_split_data(split_number = 2, output_folder = "results/charge_difference")
process_split_data(split_number = 3, output_folder = "results/charge_difference")
process_split_data(split_number = 4, output_folder = "results/charge_difference")

# split_number <-  1
# output_folder <- "results/charge_difference"
# tab_folder <- "results/vmin"
