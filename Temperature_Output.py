from Read_Port import read_port_data

# Establish list of likely COM ports.
port_list = ["COM3", "COM4", "COM5", "COM6"]

# Establish baud rate utilized.
baud = 9600

# Execute function to get temperature from Arduino, and output the results.
temperature = read_port_data(port_list, baud)

print(float(temperature))
