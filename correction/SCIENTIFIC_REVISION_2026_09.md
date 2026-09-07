# Scientific Revision: Global Optimality, Answer-Rate Limits, and Source Errors

**Ruge Lin | 7 September 2026 | Repository analysis, not peer reviewed**

This revision changes the scientific conclusions, not merely their software implementation. It supplements the dated [August author correction](AUTHOR_CORRECTION.md), which remains available unchanged. Neither document is an APS Erratum or a modification of the 2022 journal article. The IBM proof-of-concept experiment remains outside scope. The new results below are derived here; no priority claim is made for general discrimination or certification methods.

## Summary of the revised conclusions

1. The original special-outcome all-Hadamard decoder is optimal against **every one-sample quantum measurement**, not only other classical decoders of Hadamard data.
2. Independently refreshing the full secret while keeping its parity fixed makes that same decoder **globally optimal for any number of samples**. This obvious attempt to repair the baseline also removes every collective-measurement accuracy advantage.
3. The heralded witness has an exact, achievable **confidence-versus-total-answer-rate frontier**. Its confidence advantage vanishes at total conclusive rate $q\ge 1/N$. Increasing $N$ does not increase the best confidence gap; it reduces the usable answer rate.
4. A decomposable operator certificate strengthens the single-round null from separable effects to **positive-partial-transpose (PPT) effects**. A violation certifies a negative partial transpose in at least one effective conclusive effect, under the input assumptions.
5. Secret-independent local source noise preserves the original separable inequality. **Arbitrary small preparation leakage does not preserve a loss-independent 75 percent confidence ceiling.** General source errors require a calibrated allowance and a different finite-sample test.

The original shared-secret $23/32$ versus $25/32$ counterexample, its consequence for $p_B$, the exact ParitySolve probabilities, and the Bernoulli correction all remain valid.

## 1. Definitions and assumptions

Let $N=2^n$, $n\ge1$. The original unmodified DCP sample is

$$
|\psi_{x,s}\rangle=\frac{|0\rangle|x\rangle+|1\rangle|x+s\bmod N\rangle}{\sqrt2}.
$$

The parity $b=s\bmod2$ has equal prior probabilities. Unless stated otherwise, $s$ is uniform within its parity class, $x$ is independently uniform, and the receiver has no classical preparation record or other secret-correlated side information. Results about recovering parity under these priors are not statements about recovering the full secret.

For the heralded protocol, two samples share an independent hidden phase $\alpha\in\{0,\pi/2,\pi,3\pi/2\}$. The full parity-conditioned pair is denoted by $\rho_b$. All claims are about the complete input cells, not just labels or successes reported by the receiver.

For a three-outcome measurement $\{M_0,M_1,M_\perp\}$ define unconditional probabilities

$$
c=\frac12\sum_b\operatorname{Tr}(M_b\rho_b),\qquad
w=\frac12\sum_b\operatorname{Tr}(M_{1-b}\rho_b),\qquad q=c+w.
$$

The average conclusive confidence is $\mathcal C=c/q$ for $q>0$. Here $q$ is the total conclusive probability **over all attempted rounds**, not a rate conditional on Fourier collision and not the probability of one selected outcome. A population frontier is not itself a finite-data hypothesis test.

## 2. Global one-sample optimality

**Theorem 1.** Under the priors in Section 1, the optimum parity success over all POVMs on one original DCP sample is

$$
p^{(1)}_{\rm ALL}=\frac12+\frac1{2N}.
$$

The original all-Hadamard special-outcome rule attains this unrestricted optimum.

**Proof.** Apply the local Fourier transform to the rotation register and average over $x$. In the register ordering Fourier label followed by reflection qubit, the parity-averaged state is

$$
\eta_b=\frac1N\bigoplus_{k=0}^{N-1}\tau_b(k),\qquad
\tau_b(k)=\begin{cases}
|+\rangle\langle+|,&k=0,\\
|(-)^b\rangle\langle(-)^b|,&k=N/2,\\
I_2/2,&\text{otherwise},
\end{cases}
$$

where $|(-)^b\rangle=(|0\rangle+(-1)^b|1\rangle)/\sqrt2$. This follows from

$$
\frac2N\sum_{s\equiv b\ (2)}e^{2\pi i ks/N}
=\begin{cases}1,&k=0,\\(-1)^b,&k=N/2,\\0,&\text{otherwise}.\end{cases}
$$

Thus the two states commute and differ only in one label block:

$$
\eta_0-\eta_1=\frac1N|N/2\rangle\langle N/2|\otimes X,
\qquad \|\eta_0-\eta_1\|_1=\frac2N.
$$

