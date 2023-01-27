rm(list = ls()) #reset environment and variables

#import readxl library to read excel files in case there are problems with loading the .RData files
#library("readxl")
#waste_A_data <- readxl("waste_data.xlsx", sheet = "Company A")
#waste_A_data <- readxl("waste_data.xlsx", sheet = "Company B")

#read data
load(file = "wasteAData.RData")
load(file = "wasteBData.RData")

#extract data in the form of vectors/list
waste_per_week_per_region_A <- waste_A_data$'total waste'
region_A_col <- waste_A_data$Region

waste_per_week_per_region_B <- waste_B_data$'total waste'
region_B_col <- waste_B_data$'Region'

#The amount of regions
REGIONS_A <- 16
REGIONS_B <- 20


#Empty numeric vector, where element 1 represents total waste in region 1, etc.
weekly_regional_avg_A <- numeric(REGIONS_A)
weekly_regional_avg_B <- numeric(REGIONS_B)

#Iterate over every region and add the waste
for ( i in 1:(length(region_A_col)) )
{
  weekly_regional_avg_A[region_A_col[i]] <- weekly_regional_avg_A[region_A_col[i]] + waste_per_week_per_region_A[i]
}

for ( i in 1:(length(region_B_col)) )
{
  weekly_regional_avg_B[region_B_col[i] - 16] <- weekly_regional_avg_B[region_B_col[i] - 16] + waste_per_week_per_region_B[i]
}

#divide to get the mean
weekly_regional_avg_A <- weekly_regional_avg_A/35
weekly_regional_avg_B <- weekly_regional_avg_B/35

#plot
barplot(weekly_regional_avg_A, main = "Weekly Average Waste Per Region Managed by Company A", 
        xlab = "Regions", 
        ylab = expression("Waste in m"^3),
        names.arg = 1:REGIONS_A
        )

barplot(weekly_regional_avg_B, main = "Weekly Average Waste Per Region Managed by Company B", 
        xlab = "Regions", 
        ylab = expression("Waste in m"^3), 
        names.arg = (REGIONS_A + 1):(REGIONS_A + REGIONS_B)
        )

#extract data as vectors
recyclable_A <- waste_A_data$'recyclable waste'
recyclable_B <- waste_B_data$'recyclable waste'

#get weekly workload for recycled waste
weekly_avg_A <- sum(recyclable_A)/35
weekly_avg_B <- sum(recyclable_B)/35

#weekly average of each company, summed over all regions
c(weekly_avg_A, weekly_avg_B)

#average per week per region managed by each company
avg_per_week_per_region_A <- sum(waste_per_week_per_region_A)/length(waste_per_week_per_region_A)
avg_per_week_per_region_B <- sum(waste_per_week_per_region_B)/length(waste_per_week_per_region_B)

recycled_avg_per_week_per_region_A <- sum(recyclable_A)/length(recyclable_A)
recycled_avg_per_week_per_region_B <- sum(recyclable_B)/length(recyclable_B)

#recycling ratio calculation
recycling_ratio_A <- sum(recyclable_A)/sum(waste_per_week_per_region_A)
recycling_ratio_B <- sum(recyclable_B)/sum(waste_per_week_per_region_B)
