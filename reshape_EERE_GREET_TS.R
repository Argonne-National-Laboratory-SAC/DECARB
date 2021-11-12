rm(list = ls())

library(tidyverse)
library(readxl)
library(writexl)

fpath <- "C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization"
#fname <- "EERE_scenarios_TS_GREET1_all_v2.xlsx"
fname <- "EERE_scenarios_TS_GREET1_all_v2 - EnergyUsePowerPlantConstMaterial=YES.xlsx"
fr_bau <- "BAU"
fr_elec0 <- "Elec0"

d_bau <- read_excel(paste0(fpath,"\\", fname), sheet = fr_bau, na = c("NA", "Na", "na"))
d_elec0 <- read_excel(paste0(fpath,"\\", fname), sheet = fr_elec0, na = c("NA", "Na", "na"))

d_bau <- d_bau %>%
  select(!c(`Scenario ID`, `TEMP_series name`)) %>%
  filter(`Functional Unit` %in% c("mmbtu"),
         Metric %in% c("CO2 (w/ C in VOC & CO)", "CO2",
                       "CH4", "N2O", "GHGs")) %>%
  pivot_longer(!c("FINAL_series name", "Fuel Category", "Vehicle Class",    
                  "Vehicle", "Metric", "Metric Unit",      
                  "Functional Unit", "LC Phase"),
               names_to = "Year", values_to = "BAU") %>%
  mutate(`LC Phase` = if_else(`LC Phase` %in% c('Feedstock', 'Fuel', 'Conversion', 'WTP'), 'Supply Chain',
                              if_else(`LC Phase` %in% c('Vehicle Operation', 'Combustion', 'PTWa'), 'Direct, Combustion',
                              if_else(`LC Phase` %in% c('WTW', 'WTH'), 'Total', `LC Phase`))) ) %>%
  select(`FINAL_series name`, `Fuel Category`, `Vehicle Class`, 
         Vehicle, Metric, `Metric Unit`, 
         `Functional Unit`, Year, `LC Phase`, BAU) %>%
  group_by(`FINAL_series name`, `Fuel Category`, `Vehicle Class`, 
           Vehicle, Metric, `Metric Unit`, 
           `Functional Unit`, Year, `LC Phase`) %>%
  summarise(BAU = sum(BAU, na.rm = T)) %>%
  ungroup() %>%
  pivot_wider(c("FINAL_series name", "Fuel Category", "Vehicle Class", 
                  "Vehicle", "Metric Unit", 
                  "Functional Unit", "Year", "LC Phase"),
              names_from = "Metric", values_from = BAU) %>%
  mutate(CO2 = if_else(is.na(`CO2 (w/ C in VOC & CO)`), CO2, `CO2 (w/ C in VOC & CO)`)) %>%
  select(!`CO2 (w/ C in VOC & CO)`) %>%
  pivot_longer(!c("FINAL_series name", "Fuel Category", "Vehicle Class", 
                 "Vehicle", "Metric Unit", 
                 "Functional Unit", "Year", "LC Phase"),
               names_to = "Metric", values_to = "BAU")

d_elec0 <- d_elec0 %>%
  select(!c(`Scenario ID`, `TEMP_series name`)) %>%
  filter(`Functional Unit` %in% c("mmbtu"),
         Metric %in% c("CO2 (w/ C in VOC & CO)", "CO2",
                       "CH4", "N2O", "GHGs")) %>%
  pivot_longer(!c("FINAL_series name", "Fuel Category", "Vehicle Class",    
                  "Vehicle", "Metric", "Metric Unit",      
                  "Functional Unit", "LC Phase"),
               names_to = "Year", values_to = "Elec0") %>%
  mutate(`LC Phase` = if_else(`LC Phase` %in% c('Feedstock', 'Fuel', 'Conversion', 'WTP'), 'Supply Chain',
                              if_else(`LC Phase` %in% c('Vehicle Operation', 'Combustion', 'PTWa'), 'Direct, Combustion',
                                      if_else(`LC Phase` %in% c('WTW', 'WTH'), 'Total', `LC Phase`))) ) %>%
  select(`FINAL_series name`, `Fuel Category`, `Vehicle Class`, 
         Vehicle, Metric, `Metric Unit`, 
         `Functional Unit`, Year, `LC Phase`, Elec0) %>%
  group_by(`FINAL_series name`, `Fuel Category`, `Vehicle Class`, 
           Vehicle, Metric, `Metric Unit`, 
           `Functional Unit`, Year, `LC Phase`) %>%
  summarise(Elec0 = sum(Elec0, na.rm = T)) %>%
  ungroup() %>%
  pivot_wider(c("FINAL_series name", "Fuel Category", "Vehicle Class", 
                "Vehicle", "Metric Unit", 
                "Functional Unit", "Year", "LC Phase"),
              names_from = "Metric", values_from = Elec0) %>%
  mutate(CO2 = if_else(is.na(`CO2 (w/ C in VOC & CO)`), CO2, `CO2 (w/ C in VOC & CO)`)) %>%
  select(!`CO2 (w/ C in VOC & CO)`) %>%
  pivot_longer(!c("FINAL_series name", "Fuel Category", "Vehicle Class", 
                  "Vehicle", "Metric Unit", 
                  "Functional Unit", "Year", "LC Phase"),
               names_to = "Metric", values_to = "Elec0")

d <- d_bau %>%
  left_join(d_elec0, by = c("FINAL_series name", "Fuel Category", "Vehicle Class",    
                            "Vehicle", "Metric", "Metric Unit",      
                            "Functional Unit",  "Year", "LC Phase"))

d_elec <- d %>%
  filter(`Vehicle Class` %in% c("Electricity: Stationary: U.S. Mix"),
         `LC Phase` %in% c("Total")) %>%
  select(Metric, Year,  BAU) %>%
  rename(Elec_BAU = BAU)

d <- d %>%
  left_join(d_elec, by = c("Metric",  "Year")) %>%
  mutate(Elec_CI_depend_frac = (BAU - Elec0) / Elec_BAU)

View (d)

#write_xlsx(d, paste0(fpath, "\\", 'EERE_scenarios_TS_GREET1_all_summary_v2.xlsx'))
write_xlsx(d, paste0(fpath, "\\","EERE_scenarios_TS_GREET1_all_summary_v2 - EnergyUsePowerPlantConstMaterial=YES.xlsx"))