The equal-prior binary optimum is $1/2+\|\eta_0-\eta_1\|_1/4$, giving the theorem. The Hadamard rotation outcome $y=1$ projects onto the same Fourier character $(-1)^x$ as label $k=N/2$. In that block the reflection Hadamard result reveals $b$; outside it the parity ensembles coincide. Therefore the published rule attains the optimum. This proof covers arbitrary ancillas and arbitrary one-cell quantum measurements, not merely one chosen basis. $\square$

**Consequence.** The baseline was genuinely optimal for the one-sample parity task. Its extension to a shared-secret record was the error. Global one-sample optimality cannot be tensorized through a mixture with a reused secret.

## 3. Why refreshing the secret cannot restore an accuracy separation

**Theorem 2.** Suppose a fixed hidden parity $b$ is retained, but each of $L$ samples independently draws its own $s_j$ uniformly within that parity class, and its own $x_j$. Then even an arbitrary collective POVM has success at most

$$
p^{(L)}_{\rm ALL,refresh}
=1-\frac12\left(1-\frac1N\right)^L.
$$

Independent all-Hadamard measurements with the original special-outcome decoder attain equality.

**Proof.** The states are now $\eta_b^{\otimes L}$, rather than a mixture over fixed-secret tensor powers. They share the same orthogonal label decomposition. If any label equals $N/2$, the two hypotheses occupy orthogonal reflection states. If no label does, they coincide. The latter event has probability $(1-1/N)^L$. No measurement can outperform perfect identification on the first event and random guessing on the second; the product strategy realizes both. $\square$

This is a limitation on a specific proposed repair, not a theorem about all possible DCP-derived challenges. It does not apply to the original same-$s$ ensemble or to the phase-twirled pair witness.

## 4. Complete pair states and a calibrated phase model

Let

$$
K=|01\rangle\langle10|+|10\rangle\langle01|,
\qquad a=\frac1{2N}.
$$

For the ideal phase-twirled source, the full Fourier-block representation is

$$
\rho_b(1)=\frac1{N^2}\bigoplus_{k,\ell}\frac{I_4+\gamma_b(\ell-k)K}{4},
$$

with $\gamma_b(0)=1$, $\gamma_b(N/2)=(-1)^b$, and zero otherwise (differences modulo $N$).

A precisely specified noisy-source family replaces $K$ by $vK$, with $0\le v\le1$. It is physically obtained by applying an unreported $Z$ to the second reflection qubit with probability $(1-v)/2$, independently of every hidden preparation variable. The noise acts on every Fourier block. The collision states are

$$
\sigma_b(v)=\frac14\left(I_4+(-1)^b vK\right).
$$

This is a source model, not a model for arbitrary experimental errors. Its $v$ must not be inferred solely from outputs of the untrusted device and then used to lower that device's null threshold. A known common local phase can be compensated, but an unknown phase or an arbitrary source map is not automatically described by this one-parameter family.

## 5. Exact confidence-versus-answer-rate frontiers

**Theorem 3.** For the full pair ensemble $\rho_b(v)$, fixed total conclusive rate $0<q\le1$, and arbitrary measurements,

$$
\boxed{c_{\rm G}^{\max}(q,v)=\frac{q+v\min(q,a)}2.}
$$

For separable, PPT, or LOCC measurements, the three optima coincide for this ensemble:

$$
\boxed{c_{\rm SEP}^{\max}(q,v)=c_{\rm PPT}^{\max}(q,v)
=c_{\rm LOCC}^{\max}(q,v)=\frac{q+v\min(q/2,a)}2.}
$$

The minimum error is $w=q-c^{\max}$ and confidence is $c^{\max}/q$. This equality does not assert equivalence of SEP, PPT, and LOCC measurement classes for other ensembles.

### 5.1 Global upper bound

Write $\bar\rho=(\rho_0+\rho_1)/2$ and $D=(\rho_0-\rho_1)/2$. The block structure gives

$$
-v\bar\rho\preceq D\preceq v\bar\rho,\qquad \|D\|_1=va.
$$

Since $c-w=\operatorname{Tr}[(M_0-M_1)D]$, positivity yields $c-w\le vq$. Also $-I\preceq M_0-M_1\preceq I$, so $c-w\le va$. Together these imply the global formula.

### 5.2 PPT upper bound and an exact operator certificate

Define $P_{\Psi^\pm}=|\Psi^\pm\rangle\langle\Psi^\pm|$ and $P_{\Phi^\pm}=|\Phi^\pm\rangle\langle\Phi^\pm|$, with the standard Bell states. Partial transpose $\Gamma$ is on the second side. Direct matrix multiplication gives

