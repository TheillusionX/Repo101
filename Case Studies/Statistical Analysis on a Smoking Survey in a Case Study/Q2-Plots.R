rm(list = ls())

library(readxl)
library(reshape2)
library(ggplot2)
library(tidyverse)
library(rgl)

#loading data
load(file = "RDRData.RData")

#helper function
numerize <- function(x)
{
    if (x == "Zero")
    {
      return(0)
    } else if (x == "One")
    {
      return(1)
    } else if (x == "Two")
    {
      return(2)
    } else 
    {
      return(3)
    }
}

#extracting data in the form of vectors
lung_cap <- data$`Lung capacity`

participant <- data$Participant
n <- length(participant)

duration_of_smoking <- data$`Duration of Smoking`
informed_or_not <- data$`Warned by Family`
income <- data$`Income in TL`

#creating lists for plotting
capacity_of_warned_smokers <- c()
duration_of_warned_smokers <- c()

capacity_of_non_warned_smokers <- c()
duration_of_non_warned_smokers <- c()


#interaction is found
#lung capacity and duration of smoking grouped by gender
#scatterplot
ggplot(data, aes(x = duration_of_smoking, y = lung_cap * 100, 
                 color = `Gender`)) +
  geom_point() +
  xlab("Duration of Smoking (in years)") +
  ylab("Lung Capacity (in Percent)") +
  ggtitle("Lung Capacity Vs. Duration of Smoking Grouped by Gender") +
  labs(color = "Legend") +
  scale_color_manual(values = c("Male" = "blue", "Female" = "pink"))

#lung capacity and duration of smoking grouped by family awareness
#scatterplot
ggplot(data, aes(x = duration_of_smoking, y = lung_cap * 100, 
                 color = as.character(`Warned by Family`))) +
  geom_point() +
  xlab("Duration of Smoking (in years)") +
  ylab("Lung Capacity (in Percent)") +
  ggtitle("Lung Capacity Vs. Duration of Smoking Grouped by Family Awareness") +
  labs(color = "Legend") +
  scale_color_manual(values = c("1" = "green", "0" = "red"))

#lung capacity and duration of smoking grouped by school awareness
#scatterplot
ggplot(data, aes(x = duration_of_smoking, y = lung_cap * 100, 
                 color = as.character(`Warned in School`))) +
  geom_point() +
  xlab("Duration of Smoking (in years)") +
  ylab("Lung Capacity (in Percent)") +
  ggtitle("Lung Capacity Vs. Duration of Smoking Grouped by School Awareness") +
  labs(color = "Legend") +
  scale_color_manual(values = c("1" = "green", "0" = "red"))

#lung capacity and duration of smoking grouped by anti-tobacco ads viewing
#scatterplot
ggplot(data, aes(x = duration_of_smoking, y = lung_cap * 100, 
                 color = as.character(`Seen anti-tobacco ads`))) +
  geom_point() +
  xlab("Duration of Smoking (in years)") +
  ylab("Lung Capacity (in Percent)") +
  ggtitle("Lung Capacity Vs. Duration of Smoking Grouped by Seeing Anti-tobacco ads") +
  labs(color = "Legend") +
  scale_color_manual(values = c("1" = "green", "0" = "red"))

#lung capacity and duration of smoking grouped by smoking family members
#scatterplot
ggplot(data, aes(x = duration_of_smoking, y = lung_cap * 100, 
                 color = `Smoking Family Members`)) +
  geom_point() +
  xlab("Duration of Smoking (in years)") +
  ylab("Lung Capacity (in Percent)") +
  ggtitle("Lung Capacity Vs. Duration of Smoking Grouped by Smoking Family Members") +
  labs(color = "Legend") +
  scale_color_manual(values = c("Zero" = "black", "One" = "red", "Two" = "green", "More than 3" = "blue"))

#lung capacity and duration of smoking grouped by smoking friends
#scatterplot
ggplot(data, aes(x = duration_of_smoking, y = lung_cap * 100, 
                 color = `Smoking Friends`)) +
  geom_point() +
  xlab("Duration of Smoking (in years)") +
  ylab("Lung Capacity (in Percent)") +
  ggtitle("Lung Capacity Vs. Duration of Smoking Grouped by Smoking Friends") +
  labs(color = "Legend") +
  scale_color_manual(values = c("Zero" = "black", "One" = "red", "Two" = "green", "More than 3" = "blue"))

#lung capacity vs income grouped by gender
#scatterplot
ggplot(data, mapping = aes(x = income, y = lung_cap, color = `Gender`)) +
  geom_point() +
  xlab("Income (in TL)") +
  ylab("Lung Capacity") +
  ggtitle("Lung Capacity Vs. Family Income Grouped by Gender") +
  labs(color = "Legend") +
  scale_color_manual(values = c("Male" = "blue", "Female" = "pink"))

#lung capacity vs income grouped by number of smoking family members
#scatterplot
ggplot(data, mapping = aes(x = income, y = lung_cap, color = `Smoking Family Members`)) +
  geom_point() +
  xlab("Income (in TL)") +
  ylab("Lung Capacity") +
  ggtitle("Lung Capacity Vs. Family Income Grouped by Smoking Family Members") +
  labs(color = "Legend") +
  scale_color_manual(values = c("Zero" = "black", "One" = "red", "Two" = "green", "More than 3" = "blue"))

