# Author Technical Correction and Updated Analysis

## For “A quantum computation capability verification protocol for NISQ devices with dihedral coset problem”

**Ruge Lin**  
**Date:** 17 August 2026

> **Status.** This is an author-maintained technical correction hosted with the code repository. It is not an APS Erratum, has not been peer reviewed as a replacement article, and does not alter the journal version. The statements here are made by Ruge Lin and should not be read as a statement on behalf of the journal or as an assertion of endorsement by the coauthor.

## Abstract

The 2022 article proposed a DCP-derived circuit, called ParitySolve, and interpreted its success probability relative to a quantity denoted by $p_B$ as a verification of quantum-computation capability. A later reanalysis shows that the circuit-level parity extraction is correct, but the verification interpretation is not. The quantity $p_B$ is the success probability of one specified all-Hadamard decoder; it is neither proved nor valid as an upper bound over all strategies using the same product measurements and classical postprocessing. An exact two-sample counterexample gives success $25/32$, compared with $23/32$ for the published decoder, without adding any quantum operation. Consequently, the acceptance condition $p>p_B$ does not establish the claimed capability.

This note records what survives, supplies an exact formula for the ideal ParitySolve probability, corrects the numerical interpretation of the parameter choices used in Figure 5, replaces the reported fluctuation formula by the Bernoulli standard error, and gives the strongest aggregate reconstruction supported by the IBM counts retained in the repository. The defensible surviving interpretation is a structured DCP-derived circuit workload, not an adversarially sound verification protocol.

## 1. Scope and bibliographic record

This note concerns:

Ruge Lin and Weiqiang Wen, “A quantum computation capability verification protocol for NISQ devices with dihedral coset problem,” *Physical Review A* **106**, 012430 (2022), DOI: `10.1103/PhysRevA.106.012430`, arXiv:2202.06984.

The original repository state is preserved by the immutable GitHub release and tag `paper-2022-original`. The present repository branch adds new files but leaves the six original Python scripts unchanged.

The correction has four purposes:

1. preserve the valid circuit construction;
2. withdraw the unsound interpretation of $p_B$;
3. make the corrected calculations exactly reproducible;
4. separate a later DCP-derived witness from the claims of the 2022 article.

Citation history, peer-review history, and the reception of the article are outside the scope of this note.

## 2. Circuit result that remains correct

Let $N=2^n$, and let a DCP sample be

$$
\lvert\psi_{x,s}\rangle
=
\frac{
\lvert0\rangle\lvert x\rangle
+
\lvert1\rangle\lvert x+s\bmod N\rangle
}{\sqrt2},
\qquad x,s\in\mathbb Z_N.
$$

After applying the Fourier transform $F_N$ to the rotation register and measuring the Fourier label $k$, the reflection qubit is, up to a global phase,

$$
\lvert\phi_{k,s}\rangle
=
\frac{\lvert0\rangle+\omega_N^{ks}\lvert1\rangle}{\sqrt2},
\qquad
\omega_N=e^{2\pi i/N}.
$$

Suppose two measured labels satisfy

$$
k_1-k_2\equiv \frac N2\pmod N.
$$

On the selected output branch of the two-reflection-qubit CNOT operation, the remaining relative phase is

$$
\omega_N^{(k_1-k_2)s}
=
\omega_N^{Ns/2}
=
(-1)^s.
$$

A final Hadamard measurement therefore returns $s\bmod2$ exactly in the ideal model. This ParitySolve algebra is correct. The circuit remains a meaningful workload involving DCP preparation, Fourier transforms, measurement, collision search, inter-cell interference, and readout.

The correction does not withdraw this circuit identity.

## 3. The original baseline and its limitation

### 3.1 What $p_B$ actually computes

The article considered applying Hadamard gates to every qubit of every DCP sample. Write one measurement outcome as $(r,y)$, where $r\in\{0,1\}$ is the reflection result and $y\in\mathbb Z_N$ is the rotation-register result.

After averaging over the uniform preparation label $x$, the exact conditional probability is

$$
q_s(r,y)
=
\frac1{N^2}
\#\left\{
 x\in\mathbb Z_N:
 r=x\mathbin{\cdot}y
 \oplus
 ((x+s)\bmod N)\mathbin{\cdot}y