$$
\frac{I_4}{2}\pm K=P_{\Psi^\pm}+(P_{\Phi^\pm})^\Gamma.
$$

Consequently, with $\kappa_v=(2+v)/(2-v)$,

$$
\kappa_v\sigma_1(v)-\sigma_0(v)
=\frac{v}{2-v}\left[P_{\Psi^-}+(P_{\Phi^-})^\Gamma\right],
$$

and the plus version proves the reverse inequality. Both expectations are nonnegative for every $E\succeq0$ with $E^\Gamma\succeq0$. Locally dephasing the full Fourier registers preserves PPT, and all noncomplementary blocks are identical under the two hypotheses. Therefore

$$
c\le\kappa_v w,\qquad c-w\le\frac v2q.
$$

Combining this with $c-w\le va$ proves the PPT upper bound. At $v=1$ this is the factor-three theorem, now certified for PPT effects as well as separable effects. A positive ideal score $c-3w$ therefore requires at least one conclusive effect whose partial transpose is not positive. This is a sufficient witness, not tomography of the measurement or a test detecting every NPT measurement.

### 5.3 Attainment

For GLOBAL, Bell-measure the reflection qubits in complementary-label blocks, accepting the $\Psi^+$ and $\Psi^-$ outcomes. This gives $q=a$ and $c-w=va$. For $q<a$, independently retain a fraction $q/a$ of these answers. For $q>a$, add randomly guessed answers from the remaining outcomes to reach the required rate. Their net correct-minus-wrong contribution is zero.

For LOCC, read both Fourier labels locally. On a complementary block, measure each reflection qubit in the $X$ basis and report whether the two signs agree. This gives $q=1/N=2a$ and $c-w=va$. Thin these answers for $q<2a$; add random answers from noncomplementary blocks for $q>2a$. These constructions attain both upper bounds at every rate. In particular, the upper bound does not depend on trusting reported Fourier labels: arbitrary full-cell measurements were included from the outset. $\square$

### 5.4 Consequences that change the interpretation

At $v=1$,

$$
\mathcal C_{\rm G}(q)=\begin{cases}1,&q\le1/(2N),\\1/2+1/(4Nq),&q\ge1/(2N),\end{cases}
$$

$$
\mathcal C_{\rm SEP}(q)=\begin{cases}3/4,&q\le1/N,\\1/2+1/(4Nq),&q\ge1/N.\end{cases}
$$

For $N=2$:

| Total conclusive rate | GLOBAL confidence | SEP / PPT / LOCC confidence |
|---|---:|---:|
| $1/8$ | $1$ | $3/4$ |
| $1/4$ | $1$ | $3/4$ |
| $3/8$ | $5/6$ | $3/4$ |
| $1/2$ | $3/4$ | $3/4$ |
| $1$ | $5/8$ | $5/8$ |

Thus **no confidence advantage remains for $q\ge1/N$**. Increasing $n$ reduces the informative-label frequency, without enlarging the maximal confidence gap of $1/4$. Within this pair-per-round protocol, the optimum zero-error conclusive rate is $1/(2N)$; the honest implementation needs $2NC$ rounds on average for $C$ conclusive answers. A direct trusted two-equatorial-qubit version has the same collision ensembles without the $1/N$ label-selection cost. The DCP version is an embedding tied to the original project, not a resource-minimal primitive or evidence of DCP computational hardness.

For $0\le v<1$, both full parity states are strictly positive, so **nonzero-rate, exactly zero-error discrimination is impossible**. The best small-rate global confidence becomes $(1+v)/2$, and its separable counterpart is $1/2+v/4$. The confidence gap remains $v/4$ for a calibrated nonzero $v$. The unmodified score $c-3w$ for the standard Bell strategy equals $a(2v-1)$ and is positive only for $v>1/2$. A source-calibrated score $c-\kappa_v w$ has a different, proven null; a measured device visibility alone does not authorize this recalibration.

## 6. Source imperfections: two fundamentally different cases

### 6.1 A common separable source channel preserves the original bound

**Theorem 4.** Let $\Lambda$ be a fixed trace-preserving channel with product Kraus operators,

$$
\Lambda(\rho)=\sum_j(A_j\otimes B_j)\rho(A_j\otimes B_j)^\dagger,
$$

independent of $b,s,x_1,x_2,\alpha$. If the actual inputs are $\Lambda(\rho_b)$, every separable measurement still satisfies $c\le3w$.

