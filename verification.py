import circuit
import proba
import numpy as np
import argparse
import csv
import time
import random
import matplotlib.pyplot as plt
import scipy.stats as stats
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
    p_B=proba.p_B(n,m,t)
    print('p_upper:', p_upper)
    print('p_B:', p_B)
    if p_upper-p_B>0.1:
       print('difference more than 10%, we are fine.')
    else:
       print('difference less than 10%, we might have a problem.')
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
    sigma_clean=np.sqrt((1-p_clean)/2)/np.sqrt(r)
    print(trial, 'trials, each with',r,'repetitions')
    print('Simulation probability (average p_clean):', p_clean)
    print('sigma_clean:', sigma_clean)
    print("--- %s seconds ---" % (time.time() - start_time))
    print('- - - - - - - - - -')
    distribution_Hbasis=[]
    for k in range(trial):
        SUM=0
        for i in range(r):
            s=random.randrange(2**n)
            if s%2==circuit.DCP_Hbasis(s,n,m,t):
               SUM=SUM+1
        SUM=SUM/r
        distribution_Hbasis.append(SUM)
    p_Hbasis=mean(distribution_Hbasis)
    sigma_Hbasis=np.sqrt((1-p_Hbasis)/2)/np.sqrt(r)
    print(trial, 'trials, each with',r,'repetitions')
    print('Noisy circuit simulation probability (average p_Hbasis):', p_Hbasis)
    print('sigma_Hbasis:', sigma_Hbasis)
    print("--- %s seconds ---" % (time.time() - start_time))
    plt.figure(figsize=(4.8,3.6))
    x = np.linspace(1, 0.5, 100)
    plt.hist(distribution_clean,density=True,bins=np.arange(0.5, 1, 0.5/250),align='mid',color='skyblue',alpha =0.8,label=''r'$\mathbf{p}_{clean}$')
    plt.hist(distribution_Hbasis,density=True,bins=np.arange(0.5, 1, 0.5/250),align='mid',color='forestgreen',alpha =0.8,label=''r'$\mathbf{p}_{Hbasis}$')
    plt.axvline(x=p_upper,color='k',linestyle='dashed',label=''r'$p_{upper}$') 
    plt.axvline(x=p_B,color='k',linestyle='dotted',label=''r'$p_{B}$')
    plt.plot(x, stats.norm.pdf(x, p_clean, sigma_clean), color='skyblue')
    plt.plot(x, stats.norm.pdf(x, p_Hbasis, sigma_Hbasis), color='forestgreen')
    plt.xlim(0.5,1)
    plt.ylim(0,63)
    plt.xlabel('Accuracy')
    plt.ylabel('Probability distribution')
    plt.title('m=%i'%m+' ,n=%i'%n+' ,t=%i'%t+' ,r=1000')
    plt.legend()
    plt.tight_layout()
    plt.savefig('verification.pdf')
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", default=9, type=int)
    parser.add_argument("--n", default=6, type=int)
    parser.add_argument("--t", default=4, type=int)
    args = vars(parser.parse_args())
    main(**args)
