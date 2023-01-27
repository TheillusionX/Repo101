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

#extract data
plastic_A <- waste_A_data$'total waste from plastic recycling bins'
glass_A <- waste_A_data$'total waste from glass recycling bins'
aluminum_A <- waste_A_data$'total waste from aluminum recycling bins'

non_rec_plastic_A <- waste_A_data$'non-recyclable waste from plastic recycling bins'
non_rec_glass_A <- waste_A_data$'non-recyclable waste from glass recycling bins'
non_rec_aluminum_A <- waste_A_data$'non-recyclable waste from aluminum recycling bins'

plastic_B <- waste_B_data$'total waste from plastic recycling bins'
glass_B <- waste_B_data$'total waste from glass recycling bins'
aluminum_B <- waste_B_data$'total waste from aluminum recycling bins'

non_rec_plastic_B <- waste_B_data$'non-recyclable waste from plastic recycling bins'
non_rec_glass_B <- waste_B_data$'non-recyclable waste from glass recycling bins'
non_rec_aluminum_B <- waste_B_data$'non-recyclable waste from aluminum recycling bins'


#number of weeks
WEEKS <- max(week_col_A)

#initiate data frame to sum up each type of waste to its respective week
waste_type_per_week_A <- data.frame( Waste_Type = c("Total Plastic", "Not recycled Plastic", "Glass", "Not recycled Glass" ,"Aluminum", "Not recycled Aluminum") )
waste_type_per_week_B <- data.frame( Waste_Type = c("Total Plastic", "Not recycled Plastic", "Glass", "Not recycled Glass" ,"Aluminum", "Not recycled Aluminum") )

#initiating data
for (i in 1:WEEKS )
{

  waste_type_per_week_A[[ paste("Week", as.character(i)) ]] <- numeric(6)
  waste_type_per_week_B[[ paste("Week", as.character(i)) ]] <- numeric(6)

}

for (i in 1:length(week_col_A) )
{
  week <- week_col_A[i]
  
  #placing and adding data to the right cell in the dataframe
  waste_type_per_week_A[[ paste("Week", as.character(week)) ]][1] <- waste_type_per_week_A[[ paste("Week", as.character(week)) ]][1] + plastic_A[i]
  waste_type_per_week_A[[ paste("Week", as.character(week)) ]][2] <- waste_type_per_week_A[[ paste("Week", as.character(week)) ]][2] + non_rec_plastic_A[i]
  
  waste_type_per_week_A[[ paste("Week", as.character(week)) ]][3] <- waste_type_per_week_A[[ paste("Week", as.character(week)) ]][3] + glass_A[i]
  waste_type_per_week_A[[ paste("Week", as.character(week)) ]][4] <- waste_type_per_week_A[[ paste("Week", as.character(week)) ]][4] + non_rec_glass_A[i]
  
  waste_type_per_week_A[[ paste("Week", as.character(week)) ]][5] <- waste_type_per_week_A[[ paste("Week", as.character(week)) ]][5] + aluminum_A[i]
  waste_type_per_week_A[[ paste("Week", as.character(week)) ]][6] <- waste_type_per_week_A[[ paste("Week", as.character(week)) ]][6] + non_rec_aluminum_A[i]
}

#repeating the previous steps but for company B
for (i in 1:length(week_col_B) )
{
  week <- week_col_B[i]
  
  waste_type_per_week_B[[ paste("Week", as.character(week)) ]][1] <- waste_type_per_week_B[[ paste("Week", as.character(week)) ]][1] + plastic_B[i]
  waste_type_per_week_B[[ paste("Week", as.character(week)) ]][2] <- waste_type_per_week_B[[ paste("Week", as.character(week)) ]][2] + non_rec_plastic_B[i]
  
  waste_type_per_week_B[[ paste("Week", as.character(week)) ]][3] <- waste_type_per_week_B[[ paste("Week", as.character(week)) ]][3] + glass_B[i]
  waste_type_per_week_B[[ paste("Week", as.character(week)) ]][4] <- waste_type_per_week_B[[ paste("Week", as.character(week)) ]][4] + non_rec_glass_B[i]
  
  waste_type_per_week_B[[ paste("Week", as.character(week)) ]][5] <- waste_type_per_week_B[[ paste("Week", as.character(week)) ]][5] + aluminum_B[i]
  waste_type_per_week_B[[ paste("Week", as.character(week)) ]][6] <- waste_type_per_week_B[[ paste("Week", as.character(week)) ]][6] + non_rec_aluminum_B[i]
}

#initiate data frame to store whether the week was lost or not for each waste type
week_lost_frame_A <- data.frame(Week = 1:WEEKS)
week_lost_frame_B <- data.frame(Week = 1:WEEKS)

for (i in 1:WEEKS) 
{
  #assigning column
  data_col <- waste_type_per_week_A[[ paste("Week", as.character(i)) ]]
  
  #calculating ratios
  plastic_ratio <- data_col[2] / data_col[1]
  glass_ratio <- data_col[4] / data_col[3]
  aluminum_ratio <- data_col[6] / data_col[5]
  
  #calculating whether week was lost or not and placing the result in the dataframe in the form of a boolean
  week_lost_frame_A[["Plastic"]][i] <- plastic_ratio >= 0.2
  week_lost_frame_A[["Glass"]][i] <- glass_ratio >= 0.13
  week_lost_frame_A[["Aluminum"]][i] <- aluminum_ratio >= 0.25
  
  #repeat for company B
  data_col <- waste_type_per_week_B[[ paste("Week", as.character(i)) ]]
  
  plastic_ratio <- data_col[2] / data_col[1]
  glass_ratio <- data_col[4] / data_col[3]
  aluminum_ratio <- data_col[6] / data_col[5]
  
  week_lost_frame_B[["Plastic"]][i] <- plastic_ratio >= 0.2
  week_lost_frame_B[["Glass"]][i] <- glass_ratio >= 0.13
  week_lost_frame_B[["Aluminum"]][i] <- aluminum_ratio >= 0.25
}

#calculating confidence intervals
alpha = 0.05

lost_plastic_A <- week_lost_frame_A[["Plastic"]]
lost_plastic_B <- week_lost_frame_B[["Plastic"]]

n1 <- length(lost_plastic_A)
n2 <- length(lost_plastic_B)

p_A <- sum(lost_plastic_A)/n1
p_B <- sum(lost_plastic_B)/n2

#sample variances for A and B
sam_var_A <- p_A * (1 - p_A) #s1**2
sam_var_B <- p_B * (1 - p_B) #s2**2

z_score <- qnorm(alpha /  2, lower.tail = FALSE)
sigma_pA_pB <- sqrt(  sam_var_A / n1 + sam_var_B / n2 )

bound_lower <- p_A - p_B - z_score * sigma_pA_pB
bound_upper <- p_A - p_B + z_score * sigma_pA_pB

