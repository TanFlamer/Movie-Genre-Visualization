import math
import numpy as np
import scipy


# Get statistics
def get_statistics(results, t_test_values):
    runs = len(results)
    if runs <= 1:
        result = 0 if runs == 0 else results[0]
        return [result, 0, result, 0, result, result, 0]
    else:
        # Get sample sum
        sample_sum = sum(results)
        # Get sample variance
        sample_variance = (sum(np.square(results)) - (sample_sum * sample_sum) / runs) / (runs - 1)
        # Get sample mean
        mean = sample_sum / runs
        # Get sample standard deviation
        std = math.sqrt(sample_variance)
        # Get quartiles
        [median, inter_quartile_range] = get_quartiles(results)
        # Get t-value
        t_value = calculate_t_value(t_test_values, [mean, std, runs])
        # Return results
        return [mean, std, median, inter_quartile_range, max(results), min(results), t_value]


# Get the median and inter_quartile range
def get_quartiles(results):
    # Get intermediate data
    def get_data(parity): return [(len(results) - parity) // 2, parity, (len(results) + parity) // 2 - 1]
    # Get average
    def get_average(index): return (results[index] + results[index + 1]) / 2
    # Get results
    def get_results(point, parity): return results[point] if parity else get_average(point)

    # Sort results
    results.sort()

    # Get median
    median_parity = len(results) % 2
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
def calculate_t_value(t_test_values, second_results):
    # Unpack first sample data
    [confidence_level, first_mean, first_std, first_size] = t_test_values
    # Unpack second sample data
    [second_mean, second_std, second_size] = second_results

    # Get pooled standard deviation from both samples
    pooled_std = get_pooled_std(first_std, first_size, second_std, second_size)
    # Calculate intermediate data of t-test
    t_test_bottom = pooled_std * math.sqrt(1 / first_size + 1 / second_size)
    # Get difference in mean of both samples
    mean_difference = first_mean - second_mean
    # Get critical value from confidence level and degrees of freedom
    critical_value = scipy.stats.t.ppf(confidence_level, first_size + second_size - 2)

    # Calculate the expected difference between the two samples
    difference = mean_difference - critical_value * t_test_bottom
    # Return the expected difference between the two samples or 0 if t-test fails
    return max(difference, 0)


def get_pooled_std(first_std, first_size, second_std, second_size):
    # Get intermediate data
    def get_data(std, size): return (std * std) * (size - 1)
    # Get intermediate data of samples
    [first_data, second_data] = [get_data(first_std, first_size), get_data(second_std, second_size)]
    # Get pooled variance from both samples
    pooled_variance = (first_data + second_data) / (first_size + second_size - 2)
    # Get pooled standard deviation from both samples
    return math.sqrt(pooled_variance)


# Print out all results of experiment
def print_results(results, t_test_values):
    # Get statistics
    [mean, std, median, inter_quartile_range, max_val,
     min_val, t_value] = get_statistics(results, t_test_values)
    # Print statistics
    print("\nResults = " + results)
    print("Mean = %.2f" % mean)
    print("Standard Deviation = %.2f" % std)
    print("Median = %.1f" % median)
    print("Inter-Quartile Range = %.1f" % inter_quartile_range)
    print("Max = %d" % max_val)
    print("Min = %d" % min_val)
    print("Difference = %.2f" % t_value)
