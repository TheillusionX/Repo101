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

#turning data into numbers and turning them to lists
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

#initializing regression dataframe to store numerized values
variables_vector <- list(y, x1, x2, x3, x4, x5, x6, x7, x8, x9, 
                         x10, x11, x12, x13, x14, x15)

regression_DF <- as.data.frame(do.call(cbind, variables_vector))

colnames(regression_DF) <- c("y", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", 
                             "x10", "x11", "x12", "x13", "x14", "x15")

#unlisting values, since lm() doesnt take lists
for (i in 1:length(colnames(regression_DF)))
{
  regression_DF[[i]] <- unlist(regression_DF[[i]])
}

#for each iteration, each variable will be added on its own with the variables already present in the model
remaining_vars <- list(x1, x2, x3, x4, x5, x6, x7, x8, x9, 
                         x10, x11, x12, x13, x14, x15)
remaining_var_names <- c("x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", 
           "x10", "x11", "x12", "x13", "x14")

#gets adjusted R2 for every iteration
adj_R_2_list <- c()

shell("cls") 

#starting with no variables
for (i in 1:length(remaining_vars))
{
  name <- remaining_var_names[i]
  m <- lm(y ~ unlist(remaining_vars[i]), data = regression_DF)
  
  
  print("")
  print(paste("Now adding ", name))
  print(anova(m))
}

shell("cls")


# x1 was added
model <- lm(y ~ x1, data = regression_DF)
adj_R_2_list <- c(adj_R_2_list, summary(model)$adj.r.squared)

remaining_vars <- list(x2, x3, x4, x5, x6, x7, x8, x9,
                        x10, x11, x12, x13, x14, x15)

remaining_var_names<- c("x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9",
                        "x10", "x11", "x12", "x13", "x14")

for (i in 1:length(remaining_vars))
{
  name <- remaining_var_names[i]
  m <- lm(y ~ x1 + unlist(remaining_vars[i]), data = regression_DF)

  print("")
  print(paste("Now adding ", name))
  # print(summary(m))
  print(anova(m))
}

# x10 was added
model <- lm(y ~ x1 + x10, data = regression_DF)
adj_R_2_list <- c(adj_R_2_list, summary(model)$adj.r.squared)

remaining_vars <- list(x2, x3, x4, x5, x6, x7, x8, x9,
             x11, x12, x13, x14, x15)
remaining_var_names<- c("x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9",
          "x11", "x12", "x13", "x14", "x15")

shell("cls")

for (i in 1:length(remaining_vars))
{
  name <- remaining_var_names[i]
  m <- lm(y ~ x1 + x10 + unlist(remaining_vars[i]), data = regression_DF)

  print("")
  print(paste("Now adding ", name))
  # print(summary(m))
  print(anova(m))
}

# x15 is to be added
model <- lm(y ~ x1 + x10 + x15, data = regression_DF)
adj_R_2_list <- c(adj_R_2_list, summary(model)$adj.r.squared)

remaining_vars <- list(x2, x3, x4, x5, x6, x7, x8, x9,
             x11, x12, x13, x14)
remaining_var_names<- c("x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9",
          "x11", "x12", "x13", "x14")

shell("cls")

for (i in 1:length(remaining_vars))
{
  name <- remaining_var_names[i]
  m <- lm(y ~ x1 + x10 + x15 + unlist(remaining_vars[i]), data = regression_DF)
  
  print("")
  print(paste("Now adding ", name))
  # print(summary(m))
  print(anova(m))
}

# x3 is to be added
model <- lm(y ~ x1 + x10 + x15 + x3, data = regression_DF)
adj_R_2_list <- c(adj_R_2_list, summary(model)$adj.r.squared)

remaining_vars <- list(x2, x4, x5, x6, x7, x8, x9,
             x11, x12, x13, x14)
remaining_var_names<- c("x2", "x4", "x5", "x6", "x7", "x8", "x9",
          "x11", "x12", "x13", "x14")

shell("cls")

for (i in 1:length(remaining_vars))
{
  name <- remaining_var_names[i]
  m <- lm(y ~ x1 + x10 + x15 + x3 + unlist(remaining_vars[i]), data = regression_DF)
  
  print("")
  print(paste("Now adding ", name))
  # print(summary(m))
  print(anova(m))
}

# x12 is to be added
model <- lm(y ~ x1 + x10 + x15 + x3 + x12, data = regression_DF)
adj_R_2_list <- c(adj_R_2_list, summary(model)$adj.r.squared)

remaining_vars <- list(x2, x4, x5, x6, x7, x8, x9,
             x11, x13, x14)
remaining_var_names<- c("x2", "x4", "x5", "x6", "x7", "x8", "x9",
          "x11", "x13", "x14")

shell("cls")

for (i in 1:length(remaining_vars))
{
  name <- remaining_var_names[i]
  m <- lm(y ~ x1 + x10 + x15 + x3 + x12 + unlist(remaining_vars[i]), data = regression_DF)
  
  print("")
  print(paste("Now adding ", name))
  # print(summary(m))
  print(anova(m))
}

