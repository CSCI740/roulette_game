# Random Number Generator
import math
import random

class RandomNumGen:
    def __init__(self, probabilities):
        """
        Initialize the LCM-based random number generator for discrete probabilities.
        
        :param probabilities: A dictionary where keys are outcomes (k) and values are tuples (r_k, q_k).
                              - k: The discrete outcome.
                              - r_k: The numerator of the probability (relative weight of the outcome).
                              - q_k: The denominator of the probability (total weight of all outcomes).
        
        Variables:
        - self.probabilities: Stores the input dictionary of probabilities.
        - self.Q: The least common multiple (LCM) of all q_k values in the probabilities.
        - self.mapping_table: A list (mapping table) that maps uniformly random integers to outcomes 
                              based on their probabilities.
        """
        self.probabilities = probabilities
        self.Q = self.calculate_lcm([q_k for _, q_k in probabilities.values()])
        self.mapping_table = self.build_mapping_table()

    @staticmethod
    def calculate_lcm(numbers):
        """
        Calculate the least common multiple (LCM) of a list of numbers.
        
        :param numbers: A list of integers for which the LCM will be computed.
        :return: The least common multiple of the numbers.
        
        Variables:
        - lcm: A variable to hold the running LCM during computation.
        - num: Each number in the input list is iterated over to compute the LCM.
        """
        lcm = numbers[0]  # Initialize LCM with the first number in the list.
        for num in numbers[1:]:
            lcm = lcm * num // math.gcd(lcm, num)  # Compute LCM using the formula.
        return lcm

    def build_mapping_table(self):
        """
        Build the mapping table (A[i]) based on probabilities.
        The table ensures that each outcome k appears in the table in proportion to its probability.

        :return: A list (mapping table) where each index maps to a specific outcome k.

        Variables:
        - mapping_table: A list that stores the mapping from indices to outcomes.
        - k: A key representing an outcome from the probabilities dictionary.
        - r_k: The numerator of the probability of k.
        - q_k: The denominator of the probability of k.
        - count: The number of slots in the mapping table that should be assigned to outcome k,
                 calculated as r_k * (Q / q_k).
        """
        mapping_table = []  # Initialize an empty list for the mapping table.
        for k, (r_k, q_k) in self.probabilities.items():
            count = r_k * (self.Q // q_k)  # Compute the number of slots for outcome k.
            mapping_table.extend([k] * count)  # Add k to the table `count` times.
        return mapping_table

    def randint(self):
        """
        Generate a random outcome k based on the discrete probability distribution.

        :return: A random outcome k, determined by sampling from the mapping table.

        Variables:
        - i: A random index generated uniformly in the range [0, Q-1].
        """
        i = random.randint(0, self.Q - 1)  # Randomly sample an index between 0 and Q-1.
        return self.mapping_table[i]  # Return the outcome corresponding to the sampled index.



""" Example Usage:
# Define probabilities as {k: (r_k, q_k)}, where p_k = r_k / q_k
probabilities = {
    0: (3, 14),  # Outcome 0 has a probability of 3/14
    1: (4, 14),  # Outcome 1 has a probability of 4/14
    2: (2, 14),  # Outcome 2 has a probability of 2/14
    3: (5, 14),  # Outcome 3 has a probability of 5/14
}

# Create the random number generator
rng = RandomNumGen(probabilities)

# Generate 10 random outcomes
random_outcomes = [rng.randint() for _ in range(10)]
print(random_outcomes)

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

"""
