import numpy as np
import math
from qibo import gates
from qibo.models import Circuit
from qibo.models import QFT
import random
import time

'''
Noise Map
'''
bit_error=0.01
phase_error=0.01
measure_error=0.03

def int_to_bin(x,n):
    '''
    turning an integer x
    into a binary string of length n
    '''
    ibinary=[int(i) for i in str(bin(x))[2:]]
    ibinary=[0]*(n-len(ibinary))+ibinary
    return ibinary

def DCP_samples(n,s,error):
    '''
    Alice: generate a random DCP sample for given s and n
    '''
    x=random.randrange(2**n)
    s=(x+s)%(2**n)
    s_bin=int_to_bin(s,n)
    x_bin=int_to_bin(x,n)
    c = Circuit(n+1)
    c.add(gates.H(0))
    for i in range(1,n+1):
        if s_bin[-i]==x_bin[-i]:
           if s_bin[-i]==1: 
              c.add(gates.X(i))
        else:
           if s_bin[-i]==0:
              c.add(gates.X(i))
              c.add(gates.CNOT(0,i))
           else: 
              c.add(gates.CNOT(0,i))
    '''
    Bob: apply QFT on last n bits then mearue it
    '''
    c.add(QFT(n).on_qubits(*range(n,0,-1)))
    if error==True:
       noise_map = (bit_error, 0.0, phase_error)
       c = c.with_noise(noise_map)
    output=c.add(gates.M(*range(1,n+1),collapse=True))
    result = c()
    a = output.samples()[0]
    b = output.samples(binary=False)[0]
    full_state = result.state()
    state = np.zeros(2, dtype=full_state.dtype)
    state[0], state[1] = full_state[b], full_state[b + 2**n]
    if error==True:
       flip = np.random.random(n) < measure_error
       a=a+(1-2*a)*flip
    '''
    return measurement as a list and the state of the first qubit
    '''
    return a,state

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

def check_list(m):
    '''
    generate a list to check if there is a collision in m cells
    '''
    List=[]
    for i in range(m):
        for j in range(i+1,m):
            List.append([i,j])
    return List

def Solve(pool_result,pool_state,List,error):
    '''
    try to solve with m samples
    '''
    for i in List:
        a0,a1=i
        a=collision(pool_result[a0],pool_result[a1])
        if a==0:
           state0=pool_state[a0]
           state1=pool_state[a1]
           solution=add_CNOT(state0,state1,error)
           '''
           0 is measured after CNOT
           '''
           if solution==2:
              return 2,[a0,a1]
           # return solution
           else: 
              return solution,[a0,a1]
    '''
    no collision
    '''
    return 3,[0,0]

def add_CNOT(state0,state1,error):
    '''
    tensor product of 2 states after collision
    '''
    input_state = np.kron(state0, state1).ravel()
    c = Circuit(2)
    c.add(gates.CNOT(0, 1))
    c.add(gates.H(0))
    if error==True:
       noise_map = (bit_error, 0.0, phase_error)
       c = c.with_noise(noise_map)
    c.add(gates.M(0,1))
    result = c(initial_state=input_state, nshots=1)
    if error==True:
       result.apply_bitflips(measure_error)
    m0,m1 = result.samples()[0]
    '''
    return the result
    '''
    if m1 == 1:
       return m0
    # 0 is measured after CNOT
    else:
       return 2

def DCP(s,n,m,t,error):
    '''
    DCP challenge simulation with circuit
    '''
    List=check_list(m)
    T=0
    while T<t:
          pool_state=[]
          pool_result=[]
          for i in range(m):
              '''
              fill m cells wit m random DCP samples
              '''
              result,state=DCP_samples(n,s,error)
              pool_state.append(state)
              pool_result.append(result)
          T=T+1
          solution=Solve(pool_result,pool_state,List,error)
          if solution[0]==0:
             return 0
          if solution[0]==1:
             return 1
    '''
    guess a random result when can't solve
    '''
    return random.choice([0,1])
