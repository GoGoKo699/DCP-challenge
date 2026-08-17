# Audit of the IBM Reconstruction

## 1. Physical and coded variables

In the paper, the eight cases A-H are indexed by the prepared values `(s,x0,x1)`. The postselection event is defined by measured output bits:

\[
q_0\ne q_3,\qquad q_2=1.
\]

In `IBM.py`, however, the same prepared variables `x0,x1` are used in

```python
if x0 != x1:
```

as the collision test. These are not the measured Fourier labels. In an ideal `N=2` DCP sample, the Fourier label is uniformly random and is not equal to the preparation label `x`.

## 2. Consequence

The legacy simulation permits a definitive result only for cases B, C, F, and G. Cases A, D, E, and H are never used in the simulated successful branch, despite having valid postselected hardware counts in the source data.

The code also replaces the empirically observed postselection rate with an ideal independent probability of `1/4`.

## 3. Aggregate-data reconstruction

Each case contains five 1024-shot experiments. The numbers in `IBM.py` give:

- the total selected counts (`q0 != q3` and `q2=1`);
- the number of selected counts with `q1=1`.

For each case, the three aggregate probabilities—correct selected, wrong selected, and not selected—can therefore be reconstructed. Averaging uniformly over the four preparation cases for each `s` and applying the published `t=3` retry rule gives

\[
 p_{\rm IBM,aggregate}=0.7439808125.
\]

For comparison:

\[
 p_{\rm legacy\ code}=0.7545878022,
\qquad
 p_{\rm ideal}=0.7890625.
\]

A multinomial bootstrap of the stored aggregate counts gives an indicative 95% interval `[0.739820,0.748090]` (100,000 multinomial resamples; seed `20260817`) for the aggregate reconstruction. This interval accounts for finite shot counts, not hardware drift or correlations between shots.

## 4. Interpretation

The hardware data still shows that the selected Bell-type branch has nontrivial parity fidelity. It should not be described as a direct end-to-end execution of the challenge, and Figure 9 should not be regenerated from the current legacy logic.

A fully faithful reanalysis would ideally use raw shot records and timestamps. Those are not present in the repository, so the aggregate reconstruction above is the strongest correction supported by the archived data.
