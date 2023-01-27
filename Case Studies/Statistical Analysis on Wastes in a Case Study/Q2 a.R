rm(list = ls()) #reset environment and variables

#import readxl library to read excel files in case there are problems with loading the .RData files
#library("readxl")
#waste_A_data <- readxl("waste_data.xlsx", sheet = "Company A")
#waste_A_data <- readxl("waste_data.xlsx", sheet = "Company B")

#extract data as list/vector
plastic_A <- waste_A_data$'total waste from plastic recycling bins'
plastic_B <- waste_B_data$'total waste from plastic recycling bins'

glass_A <- waste_A_data$'total waste from glass recycling bins'
glass_B <- waste_B_data$'total waste from glass recycling bins'

#extract data as list/vector
total_A <- waste_A_data$'total waste'
total_B <- waste_B_data$'total waste'

alpha <- 0.05

#Perform statistical inferential analysis
#i will iterate over a list of lists
#each nested list has 3 elements, the first is a description of what is being analyzed
#the second and third element are what are being compared
for (i in list( list("Plastic", plastic_A, plastic_B), 
                list("Glass", glass_A, glass_B), 
                list("Plastic and Glass of COmpany A", plastic_A, glass_A) ) 
     )
{
  #assigning the list elements to variabls to avoid confusion and for simplicity
  waste_type <- i[[1]]
  data_A <- i[[2]]
  data_B <- i[[3]]
  
  n1 <- length(data_A)
  n2 <- length(data_B)
  
  #sample variances for A and B
  sam_var_A <- var(data_A) #s1**2
  sam_var_B <- var(data_B) #s2**2
  
  #ratio of the sample variances A over that of B
  sam_var_ratio <- sam_var_A / sam_var_B
  
  #calculating bounds and f score using qf function
  low_bound <- sam_var_ratio / qf(alpha/2, df1 = n1 - 1, df2 = n2 - 1, lower.tail = FALSE)
  upp_bound <- sam_var_ratio * qf(alpha/2, df1 = n2 - 1, df2 = n1 - 1, lower.tail = FALSE)
  
  print(paste(waste_type, "data variance bounds"))
  print(c(low_bound, upp_bound))
  print("")
  
  #assume variances are identical
  mean_A <- sum(data_A)/35
  mean_B <- sum(data_B)/35
  
  #t score
  t_score <- qt(alpha/2, df = n1 + n2 - 2, lower.tail = FALSE )
  s_p = sqrt( ( (n1-1)*sam_var_A + (n2 - 1)*sam_var_B )/(n1 + n2 - 2) )
  
  low_bound <- mean_A - mean_B - t_score * s_p * sqrt(1/n1 + 1/n2)
  upp_bound <- mean_A - mean_B + t_score * s_p * sqrt(1/n1 + 1/n2)
  
  print(paste(waste_type, "data: Difference of means' bounds, assuming variances are identical"))
  print(c(low_bound, upp_bound))
  print("")
  
  #assuming variances aren't identical
  #calculating degrees of freedom, v
  v = (sam_var_A / n1 + sam_var_B / n2)/( (sam_var_A / n1)**2/(n1 + 1) + (sam_var_B / n2)**2/(n2 + 1)  ) - 2
  t_score <- qt(alpha/2, df = v, lower.tail = FALSE )

  low_bound <- mean_A - mean_B - t_score * sqrt( sam_var_A /n1 + sam_var_B/n2)
  upp_bound <- mean_A - mean_B + t_score * sqrt( sam_var_A /n1 + sam_var_B/n2)
  
  print(paste(waste_type, "data: Difference of means' bounds, assuming variances are not identical"))
  print(c(low_bound, upp_bound))
  print("")
  
  #mean per week per region, since company B manages more regions
  mean_A <- sum(data_A)/length(data_A)
  mean_B <- sum(data_B)/length(data_B)
  
  t_score <- qt(alpha/2, df = n1 + n2 - 2, lower.tail = FALSE )
  s_p = sqrt( ( (n1-1)*sam_var_A + (n2 - 1)*sam_var_B )/(n1 + n2 - 2) )
  
  low_bound <- mean_A - mean_B - t_score * s_p * sqrt(1/n1 + 1/n2)
  upp_bound <- mean_A - mean_B + t_score * s_p * sqrt(1/n1 + 1/n2)
  
  print(paste(waste_type, "data: Difference of means' bounds (mean per week per region), assuming variances are identical"))
  print(c(low_bound, upp_bound))
  print("")
  
  #assuming variances aren't identical
  low_bound <- mean_A - mean_B - t_score * sqrt( sam_var_A /n1 + sam_var_B/n2)
  upp_bound <- mean_A - mean_B + t_score * sqrt( sam_var_A /n1 + sam_var_B/n2)
  
  print(paste(waste_type, "data: Difference of means' bounds (mean per week per region), assuming variances are not identical"))
  print(c(low_bound, upp_bound))
  print("")
}






