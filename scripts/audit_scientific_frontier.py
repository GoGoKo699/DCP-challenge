"""Independent raw-state construction + linear programs for the rate frontier.

Run with the optional audit dependency: pip install -e '.[audit]'.
The Bell-diagonal reduction is exact: local Fourier-label dephasing followed by
bilateral Pauli twirling leaves both states invariant and preserves PPT/SEP.
For a Bell-diagonal two-qubit effect with weights e_i, PPT is equivalent to
2 e_i <= sum_j e_j for all i. These constraints apply to all three effects.
This script obtains spectra from raw prepared states, not the frontier formula.
"""
from __future__ import annotations

from fractions import Fraction
import json

import numpy as np
from scipy.optimize import linprog

from dcp_challenge.scientific_revision import confidence_frontier


def raw_state(n, b):
    N = 1 << n
    result = np.zeros((4*N*N,4*N*N),complex)
    for s in range(b,N,2):
        for x in range(N):
            for y in range(N):
                for alpha_index in range(4):
                    a,c = np.zeros(2*N,complex),np.zeros(2*N,complex)
                    a[x]=c[y]=1/np.sqrt(2)
                    a[N+(x+s)%N]=c[N+(y+s)%N]=(1j)**alpha_index/np.sqrt(2)
                    v=np.kron(a,c)
                    result+=np.outer(v,v.conj())/(4*(N//2)*N*N)
    F=np.exp(2j*np.pi*np.outer(np.arange(N),np.arange(N))/N)/np.sqrt(N)
    U=np.kron(np.kron(np.eye(2),F),np.kron(np.eye(2),F))
    return U@result@U.conj().T


def spectra(n, visibility):
    N=1<<n
    bell=np.array([[1,1,0,0],[0,0,1,1],[0,0,1,-1],[1,-1,0,0]])/np.sqrt(2)
    ZB=np.kron(np.eye(2*N),np.kron(np.diag([1,-1]),np.eye(N)))
    out=[]
    for b in range(2):
        r=raw_state(n,b)
        r=(1+visibility)/2*r+(1-visibility)/2*(ZB@r@ZB)
        entries=[]
        for k in range(N):
            for ell in range(N):
                ids=[(a*N+k)*(2*N)+c*N+ell for a in range(2) for c in range(2)]
                block=bell.T@r[np.ix_(ids,ids)]@bell
                if np.max(np.abs(block-np.diag(np.diag(block))))>1e-12:
                    raise AssertionError('Bell reduction failed')
                entries.extend(np.diag(block).real)
        out.append(np.array(entries))
    return out


def optimum(p0,p1,q,ppt):
    D=(p0-p1)/2; R=(p0+p1)/2
    dim=len(D); rows=[]; bounds=[]
    for i in range(dim):
        row=np.zeros(2*dim); row[i]=row[dim+i]=1
        rows.append(row); bounds.append(1.)
    if ppt:
        for start in range(0,dim,4):
            for i in range(start,start+4):
                for b in (0,1):
                    row=np.zeros(2*dim); row[b*dim+start:b*dim+start+4]=-1
                    row[b*dim+i]+=2
                    rows.append(row); bounds.append(0.)
                # The inconclusive effect I-E0-E1 must also be PPT.
                row=np.zeros(2*dim)
                for b in (0,1):
                    row[b*dim+start:b*dim+start+4]=1
                    row[b*dim+i]-=2
                rows.append(row); bounds.append(2.)
    solved=linprog(np.r_[-D,D],A_ub=np.array(rows),b_ub=bounds,
                   A_eq=np.r_[R,R][None,:],b_eq=[float(q)],bounds=(0,1),method='highs')
    if not solved.success: raise AssertionError(solved.message)
    return (float(q)-solved.fun)/2


def main():
    checked=0; worst=0.
    for n in (1,2):
        N=1<<n
        for v in (Fraction(0),Fraction(1,4),Fraction(3,5),Fraction(1)):
            p0,p1=spectra(n,float(v))
            for q in (Fraction(1,4*N),Fraction(1,2*N),Fraction(3,4*N),
                      Fraction(1,N),Fraction(3,4),Fraction(1)):
                for group in ('global','ppt'):
                    actual=optimum(p0,p1,q,group=='ppt')
                    expected=float(confidence_frontier(n,q,group,v).correct)
                    error=abs(actual-expected); worst=max(worst,error)
                    if error>1e-9:
                        raise AssertionError((n,v,q,group,actual,expected))
                    checked+=1
    print(json.dumps({'raw_preparation_linear_programs':checked,
                      'maximum_absolute_correct_probability_error':worst,
                      'status':'passed'},indent=2))


if __name__=='__main__': main()
