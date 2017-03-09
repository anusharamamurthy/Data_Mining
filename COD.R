hypersphere = function(n){
  volume = 0
  if (n < 0)
    return(0)
  if (n == 0)
    return(1)
  else if (n == 1)
    return (2)
  else
    volume = ((2*(22/7)/n)*hypersphere(n - 2))
  return(volume)
  
}
volume =0
for (i in c(rep(0:20)))
  volume[i+1] = hypersphere(i)
plot(0:20,volume,main="Volume of Hypersphere for n = 0,1,2,...,20",xlab=" dimensions", 
     ylab = "Volume of Hypersphere",type="b",col = "red")