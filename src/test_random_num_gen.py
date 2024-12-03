from random_num_gen import RandomNumGen

# Define probabilities as {k: (r_k, q_k)}, where p_k = r_k / q_k
probabilities = {
    0: (3, 14),  # Outcome 0 has a probability of 3/14
    1: (4, 14),  # Outcome 1 has a probability of 4/14
    2: (2, 14),  # Outcome 2 has a probability of 2/14
    3: (5, 14),  # Outcome 3 has a probability of 5/14
}

# Initialize the random number generator
rng = RandomNumGen(probabilities)

# Generate random outcomes and count their frequencies
outcome_counts = {k: 0 for k in probabilities.keys()}
num_trials = 10000  # Number of samples to generate

for _ in range(num_trials):
    outcome = rng.randint()
    outcome_counts[outcome] += 1

# Display the results
print("\n--- Test Results ---")
print(f"Number of trials: {num_trials}")
for k, count in outcome_counts.items():
    expected_prob = probabilities[k][0] / probabilities[k][1]
    observed_prob = count / num_trials
    print(f"Outcome {k}:")
    print(f"  Expected probability: {expected_prob:.4f}")
    print(f"  Observed probability: {observed_prob:.4f} ({count} occurrences)")
