# Minimal Four-Qubit Circuit

Choose \(N=2\). Use qubit order

```text
r1, q1, r2, q2
```

where each \(r_j\) is a reflection qubit and each \(q_j\) is a one-qubit rotation register.

## Trusted preparation

For each cell:

1. prepare \(q_j\) in \(|x_j\rangle\);
2. apply \(H\) to \(r_j\);
3. apply the same hidden phase \(S^a\), with \(a\in\{0,1,2,3\}\), to both reflection qubits;
4. if \(s=1\), apply CNOT from \(r_j\) to \(q_j\).

## Measurement circuit

1. apply \(H\) to \(q_1,q_2\), which is the \(N=2\) Fourier transform;
2. Bell-measure \(r_1,r_2\) by CNOT \(r_1\to r_2\), then \(H\) on \(r_1\);
3. measure all four qubits in the computational basis.

All operations are static. No mid-circuit measurement is needed.

## Classical decoder

Let the final bits still be denoted \(r_1,q_1,r_2,q_2\).

- require the complementary-label condition \(q_1\ne q_2\);
- require the Bell-\(\Psi\) indicator \(r_2=1\);
- if both conditions hold, return \(r_1\);
- otherwise return \(\perp\).

Under the conventional Bell transform,

```text
Psi+ -> r1 r2 = 01 -> answer 0
Psi- -> r1 r2 = 11 -> answer 1
```

## Maximum resources per round

| Resource | Count |
|---|---:|
| Qubits | 4 |
| Ancillas | 0 |
| Preparation CNOTs | at most 2 |
| Bell-measurement CNOTs | 1 |
| Total CNOTs | at most 3 |
| Non-Clifford gates | 0 |
| Mid-circuit measurements | 0 |
| Dynamic feed-forward | 0 |

The implementation in `src/dcp_challenge/minimal_circuit.py` exhaustively averages all values of \(s,x_1,x_2\), and the four shared phases.