**Proof.** Its effective ideal-input effects are $\Lambda^*(M_z)$. The adjoint sends a positive separable effect to a positive separable effect, and trace preservation sends a complete POVM to a complete POVM. Apply the original inequality to these effective effects. $\square$

This includes ordinary local dephasing, local depolarization, local amplitude damping, and local erasure channels when all flags are included and the noise mechanism is independent of the preparation label. Measurement loss is already allowed as abstention. Honest performance can deteriorate while soundness remains intact. A physical preparation apparatus must actually satisfy the common-channel premise; it cannot be assumed merely because its imperfections are called local noise.

### 6.2 Small unrestricted source errors can defeat a fixed confidence ceiling

Embed the ideal inputs into a larger local Hilbert space with a publicly specified, parity-independent no-leak flag. With probability $1-\epsilon$ deliver the ideal state. With probability $\epsilon$ deliver a product state carrying an orthogonal, locally readable flag encoding $b$. For each parity,

$$
D(\widetilde\rho_b,\rho_b)=\epsilon,
\qquad D(\rho,\sigma)=\tfrac12\|\rho-\sigma\|_1.
$$

A local receiver reads the leak flag, answers only on leakage events, and otherwise abstains. It has $q=\epsilon$, confidence $1$, and zero errors. The actual inputs are still separable across the cells. The flaw is hidden-label leakage, not an entangled source.

This construction exists for arbitrarily small $\epsilon>0$. Therefore a uniform 75 percent confidence ceiling at arbitrarily low answer rates **cannot follow from a small nonzero trace-distance error budget alone**. All receiver-accessible side channels must be included in the trusted-input model. This is an explicit DCP instance of the broader noisy-input concern in trusted-input certification [4].

## 7. A source-error-aware statistical certificate

### 7.1 Population bound

**Theorem 5.** Suppose the complete actual parity ensembles satisfy externally justified bounds

$$
D(\widetilde\rho_b,\rho_b)\le\epsilon_b.
$$

For a separable effective POVM, its actual score obeys

$$
\boxed{c-3w\le\beta,\qquad \beta=2(\epsilon_0+\epsilon_1).}
$$

Equivalently, at nonzero actual rate $q$,

$$
\mathcal C_{\rm SEP}\le
\min\!\left\{1,\frac34+\frac{\epsilon_0+\epsilon_1}{2q}\right\}.
$$

These are conservative bounds, not asserted to be tight for arbitrary source-error sets.

**Proof.** For parity $b$, let $A_b=M_b-3M_{1-b}$. Since $0\preceq M_b,M_{1-b}$ and $M_b+M_{1-b}\preceq I$, one has $-3I\preceq A_b\preceq I$. The spectral range is four, so a trace-distance perturbation of size $\epsilon_b$ changes its mean by at most $4\epsilon_b$. Averaging over the two equal priors gives at most $2(\epsilon_0+\epsilon_1)$ above the ideal null score zero. Substitution of $w=q-c$ yields the confidence bound. $\square$

### 7.2 Fixed-round finite-sample bound

Use a **predeclared fixed number $R$ of total rounds**. Count every abstention and loss. Let $Z_t$ be $+1$ for a correct conclusive answer, $-3$ for an incorrect conclusive answer, and $0$ otherwise. Require the source-error bounds and effective separability premise after every history, not merely on a final averaged state.

An operational sufficient condition is fresh, independent, **separable actual input pairs**, separable initial memory, and separable instruments on every branch. Alternatively assume fresh separable memory is reestablished each round. Trace-distance closeness alone does not guarantee memory separability: an entangled faulty input could otherwise be retained as a later resource.

Then $\mathbb E[Z_t\mid\mathcal F_{t-1}]\le\beta$. Conditional Hoeffding's lemma for the range $[-3,1]$ gives

$$
\mathbb E[\exp(\lambda(Z_t-\beta))\mid\mathcal F_{t-1}]
\le \exp(2\lambda^2),\qquad\lambda\ge0.
$$

Multiplication over rounds, Markov's inequality, and optimization at $\lambda=(z-\beta)/4$ prove

$$
\boxed{\Pr_{\rm null}[\overline Z\ge z]
\le \exp\!\left[-\frac{R(z-\beta)^2}{8}\right],\qquad z>\beta.}
$$

At $z\le\beta$ use bound one. This permits adaptive separable strategies; independent receiver errors are unnecessary. It is a fixed-horizon bound, not an anytime-valid rule. The general concentration method is established [5]; the DCP-specific step is the calibrated conditional score allowance.

