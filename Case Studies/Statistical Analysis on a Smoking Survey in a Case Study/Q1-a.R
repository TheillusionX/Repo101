rm(list = ls())

#import readxl library to read excel files
load(file = "RDRData.RData")

#collecting data and setting significance level
participant <- data$Participant
n = length(participant)
alpha = 0.05

#initiating dataFrame of gender vs duration of smoking
Duration_Gender_DF <- data.frame("male" = numeric(5), "Female" = numeric(5))
colnames(Duration_Gender_DF) <- c("Male", "Female")
rownames(Duration_Gender_DF) <- c("0-1", "1-2", "2-3", "3-4", "4+")

#counting observations and placing them in correct category by iterating over all participants
for (i in 1:n)
{
  year <- data$`Duration of Smoking`[i]
  gender <- data$Gender[i]
  
  if (0 <= year && year < 1)
  {
    year_range = "0-1"
  } else if (1 <= year && year < 2)
  {
    year_range = "1-2"
  } else if (2<= year && year <3)
  {
    year_range = "2-3" 
  } else if (3 <= year && year < 4)
  {
    year_range = "3-4"
  } else if (4 <= year)
  {
    year_range = "4+"
  }
  
  Duration_Gender_DF[year_range, gender] <- Duration_Gender_DF[year_range, gender] + 1
}

#initiating dataFrame of EXPECTED gender vs duration of smoking frequencies
#dataFrame is initiated with n in every cell, representing total
Duration_Gender_DF_Expected <- data.frame("male" = rep(n, 5), "Female" = rep(n, 5))
colnames(Duration_Gender_DF_Expected) <- c("Male", "Female")
rownames(Duration_Gender_DF_Expected) <- c("0-1", "1-2", "2-3", "3-4", "4+")

#iterates over all columns
for (i in 1:length(colnames(Duration_Gender_DF)))
{
  #gets column, sums the total, and divides by n
  col = Duration_Gender_DF[, i]
  sum = sum(col)
  p = sum/n
  
  #multiplies the same column in EXPECTED dataFrame by p
  Duration_Gender_DF_Expected[, i] <- Duration_Gender_DF_Expected[, i] * p
}

#same as above but iterates over rows
for (i in 1:length(rownames(Duration_Gender_DF)))
{
  row = Duration_Gender_DF[i, ]
  sum = sum(row)
  p = sum/n
  
  Duration_Gender_DF_Expected[i, ] <- Duration_Gender_DF_Expected[i, ] * p
}

#initializing
chi_0 = 0

for (i in 1:length(colnames(Duration_Gender_DF)))
{
  for (j in 1:length(rownames(Duration_Gender_DF)))
  {
    #calculating observation and expectation
    O <- Duration_Gender_DF[j, i]
    E <- Duration_Gender_DF_Expected[j, i]
    
    #summing up
    chi_0 <- chi_0 + ((O - E) ** 2) / (E ** 2)
  }
}

chi <- qchisq(alpha, df = (length(colnames(Duration_Gender_DF)) - 1) * (length(rownames(Duration_Gender_DF)) - 1), lower.tail = TRUE)
p_chi <- pchisq(chi_0, (length(colnames(Duration_Gender_DF)) - 1) * (length(rownames(Duration_Gender_DF)) - 1), lower.tail = TRUE)

#deletes all iteration variables for easy viewing
rm(year_range, gender, sum, p, O, E, i, j, year, col, row)
