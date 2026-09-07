"""Release audit with no imports from dcp_challenge.

Checks unrestricted full-space operator certificates in computational coordinates,
raw-state Helstrom optima, and adversarial finite-horizon stopping by exact dynamic
programming. Numerical checks supplement, and do not replace, the written proofs.
Run: OPENBLAS_NUM_THREADS=1 python scripts/audit_release_science.py
"""
from __future__ import annotations

from fractions import Fraction as F
from functools import lru_cache
from math import comb, exp, log
import json
import numpy as np


def projector(x):
    return np.outer(x, x.conj())


def raw_cell(n, secret, phase=1):
    N = 2**n
    rho = np.zeros((2*N, 2*N), complex)
    for x in range(N):
        ket = np.zeros(2*N, complex)
        ket[x], ket[N + (x+secret) % N] = 1, phase
        rho += projector(ket)/(2*N)
    return rho


def raw_pair(n, parity, visibility):
    N = 2**n
    rho = np.zeros((4*N*N, 4*N*N), complex)
    # The two x labels are independent conditional on s and the common phase.
    for s in range(parity, N, 2):
        for j in range(4):
            cell = raw_cell(n, s, (1j)**j)
            rho += np.kron(cell, cell)/(4*(N//2))
    z = np.kron(np.eye(2*N), np.kron(np.diag([1,-1]), np.eye(N)))
    return (1+visibility)*rho/2 + (1-visibility)*(z@rho@z)/2


def partial_transpose(a, d):
    return a.reshape(d,d,d,d).transpose(0,3,2,1).reshape(d*d,d*d)


def dual_in_raw_basis(n, visibility, sign):
    """P,Q >= 0 for kappa*rho_{1-b}-rho_b = P + Q^Gamma.

    sign=-1 corresponds to kappa*rho_1-rho_0. This certificate constrains
    arbitrary full-cell PPT effects, without presuming their block structure.
    """
    N=2**n
    K=np.zeros((4,4)); K[1,2]=K[2,1]=1
    psi=np.array([0,1,sign,0],complex)
    phi=np.array([1,0,0,sign],complex)
    kappa=(2+visibility)/(2-visibility)
    P=np.zeros((4*N*N,4*N*N),complex); Q=np.zeros_like(P)
    for k in range(N):
        for ell in range(N):
            ids=[(a*N+k)*(2*N)+b*N+ell for a in (0,1) for b in (0,1)]
            if (ell-k)%N==N//2:
                factor=visibility/(2-visibility)/(N*N)
                P[np.ix_(ids,ids)]=factor*projector(psi)/2
                Q[np.ix_(ids,ids)]=factor*projector(phi)/2
            else:
                common=(np.eye(4)+(visibility*K if ell==k else 0))/(4*N*N)
                P[np.ix_(ids,ids)]=(kappa-1)*common
    fourier=np.exp(2j*np.pi*np.outer(np.arange(N),np.arange(N))/N)/np.sqrt(N)
    U=np.kron(np.eye(2),fourier)
    T=np.kron(U.conj().T,U.conj().T)
    S=np.kron(U.conj().T,U.T)
    return T@P@T.conj().T, S@Q@S.conj().T


def check_full_certificates():
    maximum_residual=0.; minimum_eigenvalue=0.; count=0
    for n in (1,2,3):
        for visibility in (0.,.05,.3,.8,1.):
            r0,r1=[raw_pair(n,b,visibility) for b in (0,1)]
            R,D=(r0+r1)/2,(r0-r1)/2
            residual=abs(np.abs(np.linalg.eigvalsh(D)).sum()-visibility/(2*2**n))
            maximum_residual=max(maximum_residual,float(residual))
            for H in (r0,r1,visibility*R+D,visibility*R-D):
                minimum_eigenvalue=min(minimum_eigenvalue,float(np.linalg.eigvalsh(H).min()))
            kappa=(2+visibility)/(2-visibility)
            for sign in (-1,1):
                P,Q=dual_in_raw_basis(n,visibility,sign)
                W=kappa*r1-r0 if sign==-1 else kappa*r0-r1
                maximum_residual=max(maximum_residual,float(np.max(np.abs(W-P-partial_transpose(Q,2*2**n)))))
                minimum_eigenvalue=min(minimum_eigenvalue,float(np.linalg.eigvalsh(P).min()),float(np.linalg.eigvalsh(Q).min()))
                count+=1
    if maximum_residual>1e-11 or minimum_eigenvalue < -1e-11:
        raise AssertionError((maximum_residual,minimum_eigenvalue))
    return {'full_space_ppt_certificates':count,'maximum_operator_residual':maximum_residual,
            'minimum_psd_eigenvalue':minimum_eigenvalue}


def check_helstrom():
    count=0; worst=0.
    for n in (1,2,3,4):
        N=2**n
        pair=[sum((raw_cell(n,s) for s in range(b,N,2)))/(N//2) for b in (0,1)]
        for copies in ((1,2,3) if n<=2 else (1,2) if n==3 else (1,)):
            states=[]
            for cell in pair:
                state=np.ones((1,1),complex)
                for _ in range(copies): state=np.kron(state,cell)
                states.append(state)
            actual=.5+.25*np.abs(np.linalg.eigvalsh(states[0]-states[1])).sum()
            expected=float(1-F(1,2)*F(N-1,N)**copies)
            worst=max(worst,abs(actual-expected));count+=1
    if worst>1e-11: raise AssertionError(worst)
    return {'raw_tensor_power_helstrom_cases':count,'maximum_helstrom_error':float(worst)}


def worst_stopped_acceptance(C,E,R):
    @lru_cache(None)
    def value(rounds,k,e):
        if e>E: return F(0)
        if k==C: return F(1)
        if rounds==0: return F(0)
        abstain=value(rounds-1,k,e)
        right=value(rounds-1,k+1,e)
        wrong=value(rounds-1,k+1,e+1)
        # Vertices of c>=0,w>=0,c+w<=1,c<=3w.
        return max(abstain,wrong,(3*right+wrong)/4)
    return value(R,0,0)


def check_stopping(max_C=12):
    count=0
    for C in range(1,max_C+1):
        for E in range(C+1):
            bound=sum(F(comb(C,j)*3**(C-j),4**C) for j in range(E+1))
            for R in (C-1,C,C+1,C+5):
                actual=worst_stopped_acceptance(C,E,R)
                expected=F(0) if R<C else bound
                if actual!=expected: raise AssertionError((C,E,R,actual,expected))
                count+=1
    return {'exact_adaptive_stopping_cases':count,'all_exact':True}


def check_source_score_mgf():
    count=0; largest_excess=0.
    for beta in (0.,.001,.04,.3,.75,1.):
        for lam in (.001,.05,.3,1.,3.,10.):
            for c,w in ((0.,0.),(0.,1.),(beta,0.),((3+beta)/4,(1-beta)/4)):
                mgf=c*exp(lam*(1-beta))+w*exp(lam*(-3-beta))+(1-c-w)*exp(-lam*beta)
                excess=log(mgf)-2*lam*lam
                largest_excess=max(largest_excess,excess);count+=1
                if excess>1e-12: raise AssertionError((beta,lam,c,w,excess))
    return {'conditional_hoeffding_vertex_checks':count,'maximum_log_bound_excess':largest_excess}


def main():
    out={**check_full_certificates(),**check_helstrom(),**check_stopping(),**check_source_score_mgf(),
         'status':'passed','scope':'independent implementation; not independent peer review'}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__': main()
