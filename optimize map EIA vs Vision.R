rm(list = ls())

library(tidyverse)
library(readxl)

# EIA data summary

fpath <- "C:\\Users\\skar\\Box\\saura_self\\EERE"
fname <- "EERE Tool_v7.xlsx"
frange <- "EIA AEO!A6:O9988"

d.eia <- read_excel(paste0(fpath,"\\", fname), range = frange)

d.eia <- d.eia %>%
  filter(Sector %in% c("Transportation"),
         `End-Use Application` %in% c("Light-Duty Vehicle", "Commercial Light Trucks", "Freight Trucks"))

d.eia <- d.eia %>%
  group_by(`End-Use Application`, Year, Unit) %>%
  summarise(Total = sum(Value))

d1.eia <- d.eia %>%
  filter(Year %in% c(2020))

# VISION data summary

fpath <- "C:\\Users\\skar\\Box\\saura_self\\EERE\\mitigation scenarios"
fname <- "Mitigation rearrange for LDV MDV HDV.xlsx"
frange <- "Mitigation Table!A5:Q1586"

d.vis <- read_excel(paste0(fpath,"\\", fname), range = frange)

d1.vis <- d.vis %>%
  filter (Year %in% c(2020)) %>%
  select (Subsector, `End-Use Application`, `Value (Trillion BTU)`) %>%
  group_by(Subsector, `End-Use Application`) %>%
  summarise(`Value (Trillion BTU)` = sum (`Value (Trillion BTU)`))


opt_fn <- function (fr1){
  abs(d1.eia$Total[d1.eia$`End-Use Application` == "Light-Duty Vehicle"] * fr1 - 
    d1.vis$`Value (Trillion BTU)`[d1.vis$`End-Use Application` == "Auto"]) +
    
  abs(d1.eia$Total[d1.eia$`End-Use Application` == "Light-Duty Vehicle"] * (1-fr1) +
        d1.eia$Total[d1.eia$`End-Use Application` == "Commercial Light Trucks"] - 
        d1.vis$`Value (Trillion BTU)`[d1.vis$`End-Use Application` == "LT"]) 
}

optim(c(0.5), opt_fn, lower = 0, upper = 1, method = "L-BFGS-B")
# optimal fraction: 0.38395

fr1 =  0.3615
opt_fn(fr1)


# Different equation based approach

# f1 and c are constants, e is error constant

#EIA.LDV = (V.LDV-c) * fr1
#EIA.CLT = (V.LDV-c) * (1-fr)
#EIA.FT = V.MDV + V.HDV + c + e

#c = V.LDV - EIA.CLT / (1-fr)

#e = EIA.FT - (V.MDV + V.HDV + c)
#e = EIA.FT - (V.MDV + V.HDV + (V.LDV - EIA.CLT / (1-fr)) )

EIA.FT <- d1.eia$Total[d1.eia$`End-Use Application` == "Freight Trucks"]
V.MDV <- d1.vis$`Value (Trillion BTU)`[d1.vis$Subsector == "MDV"]
V.HDV <- sum(d1.vis$`Value (Trillion BTU)`[d1.vis$Subsector == "HDV"])
V.LDV <- sum(d1.vis$`Value (Trillion BTU)`[d1.vis$Subsector == "LDV"])
EIA.CLT <- d1.eia$Total[d1.eia$`End-Use Application` == "Commercial Light Trucks"]

opt_fn1 <- function (fr1) {
  abs( EIA.FT - (V.MDV + V.HDV + (V.LDV - EIA.CLT / (1-fr1)) ) )
}
optim(c(0.5), opt_fn1, lower = 0, upper = 0.9999, method = "L-BFGS-B")

# optimal value, fr1 = 0.9418184
fr1 = 0.9418184
opt_fn1(fr1)
# error, 4.060702
# solving for c, c = 1843.303
c = V.LDV - EIA.CLT / (1-fr1)