\right\},
$$

where the dot denotes the binary inner product.

For $y=1$, only the least significant bit is selected, so

$$
r=x_0\oplus(x+s)_0=s\bmod2.
$$

Thus one sample yields a special parity-revealing outcome with probability $1/N$. The published decoder retained only this outcome and guessed uniformly if none of the $mt$ samples produced it. Its success probability is

$$
\boxed{
 p_B
 =
 1-\frac12\left(\frac{N-1}{N}\right)^{mt}
}.
$$

This formula is correct for that specific decoder. It should therefore be renamed descriptively, for example as the *special-outcome all-H decoder probability*.

### 3.2 Why the one-sample calculation looked convincing

For a single sample, the special-outcome decoder is optimal for discriminating the parity after the all-H product measurement. The problem is not the one-sample formula.

The problem is that all $mt$ samples in one repetition share the same hidden secret $s$. The relevant parity-conditioned record is consequently a mixture over fixed-secret product distributions,

$$
\frac2N
\sum_{s\equiv b\ (2)}
q_s^{\otimes mt},
$$

rather than the tensor power of a one-sample parity average. Outcomes that are inconclusive individually can therefore be correlated through the reused secret and become informative when processed together.

### 3.3 Exact two-sample counterexample

Take

$$
N=4,\qquad m=2,\qquad t=1.
$$

Use exactly the same all-H product measurements as the published baseline. The published decoder succeeds with

$$
p_B
=
1-\frac12\left(\frac34\right)^2
=
\frac{23}{32}.
$$

Now use the following classical decoder on the same two outcomes $(r_1,y_1)$ and $(r_2,y_2)$:

1. if either $y_j=1$, return the corresponding $r_j$;
2. otherwise, if $y_1,y_2\in\{2,3\}$, return $r_1\oplus r_2$;
3. otherwise, guess uniformly.

The first event occurs with probability

$$
1-\left(\frac34\right)^2=\frac7{16}
$$

and reveals the parity exactly.

The additional event $y_1,y_2\in\{2,3\}$ occurs with probability $1/4$, is disjoint from the first event, and gives conditional success $3/4$: for even $s$, the XOR is always zero; for odd $s$, it is uniform. With equal parity priors, the decoder is therefore correct with probability $3/4$ on this event.

Hence

$$
\begin{aligned}
p_{\rm better}
&=
\frac7{16}
+
\frac14\cdot\frac34
+
\left(1-\frac7{16}-\frac14\right)\frac12\\[2mm]
&=
\frac{25}{32}.
\end{aligned}
$$

The improvement is

$$
\frac{25}{32}-\frac{23}{32}=\frac1{16}.
$$

No entangling operation, quantum memory, alternative measurement basis, additional sample, or quantum postprocessing is used. The difference comes solely from retaining correlations discarded by the original classical decoder.

This counterexample disproves the interpretation of $p_B$ as a general upper bound for the intended weaker class. Therefore the implication

$$
p>p_B
\quad\Longrightarrow\quad
\text{verified quantum-computation capability}
$$

is withdrawn.

### 3.4 Full likelihood decoder

For any fixed all-H record $o_1,\ldots,o_\ell$, with $\ell=mt$, the Bayes-optimal parity likelihoods are

$$
L_b(o_1,\ldots,o_\ell)
=
\frac2N
\sum_{\substack{s=0\\s\equiv b\ (2)}}^{N-1}
\prod_{j=1}^{\ell}q_s(o_j),
\qquad b\in\{0,1\}.
$$

Returning the larger likelihood systematically uses all information in the original measurement record. The repository implements this decoder exactly for small cases and by fixed-seed Monte Carlo for the larger published instances.

## 4. Exact ideal ParitySolve probability

The original analysis used upper and lower bounds for the probability of finding a complementary Fourier-label collision. An exact finite formula is available.

Partition the $N$ labels into $N/2$ complementary pairs

$$
\{a,a+N/2\}.
$$

