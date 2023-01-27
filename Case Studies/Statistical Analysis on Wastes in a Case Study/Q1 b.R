rm(list = ls()) #reset environment and variables

#import readxl library to read excel files in case there are problems with loading the .RData files
#library("readxl")
#waste_A_data <- readxl("waste_data.xlsx", sheet = "Company A")
#waste_A_data <- readxl("waste_data.xlsx", sheet = "Company B")

#read data
load(file = "wasteAData.RData")
load(file = "wasteBData.RData")

#extract data
plastic_A <- waste_A_data$'total waste from plastic recycling bins'
glass_A <- waste_A_data$'total waste from glass recycling bins'
aluminum_A <- waste_A_data$'total waste from aluminum recycling bins'

plastic_B <- waste_B_data$'total waste from plastic recycling bins'
glass_B <- waste_B_data$'total waste from glass recycling bins'
aluminum_B <- waste_B_data$'total waste from aluminum recycling bins'

#extracts week column for iteration purposes
week_col_A <- waste_A_data$'Week'
week_col_B <- waste_B_data$'Week'

#number of weeks where the data is collected over
no_weeks <- max(week_col_A)

#dataframes to order the data and arrange it
weekly_sorted_waste_A = data.frame( Week = 1:no_weeks, Plastic = numeric(35), Glass = numeric(35), Aluminum = numeric(35) )
weekly_sorted_waste_B = data.frame( Week = 1:no_weeks, Plastic = numeric(35), Glass = numeric(35), Aluminum = numeric(35) )


for (i in 1:length(week_col_A))
{
  week <- week_col_A[i]
  weekly_sorted_waste_A[["Plastic"]][week] <- weekly_sorted_waste_A[["Plastic"]][week] + plastic_A[i]
  weekly_sorted_waste_A[["Glass"]][week] <- weekly_sorted_waste_A[["Glass"]][week] + glass_A[i]
  weekly_sorted_waste_A[["Aluminum"]][week] <- weekly_sorted_waste_A[["Aluminum"]][week] + aluminum_A[i]
}

for (i in 1:length(week_col_B))
{
  week <- week_col_B[i]
  weekly_sorted_waste_B[["Plastic"]][week] <- weekly_sorted_waste_B[["Plastic"]][week] + plastic_B[i]
  weekly_sorted_waste_B[["Glass"]][week] <- weekly_sorted_waste_B[["Glass"]][week] + glass_B[i]
  weekly_sorted_waste_B[["Aluminum"]][week] <- weekly_sorted_waste_B[["Aluminum"]][week] + aluminum_B[i]
}

#Dataframe to better visualize correlation pairs
correlation_frame <- data.frame(Correlation_of = c("Plastic-Glass", "Plastic-Aluminum", "Glass-Aluminum"), 
                                Company_A = numeric(3), Company_B = numeric(3))

#calculate correlation
correlation_frame[["Company_A"]][1] <- cor(weekly_sorted_waste_A[["Plastic"]], weekly_sorted_waste_A[["Glass"]], method = "pearson", use = "complete.obs")
correlation_frame[["Company_A"]][2] <- cor(weekly_sorted_waste_A[["Plastic"]], weekly_sorted_waste_A[["Aluminum"]], method = "pearson", use = "complete.obs")
correlation_frame[["Company_A"]][3] <- cor(weekly_sorted_waste_A[["Glass"]], weekly_sorted_waste_A[["Aluminum"]], method = "pearson", use = "complete.obs")

correlation_frame[["Company_B"]][1] <- cor(weekly_sorted_waste_B[["Plastic"]], weekly_sorted_waste_B[["Glass"]], method = "pearson", use = "complete.obs")
correlation_frame[["Company_B"]][2] <- cor(weekly_sorted_waste_B[["Plastic"]], weekly_sorted_waste_B[["Aluminum"]], method = "pearson", use = "complete.obs")
correlation_frame[["Company_B"]][3] <- cor(weekly_sorted_waste_B[["Glass"]], weekly_sorted_waste_B[["Aluminum"]], method = "pearson", use = "complete.obs")

#print correlation of all combinations of wastes by each company
correlation_frame







