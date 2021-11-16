rm(list = ls())

library(tidyverse)
library(readxl)
library(writexl)

fpath <- "C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization"

f_eere <- "EERE Tool_v12.xlsx"

f_eere2 <- "EERE Tool_v13_.xlsx"

fr_eere <- "GREET Elec Gen CI"
fr_cor <- "Corr_EF_GREET!A4:J542"

d_eere <- read_excel(paste0(fpath,"\\", f_eere), sheet = fr_eere, na = c("NA", "Na", "na"))
d_cor <- read_excel(paste0(fpath,"\\", f_eere2), range = fr_cor, na = c("NA", "Na", "na")) %>%
  filter(Sector %in% c("Electric Power"), 
         Activity %in% c("Electricity"))

d_eere <- d_eere %>%
  filter (Measures %in% c("CO2", "N2O", "CH4")) %>% 
  select(!c(Total, `GREET Pathway`)) %>%
  pivot_longer(c("Feedstock", "Fuel"), names_to = "Scope",  values_to = "Value") %>%
  mutate(Scope = if_else(Scope %in% c('Feedstock', 'Fuel'), 'Electricity, Supply Chain', "Electricity, Combustion"))

d_eere <- d_eere %>%
  left_join(d_cor, by = c("Activity Type", "Scope"))

write_csv(d_eere, paste0(fpath, "\\", "GREET_LCI_Electric.csv"))
