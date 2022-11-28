#Copyright © 2022, UChicago Argonne, LLC
#The full description is available in the LICENSE.md file at location:
#    https://github.com/Argonne-National-Laboratory-SAC/DECARB 

rm(list = ls())

library(tidyverse)
library(readxl)

# EIA data summary

fpath <- "C:\\Users\\skar\\Box\\saura_self\\EERE\\mitigation scenarios"
fname <- "Buildings Decarbonization Scenarios.xlsx"
frange <- "Mitigation Table!A5:O1223"

d <- read_excel(paste0(fpath,"\\", fname), range = frange)

d1 <- d %>%
  select(`Mitigation Measure`, Sector, `End-Use Application`, 
           `End-Use Application Detailed`, `Energy Carrier`) %>%
  distinct() 

yrs <- 2020:2050

row_idx <- rep(1:nrow(d1), length(yrs))

d2 <- d1[row_idx,]

d2$Year <- sort( rep(yrs, nrow(d1)) )

d3 <- d2 %>%
  left_join(d, by = c("Mitigation Measure", "Sector", "End-Use Application", 
                      "End-Use Application Detailed", "Energy Carrier", "Year")) %>%
  select("Mitigation Measure", "Sector", "End-Use Application", 
         "End-Use Application Detailed", "Energy Carrier", "Year",
         Unit, Value, `Value (quads)`)

d4 <- d3 %>%
  filter(Year < 2046) %>%
  group_by(`Mitigation Measure`, Sector, `End-Use Application`, `End-Use Application Detailed`,
           `Energy Carrier`, Year) %>%
  mutate(Value_ = if_else((Year %% 5) %in% c(0), Value,
                          Value + ( (Year %% 5) * (as.double(d3[which(d3$`Mitigation Measure` == `Mitigation Measure` &
                                                                        d3$Sector == Sector &
                                                                        d3$`End-Use Application` == `End-Use Application` &
                                                                        d3$`End-Use Application Detailed` == `End-Use Application Detailed` &
                                                                        d3$`Energy Carrier` == `Energy Carrier` &
                                                                        d3$Year == (Year+5)),"Value"]) - 
                                                     as.double(d3[which(d3$`Mitigation Measure` == `Mitigation Measure` &
                                                                          d3$Sector == Sector &
                                                                          d3$`End-Use Application` == `End-Use Application` &
                                                                          d3$`End-Use Application Detailed` == `End-Use Application Detailed` &
                                                                          d3$`Energy Carrier` == `Energy Carrier` &
                                                                          d3$Year == Year),"Value"]) ) / 5) ) )