Let $k_{\rm nc}(N,m)$ be the probability that $m$ independent uniform labels contain no complementary pair. If exactly $j$ complementary pairs are occupied without a collision, then:

1. choose the occupied pairs: $\binom{N/2}{j}$;
2. choose one member of each pair: $2^j$;
3. assign the $m$ labelled samples surjectively to the $j$ selected labels: $j!\,{m\brace j}$.

Therefore

$$
\boxed{
k_{\rm nc}(N,m)
=
\frac1{N^m}
\sum_{j=1}^{\min(m,N/2)}
\binom{N/2}{j}
2^j j!\,{m\brace j}
},
$$

where ${m\brace j}$ is a Stirling number of the second kind. The case $m=0$ is defined as $k_{\rm nc}=1$.

In one batch, a complementary collision exists with probability $1-k_{\rm nc}$. The selected CNOT branch succeeds with probability $1/2$. Under the retry rule implemented in the original code, one batch fails to return a definitive parity with probability

$$
\frac{1+k_{\rm nc}}2.
$$

After $t$ batches, the exact ideal success probability, including a final random guess, is

$$
\boxed{
p_{\rm exact}
=
1-\frac12
\left(\frac{1+k_{\rm nc}}2\right)^t
}.
$$

The repository checks the formula against exhaustive enumeration for all test instances with $n\le3$ and $m\le4$.

## 5. Corrected interpretation of the Figure 5 parameter choices

The original parameter search selected instances from the difference between the published upper bound $p_{\rm upper}$ and $p_B$. That is a legitimate bound comparison, but it does not establish the actual honest separation. The corrected values are:

| Figure | $(n,m,t)$ | $p_B$ | Published $p_{\rm upper}$ | Exact honest $p$ | Full-likelihood all-H |
|---|---:|---:|---:|---:|---:|
| 5(a) | $(4,6,1)$ | 0.660533 | 0.664083 | **0.652965** | **0.810940**, exact |
| 5(b) | $(6,9,4)$ | 0.716371 | 0.817392 | **0.810918** | **0.937289**, Monte Carlo |
| 5(c) | $(9,21,9)$ | 0.654461 | 0.906606 | **0.904804** | **0.957183**, Monte Carlo |

For Figure 5(a), the actual honest difference is negative:

$$
p_{\rm exact}-p_B=-0.007568.
$$

For Figure 5(b), the actual difference is

$$
0.094547,
$$

which is below 10 percent. Figure 5(c) retains an honest difference of approximately 25.03 percent against the special-outcome decoder, but the optimized decoder using the same all-H measurement data exceeds the honest ParitySolve score. None of these comparisons supplies a sound verification gap.

The Figure 5(a) optimized value is exact:

$$
\frac{27863673495}{34359738368}
\approx0.8109396293.
$$

The Figure 5(b) and 5(c) values are fixed-seed Monte Carlo estimates with Wilson intervals recorded in `results/figure5_corrected.csv`.

## 6. Corrected statistical uncertainty

Each complete repetition returns one correct-or-incorrect bit. Let $Y$ be its correctness indicator. Irrespective of the internal decomposition into definitive branches and random guesses,

$$
Y\sim\operatorname{Bernoulli}(p).
$$

For $r$ independent repetitions, the empirical accuracy therefore has standard error

$$
\boxed{
\operatorname{SE}(\widehat p)
=
\sqrt{\frac{p(1-p)}r}
}.
$$

The expression used in the original paper and scripts,

$$
\sqrt{\frac{1-p}{2r}},
$$

accounts for the random final guess conditional on failure but omits the fluctuation in whether a definitive branch occurs.

At the exact Figure 5(b) value with $r=1000$, the two formulas give

$$
0.009723
\quad\text{and}\quad
0.012383,
$$

respectively.

## 7. IBM aggregate reconstruction

The article describes a postselection condition based on measured output bits. In the original `IBM.py`, the prepared values `x0` and `x1` are also used as the collision test through

```python
if x0 != x1:
```

The preparation labels are not the measured Fourier labels. This legacy reconstruction consequently uses only cases B, C, F, and G in the definitive branch, although all eight preparation cases contain selected hardware counts. It also substitutes an idealized selection probability for the observed selection rate.

