# DCP Challenge: Corrected Analysis and Measurement Witness

**Ruge Lin | 7 September 2026 | Version 1.2.1**

**Status.** This is the current, self-contained author-maintained technical note for the DCP-challenge repository. It incorporates the August correction and the September scientific extension. It is not an APS Erratum, does not modify the journal article, and has not received independent peer review. Statements are made by Ruge Lin, not on behalf of the journal, the original coauthor, or an AI provider. The original IBM proof-of-concept experiment is outside this note's scope.

## 1. Scope, conclusions, and notation

The 2022 article [1] proposed a trusted-input DCP challenge and a circuit called ParitySolve. Its selected parity-extraction branch is correct. Its verification condition, accuracy exceeding a reference value $p_B$, is not sound: the same product measurements with better classical processing already exceed that reference.

The corrected position has three parts. First, the original circuit remains a structured workload, not an adversarial verification theorem. Second, its reference decoder was genuinely optimal for one input cell, but that optimality does not extend to a record reusing the full secret. Third, a different, phase-twirled two-cell challenge witnesses nonseparable measurement through confidence with abstention. The latter has exact answer-rate limits and explicit source assumptions; it does not certify universal computation or computational speedup.

Throughout, $N=2^n$ with $n\ge1$. Arithmetic on rotation labels is modulo $N$. A cell has a reflection qubit and an $n$-qubit rotation register. The parity $b=s\bmod2$ has equal prior probabilities, and $s$ is uniform within its parity class. Preparation labels $x$ are uniform and independent unless specified otherwise. No receiver-accessible classical record or side channel reveals a hidden preparation variable. Binary inner products use the least-significant-bit convention, so integer label $1$ denotes that single bit.

We use $L$ for the number of samples, $m$ for a batch size, $t$ for a maximum number of batches, and $R$ for the total number of experimental rounds. A quantum measurement is a positive-operator-valued measure (POVM): positive effects summing to the identity. Across the two complete cells, LOCC means local operations and classical communication, SEP means separable effects, and PPT means effects with positive partial transpose. These classes obey LOCC $\subseteq$ SEP $\subseteq$ PPT $\subseteq$ unrestricted measurements. Equality of particular optimal scores below does not equate the classes themselves.

For a three-output witness, write $c,w$ for unconditional correct and wrong conclusive probabilities. The total answer rate and average conclusive confidence are

$$
q=c+w,\qquad \mathcal C=\frac{c}{q}\quad(q>0).
$$

**Every rate in the DCP frontier is measured over all attempted rounds**, including noncollisions and abstentions. A population tradeoff is not by itself a finite-data test.

## 2. The original circuit and the failure of its threshold

### 2.1 What ParitySolve correctly does

An original DCP sample is

$$
|\psi_{x,s}\rangle=\frac{|0\rangle|x\rangle+|1\rangle|x+s\rangle}{\sqrt2}.
$$

With $F_N|x\rangle=N^{-1/2}\sum_k\omega_N^{kx}|k\rangle$ and $\omega_N=e^{2\pi i/N}$, measuring the rotation register after $F_N$ leaves the reflection state

$$
|\phi_{k,s}\rangle=\frac{|0\rangle+\omega_N^{ks}|1\rangle}{\sqrt2}.
$$

The label $k$ is uniform. For two labels with $k_1-k_2=N/2$, a CNOT between their reflection qubits followed by the target outcome $1$ leaves relative phase

$$
\omega_N^{(k_1-k_2)s}=(-1)^s.
$$

A final Hadamard measurement gives $b$ without error. The selected CNOT branch has probability $1/2$. This identity is retained. Hardware sensitivity of the resulting workload does not establish an optimal bound against alternative receivers.

### 2.2 The reference decoder and the exact counterexample

Apply Hadamards to all qubits of each original sample and measure $(r,y)$, where $r$ is the reflection result. Averaging over $x$ gives

$$
q_s(r,y)=\frac{1}{N^2}\#\{x:r=x\cdot y\oplus((x+s)\bmod N)\cdot y\}.
$$

When $y=1$, $r=x_0\oplus(x+s)_0=b$. This event has probability $1/N$. The published reference keeps only these events and guesses fairly if none occurs. For $L=mt$ samples its accuracy is

$$
p_B=1-\frac12\left(1-\frac1N\right)^L.
$$

This formula correctly describes that decoder; it is not a general soundness bound.

