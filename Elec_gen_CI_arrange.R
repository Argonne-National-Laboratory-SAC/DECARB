#Copyright © 2022, UChicago Argonne, LLC
#The full description is available in the LICENSE.md file at location:
#    https://github.com/Argonne-National-Laboratory-SAC/DECARB 

rm(list = ls())

library(tidyverse)
library(readxl)
library(writexl)

fpath <- "C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization"

f_eere <- "EERE Tool_v12.xlsx"
f_hvs <- "GREETheatingValues.xlsx"

f_eere2 <- "EERE Tool_v13.xlsx"

fr_eere <- "GREET Elec Gen CI"
fr_cor <- "Corr_EF_GREET!A4:J542"
fr_hvs <- "mappings_elec_gen"

d_eere <- read_excel(paste0(fpath,"\\", f_eere), sheet = fr_eere, na = c("NA", "Na", "na"))
d_cor <- read_excel(paste0(fpath,"\\", f_eere2), range = fr_cor, na = c("NA", "Na", "na")) %>%
  filter(Sector %in% c("Electric Power"), 
         Activity %in% c("Electricity")) %>%
  select(!c(Index, `End-Use Application`, Sector, Subsector, Activity, `GREET Version`, `GREET Tab`))
d_hvs <- read_excel(paste0(fpath,"\\", f_hvs), sheet = fr_hvs, na = c("NA", "Na", "na", " "))


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
  group_by(Measures, `GREET Pathway`, `Activity Type`, Scope) %>%
  summarise(Value = sum(Value)) %>%
  ungroup()

d_eere <- d_eere %>%
  left_join(d_cor, by = c("Activity Type", "Scope")) %>%
  select(!c("Activity Type", "GREET Pathway.x")) %>%
  distinct() %>%
  rename("GREET Pathway" = "GREET Pathway.y") %>%
  left_join(d_hvs, by = c("GREET Pathway" = "EERE_pathway")) %>%
  select(!c(GREET_Fuel)) %>%
  mutate(LHV_by_HHV = as.numeric(LHV_by_HHV)) %>%
  #group_by(Index) %>%
  mutate(Value_HHV =  if_else(is.na(LHV_by_HHV), Value, Value * LHV_by_HHV))

write_xlsx(d_eere, paste0(fpath, "\\", "GREET_LCI_Electric.xlsx"))
