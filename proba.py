import numpy as np
import random
import time

def check_list(m):
    '''
    generate a list to check if there is a collision in m cells
    '''
    List=[]
    for i in range(m):
        for j in range(i+1,m):
            List.append([i,j])
    return List

def random_binary(n):
    '''
    generate a random bitstring
    '''
    state=[]
    for i in range(n):
        state.append(random.choice([0,1]))
    return state

def collision(a0,a1):
    '''
    check if two lists a0 and a1 is a collision
    '''
    n=len(a0)
    if np.array_equal(a0[:n-1], a1[:n-1]):
       if a0[-1]!=a1[-1]:
          return 0
       else:
          return 1
    else:
       return 1

def Solve(s,pool_result,List):
    '''
    try to solve with m samples
    '''
    for i in List:
        a0,a1=i
        a=collision(pool_result[a0],pool_result[a1])
        if a==0:
           CNOT=random.choice([0,1])
           '''
           return solution
           '''
           if CNOT==1:
              return s%2,[a0,a1]
           # 0 is measured after CNOT
           else:
              return 2,[a0,a1]
    '''
    no collision
    '''
    return 3,[0,0]

def DCP(s,n,m,t):
    '''
    DCP challenge simulation with bitstring
    '''
    List=check_list(m)
    T=0
    while T<t:
          pool_result=[]
          for i in range(m):
              pool_result.append(random_binary(n))
          T=T+1
          solution=Solve(s,pool_result,List)
          if solution[0]==0:
             return 0
          if solution[0]==1:
             return 1
    return random.choice([0,1])

def k_lower(n,m):
    '''
    calculate k_lower
    '''
    N=2**n
    P=1
    for i in range(m):
        P=P*(N-i)/N
    return P

def k_upper(n,m):
    '''
    calculate k_upper
    '''
    N=2**(n-1)
    P=1
    for i in range(m):
        P=P*(N-i)/N
    return P/2+1/2

def p_upper(n,m,t):
    '''
    calculate p_upper
    '''
    P=k_lower(n,m)
    P=P+1
    P=P/2
    P=P**t
    P=2-P
    P=P/2
    return P

def p_lower(n,m,t):
    '''
    calculate p_lower
    '''
    P=k_upper(n,m)
    P=P+1
    P=P/2
    P=P**t
    P=2-P
    P=P/2
    return P
