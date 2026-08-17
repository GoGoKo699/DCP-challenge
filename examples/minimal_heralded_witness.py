from dcp_challenge.heralded_witness import (
    finite_sample_examples,
    minimal_four_qubit_resources,
    witness_summary,
)

print("N=2 ideal witness summary:")
for key, value in witness_summary(1).items():
    print(f"  {key}: {value}")
print("Finite-sample examples:", finite_sample_examples())
print("Maximum circuit resources:", minimal_four_qubit_resources())
