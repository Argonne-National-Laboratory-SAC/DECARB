rm(list = ls())

library(tidyverse)
library(readxl)
library(writexl)

fpath <- "C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization"

f_eere <- "EERE Tool_v12.xlsx"

f_eere2 <- "EERE Tool_v13.xlsx"

fr_eere <- "GREET Elec Gen CI"
fr_cor <- "Corr_EF_GREET!A4:J542"

d_eere <- read_excel(paste0(fpath,"\\", f_eere), sheet = fr_eere, na = c("NA", "Na", "na"))
d_cor <- read_excel(paste0(fpath,"\\", f_eere2), range = fr_cor, na = c("NA", "Na", "na")) %>%
  filter(Sector %in% c("Electric Power"), 
         Activity %in% c("Electricity")) %>%
  select(!c(Index, `End-Use Application`, Sector, Subsector, Activity, `GREET Version`, `GREET Tab`))

d_eere <- d_eere %>%
  filter (Measures %in% c("CO2", "N2O", "CH4")) %>% 
  select(!c(Total)) %>%
  pivot_longer(c("Feedstock", "Fuel"), names_to = "Scope",  values_to = "Value") %>%
  mutate(Scope = if_else(`GREET Pathway` %in% c('Table 9, Wind Power Plant', 
                                        'Table 9, PV Power Plant', 
                                        'Table 9, Geothermal-Flash Power Plant',
                                        'Table 9, Hydroelectric Power Plant'),
                         'Electricity, Supply Chain',
                         if_else(Scope %in% c('Feedstock'), 'Electricity, Supply Chain', 'Electricity, Combustion'))) %>%
  group_by(Measures, `Activity Type`, Scope, `GREET Pathway`) %>%
  summarise(Value = sum(Value)) %>%
  ungroup()

d_eere <- d_eere %>%
  left_join(d_cor, by = c("Activity Type", "Scope")) %>%
  distinct() %>%
  select(!`GREET Pathway.x`) %>%
  rename("GREET Pathway" = "GREET Pathway.y")
write_xlsx(d_eere, paste0(fpath, "\\", "GREET_LCI_Electric.xlsx"))
