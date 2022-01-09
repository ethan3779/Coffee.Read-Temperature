# Script to return the current temperature measured by the Arduino at the point in time script is executed.
import serial


# Define a function which reads data from the port list provided.
def read_port_data(list_of_ports: list, baud_rate: int) -> str:
    """
    Function which returns the output of a device using one of the ports and the baud rate provided.
    :param list_of_ports: A list of strings which contain possible ports where a device could be found.
    :param baud_rate: An integer which represents the baud rate utilized by a device.
    :return: A string of the device output.
    """
    # Attempt to read from device, but do not throw an error if unable.
    try:
        # Determine the port utilized for the device based upon the port list and baud rate provided, and
        # establish a connection.
        for port in list_of_ports:
            try:
                device = serial.Serial(port, baud_rate)
                break
            except:
                pass

        # Read the raw data from the device.
        raw_data = device.readline()

        # Decode the raw data from the device for a usable output.
        decoded_data = raw_data.decode("utf8")

        # Ensure the output is not blank or null and if not, return the output.
        if decoded_data != '' or decoded_data is not None:
            return decoded_data

        # Close the connection to the device.
        device.close()

    except:
        pass
