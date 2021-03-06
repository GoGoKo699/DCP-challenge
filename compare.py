import random
import matplotlib.pyplot as plt
import proba
import numpy as np

def compare(n,m,diff):
    t=1
    while t<26:
          if (proba.p_upper(n,m,t)-proba.p_B(n,m,t))>diff:
             return 'good',t,proba.p_B(n,m,t),proba.p_upper(n,m,t)
          t=t+1
    return 'bad',t,proba.p_B(n,m,t),proba.p_upper(n,m,t)

qubits=[]
data=[]
plt.figure(1,figsize=(4,4))
for n in range(2,21):
    for m in range(2,101):
        if (n+1)*m<1601:
           result,t,p_B,p_upper=compare(n,m,0)
           if result=='good':
              plt.plot(n,m,'o',color='steelblue',markersize=1)
              qubits.append((n+1)*m)
              data.append([n,m,t,p_B,p_upper])
           else:
              plt.plot(n,m,'o',color='pink',markersize=1)
index=np.argmin(qubits)
n,m,t,p_B,p_upper=data[index]
print('----------')
print('smallest instance for p_upper-p_B>0')
print('n=',n,',m=',m,',t=',t)
print('total number of qubits=',qubits[index])
print('p_B=',p_B,',p_upper=',p_upper)
plt.xlabel('n')
plt.ylabel('m')
plt.title(''r'small gap $g=0\%$')
plt.tight_layout() 
plt.savefig('small_gap.pdf')

qubits=[]
data=[]
plt.figure(2,figsize=(4,4))
for n in range(2,21):
    for m in range(2,101):
        if (n+1)*m<1601:
           result,t,p_B,p_upper=compare(n,m,0.1)
           if result=='good':
              plt.plot(n,m,'o',color='steelblue',markersize=1)
              qubits.append((n+1)*m)
              data.append([n,m,t,p_B,p_upper])
           else:
              plt.plot(n,m,'o',color='pink',markersize=1)
index=np.argmin(qubits)
n,m,t,p_B,p_upper=data[index]
print('----------')
print('smallest instance for p_upper-p_B>10% with t < 26')
print('n=',n,',m=',m,',t=',t)
print('total number of qubits=',qubits[index])
print('p_B=',p_B,',p_upper=',p_upper)
plt.xlabel('n')
plt.ylabel('m')
plt.title(''r'medium gap $g=10\%$')
plt.tight_layout() 
plt.savefig('mid_gap.pdf')

qubits=[]
data=[]
plt.figure(3,figsize=(4,4))
for n in range(1,21):
    for m in range(2,101):
        if (n+1)*m<1601:
           result,t,p_B,p_upper=compare(n,m,0.25)
           if result=='good':
              plt.plot(n,m,'o',color='steelblue',markersize=1)
              qubits.append((n+1)*m)
              data.append([n,m,t,p_B,p_upper])
           else:
              plt.plot(n,m,'o',color='pink',markersize=1)
index=np.argmin(qubits)
n,m,t,p_B,p_upper=data[index]
print('----------')
print('smallest instance for p_upper-p_B>25% with t < 26')
print('n=',n,',m=',m,',t=',t)
print('total number of qubits=',qubits[index])
print('p_B=',p_B,',p_upper=',p_upper)
plt.xlabel('n')
plt.ylabel('m')
plt.title(''r'big gap $g=25\%$')
plt.tight_layout() 
plt.savefig('big_gap.pdf')