Using all eight archived aggregate cases and their observed selected-count rates gives

$$
p_{\rm IBM,aggregate}=0.7439808125.
$$

For comparison,

$$
p_{\rm legacy\ code}=0.7545878022,
\qquad
p_{\rm ideal}=0.7890625.
$$

A 100,000-trial multinomial bootstrap of the three retained aggregate categories gives the indicative 95 percent interval

$$
[0.739820,\,0.748090].
$$

This interval measures finite-count uncertainty only. The repository does not contain the raw shot records or timestamps, so temporal drift and shot-level correlations cannot be reconstructed.

The defensible interpretation is that the archived data show nontrivial fidelity in the selected Bell-type branch. They do not constitute a direct end-to-end execution of the challenge, and Figure 9 should not be regenerated from the legacy reconstruction logic as though it did.

## 8. Effect on the conclusions

### Retained

- the DCP sample construction;
- the post-Fourier reflection phase state;
- the complementary-label collision mechanism;
- the selected ParitySolve branch and its exact parity output;
- the original collision expressions as upper and lower bounds;
- the use of the circuit as a structured, hardware-sensitive workload;
- the original clean/noisy simulations as illustrations of the specified circuit and noise model.

### Corrected or withdrawn

- $p_B$ is not a general soundness bound;
- $p>p_B$ does not verify the claimed quantum-computation capability;
- the statement that no analytic ideal probability is available is replaced by the exact formula above;
- Figure 5 parameter gaps must be interpreted using the exact honest probability, not only an upper bound;
- the standard-error formula is replaced by the Bernoulli formula;
- the IBM reconstruction is replaced by the aggregate-only calculation above.

### Surviving scientific classification

The original construction is best classified as a **DCP-derived circuit benchmark or workload**. Calling it an adversarial capability-verification protocol would require an explicit null class and a proved optimal soundness bound against that entire class. The 2022 threshold does not provide such a bound.

## 9. Separate follow-up result

The repository also contains a later phase-twirled, heralded DCP construction under `witness/`. It is not a repair already present in the 2022 article. Its ideal theorem concerns a narrower capability: a nonseparable joint measurement across two trusted DCP input cells, against POVMs whose effects are separable across the cell partition.

That follow-up is explicitly labelled non-peer-reviewed and is separated from this correction. It does not restore the original claim of general quantum-computation verification.

## 10. Reproducibility

The decisive calculations can be reproduced from a modern Python environment without Qibo:

```bash
python -m pip install -e .[test]
python examples/reproduce_counterexample.py
python examples/reproduce_figure5.py
python examples/reproduce_ibm_reanalysis.py
pytest -q
```

The committed machine-readable outputs are:

- `results/correction_core_results.json`;
- `results/figure5_corrected.csv`;
- `results/ibm_aggregate_reanalysis.json`;
- `results/heralded_witness_results.json`.

The six original scripts remain unchanged. They require their historical software stack and are not imported by the corrected tests.

## Appendix A. Exact outcome table for the smallest counterexample

For $N=4$, the integer counts $16q_s(r,y)$, with columns ordered by $(r=0,y=0,1,2,3)$ followed by $(r=1,y=0,1,2,3)$, are

$$
\begin{array}{c|rrrrrrrr}
s&0,0&0,1&0,2&0,3&1,0&1,1&1,2&1,3\\\hline
0&4&4&4&4&0&0&0&0\\
1&4&0&2&2&0&4&2&2\\
2&4&4&0&0&0&0&4&4\\
3&4&0&2&2&0&4&2&2
\end{array}
$$

This table makes both parts of the improved decoder transparent. The $y=1$ columns reveal the parity exactly. Conditional on $y\in\{2,3\}$, even secrets force a fixed reflection result while odd secrets produce an unbiased result, which creates the two-sample correlation.

## Appendix B. Repository status

- Historical code snapshot: immutable tag and release `paper-2022-original`.
- Author correction branch: `author-correction-2026`.
- Original six Python scripts: preserved byte-for-byte.
- Current note: author-maintained, not an APS Erratum.
- Follow-up witness: separate, ideal-model, non-peer-reviewed.
