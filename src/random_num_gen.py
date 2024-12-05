# Random Number Generator

import random
import math

class RandomNumGen:
    #def __init__(self):

    # def randint(self, lower, upper):
    #     return random.randint(lower, upper)       

    def __init__(self, lower=None, upper=None, probabilities=None):
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
        if probabilities:
            self.probabilities = probabilities
        elif lower is not None and upper is not None:
            # Generate uniform probabilities for the range [lower, upper]
            denominator=upper - lower + 1
            print("denominator")
            print(denominator)
            self.probabilities = {k: (1, (denominator)) for k in range(lower, upper + 1)}
        else:
            raise ValueError("You must either provide 'probabilities' or both 'lower' and 'upper' bounds for uniform probabilities.")
        
        denominators = [q_k for _, q_k in self.probabilities.values()]
        self.Q = self.calculate_lcm(denominators)
        self.mapping_table = self.build_mapping_table()


    def calculate_lcm(self, numbers):
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
        print("mapping_table")
        print(mapping_table)
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

