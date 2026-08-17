# Protocol Specification

Let $N=2^n$. Each round uses fresh randomness.

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

The verifier supplies the quantum states, not a classical circuit description revealing $s$ or $\alpha$.

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
   \Psi^+\mapsto0,\qquad \Psi^-\mapsto1,
   $$
   and $\perp$ on the remaining Bell outcomes.

All measurements may be deferred to the end of the circuit.

## Linear score

For one round, assign

$$
Z=
\begin{cases}
+1,&\text{correct conclusive answer},\\
-3,&\text{wrong conclusive answer},\\
0,&\text{inconclusive answer}.
\end{cases}
$$

Every separable strategy in the stated null class satisfies

$$
\mathbb E[Z]\le0.
$$

The ideal honest strategy satisfies

$$
\mathbb E[Z]=\frac1{2N}.
$$

## Conclusive-outcome test

An alternative test stops after $C$ conclusive answers. Under the separable null, the conditional error probability is at least $1/4$ on each conclusive round, including after conditioning on previous public history. A conservative lower-tail bound for observing at most $E$ errors is

$$
\sum_{j=0}^{E}
\binom{C}{j}
\left(\frac14\right)^j
\left(\frac34\right)^{C-j}.
$$

Examples:

- 0 errors among 50 conclusive answers: $5.6632\times10^{-7}$;
- at most 20 errors among 200 conclusive answers: $7.0323\times10^{-8}$.

The experiment duration remains random because honest conclusive outcomes occur with probability $1/(2N)$.
