import datetime
import os
from signal import signal, SIGINT
import statistics
import sys
import time
from Read_Port import read_port_data


# Define a function to stop the script when a keyboard interruption takes place.
def handler(signal_received, frame):
    # Notify user of termination of script.
    os.system("cls")
    print("** Terminated by User **")

    # Print final output to the screen.
    print("\n")
    print(f"Time Duration: {current_time - start_time}")
    print(f"Number of Data Points Analyzed: {num_data_point}")
    print(f"Number of Errors and Values: {num_errors} - {all_error_list}")
    print(f"Error Rate: {(num_errors / num_data_point) * 100}%")

    # Stop script
    return sys.exit(0)


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


def get_hour_diff(start_time: datetime, end_time: datetime):
    """
    Function returns the number of hours between two given datetimes.
    :param start_time: Datetime
    :param end_time: Datetime
    :return: float
    """
    sec_diff = end_time - start_time

    hour_diff = sec_diff.total_seconds() / 60 / 60

    return float(hour_diff)


# try:

signal(SIGINT, handler)

# Set threshold values where script will continue to execute until met.
hours_to_run = 6
data_points_to_analyze = 1000000
allowed_failed_reads = 5

# Set the start time and current time.
start_time = datetime.datetime.now()
current_time = start_time

# Establish list of likely COM ports, baud rate utilized, and number of failed reads tolerated.
port_list = ["COM3", "COM4", "COM5", "COM6"]
baud = 9600

# Set the counts to zero.
num_data_point = 0
num_errors = 0
failed_reads = 0

# Establish sample size and increment collected.
sample_size = 5
seconds_increment = 0

# Create a list for temperatures and add the number of temperatures equivalent to the sample size.
all_error_list = []

# Execute while thresholds have not yet been met and script is not failing to read the device.
while get_hour_diff(start_time, current_time) <= hours_to_run and num_data_point <= data_points_to_analyze:
    # Create a list for temperatures and add the number of temperatures equivalent to the sample size.
    temperature_sample_list = []

    # Add ten data points to the temperature list for analysis.
    while len(temperature_sample_list) < sample_size and failed_reads <= allowed_failed_reads:
        try:
            # Pull reading from device and add it to sample set.
            temperature = read_port_data(port_list, baud)
            temperature_sample_list.append(float(temperature))
            failed_reads = 0
        except:
            failed_reads = failed_reads + 1
            if failed_reads == allowed_failed_reads:
                print("Exiting... Unable to read device.")
                sys.exit(1)
            pass

    # Increment the total number of data points pulled for sampling.
    num_data_point = num_data_point + len(temperature_sample_list)

    # Identify any outliers and if any are found, increment the total number of errors count and add the data point
    # to the error list.
    if len(get_outlier(temperature_sample_list)) > 0:
        num_errors = num_errors + len(get_outlier(temperature_sample_list))
        all_error_list.append(get_outlier(temperature_sample_list))

    # Update the current time.
    current_time = datetime.datetime.now()

    # Limit output to only update when number of data points analyzed are divisible by a defined number.
    if num_data_point % 10 == 0:
        # Print the output to the screen.
        os.system("cls")
        print(f"Time in Progress: {current_time - start_time}")
        print(f"Number of Data Points Analyzed: {num_data_point}")
        print(f"Number of Errors and Values: {num_errors} - {all_error_list}")
        print(f"Error Rate: {(num_errors / num_data_point) * 100}%")

    # Set delay
    time.sleep(seconds_increment)

# Print final output to the screen.
os.system("cls")
print(f"Total Time: {current_time - start_time}")
print(f"Number of Data Points Analyzed: {num_data_point}")
print(f"Number of Errors and Values: {num_errors} - {all_error_list}")
print(f"Error Rate: {(num_errors / num_data_point) * 100}%")

#
# except KeyboardInterrupt:
#     os.system("cls")
#     print("** Terminated by User **")
#
# finally:
#     # Print the output to the screen.
#     print("\n")
#     print(f"Number of Data Points Analyzed: {num_data_point}")
#     print(f"Number of Errors and Values: {num_errors} - {all_error_list}")
#     print(f"Error Rate: {(num_errors / num_data_point) * 100}%")
