rm(list = ls())

#import readxl library to read excel files
load(file = "RDRData.RData")

#collecting data and setting significance level
participant <- data$Participant
n = length(participant)
alpha = 0.05

#initiating dataFrame of gender vs duration of smoking
Family_Friend_Smokers_DF <- data.frame("Zero Family Members" = rep(0, 4), 
                                       "One Family Members" = rep(0, 4), 
                                       "Two Family Members" = rep(0, 4), 
                                       "More than 3 Family Members" = rep(0, 4),
                                       check.names = FALSE)
rownames(Family_Friend_Smokers_DF) <- c("Zero Friends", 
                                        "One Friends", 
                                        "Two Friends", 
                                        "More than 3 Friends")

#counting observations and placing them in correct category by iterating over all participants
for (i in 1:n)
{
  family <- data$`Smoking Family Members`[i]
  family <- paste(family, "Family Members")
  
  friend <- data$`Smoking Friends`[i]
  friend <- paste(friend, "Friends")
  
  colnames(Family_Friend_Smokers_DF)
  
  Family_Friend_Smokers_DF[friend, family] <- Family_Friend_Smokers_DF[friend, family] + 1
}

#initiating dataFrame of EXPECTED gender vs duration of smoking frequencies
#dataFrame is initiated with n in every cell, representing total
Family_Friend_Smokers_DF_Expected <- data.frame("Zero Family Members" = rep(n, 4), 
                                                "One Family Members" = rep(n, 4), 
                                                "Two Family Members" = rep(n, 4), 
                                                "More than 3 Family Members" = rep(n, 4),
                                                check.names = FALSE)
rownames(Family_Friend_Smokers_DF_Expected) <- c("Zero Friends", 
                                                 "One Friends", 
                                                 "Two Friends", 
                                                 "More than 3 Friends")

#iterates over all columns
for (i in 1:length(colnames(Family_Friend_Smokers_DF)))
{
  #gets column, sums the total, and divides by n
  col = Family_Friend_Smokers_DF[, i]
  sum = sum(col)
  p = sum/n
  
  #multiplies the same column in EXPECTED dataFrame by p
  Family_Friend_Smokers_DF_Expected[, i] <- Family_Friend_Smokers_DF_Expected[, i] * p
}

#same as above but iterates over rows
for (i in 1:length(rownames(Family_Friend_Smokers_DF)))
{
  row = Family_Friend_Smokers_DF[i, ]
  sum = sum(row)
  p = sum/n
  
  Family_Friend_Smokers_DF_Expected[i, ] <- Family_Friend_Smokers_DF_Expected[i, ] * p
}

chi_0 = 0

for (i in 1:length(colnames(Family_Friend_Smokers_DF)))
{
  for (j in 1:length(rownames(Family_Friend_Smokers_DF)))
  {
    #calculating observation and expectation
    O <- Family_Friend_Smokers_DF[j, i]
    E <- Family_Friend_Smokers_DF_Expected[j, i]
    
    #summing up
    chi_0 <- chi_0 + ((O - E) ** 2) / (E ** 2)
  }
}

chi <- qchisq(alpha, df = (length(colnames(Family_Friend_Smokers_DF)) - 1) * (length(rownames(Family_Friend_Smokers_DF)) - 1), lower.tail = TRUE)
p_chi <- pchisq(chi_0, (length(colnames(Family_Friend_Smokers_DF)) - 1) * (length(rownames(Family_Friend_Smokers_DF)) - 1), lower.tail = TRUE)



#deletes all iteration variables for easy viewing
rm(family, friend, sum, p, O, E, i, j, col, row)
