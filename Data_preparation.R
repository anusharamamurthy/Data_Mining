##install required packages
#install.packages("RMySQL")
#library(RMySQL)

## Connect to the database
bcdb = dbConnect(MySQL(), user='root', 
                 password='', dbname='mysql', host='127.0.0.1')

##Select everything from data

query = ("SELECT * from BCancerdb")

results = dbGetQuery(bcdb, query)

##select missing values from data

##MySql changed the '?' value to zero as I took each of the domains to be int

missing_scn = ("SELECT SCN from BCancerdb where Bare_Nuclei = 0")

res_missing = dbGetQuery(bcdb, missing_scn)

res_missing$SCN

data_without_missing_vals = ("SELECT * FROM `BCancerDB` WHERE `Bare_Nuclei` != 0")

res_withoutmiss = dbGetQuery(bcdb,data_without_missing_vals)

mean(res_withoutmiss$Bare_Nuclei)

table(as.vector(res_withoutmiss$Bare_Nuclei))

len_res = length(results$Bare_Nuclei)
for (i in c(1:len_res))
  if (results$Bare_Nuclei[i] == 0)
    results$Bare_Nuclei[i] = mean(res_withoutmiss$Bare_Nuclei)

write.csv(results, file = "DeltaFix.csv")

results$Bare_Nuclei

#we see 1 to be the mode
table(as.vector(res_withoutmiss$Bare_Nuclei))

len_res = length(results$Bare_Nuclei)
for (i in c(1:len_res))
  if (results$Bare_Nuclei[i] == 0)
    results$Bare_Nuclei[i] = which.max(table(as.vector(res_withoutmiss$Bare_Nuclei)))

results$Bare_Nuclei

cor(res_withoutmiss$Bare_Nuclei,res_withoutmiss$Clump_Thickness)
cor(res_withoutmiss$Bare_Nuclei,res_withoutmiss$Uni_of_Cell_Size)
cor(res_withoutmiss$Bare_Nuclei,res_withoutmiss$Uni_of_Cell_Shape)
cor(res_withoutmiss$Bare_Nuclei,res_withoutmiss$Marginal_Adhesion)
cor(res_withoutmiss$Bare_Nuclei,res_withoutmiss$Single_Epithelial_Cell_Size)
cor(res_withoutmiss$Bare_Nuclei,res_withoutmiss$Bland_Chromatin)
cor(res_withoutmiss$Bare_Nuclei,res_withoutmiss$Normal_Nucleoli)
cor(res_withoutmiss$Bare_Nuclei,res_withoutmiss$Mitoses)

#highest correlation with Uniformity of Cell shape

query_bn = ("Select Bare_Nuclei, Uni_of_Cell_Shape from BCancerDB where Bare_Nuclei = 0")

res_bn_uns = dbGetQuery(bcdb,query_bn)

res_bn_uns$Bare_Nuclei

#replace missing values of Bare Nuclei with the corresponding values of 
#Uniforminty of Cell Shape

len_res = length(results$Bare_Nuclei)
for (i in c(1:len_res))
  if (results$Bare_Nuclei[i] == 0)
    results$Bare_Nuclei[i] = results$Uni_of_Cell_Shape[i]


#write results to DeltaFix.csv
write.csv(results, file = "DeltaFix.csv")