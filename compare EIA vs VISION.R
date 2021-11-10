rm(list = ls())

library(tidyverse)
library(readxl)

# EIA data summary

fpath <- "C:\\Users\\skar\\Box\\saura_self\\EERE"
fname <- "EERE Tool_v7.xlsx"
frange <- "EIA AEO!A6:O9988"

d <- read_excel(paste0(fpath,"\\", fname), range = frange)

d <- d %>%
  filter(Sector %in% c("Transportation"),
         `End-Use Application` %in% c("Light-Duty Vehicle", "Commercial Light Trucks", "Freight Trucks"))

d <- d %>%
  group_by(Sector, `End-Use Application`, Year, Unit) %>%
  summarise(Total = sum(Value))

# VISION data summary

fpath <- "C:\\Users\\skar\\Box\\saura_self\\EERE\\mitigation scenarios"
fname <- "Mitigation rearrange for LDV MDV HDV.xlsx"
frange <- "Mitigation Table!A5:Q1586"

d1 <- read_excel(paste0(fpath,"\\", fname), range = frange)

d1 <- d1 %>%
  group_by(Sector, `Vision_to_EIA Subsector_map5`, Year) %>%
  summarise(Total = sum(`Value (Trillion BTU)`)) %>%
  mutate(Unit = 'Trillion Btu')

d2 <- d %>%
  left_join(d1, by = c("Sector", "End-Use Application" = "Vision_to_EIA Subsector_map5", "Year", "Unit"))

d2 <- rename(d2, `EIA estimate` = Total.x, `Vision estimate_map5` = Total.y)

d2 <- d2 %>%
  mutate(EIA_subt_Vision = `Vision estimate_map5` - `EIA estimate`)

write_csv(d2, paste0(fpath, '\\', 'diff_EIA_Vision_map5.csv'))