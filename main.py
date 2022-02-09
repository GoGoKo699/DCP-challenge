import circuit
import proba
import numpy as np
import argparse
import time
import random
import matplotlib.pyplot as plt
from statistics import mean


def main(m, n, t):
    r=1000
    print('- - - - - starting DCP challenge simulation - - - - -')
    print('Starting an instance with',m,'cells of',n+1,'qubits...')
    print('total number of qubits:',m*(n+1))
    print('number of iterations:',t)
    print('number of repetition:',r)
    print('total number of DCP samples:', m*t*r)
    print('- - - - - - - - - -')
    start_time = time.time()
    '''
    calculate a recommended t
    '''
    p=0.8
    t_estimate=np.log(2-2*p)/(np.log((1+proba.k_lower(n,m))/2))
    print('t is recommended to be greater than:', t_estimate)
    p_upper=proba.p_upper(n,m,t)
    p_lower=proba.p_lower(n,m,t)
    print('p_upper:', p_upper)
    print('p_lower:', p_lower)
    if p_upper>0.8:
       print('p_upper is more than 80%, we are fine.')
    else:
       print('p_upper is less than 80%, please increase t.')
    print('- - - - - - - - - -')

    '''
    simulation with bitstring
    '''
    distribution=[]
    for k in range(100):
        SUM=0
        for i in range(r):
            s=random.randrange(2**n)
            if s%2==proba.DCP(s,n,m,t):
               SUM=SUM+1
        SUM=SUM/r
        distribution.append(SUM)
    p_bit=mean(distribution)
    print('Bitstring simulation probability (p_bit):', p_bit)
    print("--- %s seconds ---" % (time.time() - start_time))
    print('- - - - - - - - - -')

    '''
    simulation with clean circuit
    '''
    SUM=0
    for i in range(r):
        s=random.randrange(2**n)
        if s%2==circuit.DCP(s,n,m,t,False):
           SUM=SUM+1
    p_clean=SUM/r
    print('Circuit simulation probability (p_clean):', p_clean)
    print("--- %s seconds ---" % (time.time() - start_time))
    print('- - - - - - - - - -')

    '''
    simulation with clean circuit
    '''
    SUM=0
    for i in range(r):
        s=random.randrange(2**n)
        if s%2==circuit.DCP(s,n,m,t,True):
           SUM=SUM+1
    p_error=SUM/r
    print('Noisy circuit simulation probability (p_error):', p_error)
    print('Noise: 1% bit error and phase error, 3% measurement error.')
    print("--- %s seconds ---" % (time.time() - start_time))
    plt.figure(figsize=(8,5))
    plt.hist(distribution,density=True,bins=np.arange(0.5, 1, 0.5/500),align='mid',color='deepskyblue',label=''r'$\mathbf{p}_{bit}$')
    plt.axvline(x=p_upper,color='k',linestyle='dashed',label=''r'$p_{upper}$') 
    plt.axvline(x=p_lower,color='gray',linestyle='dashed',label=''r'$p_{lower}$') 
    plt.axvline(x=p_error,color='m',linestyle='dashed',label=''r'$\mathbf{p}_{error}$')
    plt.axvline(x=p_clean,color='b',linestyle='dashed',label=''r'$\mathbf{p}_{clean}$')
    plt.xlim(0.495,1.05)
    plt.legend()
    plt.title('m=%i'%m+', n=%i'%n+', t=%i'%t+' ,r=%i'%r)
    plt.xlabel('Accuracy')
    plt.ylabel('Probability distribution')
    plt.tight_layout()
    plt.savefig('Probability_distribution')
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", default=4, type=int)
    parser.add_argument("--n", default=3, type=int)
    parser.add_argument("--t", default=3, type=int)
    args = vars(parser.parse_args())
    main(**args)