For $N=4$ and $L=2$, use the same measured outcomes $(r_1,y_1),(r_2,y_2)$. Return $r_j$ if either $y_j=1$. Otherwise, if both $y_j\in\{2,3\}$, return $r_1\oplus r_2$. Guess fairly in all remaining cases. The special event has probability $7/16$ and is error-free. The additional event has probability $1/4$ and conditional accuracy $3/4$: for even secrets the XOR is zero, whereas for odd secrets it is uniform. Thus

$$
p_B=\frac{23}{32},\qquad
p_{\rm better}=\frac7{16}+\frac14\frac34+\frac5{16}\frac12=\frac{25}{32}.
$$

No additional sample, gate, basis choice, coherent memory, or quantum postprocessing is used. This finite counterexample withdraws the implication that $p>p_B$ verifies the claimed capability.

The mechanism is shared-secret correlation. The distribution of an $L$-sample record of parity $b$ is

$$
P_b(o_1,\ldots,o_L)=\frac2N\sum_{s\equiv b\ (2)}\prod_{j=1}^Lq_s(o_j),
$$

not the product of the one-sample parity averages. Comparing these two likelihoods is optimal classical processing of the chosen all-Hadamard record. It is not asserted to optimize all collective quantum measurements on the original shared-secret inputs.

## 3. Exact honest probability and statistical correction

### 3.1 Complementary-pair occupancy

Let $k_{\rm nc}(N,m)$ be the probability that $m$ independent uniform Fourier labels contain no complementary pair. Partition labels into $N/2$ pairs $\{a,a+N/2\}$. A noncolliding record occupying $j$ pairs chooses those pairs, chooses one member of each pair, then assigns the $m$ labelled samples surjectively to those $j$ members. Therefore

$$
k_{\rm nc}(N,m)=\frac1{N^m}\sum_{j=1}^{\min(m,N/2)}
\binom{N/2}{j}2^j j!\,{m\brace j},
$$

where ${m\brace j}$ is a Stirling number of the second kind, and $k_{\rm nc}(N,0)=1$.

For the original rule, which attempts one selected pair per batch and restarts after a failed branch, one batch fails to give a definitive answer with probability $(1+k_{\rm nc})/2$. With at most $t$ fresh batches and a final fair guess,

$$
p_{\rm honest}=1-\frac12\left(\frac{1+k_{\rm nc}}2\right)^t.
$$

This is a formula for the stated ParitySolve policy, not a claim that this policy is the globally best use of a batch.

### 3.2 Corrected Figure 5 comparison

The article's parameter choices used an upper bound on the honest probability. An upper-bound gap need not be an achieved gap. The corrected numbers are:

| Figure and $(n,m,t)$ | Reference $p_B$ | Exact honest | Complete all-H decoder |
|---|---:|---:|---:|
| 5(a), $(4,6,1)$ | 0.660533 | 0.652965 | 0.810940, exact |
| 5(b), $(6,9,4)$ | 0.716371 | 0.810918 | 0.937289, estimated |
| 5(c), $(9,21,9)$ | 0.654461 | 0.904804 | 0.957183, estimated |

The honest-minus-reference gaps are respectively $-0.007568$, $0.094547$, and $0.250343$. The complete all-H decoder exceeds the honest score in these instances. Figure 5(a)'s decoder optimum is exactly $27863673495/34359738368$. The larger entries are archived Monte Carlo estimates, not exact optima certified numerically without uncertainty. Their seeds, counts, and Wilson intervals are in `results/figure5_corrected.csv`; fast validation does not rerun those large simulations.

### 3.3 Correct uncertainty

Each completed original-protocol repetition returns a correct-or-incorrect bit. For $R$ independent repetitions with success probability $p$,

$$
\mathrm{SE}(\widehat p)=\sqrt{\frac{p(1-p)}R}.
$$

The original expression $\sqrt{(1-p)/(2R)}$ conditions on failing to solve and omits the fluctuation in whether a definitive branch occurs. At the exact Figure 5(b) probability and $R=1000$, the original and corrected errors are approximately $0.009723$ and $0.012383$. The formula here assumes independent repetitions; the adaptive witness tests in Sections 7 and 8 use different arguments.

## 4. Stronger optimality and a limitation on repairing the baseline

### 4.1 Unrestricted one-cell optimum

