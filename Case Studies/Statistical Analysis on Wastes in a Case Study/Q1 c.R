rm(list = ls()) #reset environment and variables

#import readxl library to read excel files in case there are problems with loading the .RData files
#library("readxl")
#waste_A_data <- readxl("waste_data.xlsx", sheet = "Company A")
#waste_A_data <- readxl("waste_data.xlsx", sheet = "Company B")

#extract data from excel sheets
load(file = "wasteAData.RData")
load(file = "wasteBData.RData")

#extract data as list/vector
plastic_waste_A <- waste_A_data$'total waste from plastic recycling bins'
plastic_waste_B <- waste_B_data$'total waste from plastic recycling bins'

#extract data as list/vector
total_waste_A <- waste_A_data$'total waste'
total_waste_B <- waste_B_data$'total waste'

#extract region column for computational reasons
region_A_col <- waste_A_data$'Region'
region_B_col <- waste_B_data$'Region'

#create data frames to store each type of waste under a specific region
plastic_waste_per_region = data.frame(Week = 1:35, check.names = FALSE)
total_waste_per_region = data.frame(Week = 1:35, check.names = FALSE)

#number of regions
REGIONS_A <- 16
REGIONS_B <- 20

#reads the excel data, and appends the data element under a column named after the region number to
#the data frame
for (j in 1:(REGIONS_A))
{
  #temporary vectors
  tempo_plastic = c()
  tempo_total = c()
  for (i in 1:(length(region_A_col)) )
  {
    if (region_A_col[i] == j)
    {
      tempo_plastic <- c(tempo_plastic, plastic_waste_A[i])
      tempo_total <- c(tempo_total, total_waste_A[i])
    }
  }
  #adds the temporary vectors as columns to the data frames under a column heading named after the region number. i.e.: column
  #heading 1 corresponds to data from region 1
  
  #as.character transforms j to a string
  plastic_waste_per_region[ paste( "Region", as.character(j) ) ] <- tempo_plastic
  total_waste_per_region[ paste( "Region", as.character(j) ) ] <- tempo_total
}

#same iteration but over company B's regions
for (j in (REGIONS_A + 1):(REGIONS_B + REGIONS_A))
{
  tempo_plastic = c()
  tempo_total = c()
  for (i in 1:(length(region_B_col)) )
  {
    if (region_B_col[i] == j)
    {
      tempo_plastic <- c(tempo_plastic, plastic_waste_B[i])
      tempo_total <- c(tempo_total, total_waste_B[i])
    }
  }
  plastic_waste_per_region[ paste( "Region", as.character(j) ) ] <- tempo_plastic
  total_waste_per_region[ paste( "Region", as.character(j) ) ] <- tempo_total
}

for (j in 1:(REGIONS_A + REGIONS_B))
{
  #plots a histogram of the plastic waste in each region, saves it as a JPEG file.
  dataset <- plastic_waste_per_region[[paste("Region", as.character(j))]]
  
  #jpeg(paste("D:/METU/METU 4th Semester/IE266/Homework/CaseStudy1/Q1cPlots/Plastic_plot_Region_", j, ".jpeg", sep = ""), width = 350, height = 350)
  hist(dataset, main = paste("Plastic Waste in Region", j), 
       xlab = expression("Waste in m"^3), 
       ylab = "Frequency", 
       breaks = seq(min(dataset), max(dataset), length.out = 7) 
       )
  #dev.off()
  
  #plots a histogram of the total waste in each region, then saves it as a JPEG file.
  
  dataset <- total_waste_per_region[[paste("Region", as.character(j))]]
  
  #jpeg(paste("D:/METU/METU 4th Semester/IE266/Homework/CaseStudy1/Q1cPlots/Total_plot_Region_", j, ".jpeg", sep = ""), width = 350, height = 350)
  hist(dataset, main = paste("Total Waste in Region", j), 
       xlab = expression("Waste in m"^3), 
       ylab = "Frequency", 
       breaks = seq(min(dataset), max(dataset), length.out = 7)
       )
  
  #dev.off()
}

#plots a histogram of the total waste in all regions managed by company A, then saves it
#jpeg(paste("D:/METU/METU 4th Semester/IE266/Homework/CaseStudy1/Q1cPlots/Grand_total_plot_company_A.jpeg", sep = ""), width = 350, height = 350)
hist(total_waste_A,
     main = "Total Waste in Regions Managed by A",
     xlab = expression("Waste in m"^3), 
     breaks = seq(min(total_waste_A), max(total_waste_A), length.out = 15)
     ) #15 is optimal
#dev.off()

#plots a histogram of the total waste in all regions managed by company B, then saves it
#jpeg(paste("D:/METU/METU 4th Semester/IE266/Homework/CaseStudy1/Q1cPlots/Grand_total_plot_company_B.jpeg", sep = ""), width = 350, height = 350)
hist(total_waste_B, 
     main = "Total Waste in Regions Managed by B",
     xlab = expression("Waste in m"^3), 
     breaks = seq(min(total_waste_B), max(total_waste_B), length.out = 15)
     ) #15 is optimal
#dev.off()


#Plots are already saved as jpeg's to Q1cPlots folder
#NOTE: uncomment the jpeg and dev.off codes to save the plots to the path specified without displaying the plots 