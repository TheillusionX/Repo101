rm(list = ls()) #reset environment and variables

#import readxl library to read excel files in case there are problems with loading the .RData files
#library("readxl")
#waste_A_data <- readxl("waste_data.xlsx", sheet = "Company A")
#waste_A_data <- readxl("waste_data.xlsx", sheet = "Company B")

#load data
load(file = "wasteAData.RData")
load(file = "wasteBData.RData")

#extracts week column for iteration purposes
week_col_A <- waste_A_data$'Week'
week_col_B <- waste_B_data$'Week'

#extract data in the form of vectors/lists
region_A_col <- waste_A_data$'Region'
region_B_col <- waste_B_data$'Region'

total_waste_A <- waste_A_data$'total waste'
total_waste_B <- waste_B_data$'total waste'

recycled_A <- waste_A_data$'recyclable waste'
recycled_B <- waste_B_data$'recyclable waste'

non_recycled_A <- total_waste_A - recycled_A
non_recycled_B <- total_waste_B - recycled_B

#The amount of regions
REGIONS_A <- 16
REGIONS_B <- 20

#Weeks
WEEKS <- max(waste_A_data$'Week')

#initiate data frame to store ratios
recycling_ratio_frame <- data.frame(Week = 1:WEEKS)

for (i in 1:length(total_waste_A) )
{
  region <- region_A_col[i]
  week <- week_col_A[i]
  
  recycling_ratio_frame[[ paste("Region", as.character(region)) ]][week] <- non_recycled_A[i] / total_waste_A[i]
}

for (i in 1:length(total_waste_B) )
{
  region <- region_B_col[i]
  week <- week_col_B[i]
  
  recycling_ratio_frame[[ paste("Region", as.character(region)) ]][week] <- non_recycled_B[i] / total_waste_B[i]
}

alpha = 0.05

#initializing data frame to store bounds for easier viewing
bound_frame <- data.frame(Bounds = c("Upper Bound", "Needs awareness-raising campaign") )

campaigns_needed <- 0

for (i in 1:(REGIONS_A + REGIONS_B))
{
  data_col <- apply(recycling_ratio_frame[i + 1], 1, as.numeric)
  n <- length(data_col)
  
  sigma_2 <- var( data_col )
  avg <- mean(data_col)
  
  #variance is unknown, t score will be used for confidence intervals
  t_score <- qt(alpha, df = n - 1, lower.tail = FALSE)
  upper_bound <- avg + t_score * sqrt(sigma_2 / n)
  
  #shorthand function for if else statement
  needs_campaign <- ifelse(upper_bound > 0.18, TRUE, FALSE)
  bound_frame[[ paste("Region", as.character(i)) ]] <- list(upper_bound, needs_campaign )
  
  #counting how many campaigns are needed
  if(needs_campaign) {campaigns_needed <- campaigns_needed + 1}
}

#for city-wide data
city_non_recycled <- c(non_recycled_A, non_recycled_B)
city_total_waste <- c(total_waste_A, total_waste_B)

city_recycling_ratio <- city_non_recycled / city_total_waste

avg <- sum(city_non_recycled) / sum(city_total_waste)
n <- length(city_recycling_ratio)
sigma_2 <- var(city_recycling_ratio)

t_score <- qt(alpha, df = n - 1, lower.tail = FALSE)
city_upper_bound <- avg + t_score * sqrt(sigma_2 / n)











