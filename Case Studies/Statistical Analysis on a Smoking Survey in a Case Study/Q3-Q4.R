rm(list = ls())

load(file = "RDRData.RData")

library(readxl)
library(reshape2)
library(ggplot2)
library(tidyverse)
library(rgl)

one_zero <- function(x, y) {
  if (x == y) return(1)
  else return(0)
}

n <- length(data$Participant)

x1 <- as.list(data$`Duration of Smoking`)
x2 <- as.list(data$`Income in TL`)
x3 <- map(data$Gender, function(x) {one_zero(x, "Male")})
x4 <- map(data$`Smoking Family Members`, function(x) {one_zero(x, "Zero")})
x5 <- map(data$`Smoking Family Members`, function(x) {one_zero(x, "One")})
x6 <- map(data$`Smoking Family Members`, function(x) {one_zero(x, "Two")})
x7 <- map(data$`Smoking Family Members`, function(x) {one_zero(x, "More than 3")})
x8 <- map(data$`Smoking Friends`, function(x) {one_zero(x, "Zero")})
x9 <- map(data$`Smoking Friends`, function(x) {one_zero(x, "One")})
x10 <- map(data$`Smoking Friends`, function(x) {one_zero(x, "Two")})
x11 <- map(data$`Smoking Friends`, function(x) {one_zero(x, "More than 3")})
x12 <- as.list(data$`Warned by Family`)
x13 <- as.list(data$`Warned in School`)
x14 <- as.list(data$`Seen anti-tobacco ads`)
x15 <- Map("*", x1, x3)

y <- as.list(data$`Lung capacity`)

variables_vector <- list(y, x1, x2, x3, x4, x5, x6, x7, x8, x9, 
                         x10, x11, x12, x13, x14, x15)

regression_DF <- as.data.frame(do.call(cbind, variables_vector))

colnames(regression_DF) <- c("y", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", 
                             "x10", "x11", "x12", "x13", "x14", "x15")

for (i in 1:length(colnames(regression_DF)))
{
  regression_DF[[i]] <- unlist(regression_DF[[i]])
}

regression_DF$sqrt_y <- unlist(map(y, sqrt))

model <- lm(sqrt_y ~ x1 + x10 + x15 + x3 + x12 + x9 + x6 + x5, data = regression_DF)

#all above redefines the model done in Q2-Model

#dataframe with the specifics of the person whose confidence interval will be studied
q3_confidence_int <- data.frame(x1 = 1.65, x2 = 12500,
                                x3 = 1, x4 = 0, x5 = 1, x6 = 0,
                                x7 = 0, x8 = 0, x9 = 0,
                                x10 = 1, x11 = 0, x12 = 1,
                                x13 = 0, x14 = 1, x15 = 1.65)

#performs confidence interval and predicts it
predict(model, newdata = q3_confidence_int, 
        interval = "confidence", level = 0.95)

#dataframe with the specifics of the person whose prediction interval will be studied
q4_confidence_int <- data.frame(x1 = 3.35, x2 = 10350,
                                x3 = 0, x4 = 0, x5 = 0, x6 = 1,
                                x7 = 0, x8 = 0, x9 = 0,
                                x10 = 0, x11 = 1, x12 = 0,
                                x13 = 1, x14 = 1, x15 = 0)

#performs prediction interval
predict(model, newdata = q4_confidence_int,
        interval = "prediction", level = 0.95)