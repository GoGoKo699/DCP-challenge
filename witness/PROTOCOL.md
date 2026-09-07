# Protocol Specification

**Source assumptions matter.** The conclusive-count test below applies to the ideal source and common secret-independent separable source channels. For unrestricted calibrated preparation errors, use the [adjusted fixed-total-round score test](../correction/SCIENTIFIC_REVISION_2026_09.md), not the unmodified one-quarter-error binomial rule. The same revision gives the exact population confidence-versus-answer-rate frontier.

Let $N=2^n$. Each round uses fresh independent randomness.

## Trusted preparation

The verifier chooses:

- a uniform parity bit $b\in\{0,1\}$;
- a uniform secret $s\in\mathbb Z_N$ subject to $s\bmod2=b$;
- independent uniform $x_1,x_2\in\mathbb Z_N$;
- a shared hidden phase
  $$
  \alpha\in\{0,\pi/2,\pi,3\pi/2\}
  $$
  chosen uniformly.

She prepares two cells

$$
|\psi^{(\alpha)}_{x_j,s}\rangle
=
\frac{|0\rangle|x_j\rangle
+e^{i\alpha}|1\rangle|x_j+s\bmod N\rangle}{\sqrt2},
\qquad j=1,2.
$$

The verifier supplies quantum states, not a classical circuit description revealing $s$ or $\alpha$.

## Honest measurement

The prover:

1. applies $F_N$ to each rotation register;
2. measures the Fourier labels $k_1,k_2$;
3. returns $\perp$ unless
   $$
   k_2-k_1\equiv N/2\pmod N;
   $$
4. Bell-measures the two reflection qubits;
5. returns
   $$
   \Psi^+\mapsto0,
   \qquad
   \Psi^-\mapsto1,
   $$
   and returns $\perp$ on the remaining Bell outcomes.

All measurements may be deferred to the end of the circuit.

## Single-round linear score

Assign

$$
Z=
\begin{cases}
+1,&\text{correct conclusive answer},\\
-3,&\text{wrong conclusive answer},\\
0,&\text{inconclusive answer}.
\end{cases}
$$

Every separable POVM in the single-round null class satisfies

$$
\mathbb E[Z]\le0,
$$

whereas the ideal honest strategy satisfies

$$
\mathbb E[Z]=\frac1{2N}.
$$

## Sequential null class

For repeated rounds, the prover may be adaptive but must remain within separable processing across the cell partition:

- the initial persistent memory is separable across the two sides;
- every round uses a separable instrument, including any LOCC instrument, on the fresh cells and persistent memory;
- the prover may use arbitrary local ancillas, classical communication, and all preceding public history;
- the prover outputs $0$, $1$, or $\perp$ before receiving the next pair.

This condition preserves separability of the conditional memory and makes the one-round $1/4$ error bound applicable after every history.

## Predeclared conclusive-outcome test

Before the experiment, choose integers

$$
C\ge1,
\qquad
0\le E\le C,
\qquad
R\ge C.
$$

Run fresh sequential rounds until either:

- $C$ conclusive answers have been received; or
- $R$ total rounds have been used.

The decision rule is:

1. if fewer than $C$ conclusive answers occur by round $R$, issue **no certificate**;
2. otherwise, accept only if at most $E$ of the first $C$ conclusive answers are wrong.

Under the adaptive separable-instrument null, the false-certification probability is at most

$$
\boxed{
\sum_{j=0}^{E}
\binom{C}{j}
\left(\frac14\right)^j
\left(\frac34\right)^{C-j}.
}
$$

This bound does not assume independent errors and permits adaptive abstention. It is a bound for one predeclared run. If unsuccessful runs are discarded and the experiment is restarted, all attempts must be reported or a multiple-testing correction must be applied.

Examples:

- 0 errors among 50 conclusive answers: $5.6632\times10^{-7}$;
- at most 20 errors among 200 conclusive answers: $7.0323\times10^{-8}$.

The honest experiment duration is random because a conclusive outcome occurs with probability $1/(2N)$ per ideal round.
