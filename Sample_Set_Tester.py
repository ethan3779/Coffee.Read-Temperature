import asyncio
import sys
import statistics
import time
from Read_Port import read_port_data


# Define a function to determine whether there is an outlier in a sample set list.
def contains_outlier(sample_set: list):
    """
    Function determines whether or not a sample set list contains an outlier. If this is the case, the function will
    return True. Otherwise, False is returned.
    :param sample_set: list of floats or integers
    :return: boolean
    """
    # Determine minimum, maximum, mean, and standard deviation of the sample set.
    min_value = min(sample_set)
    max_value = max(sample_set)
    mean_value = statistics.mean(sample_set)
    std_dev = statistics.stdev(sample_set)

    # Attempt to identify outlier in sample set
    if (mean_value - min_value > std_dev) or (max_value - mean_value > std_dev):
        return True
    else:
        return False


def get_outlier(sample_set: list):
    """
    Function determines the outlier(s), if applicable, in a sample set and returns it. If there is no outlier, the
    function returns None.
    :param sample_set: list of floats or integers
    :return: list
    """
    # Establish the standard deviation multiplier which will be used to consider what is an error.
    num_std_dev = 2

    # Determine minimum, maximum, mean, and standard deviation of the sample set.
    min_value = min(sample_set)
    max_value = max(sample_set)
    mean_value = statistics.mean(sample_set)
    std_dev = statistics.stdev(sample_set)

    # Establish an empty list for results
    result_list = []

    # Attempt to identify outlier in sample set
    if mean_value - min_value > std_dev * num_std_dev:
        result_list.append(min_value)
    if max_value - mean_value > std_dev * num_std_dev:
        result_list.append(max_value)

    return result_list


# Establish list of likely COM ports and baud rate utilized.
port_list = ["COM3", "COM4", "COM5", "COM6"]
baud = 9600

# Set the output counts to zero.
num_data_point = 0
num_errors = 0

# Establish sample size and increment collected.
sample_size = 20
seconds_increment = 3

# Create a list for temperatures and add the number of temperatures equivalent to the sample size.
all_error_list = []

# Continually execute until stopped.
while True:
    # Create a list for temperatures and add the number of temperatures equivalent to the sample size.
    temperature_sample_list = []

    # Add ten data points to the temperature list for analysis.
    while len(temperature_sample_list) < sample_size:
        temperature = read_port_data(port_list, baud)
        temperature_sample_list.append(float(temperature))

    # Increment the total number of data points pulled for sampling.
    num_data_point = num_data_point + len(temperature_sample_list)

    # Identify any outliers and if any are found, increment the total number of errors count and add the data point
    # to the error list.
    if len(get_outlier(temperature_sample_list)) > 0:
        num_errors = num_errors + len(get_outlier(temperature_sample_list))
        all_error_list.append(get_outlier(temperature_sample_list))

    # Print the output to the screen.
    print(f"Number of Data Points Analyzed: {num_data_point} - {temperature_sample_list}")
    print(f"Number of Errors: {num_errors} - {all_error_list}")
    print(f"Error Rate: {(num_errors / num_data_point) * 100}%")