# x9 is to be added
model <- lm(y ~ x1 + x10 + x15 + x3 + x12 + x9, data = regression_DF)
adj_R_2_list <- c(adj_R_2_list, summary(model)$adj.r.squared)

remaining_vars <- list(x2, x4, x5, x6, x7, x8,
             x11, x13, x14)
remaining_var_names<- c("x2", "x4", "x5", "x6", "x7", "x8",
          "x11", "x13", "x14")

shell("cls")

for (i in 1:length(remaining_vars))
{
  name <- remaining_var_names[i]
  m <- lm(y ~ x1 + x10 + x15 + x3 + x12 + x9 + unlist(remaining_vars[i]), data = regression_DF)
  
  print("")
  print(paste("Now adding ", name))
  # print(summary(m))
  print(anova(m))
}

# x6 is to be added
model <- lm(y ~ x1 + x10 + x15 + x3 + x12 + x9 + x6, data = regression_DF)
adj_R_2_list <- c(adj_R_2_list, summary(model)$adj.r.squared)

remaining_vars <- list(x2, x4, x5, x7, x8,
             x11, x13, x14)
remaining_var_names<- c("x2", "x4", "x5", "x7", "x8",
          "x11", "x13", "x14")

shell("cls")

for (i in 1:length(remaining_vars))
{
  name <- remaining_var_names[i]
  m <- lm(y ~ x1 + x10 + x15 + x3 + x12 + x9 + x6 + unlist(remaining_vars[i]), data = regression_DF)
  
  print("")
  print(paste("Now adding ", name))
  # print(summary(m))
  print(anova(m))
}


# x5 is to be added
model <- lm(y ~ x1 + x10 + x15 + x3 + x12 + x9 + x6 + x5, data = regression_DF)
adj_R_2_list <- c(adj_R_2_list, summary(model)$adj.r.squared)

remaining_vars <- list(x2, x4, x7, x8,
             x11, x13, x14)
remaining_var_names<- c("x2", "x4", "x7", "x8",
          "x11", "x13", "x14")

shell("cls")

for (i in 1:length(remaining_vars))
{
  name <- remaining_var_names[i]
  m <- lm(y ~ x1 + x10 + x15 + x3 + x12 + x9 + x6 + x5 + unlist(remaining_vars[i]), data = regression_DF)
  
  print("")
  print(paste("Now adding ", name))
  # print(summary(m))
  print(anova(m))
}

#prints adjusted R2 values
print(adj_R_2_list)

#prints summary of model and the ANOVA table
summary(model)
anova(model)

#gets residuals of model
resids <- resid(model)

#gets z-score of residuals
standardized_resid <- rstandard(model)

#normal probability plot
qqnorm(standardized_resid, ylab = "Standardized Residuals", xlab = "Normal Scores", main = "Normal Probability Plot")

qqline(standardized_resid)

#Residuals vs Fitted value
ggplot(regression_DF, mapping = aes(x = y, y = resids)) +
  geom_point() +
  xlab("Fitted Value") +
  ylab("Residuals") +
  ggtitle("Residuals Vs. Fitted Value") +
  labs(subtitle = "Response is Lung Capacity (over 1)")

#histogram
hist(x = resids, xlab = "Residuals", ylab = "Frequency", main = "Histogram of Residuals")

#Residuals vs observation number
ggplot(mapping = aes(x = data$Participant, y = resids)) +
  geom_point() +
  xlab("Participant Number") +
  ylab("Residuals") +
  ggtitle("Residuals Vs. Participant")

#transforming the response variable to its square root
regression_DF$sqrt_y <- unlist(map(y, sqrt))

#redoing the linear regression model with the square root
model <- lm(sqrt_y ~ x1 + x10 + x15 + x3 + x12 + x9 + x6 + x5, data = regression_DF)

resids <- resid(model)
standardized_resid <- rstandard(model)

#normal probability plot
qqnorm(standardized_resid, ylab = "Standardized Residuals", xlab = "Normal Scores", main = "Normal Probability Plot")

qqline(standardized_resid)

#Residuals vs Fitted value
ggplot(regression_DF, mapping = aes(x = sqrt_y, y = resids)) +
  geom_point() +
  xlab("Fitted Value") +
  ylab("Residuals") +
  ggtitle("Residuals Vs. Fitted Value") +
  labs(subtitle = "Response is Square Root of Lung Capacity (over 1)")

#histogram
hist(x = resids, xlab = "Residuals", ylab = "Frequency", main = "Histogram of Residuals")

#Residuals vs observation number
ggplot(mapping = aes(x = data$Participant, y = resids)) +
  geom_point() +
  xlab("Participant Number") +
  ylab("Residuals") +
  ggtitle("Residuals Vs. Participant")

summary(model)
anova(model)