**Theorem 1 (September 2026).** Under the priors in Section 1, the best parity accuracy over all quantum POVMs on one original cell is

$$
p_{\rm ALL}^{(1)}=\frac12+\frac1{2N}.
$$

The original product-Hadamard decoder attains it.

**Proof.** Fourier transformation is used only to represent the states; no measurement restriction is imposed. Averaging over $x$ and then over secrets of parity $b$ produces

$$
\eta_b=\frac1N\bigoplus_{k=0}^{N-1}\tau_b(k),\qquad
\tau_b(k)=\begin{cases}
|+\rangle\langle+|,& k=0,\\
|(-)^b\rangle\langle(-)^b|,& k=N/2,\\
I_2/2,&\text{otherwise},
\end{cases}
$$

with $|(-)^b\rangle=(|0\rangle+(-1)^b|1\rangle)/\sqrt2$. Indeed, the parity-restricted Fourier sum equals $1$ at $k=0$, $(-1)^b$ at $k=N/2$, and zero otherwise. Thus $\eta_0-\eta_1$ is $X/N$ in just one block and has trace norm $2/N$. For equal-prior binary discrimination, maximizing $\tfrac12+\tfrac12\mathrm{Tr}[E(\eta_0-\eta_1)]$ over $0\preceq E\preceq I$ selects the positive spectral subspace and gives $\tfrac12+\tfrac14\|\eta_0-\eta_1\|_1$. This proves the bound. The Hadamard rotation outcome $y=1$ is precisely the Fourier character $(-1)^x$, so the original decoder reads this informative block and attains equality. Ancillas independent of the secret do not change the optimum.

For comparison with the August result, the all-Hadamard parity distributions satisfy

$$
P_0(r,y)-P_1(r,y)=\frac{(-1)^r}{N}\mathbf1_{\{y=1\}}.
$$

A direct proof substitutes $z=x+s$ into the signed parity sum. Since $s\bmod2=x_0\oplus z_0$, the sum factors into two Walsh sums $\sum_x(-1)^{x_0+x\cdot y}$, each nonzero only at $y=1$. This also proves optimality among classical decoders of one all-H record. Theorem 1 is stronger: it covers every one-cell measurement.

### 4.2 Independently refreshed full secrets

**Theorem 2 (September 2026).** Keep $b$ fixed, but draw each $s_j$ independently and uniformly within parity class $b$, with independent $x_j$. For $L$ such cells, even a collective POVM has optimum

$$
p_{\rm ALL,refresh}^{(L)}=1-\frac12\left(1-\frac1N\right)^L.
$$

**Proof.** The states are $\eta_b^{\otimes L}$. Their common orthogonal label decomposition has an informative block if any label is $N/2$. There the two hypotheses are orthogonal. On the remaining event, of probability $(1-1/N)^L$, they coincide. Perfect identification on the first event and a fair guess on the second is optimal, and the product decoder achieves it.

Consequently, this repair makes the baseline valid but removes the collective accuracy advantage. Neither theorem tensorizes through the original reused-secret mixture, and neither applies to the different two-cell witness below.

## 5. The phase-twirled two-cell witness

### 5.1 Trusted source and honest measurement

Each fresh round draws $b$, a uniform $s$ of parity $b$, independent $x_1,x_2$, and a hidden common phase $\alpha\in\{0,\pi/2,\pi,3\pi/2\}$. The verifier sends two cells

$$
|\psi^{(\alpha)}_{x_j,s}\rangle=
\frac{|0\rangle|x_j\rangle+e^{i\alpha}|1\rangle|x_j+s\rangle}{\sqrt2},\qquad j=1,2.
$$

The inputs are product across the two cells conditional on all preparation variables, although a cell may have internal entanglement. Bob may return $0,1,$ or $\perp$. His honest circuit Fourier-transforms and measures the rotation registers. It returns $\perp$ unless their labels differ by $N/2$, then Bell-measures the reflection qubits: $\Psi^+\mapsto0$, $\Psi^-\mapsto1$, and the other Bell outcomes map to $\perp$. Here $|\Psi^\pm\rangle=(|01\rangle\pm|10\rangle)/\sqrt2$ and $|\Phi^\pm\rangle=(|00\rangle\pm|11\rangle)/\sqrt2$.

Preparing states inside a cloud circuit whose description reveals the secret is a circuit demonstration, not this adversarial experiment. Trusted preparation and protected preparation records are material assumptions.