d4 <- d3 %>%
  group_by(`Mitigation Measure`, Sector, `End-Use Application`, `End-Use Application Detailed`,
           `Energy Carrier`, Year) %>%
  mutate(Value_continuous = if_else((Year %% 5) %in% c(0), Value,
                          as.double(d3[which(d3$`Mitigation Measure` == `Mitigation Measure` &
                                               d3$Sector == Sector &
                                               d3$`End-Use Application` == `End-Use Application` &
                                               d3$`End-Use Application Detailed` == `End-Use Application Detailed` &
                                               d3$`Energy Carrier` == `Energy Carrier` &
                                               d3$Year == (Year - Year %% 5)),"Value"]) + 
                            ( (Year %% 5) * (as.double(d3[which(d3$`Mitigation Measure` == `Mitigation Measure` &
                                                        d3$Sector == Sector &
                                                        d3$`End-Use Application` == `End-Use Application` &
                                                        d3$`End-Use Application Detailed` == `End-Use Application Detailed` &
                                                        d3$`Energy Carrier` == `Energy Carrier` &
                                                        d3$Year == ((Year - Year %% 5) + 5)),"Value"]) - 
                                              as.double(d3[which(d3$`Mitigation Measure` == `Mitigation Measure` &
                                                        d3$Sector == Sector &
                                                        d3$`End-Use Application` == `End-Use Application` &
                                                        d3$`End-Use Application Detailed` == `End-Use Application Detailed` &
                                                        d3$`Energy Carrier` == `Energy Carrier` &
                                                        d3$Year == (Year - Year %% 5)),"Value"]) ) / 5) ),
         `Value (quads)_continuous` = if_else((Year %% 5) %in% c(0), `Value (quads)`,
                          as.double(d3[which(d3$`Mitigation Measure` == `Mitigation Measure` &
                                               d3$Sector == Sector &
                                               d3$`End-Use Application` == `End-Use Application` &
                                               d3$`End-Use Application Detailed` == `End-Use Application Detailed` &
                                               d3$`Energy Carrier` == `Energy Carrier` &
                                               d3$Year == (Year - Year %% 5)),"Value (quads)"]) + 
                            ( (Year %% 5) * (as.double(d3[which(d3$`Mitigation Measure` == `Mitigation Measure` &
                                                                  d3$Sector == Sector &
                                                                  d3$`End-Use Application` == `End-Use Application` &
                                                                  d3$`End-Use Application Detailed` == `End-Use Application Detailed` &
                                                                  d3$`Energy Carrier` == `Energy Carrier` &
                                                                  d3$Year == ((Year - Year %% 5) + 5)),"Value (quads)"]) - 
                                               as.double(d3[which(d3$`Mitigation Measure` == `Mitigation Measure` &
                                                                    d3$Sector == Sector &
                                                                    d3$`End-Use Application` == `End-Use Application` &
                                                                    d3$`End-Use Application Detailed` == `End-Use Application Detailed` &
                                                                    d3$`Energy Carrier` == `Energy Carrier` &
                                                                    d3$Year == (Year - Year %% 5)),"Value (quads)"]) ) / 5) ),
         Unit = "TJ") 

View (d4)

write_csv(d4, paste0(fpath, '\\', 'building_decarb_continuous_years.csv'))


# further analysis, comparing if efficiency + demand flexibility = combined

rm(list = )

fpath <- "C:\\Users\\skar\\Box\\saura_self\\EERE\\mitigation scenarios"
fname <- "Buildings Decarbonization Scenarios.xlsx"
frange <- "Mitigation Table!A5:O1223"
d <- read_excel(paste0(fpath,"\\", fname), range = frange)

d1 <- d %>%
  filter (`Mitigation Measure` %in% c("Scenario 1 - 5% retrofits by 2035: Efficiency + Demand Flexibility",
                                      "Scenario 1 - 5% retrofits by 2035: Fuel Switching",
                                      "Scenario 1 - 5% retrofits by 2035: Combined" )) %>%
  group_by(`Mitigation Measure`, Sector, `End-Use Application`, `Energy Carrier`, Year, Unit) %>%
  summarise(Value = sum(Value),
            `Value (quads)` = sum(`Value (quads)`))

View (d1)

d1 <- d1 %>%
  group_by(`Mitigation Measure`) %>%
  mutate(MM = if_else(`Mitigation Measure` %in% c("Scenario 1 - 5% retrofits by 2035: Combined"), "Combined", "E+DF+FS")) %>%
  group_by(MM, Sector, `End-Use Application`, Year, Unit) %>%
  summarise(Value = sum(Value),
             `Value (quads)` = sum(`Value (quads)`))

d2 <- d1 %>%
  ungroup() %>%
  filter(MM %in% c("Combined")) %>%
  select(!MM)
d3 <- d1 %>%
  ungroup() %>%
  filter(MM %in% c("E+DF+FS")) %>%
  select(!MM)

d4 <- d2 %>% 
  left_join(d3, c("Sector", "End-Use Application", "Year", "Unit")) %>%
  rename("Combined"="Value.x", "E+DF+FS" = "Value.y") %>%
  mutate(`Combined subtr E+DF+FS` = Combined - `E+DF+FS`) %>%
  select(!c(`Value (quads).x`, `Value (quads).y`))
View (d4)

write_csv(d4, paste0(fpath, '\\', 'building_decarb_diff.csv'))

