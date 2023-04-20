import math

import numpy as np
import scipy


class Results:
    def __init__(self, results, episodes, t_test_values):
        # Unpack data
        self.results = results
        self.episodes = episodes
        [self.confidence_level, self.first_mean, self.first_std, self.first_size] = t_test_values
        # Sort results
        self.results.sort()
        # Print results
        self.print_results()

    def print_results(self):
        # Get statistics
        [mean, std, median, inter_quartile_range,
         max_val, min_val, t_value] = self.get_statistics()
        # Get failed runs
        failed_runs = self.results.count(self.episodes)
        # Print statistics
        print("\nResults = " + self.results)
        print("Mean = %.2f" % mean)
        print("Standard Deviation = %.2f" % std)
        print("Median = %.1f" % median)
        print("Inter-Quartile Range = %.1f" % inter_quartile_range)
        print("Max = %d" % max_val)
        print("Min = %d" % min_val)
        print("Difference = %.2f" % t_value)
        print("Failed runs = %d" % failed_runs)

    def get_statistics(self):
        runs = len(self.results)
        if runs <= 1:
            result = 0 if runs == 0 else self.results[0]
            return [result, 0, result, 0, result, result, 0]
        else:
            # Get sample sum
            sample_sum = sum(self.results)
            # Get sum squared
            sum_squared = sum(np.square(self.results))
            # Get sample variance
            sample_variance = (sum_squared - (sample_sum * sample_sum) / runs) / (runs - 1)
            # Get sample mean
            mean = sample_sum / runs
            # Get sample standard deviation
            std = math.sqrt(sample_variance)
            # Get quartiles
            [median, inter_quartile_range] = self.get_quartiles()
            # Get t-value
            t_value = self.calculate_t_value([mean, std, runs])
            # Return results
            return [mean, std, median, inter_quartile_range, max(self.results), min(self.results), t_value]

    def get_quartiles(self):
        # Get intermediate data
        def get_data(parity): return [(len(self.results) - parity) // 2, parity, (len(self.results) + parity) // 2 - 1]
        # Get average
        def get_average(index): return (self.results[index] + self.results[index + 1]) / 2
        # Get results
        def get_results(point, parity): return self.results[point] if parity else get_average(point)

        # Get median
        median_parity = len(self.results) % 2
        [runs_halved, offset, midpoint] = get_data(median_parity)
        median = get_results(midpoint, median_parity)

        # Get inter-quartile range
        quarter_parity = runs_halved % 2
        quarter_point = (runs_halved + quarter_parity) // 2 - 1
        first_quartile = get_results(quarter_point, quarter_parity)
        third_quartile = get_results(quarter_point + runs_halved + offset, quarter_parity)

        # Return results
        return median, third_quartile - first_quartile

    # Calculate the expected difference between the two samples using the t-test
    def calculate_t_value(self, second_results):
        # Unpack second sample data
        [second_mean, second_std, second_size] = second_results

        # Get pooled standard deviation from both samples
        pooled_std = self.get_pooled_std(second_std, second_size)
        # Calculate intermediate data of t-test
        t_test_bottom = pooled_std * math.sqrt(1 / self.first_size + 1 / second_size)
        # Get difference in mean of both samples
        mean_difference = self.first_mean - second_mean
        # Get critical value from confidence level and degrees of freedom
        critical_value = scipy.stats.t.ppf(self.confidence_level, self.first_size + second_size - 2)

        # Calculate the expected difference between the two samples
        difference = mean_difference - critical_value * t_test_bottom
        # Return the expected difference between the two samples or 0 if t-test fails
        return max(difference, 0)

    def get_pooled_std(self, second_std, second_size):
        # Get intermediate data
        def get_data(std, size): return (std * std) * (size - 1)

        # Get intermediate data of samples
        [first_data, second_data] = [get_data(self.first_std, self.first_size), get_data(second_std, second_size)]
        # Get pooled variance from both samples
        pooled_variance = (first_data + second_data) / (self.first_size + second_size - 2)
        # Get pooled standard deviation from both samples
        return math.sqrt(pooled_variance)