### 5.2 Complete ensembles, not trusted postselection

Write $K=|01\rangle\langle10|+|10\rangle\langle01|$. In Fourier-label coordinates the complete pair states are

$$
\rho_b=\frac1{N^2}\bigoplus_{k,\ell}\frac{I_4+\gamma_b(\ell-k)K}{4},\qquad
\gamma_b(d)=\begin{cases}1,&d=0,\\(-1)^b,&d=N/2,\\0,&\text{otherwise}.
\end{cases}
$$

Averaging over independent $x_j$ makes the Fourier labels classical. Averaging over $\alpha$ removes coherences between distinct excitation-number sectors, leaving only $K$. The parity-restricted sum over $s$ gives $\gamma_b$. Every one-cell marginal is maximally mixed, and only complementary-label blocks differ between parities.

The collision states are

$$
\sigma_0=\tfrac14|00\rangle\langle00|+\tfrac12|\Psi^+\rangle\langle\Psi^+|+\tfrac14|11\rangle\langle11|,
$$
$$
\sigma_1=\tfrac14|00\rangle\langle00|+\tfrac12|\Psi^-\rangle\langle\Psi^-|+\tfrac14|11\rangle\langle11|.
$$

Complementary labels occur with probability $1/N$. Their exclusive Bell outcome has probability $1/2$, giving $c=1/(2N)$ and $w=0$. The receiver's declared Fourier labels need not be trusted: the bounds below optimize the complete POVM on both full cells.

### 5.3 A precisely specified phase-noise model

For $0\le v\le1$, independently apply an unreported $Z$ to the second reflection qubit with probability $(1-v)/2$. This replaces $K$ by $vK$ in every Fourier block, defining $\rho_b(v)$. The parameter $v$ is an externally justified source property, not a visibility fitted only to the untrusted receiver's answers. A general preparation error, phase mismatch, or readout error need not belong to this family. In a complementary block, $\sigma_b(v)=[I_4+(-1)^b vK]/4$.

## 6. Exact confidence-rate frontiers and the PPT certificate

Let $a=1/(2N)$.

**Theorem 3 (September 2026).** At any fixed total answer rate $0<q\le1$ for $\rho_b(v)$,

$$
c_{\rm G}^{\max}(q,v)=\frac{q+v\min(q,a)}2,
$$
$$
c_{\rm SEP}^{\max}(q,v)=c_{\rm PPT}^{\max}(q,v)=c_{\rm LOCC}^{\max}(q,v)
=\frac{q+v\min(q/2,a)}2.
$$

In every case $w=q-c^{\max}$ and $\mathcal C=c^{\max}/q$.

**Global upper bound.** Set $\bar\rho=(\rho_0(v)+\rho_1(v))/2$ and $D=(\rho_0(v)-\rho_1(v))/2$. The full states obey

$$
-v\bar\rho\preceq D\preceq v\bar\rho,\qquad \|D\|_1=va.
$$

For effects $M_0,M_1$, positivity gives $c-w=\mathrm{Tr}[(M_0-M_1)D]\le vq$. Also $-I\preceq M_0-M_1\preceq I$, so $c-w\le va$. Combining both yields the global bound, without a prescribed receiver measurement.

**PPT upper bound.** Partial transpose $\Gamma$ is on the second complete cell. Write $P_\chi=|\chi\rangle\langle\chi|$ for a Bell-state projector. The exact two-qubit identities

$$
\frac{I_4}{2}\pm K=P_{\Psi^\pm}+(P_{\Phi^\pm})^\Gamma
$$

supply positive matrices whose sum with a partial transpose is nonnegative on every PPT effect. With $\kappa_v=(2+v)/(2-v)$,

$$
\kappa_v\sigma_1(v)-\sigma_0(v)
=\frac{v}{2-v}\left[P_{\Psi^-}+(P_{\Phi^-})^\Gamma\right].
$$

The plus version gives the reverse inequality. On all noncomplementary label blocks the two states coincide, adding only positive terms. Equivalently, local dephasing of any effect in the label registers leaves its probabilities unchanged and preserves PPT. Thus every PPT conclusive effect obeys the likelihood-ratio bound in both directions. Summing gives $c\le\kappa_v w$, or $c-w\le vq/2$. Together with $c-w\le va$, this proves the restricted bound.