For illustration only, $R=10000$, $2500$ correct answers, zero errors, and $7500$ inconclusive answers give $z=1/4$. With externally certified $\epsilon_0=\epsilon_1=0.01$, $\beta=0.04$ and the logarithm of the false-certification bound is $-55.125$. These counts and calibration values are **not experimental data**.

Do not substitute the observed conclusive count for $R$, discard failed runs, or reuse the ideal $1/4$ error binomial test for arbitrary imperfect sources. The original conclusive-count test remains valid for the ideal source and for the common separable-channel case in Section 6.1. In the unrestricted error-budget case, use the adjusted fixed-round score test or separately prove another calibrated null.

## 8. Literature, chronology, and scope of the new contribution

Fixed-inconclusive-rate discrimination and its interpolation between unambiguous and minimum-error measurements are established frameworks, including Bagan et al. and Herzog [1,2]. Lee and Bae's 2026 trusted-input framework explicitly treats confidence as a function of outcome rate for a different antiparallel ensemble [3]. The present total-rate curves are not their per-outcome-rate curves, and the numerical cutoffs must not be interchanged.

The new contribution recorded here is the exact closed-form solution for this DCP pair ensemble, the strengthened one-sample result and refreshed-secret limitation, and explicit DCP source-error implications. No claim is made that the general confidence-versus-rate idea, PPT witnessing, or concentration method originated here. No exhaustive novelty certification has been performed.

The 2022 paper did not contain these theorems. The August 2026 correction established the counterexample and ideal witness. **The stronger statements in this document are dated 7 September 2026**, not retroactively attributed to either earlier document. The August GPT-5.6 Pro acknowledgment is preserved; this later scientific revision was also AI-assisted. Ruge Lin remains responsible for the repository's claims. An executable check or an AI audit is not independent peer review.

No result here certifies universal computation, computational speedup, an implementation of a particular gate, or the absence of unmodeled side channels. No experimental calibration has been performed. The original paper's verification threshold remains withdrawn.

## 9. Reproducibility

The analytic proofs above establish optimality and soundness. Numerical checks are additional error-detection tools, not substitutes for them.

```bash
python -m pip install -e '.[test]'
python -m pytest -q tests/test_scientific_revision.py
python examples/reproduce_scientific_revision.py
python scripts/validate_committed_results.py
```

Checks include direct raw-state construction, Helstrom optima, tensor-power discrimination of refreshed secrets, explicit full-cell attaining POVMs, exact dyadic PPT dual identities, noisy-state construction, and the locally readable leakage example. The additional result file is `results/scientific_revision_results.json`; each field participates in the repository's deliberate-corruption validation.

An independent optimization check uses the optional SciPy audit dependency:

```bash
python -m pip install -e '.[audit]'
python scripts/audit_scientific_frontier.py
```

This constructs the raw source states, diagonalizes the label/Bell blocks, and solves the GLOBAL and PPT linear programs for 96 combinations of dimension, visibility, rate, and measurement class. Bilateral local Pauli twirling justifies the exact Bell-diagonal reduction; all three measurement effects, including abstention, are constrained. SciPy is not a runtime dependency of the analytical package.

## References

1. E. Bagan, R. Muñoz-Tapia, G. A. Olivares-Rentería, and J. A. Bergou, *Optimal discrimination of quantum states with a fixed rate of inconclusive outcomes*, Phys. Rev. A **86**, 040303(R) (2012). [DOI](https://doi.org/10.1103/PhysRevA.86.040303).
2. U. Herzog, *Optimal state discrimination with a fixed rate of inconclusive results: Analytical solutions and relation to state discrimination with a fixed error rate*, Phys. Rev. A **86**, 032314 (2012). [DOI](https://doi.org/10.1103/PhysRevA.86.032314).
3. H. Lee and J. Bae, *Semi-Device-Independent Certification for Nonlocality without Entanglement*, [arXiv:2606.13667v2](https://arxiv.org/abs/2606.13667v2) (15 June 2026; first version 11 June 2026).
4. K. Sen, C. Srivastava, S. Mal, A. Sen De, and U. Sen, *Noisy quantum input loophole in measurement-device-independent entanglement witnesses*, Phys. Rev. A **104**, 012429 (2021). [DOI](https://doi.org/10.1103/PhysRevA.104.012429); [arXiv:2012.09089](https://arxiv.org/abs/2012.09089).
5. S. R. Howard, A. Ramdas, J. McAuliffe, and J. Sekhon, *Time-uniform Chernoff bounds via nonnegative supermartingales*, Probability Surveys **17**, 257-317 (2020). [DOI](https://doi.org/10.1214/18-PS321).
