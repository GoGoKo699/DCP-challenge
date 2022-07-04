import numpy as np
import random
import time
import proba
import matplotlib.pyplot as plt
import scipy.stats as stats
from statistics import mean

print('probability of returning 1 and error of each case')

one_a=1+5+2+3+1+1+4+5+1+6
print('one_a',one_a)
total_a=1+98+5+156+2+110+3+141+1+99+135+4+99+5+116+1+111+6+134
print('total_a',total_a)
A=one_a/total_a
print('error_a',A)

one_b=1+3+3+4+1+4+3+2+1+1
print('one_b',one_b)
total_b=1+136+3+104+3+112+4+119+1+123+4+114+3+136+2+109+1+131+1+129
print('total_b',total_b)
B=one_b/total_b
print('error_b',B)

one_c=2+3+3+4+3+3+5+1+1+2
print('one_c',one_c)
total_c=2+118+3+123+3+120+4+144+3+126+3+120+5+118+1+120+1+132+2+125
print('total_c',total_c)
C=one_c/total_c
print('error_c',C)

one_d=3+1+6+1+2+2+3+3+3+6
print('one_d',one_d)
total_d=3+122+1+125+6+127+1+115+2+121+2+124+3+132+3+116+3+140+6+103
print('total_d',total_d)
D=one_d/total_d
print('error_d',D)

one_e=125+104+100+94+136+91+119+98+123+90
print('one_e',one_e)
total_e=125+14+104+10+100+19+94+10+136+17+91+11+119+22+98+14+123+17+90+11
print('total_e',total_e)
E=one_e/total_e
print('error_e',1-E)

one_f=92+90+124+100+129+98+117+103+101+99
print('one_f',one_f)
total_f=92+16+90+7+124+7+100+16+129+14+98+8+117+18+103+11+101+18+99+8
print('total_f',total_f)
F=one_f/total_f
print('error_f',1-F)

one_g=105+109+109+110+99+123+103+110+110+100
print('one_g',one_g)
total_g=105+19+109+9+109+16+110+12+99+7+123+13+103+6+110+9+110+13+100+8
print('total_g',total_g)
G=one_g/total_g
print('error_g',1-G)

one_h=106+96+99+106+130+111+101+120+124+112
print('one_h',one_h)
total_h=106+18+96+12+99+11+106+14+130+23+111+15+101+10+120+21+124+16+112+13
print('total_h',total_h)
H=one_h/total_h
print('error_h',1-H)


def P1(s,x0,x1):
    if s==0 and x0==0 and x1==0:
       return A
    if s==0 and x0==0 and x1==1:
       return B
    if s==0 and x0==1 and x1==0:
       return C
    if s==0 and x0==1 and x1==1:
       return D
    if s==1 and x0==0 and x1==0:
       return E
    if s==1 and x0==0 and x1==1:
       return F
    if s==1 and x0==1 and x1==0:
       return G
    if s==1 and x0==1 and x1==1:
       return H
   
def DCP_IBM(s,t):
    k=0
    while k<t:
          x0=random.choice([0,1])
          x1=random.choice([0,1])
          if x0!=x1:
             CNOT=random.choice([0,1])
             if CNOT==1:
                q=random.random()
                if q<P1(s,x0,x1):
                   return 1
                else:
                   return 0
          k=k+1
    return random.choice([0,1])

def IBM(r,t):
    result=0
    for i in range(r):
        s=random.choice([0,1])
        if DCP_IBM(s,t)==s:
           result=result+1
    return result/r

def bit(r,t):
    result=0
    for i in range(r):
        s=random.choice([0,1])
        if proba.DCP(s,1,2,t)==s:
           result=result+1
    return result/r

r=1000
m=2
n=1
t=3
trial=100
IBM_data=[]
bit_data=[]
for i in range(trial):
    IBM_data.append(IBM(r,t))
    bit_data.append(bit(r,t))

mean_IBM=mean(IBM_data)
sigma_IBM=np.sqrt((1-mean_IBM)/2)/np.sqrt(r)
mean_bit=mean(bit_data)
sigma_bit=np.sqrt((1-mean_bit)/2)/np.sqrt(r)

x = np.linspace(1, 0.5, 100)
plt.figure(figsize=(4.8,3.6))
plt.hist(bit_data,density=True,bins=np.arange(0.5, 1, 0.5/250),align='mid',color='skyblue',alpha =0.8,label=''r'$\mathbf{p}_{clean}$')
plt.plot(x, stats.norm.pdf(x, mean_bit, sigma_bit), color='skyblue')
plt.hist(IBM_data,density=True,bins=np.arange(0.5, 1, 0.5/250),align='mid',color='blueviolet',alpha = 0.8,label=''r'$\mathbf{p}_{IBM}$')
plt.plot(x, stats.norm.pdf(x, mean_IBM, sigma_IBM), color='blueviolet')
plt.xlim(0.5,1)
plt.ylim(0,63)
plt.legend()
plt.title('m=%i'%m+', n=%i'%n+', t=%i'%t+' ,r=%i'%r)
plt.xlabel('Accuracy')
plt.ylabel('Probability distribution')
plt.tight_layout()
plt.savefig('IBM.pdf')
plt.show()