**Attainment and completeness.** On complementary blocks, the two exclusive Bell projectors give $q=a$ and $c-w=va$. Random thinning realizes smaller $q$; random guesses from the complementary measurement remainder realize larger $q$, adding zero net advantage. All three effects stay positive and sum to identity. For LOCC, locally read the labels and, on complementary blocks, measure both reflections in $X$. Their equal/opposite signs give $q=2a$ and $c-w=va$. Thin these answers or add random answers from noncomplementary blocks. This is a complete LOCC POVM at every $q$, so the bound for the larger PPT class is attained even by LOCC.

At $v=1$, any positive ideal score $c-3w$ requires a negative partial transpose in at least one effective conclusive effect. This is sufficient certification under trusted inputs, not measurement tomography and not a test that detects every NPT effect. The repeated-round operational null below is not broadened to arbitrary PPT instruments.

For $N=2$, the ideal confidence frontier is:

| Total $q$ | Unrestricted | SEP / PPT / LOCC |
|---|---:|---:|
| $1/8$ | $1$ | $3/4$ |
| $1/4$ | $1$ | $3/4$ |
| $3/8$ | $5/6$ | $3/4$ |
| $1/2$ | $3/4$ | $3/4$ |
| $1$ | $5/8$ | $5/8$ |

The ideal gap vanishes for $q\ge1/N$. Its maximum is $1/4$; increasing $N$ lowers the useful answer rate without enlarging that gap. The maximum zero-error rate is $1/(2N)$, requiring $2NC$ rounds on average for $C$ honest conclusive answers. A direct trusted pair of equatorial reflection states realizes the collision ensemble without the $1/N$ label-selection cost. The DCP construction is an embedding connected to the original project, not a resource-minimal primitive or evidence of computational hardness.

For $v<1$ both parity states are full rank, so positive-rate, exactly zero-error discrimination is impossible. Their small-rate optimal confidences are $(1+v)/2$ and $1/2+v/4$. The standard Bell score $c-3w=a(2v-1)$ is positive only for $v>1/2$. The different score $c-\kappa_v w$ requires the stated external source calibration. At $q=1$, joint and restricted accuracy agree: $1/2+v/(4N)$.

## 7. Sequential certification with an ideal source

### 7.1 The operational null and filtration

The receiver begins with memory separable across the two cell-plus-memory sides. Each outcome map has a product-Kraus form

$$
\mathcal I_z(X)=\sum_j(A_{zj}\otimes B_{zj})X(A_{zj}\otimes B_{zj})^\dagger,
$$

with the sum over outcomes trace preserving. This is the meaning of a separable instrument here; merely requiring separable visible effects while allowing arbitrary memory updates is insufficient. LOCC instruments are included. Local ancillas, classical communication, and history-dependent strategies are unrestricted within this class. There is no pre-shared entanglement across the partition.

Every round's preparation is fresh and independent of the past; the receiver must answer before seeing the next pair. Use a filtration containing all past outcomes, preparation variables, and correctness indicators, whether or not these are disclosed. Ideal sources are product across the cells conditional on preparation variables, and separable instruments preserve conditional memory separability. Thus the effective current-round POVM remains separable after each history $h$, and

$$
c(h)\le3w(h).
$$

This is why adaptive memory does not invalidate the single-round bound. Allowing the receiver to accumulate undisclosed future pairs is a different experiment.

### 7.2 A predeclared conclusive-count test

Choose $C\ge1$, $0\le E\le C$, and $R\ge C$ before collecting data. Stop at the first $C$ conclusive answers or at $R$ total rounds. Fewer than $C$ conclusive answers means no certificate. Otherwise, accept only if the first $C$ answers contain at most $E$ errors.

**Theorem 4 (August result, sequential formulation clarified in September).** The false-certification probability under the operational null is at most

$$
B(C,E)=\sum_{j=0}^{E}\binom Cj(1/4)^j(3/4)^{C-j}.
$$

**Proof without completion postselection.** Let

$$
h(k,e)=\Pr[\mathrm{Binomial}(C-k,1/4)\le E-e],
$$

with $h(C,e)=\mathbf1_{e\le E}$. Its recursion is $h(k,e)=\tfrac34h(k+1,e)+\tfrac14h(k+1,e+1)$. Because $h(k+1,e)\ge h(k+1,e+1)$, replacing the conditional error rate by any value at least $1/4$ cannot increase its next-step expectation. Abstention leaves $(k,e)$ unchanged. Therefore $h(k_t,e_t)$ is a bounded nonnegative supermartingale over actual rounds, stopped at completion or cutoff. The acceptance indicator is at most its terminal value, including on incomplete runs. Its expectation is bounded by $h(0,0)=B(C,E)$.

