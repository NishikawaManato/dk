from scipy.stats import norm
import math
mu=10
sigma=3



for j in range (1,11):
    mu=j*10
    mean=0
    a=0
    x=norm.cdf(mu+sigma+1,mu,sigma)-norm.cdf(mu-sigma,mu,sigma)

    for i in range(mu-sigma,mu+sigma+1):
        mean=mean+i*(norm.cdf(i+1,mu,sigma)-norm.cdf(i,mu,sigma))/x
    print("mean:"+str(mean))

    for i in range(mu-sigma,mu+sigma+1):
        a=a+(i*i*(norm.cdf(i+1,mu,sigma)-norm.cdf(i,mu,sigma))/x)

    SD=math.sqrt(a-mean*mean)
    print("SD:"+str(SD))