#lung capacity vs income grouped by number of smoking friends
#scatterplot
ggplot(data, mapping = aes(x = income, y = lung_cap, color = `Smoking Friends`)) +
  geom_point() +
  xlab("Income (in TL)") +
  ylab("Lung Capacity") +
  ggtitle("Lung Capacity Vs. Family Income Grouped by Smoking Friends") +
  labs(color = "Legend") +
  scale_color_manual(values = c("Zero" = "black", "One" = "red", "Two" = "green", "More than 3" = "blue"))

#lung capacity vs income grouped by whether the person was warned by their family or not
#scatterplot
ggplot(data, mapping = aes(x = income, y = lung_cap, color = as.character(`Warned by Family`))) +
  geom_point() +
  xlab("Income (in TL)") +
  ylab("Lung Capacity") +
  ggtitle("Lung Capacity Vs. Family Income Grouped by Family Warning") +
  labs(color = "Legend") +
  scale_color_manual(values = c("1" = "green", "0" = "red"))

#lung capacity vs income grouped by whether the person has seen anti-tobacco ads or not
#scatterplot
ggplot(data, mapping = aes(x = income, y = lung_cap, color = as.character(`Seen anti-tobacco ads`))) +
  geom_point() +
  xlab("Income (in TL)") +
  ylab("Lung Capacity") +
  ggtitle("Lung Capacity Vs. Family Income Grouped by Seeing Anti-tobacco Ads") +
  labs(color = "Legend") +
  scale_color_manual(values = c("1" = "green", "0" = "red"))

#lung capacity vs income grouped by whether the person was warned by their school or not
#scatterplot
ggplot(data, mapping = aes(x = income, y = lung_cap, color = as.character(`Warned in School`))) +
  geom_point() +
  xlab("Income (in TL)") +
  ylab("Lung Capacity") +
  ggtitle("Lung Capacity Vs. Family Income Grouped by School Awareness") +
  labs(color = "Legend") +
  scale_color_manual(values = c("1" = "green", "0" = "red"))

#preparing scatterplot for smoking family members and response
#initializing values
Family_avg <- numeric(4)
length <- numeric(4)
for (i in 1:n)
{
  smoking_family <- data$`Smoking Family Members`[i]
  if (smoking_family == "Zero")
  {
    Family_avg[1] <- Family_avg[1] + lung_cap[i]
    length[1] <- length[1] + 1
  } else if (smoking_family == "One")
  {
    Family_avg[2] <- Family_avg[2] + lung_cap[i]
    length[2] <- length[2] + 1
  } else if (smoking_family == "Two")
  {
    Family_avg[3] <- Family_avg[3] + lung_cap[i]
    length[3] <- length[3] + 1
  } else if (smoking_family == "More than 3")
  {
    Family_avg[4] <- Family_avg[4] + lung_cap[i]
    length[4] <- length[4] + 1
  }
}
#getting avg
Family_avg <- Family_avg/length

#preparing scatterplot for smoking friends and response
#initializing values
Friend_avg <- numeric(4)
length <- numeric(4)
for (i in 1:n)
{
  smoking_family <- data$`Smoking Friends`[i]
  if (smoking_family == "Zero")
  {
    Friend_avg[1] <- Friend_avg[1] + lung_cap[i]
    length[1] <- length[1] + 1
  } else if (smoking_family == "One")
  {
    Friend_avg[2] <- Friend_avg[2] + lung_cap[i]
    length[2] <- length[2] + 1
  } else if (smoking_family == "Two")
  {
    Friend_avg[3] <- Friend_avg[3] + lung_cap[i]
    length[3] <- length[3] + 1
  } else if (smoking_family == "More than 3")
  {
    Friend_avg[4] <- Friend_avg[4] + lung_cap[i]
    length[4] <- length[4] + 1
  }
}

#getting avg
Friend_avg <- Friend_avg/length

#AVERAGE Lung capacity Smoking Family members 
#scatterplot
ggplot(mapping = aes(x = factor(c("Zero", "One", "Two", "More than 3"), levels = c("Zero", "One", "Two", "More than 3")),
                     y = Family_avg * 100,
                     size = 30)) +
  geom_point() +
  theme(legend.position = "none") +
  xlab("Smoking Family Members") +
  ylab("Lung Capacity (in Percent)") +
  ggtitle("Average Lung Capacity Vs Number of Smoking Family Members")


#AVERAGE Lung capacity Smoking Friends
#scatterplot
ggplot(mapping = aes(x = factor(c("Zero", "One", "Two", "More than 3"), levels = c("Zero", "One", "Two", "More than 3")),
                     y = Friend_avg * 100,
                     size = 30)) +
  geom_point() +
  theme(legend.position = "none") +
  xlab("Smoking Friends") +
  ylab("Lung Capacity (in Percent)") +
  ggtitle("Average Lung Capacity Vs Number of Smoking Friends")
  