For zero errors among 50 conclusive answers, $B=(3/4)^{50}\simeq5.6632\times10^{-7}$. At most 20 errors among 200 gives $B\simeq7.0323\times10^{-8}$. No independent-error or fair-sampling assumption is used. These are unconditional single-run guarantees, not guarantees after retaining only completed experiments. Repeatedly restarting and reporting only successful runs requires multiple-testing control.

## 8. Source imperfections and calibrated statistics

### 8.1 A common separable channel preserves the original null

Suppose a fixed trace-preserving source channel $\Lambda$ has product Kraus operators and is independent of every hidden preparation variable. On actual states $\Lambda(\rho_b)$, a separable receiver still obeys $c\le3w$: the effective ideal-input effects $\Lambda^*(M_z)$ remain positive and separable and sum to identity. This includes local dephasing, depolarization, damping, and erasure when all flags are modeled and the common-channel premise holds. Honest performance can deteriorate without changing soundness. Calling an imperfection local does not establish that premise.

### 8.2 Arbitrarily small leakage invalidates a uniform confidence ceiling

Embed ideal inputs in a larger local space with a fixed no-leak flag. With probability $1-\epsilon$, send the ideal state; otherwise send a product state with an orthogonal locally readable flag encoding $b$. For each parity the trace-distance error is exactly $\epsilon$, but a local receiver answering only on flagged rounds has $q=\epsilon$ and confidence one. The faulty inputs themselves are still separable.

Thus a nonzero trace-distance error budget alone cannot preserve the ideal 75 percent ceiling uniformly as $q\to0$. Abstention can select rare preparation leakage. This explicit example is consistent with the broader noisy-input loophole literature [9]. All receiver-accessible side channels belong in the source model.

### 8.3 A conservative population allowance

Let $D(\widetilde\rho_b,\rho_b)\le\epsilon_b$ on the complete receiver-accessible input, where $D$ is half the trace norm. For a separable effective POVM,

$$
c-3w\le\beta,\qquad \beta=2(\epsilon_0+\epsilon_1).
$$

For parity $b$, the score operator $A_b=M_b-3M_{1-b}$ has spectrum in $[-3,1]$. A trace-distance perturbation of size $\epsilon_b$ changes its mean by at most $4\epsilon_b$. Averaging over equal priors proves the allowance. Therefore

$$
\mathcal C_{\rm SEP}\le\min\left\{1,\frac34+\frac{\epsilon_0+\epsilon_1}{2q}\right\}.
$$

These are conservative bounds, not asserted to be tight for all source-error sets.

### 8.4 A fixed-total-round certificate

Predeclare $R$ total rounds and count every outcome, including losses. Score each as $Z_t=1,-3,0$ for correct, wrong, or inconclusive. The error budgets and effective separability premise must hold conditionally on every past history; an average-state calibration alone is insufficient.

A sufficient operational source condition is a fresh actual pair independent of retained receiver memory conditional on each history and current parity, separable across the two sides, with the stated trace-distance budgets. Combined with separable initial memory and product-Kraus instruments, this preserves the required effective separability. Alternatively, reestablish fresh separable receiver memory each round while still enforcing the conditional source calibration. Trace-distance closeness does not itself guarantee separable memory: a faulty entangled input could be retained as a resource.

Under these assumptions $\mathbb E[Z_t\mid\mathcal F_{t-1}]\le\beta$. Conditional Hoeffding's lemma for an interval of width four gives

$$
\mathbb E[e^{\lambda(Z_t-\beta)}\mid\mathcal F_{t-1}]\le e^{2\lambda^2},\qquad\lambda\ge0.
$$

Multiplication over rounds, Markov's inequality, and optimization at $\lambda=(z-\beta)/4$ yield

$$
\Pr_{\rm null}[\overline Z\ge z]\le\exp[-R(z-\beta)^2/8],\qquad z>\beta.
$$

Use bound one for $z\le\beta$. The general concentration method is established [10]; this result supplies the DCP-specific conditional score allowance. It is fixed-horizon, not anytime-valid.

