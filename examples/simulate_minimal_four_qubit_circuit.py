from dcp_challenge.minimal_circuit import decoded_statistics

result = decoded_statistics()
print("Averaged minimal four-qubit circuit")
for key, value in result.items():
    print(f"  {key}: {value:.12f}")
