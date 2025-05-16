
library(tidyverse)
# load the data
charge_diff_input <- c("results/charge_difference/charge_dif_1.csv",
                        "results/charge_difference/charge_dif_2.csv",
                        "results/charge_difference/charge_dif_3.csv",
                        "results/charge_difference/charge_dif_4.csv",
                        "results/charge_difference/charge_dif_5.csv")

chemistry <- read.csv("input/chemistry/chemistry_complete.csv") %>% select(-X)
# Read and row bind all CSV files in charge_diff_input
data <- lapply(charge_diff_input, read.csv) %>%
        bind_rows() %>%
        left_join(chemistry, by = c("sample_id", "mvm_id"))

data %>% rename( org_charge = "Z..6..aq.") %>% mutate(org_charge_eq_mg_C = org_charge/(TOC_mol*12.01*1000)) -> data_renamed # equivalance of charge per liter of solution
write.csv(data_renamed, "results/chemistry/complete.csv", row.names = FALSE)
