"""Independent state construction and attaining measurements for the new claims."""
from fractions import Fraction as F
import math

import numpy as np
import pytest

from dcp_challenge.scientific_revision import (
    one_sample_global_success, refreshed_secret_global_success,
    confidence_frontier, source_score_allowance,
    robust_separable_confidence_bound, fixed_round_source_error_log_bound,
    fourier_pair_states, optimal_frontier_povm,
)


def projector(v):
    return np.outer(v, v.conj())


def original_one_cell_state(n, b):
    """Direct raw DCP mixture; no probability formulas from the implementation."""
    N = 1 << n
    out = np.zeros((2*N, 2*N), dtype=complex)
    for s in range(b, N, 2):
        for x in range(N):
            v = np.zeros(2*N, dtype=complex)
            v[x] = 1/np.sqrt(2)
            v[N + (x+s) % N] = 1/np.sqrt(2)
            out += projector(v) / (N * (N//2))
    return out


def raw_pair_fourier(n, b):
    """Explicit independent raw preparation and subsequent local Fourier unitary."""
    N = 1 << n
    out = np.zeros((4*N*N, 4*N*N), dtype=complex)
    for s in range(b, N, 2):
        for x in range(N):
            for y in range(N):
                for a in range(4):
                    left, right = np.zeros(2*N,complex), np.zeros(2*N,complex)
                    left[x] = right[y] = 1/np.sqrt(2)
                    left[N+(x+s)%N] = right[N+(y+s)%N] = (1j)**a/np.sqrt(2)
                    out += projector(np.kron(left,right)) / (4*(N//2)*N*N)
    fourier = np.exp(2j*np.pi*np.outer(np.arange(N),np.arange(N))/N)/np.sqrt(N)
    U = np.kron(np.kron(np.eye(2),fourier),np.kron(np.eye(2),fourier))
    return U @ out @ U.conj().T


def pt(matrix, d):
    return matrix.reshape(d,d,d,d).transpose(0,3,2,1).reshape(d*d,d*d)


@pytest.mark.parametrize('n', [1,2,3,4,5])
def test_global_single_sample_from_raw_density_matrices(n):
    r0, r1 = original_one_cell_state(n,0), original_one_cell_state(n,1)
    assert np.allclose(r0 @ r1, r1 @ r0, atol=1e-14)
    optimum = .5+.25*np.abs(np.linalg.eigvalsh(r0-r1)).sum()
    assert math.isclose(optimum,float(one_sample_global_success(n)),abs_tol=1e-13)
    # The all-Hadarmard measurement attains the unrestricted trace-norm bound.
    H = np.array([[1,1],[1,-1]])/np.sqrt(2)
    U = H
    for _ in range(n): U = np.kron(U,H)
    measured = .5*np.maximum(np.diag(U@r0@U.T).real,np.diag(U@r1@U.T).real).sum()
    assert math.isclose(measured,optimum,abs_tol=1e-13)


@pytest.mark.parametrize('n,samples', [(1,1),(1,2),(1,3),(2,1),(2,2),(3,2)])
def test_refreshed_secret_no_go_by_tensor_power(n,samples):
    r0,r1 = original_one_cell_state(n,0),original_one_cell_state(n,1)
    a,b = np.ones((1,1)),np.ones((1,1))
    for _ in range(samples): a,b = np.kron(a,r0),np.kron(b,r1)
    optimum = .5+.25*np.abs(np.linalg.eigvalsh(a-b)).sum()
    assert math.isclose(optimum,float(refreshed_secret_global_success(n,samples)),abs_tol=1e-13)
    assert refreshed_secret_global_success(n,0)==F(1,2)


@pytest.mark.parametrize('n', [1,2])
def test_full_pair_model_independent_of_block_formula(n):
    N=1<<n
    ZB=np.kron(np.eye(2*N),np.kron(np.diag([1,-1]),np.eye(N)))
    for b in range(2):
        raw=raw_pair_fourier(n,b)
        for v in (0.,.2,.6,1.):
            noisy=(1+v)/2*raw+(1-v)/2*(ZB@raw@ZB)
            assert np.allclose(noisy,fourier_pair_states(n,v)[b],atol=1e-13)
            assert np.min(np.linalg.eigvalsh(pt(noisy,2*N)))>=-1e-12


@pytest.mark.parametrize('n', [1,2])
@pytest.mark.parametrize('measurement', ['global','separable','ppt','locc'])
def test_attainment_of_entire_rate_frontier(n,measurement):
    N=1<<n
    for q in (F(1,4*N),F(1,2*N),F(3,4*N),F(1,N),F(3,4),F(1)):
        E0,E1,Ep=optimal_frontier_povm(n,q,measurement)
        assert np.allclose(E0+E1+Ep,np.eye(4*N*N),atol=1e-13)
        for E in (E0,E1,Ep):
            assert np.min(np.linalg.eigvalsh(E))>=-1e-12
            if measurement!='global':
                assert np.min(np.linalg.eigvalsh(pt(E,2*N)))>=-1e-12
        for v in (F(0),F(1,4),F(3,5),F(1)):
            r0,r1=fourier_pair_states(n,float(v))
            c=float(np.trace(E0@r0+E1@r1).real/2)
            w=float(np.trace(E1@r0+E0@r1).real/2)
            expected=confidence_frontier(n,q,measurement,v)
            assert math.isclose(c,float(expected.correct),abs_tol=1e-12)
            assert math.isclose(w,float(expected.wrong),abs_tol=1e-12)


def test_exact_ppt_dual_certificates():
    K=np.zeros((4,4)); K[1,2]=K[2,1]=1
    for sign in (-1,1):
        # Unnormalized Bell projectors avoid square-root roundoff.
        psi=np.array([0,1,sign,0]); phi=np.array([1,0,0,sign])
        decomposition=projector(psi)/2+pt(projector(phi)/2,2)
        assert np.array_equal(decomposition,np.eye(4)/2+sign*K)
        for v in (0.,.2,.5,1.):
            sigma0=(np.eye(4)+v*K)/4; sigma1=(np.eye(4)-v*K)/4
            kappa=(2+v)/(2-v)
            if sign==-1: W=kappa*sigma1-sigma0
            else: W=kappa*sigma0-sigma1
            assert np.allclose(W,v/(2-v)*decomposition,atol=1e-15)


def test_global_operator_upper_certificates():
    for n in (1,2):
        for v in (0.,.3,1.):
            r0,r1=fourier_pair_states(n,v)
            R,D=(r0+r1)/2,(r0-r1)/2
            assert np.min(np.linalg.eigvalsh(v*R-D))>=-1e-13
            assert np.min(np.linalg.eigvalsh(v*R+D))>=-1e-13
            assert math.isclose(np.abs(np.linalg.eigvalsh(D)).sum(),v/(2*(1<<n)),abs_tol=1e-13)


def test_frontier_changes_the_scaling_conclusion():
    for n in range(1,12):
        q=F(1,1<<n)
        assert confidence_frontier(n,q,'global')==confidence_frontier(n,q,'separable')
        assert confidence_frontier(n,q/2,'global').confidence==1
        assert confidence_frontier(n,q/2,'separable').confidence==F(3,4)
        assert confidence_frontier(n,F(1),'global').confidence==F(1,2)+F(1,4*(1<<n))


def test_general_source_error_and_finite_round_bound():
    assert source_score_allowance(F(1,100),F(1,100))==F(1,25)
    assert robust_separable_confidence_bound(F(1,4),F(1,100),F(1,100))==F(79,100)
    assert robust_separable_confidence_bound(F(1,100),F(1,100),F(1,100))==1
    assert fixed_round_source_error_log_bound(2500,0,7500,F(1,100),F(1,100))==-55.125
    assert fixed_round_source_error_log_bound(3,1,0)==0


def test_arbitrarily_small_classical_leakage_breaks_uniform_confidence():
    # A source occasionally leaks b in orthogonal, locally readable flag levels.
    # Trace-distance error is epsilon, yet the SEP flag decoder has confidence 1.
    epsilon=0.001
    ideal=fourier_pair_states(1)
    d=4
    embed=np.zeros((d+2,d)); embed[:d,:d]=np.eye(d)
    U=np.kron(embed,embed)
    for b in (0,1):
        base=U@ideal[b]@U.T
        flag=np.zeros(d+2); flag[d+b]=1
        leak=projector(np.kron(flag,flag))
        actual=(1-epsilon)*base+epsilon*leak
        trace_distance=np.abs(np.linalg.eigvalsh(actual-base)).sum()/2
        assert math.isclose(trace_distance,epsilon,abs_tol=1e-13)
        assert math.isclose(np.trace(leak@actual).real,epsilon,abs_tol=1e-13)
        other_flag=np.zeros(d+2); other_flag[d+1-b]=1
        assert abs(np.trace(projector(np.kron(other_flag,other_flag))@actual))<1e-13


@pytest.mark.parametrize('function,args', [
    (one_sample_global_success,(True,)),(one_sample_global_success,(0,)),
    (refreshed_secret_global_success,(1,-1)),(confidence_frontier,(1,0)),
    (confidence_frontier,(1,float('nan'))),(confidence_frontier,(1,F(1),'bogus')),
    (confidence_frontier,(1,F(1),'global',1.01)),
    (robust_separable_confidence_bound,(0,0,0)),
    (source_score_allowance,(-.1,0)),(fixed_round_source_error_log_bound,(0,0,0)),
    (fixed_round_source_error_log_bound,(True,0,0)),
])
def test_revision_input_validation(function,args):
    with pytest.raises(ValueError): function(*args)


def test_common_local_noise_preserves_ideal_separable_bound():
    """Independent amplitude-damping channels, followed by product effects."""
    rho=fourier_pair_states(1)
    def kraus(gamma):
        return [np.kron(np.diag([1,np.sqrt(1-gamma)]),np.eye(2)),
                np.kron(np.array([[0,np.sqrt(gamma)],[0,0]]),np.eye(2))]
    noisy=[]
    for state in rho:
        result=np.zeros_like(state)
        for a in kraus(.27):
            for b in kraus(.55):
                ab=np.kron(a,b);result+=ab@state@ab.conj().T
        noisy.append(result)
    rng=np.random.default_rng(20260907)
    for _ in range(300):
        a=rng.normal(size=4)+1j*rng.normal(size=4)
        b=rng.normal(size=4)+1j*rng.normal(size=4)
        vector=np.kron(a/np.linalg.norm(a),b/np.linalg.norm(b))
        p0,p1=[np.vdot(vector,r@vector).real for r in noisy]
        assert p0<=3*p1+1e-13
        assert p1<=3*p0+1e-13


def test_sequential_completion_bound_by_exact_adaptive_dynamic_program():
    from functools import lru_cache
    from math import comb
    for C in range(1,5):
        for E in range(C+1):
            @lru_cache(None)
            def best(rounds,k,e):
                if k==C: return F(int(e<=E))
                if rounds==0: return F(0)
                choices=[]
                for q in (F(0),F(1,2),F(1)):
                    for error in (F(1,4),F(1,2),F(1)):
                        choices.append((1-q)*best(rounds-1,k,e)+q*(
                            (1-error)*best(rounds-1,k+1,e)+error*best(rounds-1,k+1,e+1)))
                return max(choices)
            bound=sum(F(comb(C,j)*3**(C-j),4**C) for j in range(E+1))
            for R in range(C+3):
                assert best(R,0,0)<=bound
                if R>=C: assert best(R,0,0)==bound
