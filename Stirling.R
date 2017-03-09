strNum = function(n,k){
  #
  strNum = 0
  summation = 0
  loop = c(rep(1:k))
  for (i in loop){
    comb = factorial(k)/(factorial(k-i) * factorial(i))
    temp = ((-1) ^ (k - i)) * comb * (i^n)
    summation = summation + temp
  }
  strNum = (1/factorial(k)) * summation
  return(strNum)
}
Stirling = function(n){
  stirlingNum = 0
  for (k in c(rep(1:10))){
    stirlingNum[k] = strNum(n,k)
  }
  return(stirlingNum)
}
numbers = Stirling(20)
plot(1:10,numbers,main="Stirling Numbers for n = 20 and k = 1 to 10"
     ,xlab="k values", ylab = "Stirling numbers of the second kind",type="b",col = "red")
