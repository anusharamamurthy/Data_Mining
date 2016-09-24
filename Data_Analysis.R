## Connect to the database
bcdb = dbConnect(MySQL(), user='root', 
                 password='', dbname='mysql', host='127.0.0.1')

##Select everything from data

query1 = ("SELECT Clump_Thickness,Uni_of_Cell_Size,
         Uni_of_Cell_Shape,
         Marginal_Adhesion,
         Single_Epithelial_Cell_Size,
         Bare_Nuclei,
         Bland_Chromatin,
         Normal_Nucleoli,
         Mitoses
         from DeltaFix")

query2 = ("SELECT Clump_Thickness as A2,Uni_of_Cell_Size as A3,
         Uni_of_Cell_Shape as A4,
         Marginal_Adhesion as A5,
         Single_Epithelial_Cell_Size as A6,
         Bare_Nuclei as A7,
         Bland_Chromatin as A8,
         Normal_Nucleoli as A9,
         Mitoses as A10,
         Class as C
         from DeltaFix")

results = dbGetQuery(bcdb, query1)

hist(results$Clump_Thickness, 
     main="Histogram for Clump Thickness", 
     xlab="Clump Thickness", 
     xlim=c(1,10), 
     las=1,#rotating the values printed on the y-axis
     )

hist(results$Uni_of_Cell_Size, 
     main="Histogram for Uniformity of Cell Size", 
     xlab="Uniformity of Cell Size", 
     xlim=c(1,10), 
     las=1,#rotating the values printed on the y-axis
)

hist(results$Uni_of_Cell_Shape, 
     main="Histogram for Uniformity of Cell Shape", 
     xlab="Uniformity of Cell Shape", 
     xlim=c(1,10), 
     las=1,#rotating the values printed on the y-axis
)

hist(results$Marginal_Adhesion, 
     main="Histogram for Marginal Adhesion", 
     xlab="Marginal Adhesion", 
     xlim=c(1,10), 
     las=1,#rotating the values printed on the y-axis
)

hist(results$Single_Epithelial_Cell_Size, 
     main="Histogram for Single Epithelial Cell Size", 
     xlab="Single Epithelial Cell Size", 
     xlim=c(1,10), 
     las=1,#rotating the values printed on the y-axis
)

hist(results$Bare_Nuclei, 
     main="Histogram for Bare Nuclei", 
     xlab="Bare Nuclei", 
     xlim=c(1,10), 
     las=1,#rotating the values printed on the y-axi
)

hist(results$Bland_Chromatin, 
     main="Histogram for Bland Chromatin", 
     xlab="Bland Chromatin", 
     xlim=c(1,10), 
     las=1,#rotating the values printed on the y-axis
)

hist(results$Normal_Nucleoli, 
     main="Histogram for Normal Nucleoli", 
     xlab="Normal Nucleoli", 
     xlim=c(1,10), 
     las=1,#rotating the values printed on the y-axis
)

hist(results$Mitoses, 
     main="Histogram for Mitoses", 
     xlab="Mitoses", 
     xlim=c(1,10), 
     las=1,#rotating the values printed on the y-axis
)

hist(results$Class, 
     main="Histogram for Class", 
     xlab="Class 2 - benign, Class 4 - malignant", 
     xlim=c(1,10), 
     las=1,#rotating the values printed on the y-axis
)


##mean median mode of each column
get_summary = function(colname,attr){
mean_val = mean(attr)
median_val = median(attr)
mode_val = table(as.vector(attr))
var_val = var(attr)
print(paste("Summary of",colname))
print(paste("Mean is:",mean_val))
print(paste("Median is :",median_val))
print(paste("Mode is:",which.max(mode_val)))
print(paste("Variance is",var_val))
}
get_summary("Clump_Thickness",results$Clump_Thickness)
get_summary("Uniformity of Cell Size",results$Uni_of_Cell_Size)
get_summary("Uniformity of Cell Shape",results$Uni_of_Cell_Shape)
get_summary("Marginal_Adhesion",results$Marginal_Adhesion)
get_summary("Single Epithelial Cell Size",results$Single_Epithelial_Cell_Size)
get_summary("Bare_Nuclei",results$Bare_Nuclei)
get_summary("Bland_Chromatin",results$Bland_Chromatin)
get_summary("Normal_Nucleoli",results$Normal_Nucleoli)
get_summary("Mitoses",results$Mitoses)
get_summary("Class",results$Class)

corvalues = cor(results,use = "pairwise.complete.obs")

corvalues

query_rs = ("SELECT Clump_Thickness as A2,
          Uni_of_Cell_Size as A3,
          Marginal_Adhesion as A5,
          Single_Epithelial_Cell_Size as A6,
          Bare_Nuclei as A7,
          Bland_Chromatin as A8,
          Normal_Nucleoli as A9,
          Mitoses as A10,
          Class as C
          from DeltaFix")

results = dbGetQuery(bcdb, query_rs)

write.csv(results, row.names = TRUE,file = "Delta2Clean.csv")
      