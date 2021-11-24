rm(list = ls())

library(tidyverse)
library(readxl)
library(writexl)

fpath <- "C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization"
#f_elec <- "EERE_scenarios_TS_GREET1_all_summary_v2.xlsx"
f_elec <- "EERE_scenarios_TS_GREET1_all_summary_v2 - EnergyUsePowerPlantConstMaterial=YES.xlsx"
f_hvs <- "GREETheatingValues.xlsx"

f_eere <- "EERE Tool_v12_gzz.xlsx"

fr_elec <- "Sheet1"
fr_eere <- "GREET LCI!A4:J20557"
fr_eere_names <- "Temp_Corr_EF_list"
#fr_eere_elecPower <- "Electric Power"
fr_hvs <- "mappings"

d_elec <- read_excel(paste0(fpath,"\\", f_elec), sheet = fr_elec, na = c("NA", "Na", "na"))
d_eere <- read_excel(paste0(fpath,"\\", f_eere), range = fr_eere, na = c("NA", "Na", "na"))
d_eere_names <- read_excel(paste0(fpath,"\\", f_eere), sheet = fr_eere_names, na = c("NA", "Na", "na")) %>%
  distinct()
d_hvs <- read_excel(paste0(fpath,"\\", f_hvs), sheet = fr_hvs, na = c("NA", "Na", "na", " "))

#d_eere_elecPower <- read_excel(paste0(fpath,"\\", f_eere), sheet = fr_eere_elecPower, skip = 3, na = c("NA", "Na", "na")) %>%
#  filter(Subsector %in% c("Electric Power Sector")) %>%
#  select(Case, `Activity Type`, `Year`, `CO2 CI with T&D loss`,	`CH4 CI with T&D loss`,	`N2O CI with T&D loss`) %>%
#  pivot_longer(c("CO2 CI with T&D loss",	"CH4 CI with T&D loss",	"N2O CI with T&D loss"), values_to = "CI", names_to = "GHG") %>%
#  mutate(GHG = if_else(GHG == "CO2 CI with T&D loss", "CO2", 
#                       if_else(GHG == "CH4 CI with T&D loss", "CH4", 
#                               if_else(GHG == "N2O CI with T&D loss", "N2O", "NA"))))

d_elec <- d_elec %>%
  left_join(d_eere_names, by = c("FINAL_series name" = "AGE Named Range")) %>%
  select(`Unique GREET scenarios`, Metric, Year, `LC Phase`, BAU, Elec0, Elec_CI_depend_frac) %>%
  mutate(Year = as.double(Year))

d_eere <- d_eere %>%
  filter(`Unit (Denominator)` %in% c("MMBtu")) %>%
  select(!Value)

d <- d_eere %>%
  left_join(d_elec, by = c("GREET Pathway" = "Unique GREET scenarios",
                           "Formula" = "Metric", 
                           "Year", 
                          "Scope" = "LC Phase")) %>%
  mutate(BAU = round(BAU, 3), Elec0 = round(Elec0, 3), Elec_CI_depend_frac = round(Elec_CI_depend_frac, 6)) %>%
  distinct() %>%
  left_join(d_hvs, by = c("GREET Pathway" = "EERE_pathway")) %>%
  select(!c(GREET_Fuel)) %>%
  mutate(LHV_by_HHV = as.numeric(LHV_by_HHV)) %>%
  mutate(BAU_HHV =  if_else(is.na(LHV_by_HHV), BAU, BAU * LHV_by_HHV),
         Elec0_HHV = if_else(is.na(LHV_by_HHV), Elec0, Elec0 * LHV_by_HHV))

#write_xlsx(d, paste0(fpath, "\\", 'GREET_LCI_forEEREtool_mmBtu.xlsx'))
write_xlsx(d, paste0(fpath, "\\", 'GREET_LCI_forEEREtool_mmBtu - EnergyUsePowerPlantConstMaterial=YES.xlsx'))

