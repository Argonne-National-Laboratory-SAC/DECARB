rm(list = ls())

library(tidyverse)
library(readxl)
library(writexl)

fpath <- "C:\\Users\\skar\\Box\\saura_self\\Proj - EERE Decarbonization"
fname <- "EERE_scenarios_TS_GREET1_all_v2.xlsx"
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
  pivot_wider(c("FINAL_series name", "Fuel Category", "Vehicle Class", 
                "Vehicle", "Metric", "Metric Unit", 
                "Functional Unit", "Year"), 
              names_from = "LC Phase", values_from = BAU) %>%
  mutate(BAU = if_else(is.na(Total), if_else(is.na(Feedstock), 0, Feedstock) +
                           if_else(is.na(Fuel), 0, Fuel) +
                           if_else(is.na(`Vehicle Operation`), 0, `Vehicle Operation`) + 
                           if_else(is.na(WTW), 0, WTW), Total)) %>%
  select(`FINAL_series name`, `Fuel Category`, `Vehicle Class`, 
         Vehicle, Metric, `Metric Unit`, 
         `Functional Unit`, Year,  BAU) %>%
  pivot_wider(c("FINAL_series name", "Fuel Category", "Vehicle Class", 
                  "Vehicle", "Metric Unit", 
                  "Functional Unit", "Year"),
              names_from = "Metric", values_from = BAU) %>%
  mutate(CO2 = if_else(is.na(`CO2 (w/ C in VOC & CO)`), CO2, `CO2 (w/ C in VOC & CO)`)) %>%
  select(!`CO2 (w/ C in VOC & CO)`) %>%
  pivot_longer(!c("FINAL_series name", "Fuel Category", "Vehicle Class", 
                 "Vehicle", "Metric Unit", 
                 "Functional Unit", "Year"),
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
  pivot_wider(c("FINAL_series name", "Fuel Category", "Vehicle Class", 
                "Vehicle", "Metric", "Metric Unit", 
                "Functional Unit", "Year"), 
              names_from = "LC Phase", values_from = Elec0) %>%
  mutate(Elec0 = if_else(is.na(Total), if_else(is.na(Feedstock), 0, Feedstock) +
                         if_else(is.na(Fuel), 0, Fuel) +
                         if_else(is.na(`Vehicle Operation`), 0, `Vehicle Operation`) +
                         if_else(is.na(WTW), 0, WTW), Total)) %>%
  select(`FINAL_series name`, `Fuel Category`, `Vehicle Class`, 
         Vehicle, Metric, `Metric Unit`, 
         `Functional Unit`, Year,  Elec0) %>%
  pivot_wider(c("FINAL_series name", "Fuel Category", "Vehicle Class", 
                "Vehicle", "Metric Unit", 
                "Functional Unit", "Year"),
              names_from = "Metric", values_from = Elec0) %>%
  mutate(CO2 = if_else(is.na(`CO2 (w/ C in VOC & CO)`), CO2, `CO2 (w/ C in VOC & CO)`)) %>%
  select(!`CO2 (w/ C in VOC & CO)`) %>%
  pivot_longer(!c("FINAL_series name", "Fuel Category", "Vehicle Class", 
                  "Vehicle", "Metric Unit", 
                  "Functional Unit", "Year"),
               names_to = "Metric", values_to = "Elec0")

d <- d_bau %>%
  left_join(d_elec0, by = c("FINAL_series name", "Fuel Category", "Vehicle Class",    
                            "Vehicle", "Metric", "Metric Unit",      
                            "Functional Unit",  "Year"))

d_elec <- d %>%
  filter(`Vehicle Class` %in% c("Electricity: Stationary: U.S. Mix")) %>%
  select(Metric, Year, BAU) %>%
  rename(Elec_BAU = BAU)

d <- d %>%
  left_join(d_elec, by = c("Metric",  "Year")) %>%
  mutate(Elec_CI_depend_frac = (BAU - Elec0) / Elec_BAU)

View (d)

write_xlsx(d, paste0(fpath, "\\", 'EERE_scenarios_TS_GREET1_all_summary_v2.xlsx'))