An illustrative, nonexperimental record with 2,500 correct answers, zero errors, and 7,500 abstentions has $z=1/4$. If $\epsilon_0=\epsilon_1=0.01$ are externally justified, $\beta=0.04$ and the log-bound is $-55.125$. No such hardware calibration or experiment has been performed here. If calibration is itself statistical, its failure probability must be incorporated by a separately justified joint error analysis; it is not included in this exponent. Neither the conclusive count nor the observed device visibility can replace the predeclared $R$ or the source-error premise.

The conclusive-count test of Section 7 remains valid for ideal inputs and the common separable-channel case of Section 8.1. It must not be reused without adjustment for arbitrary preparation leakage.

## 9. Minimal circuit and implementation boundary

At $N=2$, each cell has two qubits. In cell $j$, prepare rotation bit $x_j$, apply $H$ and $S^a$ to its reflection qubit, with $a\in\{0,1,2,3\}$ shared, and apply a reflection-to-rotation CNOT only when $s=1$. This prepares the required phase-twirled input. Bob applies $H$ to both rotation qubits, then a CNOT from reflection 1 to reflection 2 followed by $H$ on reflection 1. Measure all four qubits at the end.

Return a bit only if the two measured rotation bits differ and reflection 2 is measured as $1$. The output is the measured reflection-1 bit; all other outcomes are inconclusive. Deferring rotation readout is valid because its gates and the reflection Bell measurement act on disjoint registers.

A complete ideal round needs four qubits, at most three CNOTs including trusted preparation, no extra ancilla, only Clifford gates, and no dynamic feed-forward. Its exhaustive statevector average is $(c,w,1-q)=(1/4,0,3/4)$. This is a small circuit. Protecting the preparation randomness and justifying the input model are separate requirements, not demonstrated by circuit simulation.

## 10. Evidence, reproducibility, and release disposition

The release review checked each September theorem's quantifiers and assumptions, complete POVM attainments including abstention, transition rates, both PPT operator identities, and the actual-round stopping argument. No theorem or probability formula required alteration. In particular, the source-error guarantee is conditional and calibrated, not a claim of experimentally demonstrated robustness.

The existing 98-test suite, six-record validator, 1,268 individual field-mutation checks, 71-file source manifest, and 96-case raw-state optimization audit passed for the reviewed version 1.2.0. The release adds a separate audit with no imports from the analytical package: 30 full-space PPT certificates in computational coordinates, nine raw tensor-power discrimination cases, 360 exact adaptive-stopping optimizations, and 144 conditional moment-bound vertex checks. These supplement the proofs; they are not independent human peer review or formal proof-assistant verification.

The full-space audit tests the matrix certificates without assuming a block-diagonal receiver measurement. The optimization audit separately uses a justified Bell-diagonal reduction. Neither numerical exercise replaces the analytic argument valid for all $n$.

From a source checkout:

```bash
python -m pip install -e '.[test,audit]'
python -m pytest -q
python scripts/verify_historical_files.py
python scripts/verify_checksums.py
python scripts/validate_committed_results.py
python scripts/audit_scientific_frontier.py
OPENBLAS_NUM_THREADS=1 python scripts/audit_release_science.py
```

Exact rational results are checked exactly. Floating-point diagnostics use stated tolerances; fixed-seed Monte Carlo records are archived with trial counts and uncertainty, and fast validation does not rerun the large experiments. The binomial API supplies a log-probability interface and explicitly rejects positive probabilities that underflow in ordinary floating point. Numerical p-value evaluations are not interval-arithmetic certificates. Release checksums establish file identity, not scientific truth.

The six original scripts and dated August correction remain unchanged. The technical scope is frozen for this release: no additional hardware experiment, larger-DCP proposal, or publication campaign is implied. New evidence can motivate a later version without altering the archived release.

## 11. Chronology, related work, and responsibility

The original DCP preprint appeared on 14 February 2022 and the PRA article on 22 July 2022 [1]. It was an earlier DCP-specific trusted-input attempt to test joint processing, but it did not contain the sound maximum-confidence, phase-twirled, PPT, or source-error theorems in this note.

Maximum-confidence discrimination [2], unambiguous state comparison [3], fixed-inconclusive-rate optimization [4], and trusted-quantum-input methods [5] are established prior frameworks. Flatt and colleagues posted semi-device-independent maximum-confidence certification against noncontextual models on 17 December 2021 [6]. Ha and Kim developed nonlocal maximum-confidence bounds in 2024 [7].

