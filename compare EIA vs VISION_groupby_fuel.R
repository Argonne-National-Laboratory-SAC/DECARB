#Copyright © 2022, UChicago Argonne, LLC
#The full description is available in the LICENSE.md file at location:
#    https://github.com/Argonne-National-Laboratory-SAC/DECARB 

rm(list = ls())

library(tidyverse)
library(readxl)

# EIA data summary

fpath <- "C:\\Users\\skar\\Box\\saura_self\\EERE"
fname <- "EERE Tool_v7.xlsx"
frange <- "EIA AEO!A6:O9988"

d <- read_excel(paste0(fpath,"\\", fname), range = frange)

d <- d %>%
  filter(Sector %in% c("Transportation")) %>%
  filter(`End-Use Application` %in% c('Light-Duty Vehicle', 'Commercial Light Trucks', 'Freight Trucks'))

d <- d %>%
  group_by(Sector, `End-Use Application`, `Energy Carrier`, Year, Unit) %>%
  summarise(Total = sum(Value))
d

# VISION data summary

fpath <- "C:\\Users\\skar\\Box\\saura_self\\EERE\\mitigation scenarios"
fname <- "Mitigation rearrange for LDV MDV HDV.xlsx"
frange <- "Mitigation Table!A5:Q1586"

d1 <- read_excel(paste0(fpath,"\\", fname), range = frange)

d1 <- d1 %>%
  group_by(Sector, `Vision_to_EIA Subsector_map1`, `Energy Carrier`, Year) %>%
  summarise(Total = sum(`Value (Trillion BTU)`)) %>%
  mutate(Unit = 'Trillion Btu')
d1

fuel_lookup <- c("Bio-Diesel" = "Distillate Fuel Oil",
            "Biodiesel" = "Distillate Fuel Oil",
            "CNG" = "Compressed & Liquefied Natural Gas",
            "Diesel" = "Distillate Fuel Oil",
            "Electric" = "Electricity",
            "Electricity" = "Electricity",
            "Ethanol" = "E85",
            "F-T Diesel" = "F-T Diesel",
            "FT Diesel" = "F-T Diesel",
            "Gasoline" = "Motor Gasoline",
            "Hydrogen" = "Hydrogen",
            "LPG" = "Propane",
            "Natural Gas" = "Compressed & Liquefied Natural Gas")

d1 <- d1 %>%
  mutate(`Energy Carrier, by EIA` = fuel_lookup[`Energy Carrier`])
View (d1)

d2 <- d %>%
  right_join(d1, by = c("Sector",
                        "End-Use Application" = "Vision_to_EIA Subsector_map1",
                        "Energy Carrier"  = "Energy Carrier, by EIA",
                        "Year", "Unit"))

d2 <- rename(d2,
             `EIA estimate` = Total.x, 
             `Vision estimate` = Total.y,
             "Energy Carrier, by EIA" = `Energy Carrier`,
             "Energy Carrier, by Vision" = `Energy Carrier.y`)

d2 <- d2 %>% group_by(Sector, `End-Use Application`, `Energy Carrier, by EIA`, Year,
                Unit, `EIA estimate`) %>%
  summarise(`Vision estimate` = sum(`Vision estimate`)) %>%
  ungroup() %>%
  mutate(Vision_subt_EIA = `Vision estimate` - `EIA estimate`,
         "Mitigation Measure" = paste0(`End-Use Application`, " ", "Decarbonization"),
         Subsector = "On-Road",
         `Activity Type` = "Not Specified",
         `Activity Basis` = "Combustion") %>%
  rename("Activity" = "Energy Carrier, by EIA") %>%
  pivot_longer(`EIA estimate`:`Vision_subt_EIA`, names_to = "Case", values_to = "Value") %>%
  select(`Mitigation Measure`, 
         Sector, 
         Subsector, 
         `End-Use Application`, 
         Activity, 
         `Activity Type`,
         `Activity Basis`,
         Case,
         Unit,
         Year,
         Value)

View(d2)

write_csv(d2, paste0(fpath, '\\', 'diff_EIA_Vision_map_byfuel.csv'))

d3 <- d2 %>%
  filter (Case %in% c(Vision_subt_EIA))

ggplot(d2) +
  geom_smooth(aes(Year, Value, color = `Mitigation Measure`)) +
  labs(y = "Vision subtract EIA, Trillion Btu") +
  theme_classic() +
  facet_wrap(~ Case)
