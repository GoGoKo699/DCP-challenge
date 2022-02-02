import circuit
import proba
import numpy as np
import argparse
import csv
import time
import random
import matplotlib.pyplot as plt
from statistics import mean


def main(m, n, t):
    r=1000
    trial=100
    print('- - - - - starting DCP challenge simulation - - - - -')
    print('Starting an instance with',m,'cells of',n+1,'qubits...')
    print('total number of qubits:',m*(n+1))
    print('number of iterations:',t)
    print('number of repetition:',r)
    print('total number of DCP samples:', m*t*r)
    print('- - - - - - - - - -')
    start_time = time.time()
    p_upper=proba.p_upper(n,m,t)
    p_lower=proba.p_lower(n,m,t)
    print('p_upper:', p_upper)
    print('p_lower:', p_lower)
    if p_upper>0.8:
       print('more than 80%, we are fine.')
    else:
       print('less than 80%, we might have a problem.')
    print('- - - - - - - - - -')
    distribution_clean=[]
    for k in range(trial):
        SUM=0
        for i in range(r):
            s=random.randrange(2**n)
            if s%2==circuit.DCP(s,n,m,t,False):
               SUM=SUM+1
        SUM=SUM/r
        distribution_clean.append(SUM)
    p_clean=mean(distribution_clean)
    print('Simulation probability (p_clean):', p_clean)
    print('100 trials, each with 1000 repetition')
    print("--- %s seconds ---" % (time.time() - start_time))
    print('- - - - - - - - - -')
    distribution_error=[]
    for k in range(trial):
        SUM=0
        for i in range(r):
            s=random.randrange(2**n)
            if s%2==circuit.DCP(s,n,m,t,True):
               SUM=SUM+1
        SUM=SUM/r
        distribution_error.append(SUM)
    p_error=mean(distribution_error)
    print('Noisy circuit simulation probability (p_error):', p_error)
    print('100 trials, each with 1000 repetition')
    print('Noise: 1% bit error and phase error, 3% measurement error.')
    print("--- %s seconds ---" % (time.time() - start_time))
    plt.figure(figsize=(8,5))
    plt.hist(distribution_clean,density=True,bins=np.arange(0.5, 1, 0.5/500),align='mid',color='hotpink',label=''r'$\mathbf{p}_{clean}$')
    plt.hist(distribution_error,density=True,bins=np.arange(0.5, 1, 0.5/500),align='mid',color='c',label=''r'$\mathbf{p}_{error}$')
    plt.axvline(x=p_upper,color='k',linestyle='dashed',label=''r'$p_{upper}$') 
    plt.axvline(x=p_lower,color='gray',linestyle='dashed',label=''r'$p_{lower}$') 
    plt.xlim(0.495,1.05)
    plt.xlabel('Accuracy')
    plt.ylabel('Probability distribution')
    plt.title('m=%i'%m+' ,n=%i'%n+' ,t=%i'%t+' ,r=1000')
    plt.legend()
    plt.tight_layout()
    plt.savefig('Numerical_Simulation.pdf')
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", default=6, type=int)
    parser.add_argument("--n", default=5, type=int)
    parser.add_argument("--t", default=5, type=int)
    args = vars(parser.parse_args())
    main(**args)
