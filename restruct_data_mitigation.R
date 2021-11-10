rm(list = ls())

library(tidyverse)
library(readxl)

fpath <- "C:\\Users\\skar\\Box\\saura_self\\EERE\\mitigation scenarios"
fname <- "LDV Decarbonization Assumptions and Results_ANL.xlsx"
frange <- "Scenario Results!A116:Q148"
vehicle_category <- "LDV"

d <- read_excel(paste0(fpath,"\\", fname), range = frange)

colnames(d) <- c('year',
                 sapply(2:as.integer((ncol(d)-1)/2), function (x) paste0(d[1,x],"_", colnames(d)[2])),
                 sapply((as.integer((ncol(d)-1)/2)+1):ncol(d), function (x) paste0(d[1,x],"_", colnames(d)[as.integer((ncol(d)-1)/2)+2])))
d <- d[-1,]                 

d <- d %>% 
  pivot_longer(c(!year), names_to = "cases") %>%
  separate(cases, c('fuel_use', 'vehicle_type'), sep = '_') %>%
  mutate(vehicle_category = vehicle_category)

write_csv(d, paste0(fpath, "\\", 'reshape_vals.csv'))

#############

fpath <- "C:\\Users\\skar\\Box\\saura_self\\EERE\\mitigation scenarios"
fname <- "MDV HDV Decarbonization Assumptions and Results.xlsx"
frange <- "Scenario Results - MDV!B81:J112"
vehicle_category <- "MDV"

d <- read_excel(paste0(fpath,"\\", fname), range = frange)

colnames(d)[1] <- 'year'

d <- d %>% 
  pivot_longer(c(!year), names_to = "cases") %>%
  mutate(vehicle_category = vehicle_category)

write_csv(d, paste0(fpath, "\\", 'reshape_vals.csv'))

#############

fpath <- "C:\\Users\\skar\\Box\\saura_self\\EERE\\mitigation scenarios"
fname <- "MDV HDV Decarbonization Assumptions and Results.xlsx"
frange <- "Scenario Results - HDV!B84:AI116"
vehicle_category <- "HDV"

d <- read_excel(paste0(fpath,"\\", fname), range = frange)

d <- d %>% discard(~all(is.na(.) | . ==""))
d <- d[, -which(d[1,] == "Total")]
d <- d[, - which(d[2,] == 2020)[-1]]

colnames(d) <- c('year',
                 sapply(2:as.integer((ncol(d)-1)/3), function (x) paste0(d[1,x],"_",colnames(d)[2]) ),
                 sapply((as.integer((ncol(d)-1)/3)+1) : (as.integer((ncol(d)-1)/3) * 2), function (x) paste0(d[1, x],"_",colnames((d)[as.integer((ncol(d)-1)/3)+2])) ),
                 sapply((as.integer((ncol(d)-1)/3)*2+1) : ncol(d), function (x) paste0(d[1, x],"_",colnames((d)[as.integer((ncol(d)-1)/3)*2+2])) ))

d <- d[-1,]                 

d <- d %>% 
  pivot_longer(c(!year), names_to = "cases") %>%
  separate(cases, c('fuel_use', 'vehicle_type'), sep = '_') %>%
  mutate(vehicle_category = vehicle_category)

write_csv(d, paste0(fpath, "\\", 'reshape_vals.csv'))