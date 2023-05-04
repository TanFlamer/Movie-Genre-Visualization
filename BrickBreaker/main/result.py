import math

import numpy as np
import scipy


class Results:
    def __init__(self, results, runs, t_test_values):
        # Unpack results
        self.results = results[:runs]
        # Unpack t-test values
        [self.confidence_level, self.first_mean, self.first_std, self.first_size] = t_test_values
        # Save results
        self.exp_results = self.get_statistics() + [results[runs] - runs]
        # Print results
        self.print_results()

    def print_results(self):
        # Get statistics
        [mean, std, median, inter_quartile_range,
         max_val, min_val, t_value, failed] = self.exp_results
        # Print statistics
        print("\nResults =", self.results)
        print("Mean = %.2f" % mean)
        print("Standard Deviation = %.2f" % std)
        print("Median = %.1f" % median)
        print("Inter-Quartile Range = %.1f" % inter_quartile_range)
        print("Max = %d" % max_val)
        print("Min = %d" % min_val)
        print("Difference = %.2f" % t_value)
        print("Failed runs = %d" % failed)

    def get_statistics(self):
        # Get number of runs
        runs = len(self.results)
        if runs <= 1:
            # Results for 0 and 1 runs
            result = 0 if runs == 0 else self.results[0]
            return [result, 0, result, 0, result, result, 0]
        else:
            # Get sample mean
            mean = np.mean(self.results)
            # Get sample standard deviation
            std = np.std(self.results, ddof=1)
            # Get quartiles
            [min_val, first_q, median, third_q, max_val] = np.quantile(self.results, [0, 0.25, 0.5, 0.75, 1])
            # Get difference
            difference = self.calculate_difference(mean, std, runs)
            # Return results
            return [mean, std, median, third_q - first_q, max_val, min_val, difference]

    def calculate_difference(self, second_mean, second_std, second_size):
        # Get pooled standard deviation of both samples
        pooled_std = self.get_pooled_std(second_std, second_size)
        # Calculate noise of t-test
        noise = pooled_std * math.sqrt(1 / self.first_size + 1 / second_size)
        # Get critical value from confidence level and degrees of freedom
        critical_value = scipy.stats.t.ppf(self.confidence_level, self.first_size + second_size - 2)
        # Calculate the expected difference between the two samples
        difference = (self.first_mean - second_mean) - (critical_value * noise)
        # Return the expected difference or 0 if t-test fails
        return max(difference, 0)

    def get_pooled_std(self, second_std, second_size):
        # Get sum of squares
        def sum_of_square(std, size): return (std * std) * (size - 1)
        # Get sum of squares of samples
        first_data, second_data = sum_of_square(self.first_std, self.first_size), sum_of_square(second_std, second_size)
        # Get pooled variance of both samples
        pooled_variance = (first_data + second_data) / (self.first_size + second_size - 2)
        # Get pooled standard deviation of both samples
        return math.sqrt(pooled_variance)