Lee and Bae's preprint was first posted on 11 June 2026; this review uses version 2 of 15 June [8]. Their antiparallel-state example separates unrestricted and separable maximum confidence, including one versus three quarters at suitable outcome rates. It is directly relevant prior art. They optimize confidence for a specified individual outcome rate; this note optimizes binary average confidence at total rate $q$. Their numerical thresholds must not be substituted for the DCP total-rate cutoffs. Their paper does not cite the DCP article, but conceptual similarity and chronology do not establish influence or a citation obligation. No dependence or fault is alleged, and no novelty is claimed for the general certification framework.

The August 2026 author reanalysis established the shared-secret counterexample and ideal witness. Its public methodology credits substantial assistance from **GPT-5.6 Pro** in literature research, derivations, adversarial checking, code, and documentation. The global one-cell theorem, refreshed-secret limitation, exact rate frontiers, PPT extension, and source-error analysis are dated **7 September 2026**, not retroactively attributed to the 2022 article or August note. This consolidation and release review are also AI-assisted.

Ruge Lin retains responsibility for claim selection and accuracy. AI systems are not authors and cannot assume scientific responsibility. Repeated AI-assisted audits are not independent peer review. No exhaustive novelty determination, universal-computation certificate, quantum speedup, calibrated experimental result, or absence of unmodeled side channels is claimed.

## References

[1] R. Lin and W. Wen, *Quantum computation capability verification protocol for noisy intermediate-scale quantum devices with the dihedral coset problem*, Physical Review A **106**, 012430 (2022). [DOI](https://doi.org/10.1103/PhysRevA.106.012430); [arXiv:2202.06984v3](https://arxiv.org/abs/2202.06984v3).

[2] S. Croke, E. Andersson, S. M. Barnett, C. R. Gilson, and J. Jeffers, *Maximum Confidence Quantum Measurements*, Physical Review Letters **96**, 070401 (2006). [DOI](https://doi.org/10.1103/PhysRevLett.96.070401).

[3] S. M. Barnett, A. Chefles, and I. Jex, *Comparison of two unknown pure quantum states*, Physics Letters A **307**, 189-195 (2003). [arXiv:quant-ph/0202087](https://arxiv.org/abs/quant-ph/0202087).

[4] E. Bagan, R. Muñoz-Tapia, G. A. Olivares-Rentería, and J. A. Bergou, *Optimal discrimination of quantum states with a fixed rate of inconclusive outcomes*, Physical Review A **86**, 040303(R) (2012). [DOI](https://doi.org/10.1103/PhysRevA.86.040303).

[5] F. Buscemi, *All Entangled Quantum States Are Nonlocal*, Physical Review Letters **108**, 200401 (2012). [arXiv:1106.6095](https://arxiv.org/abs/1106.6095).

[6] K. Flatt, H. Lee, C. Roch i Carceller, J. B. Brask, and J. Bae, *Contextual Advantages and Certification for Maximum-Confidence Discrimination*, PRX Quantum **3**, 030337 (2022). [DOI](https://doi.org/10.1103/PRXQuantum.3.030337); [arXiv:2112.09626](https://arxiv.org/abs/2112.09626).

[7] D. Ha and J. S. Kim, *Entanglement witness and nonlocality in confidence of measurement from multipartite quantum state discrimination*, Scientific Reports **14**, 23815 (2024). [DOI](https://doi.org/10.1038/s41598-024-75149-y).

[8] H. Lee and J. Bae, *Semi-Device-Independent Certification for Nonlocality without Entanglement*, [arXiv:2606.13667v2](https://arxiv.org/abs/2606.13667v2) (15 June 2026; first version 11 June 2026).

[9] K. Sen, C. Srivastava, S. Mal, A. Sen De, and U. Sen, *Noisy quantum input loophole in measurement-device-independent entanglement witnesses*, Physical Review A **104**, 012429 (2021). [DOI](https://doi.org/10.1103/PhysRevA.104.012429); [arXiv:2012.09089](https://arxiv.org/abs/2012.09089).

[10] S. R. Howard, A. Ramdas, J. McAuliffe, and J. Sekhon, *Time-uniform Chernoff bounds via nonnegative supermartingales*, Probability Surveys **17**, 257-317 (2020). [DOI](https://doi.org/10.1214/18-PS321).
