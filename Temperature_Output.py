# Script to return the current temperature measured by the Arduino at the point in time script is executed.
import serial

# Establish list of likely COM ports.
portList = ["COM3", "COM4", "COM5", "COM6"]

# Attempt to read from Arduino, but do not throw an error if unable.
try:
    # Determine the port utilized for the Arduino based upon the list provided, and establish a connection.
    for port in portList:
        try:
            arduino = serial.Serial(port, 9600)
            break
        except:
            pass

    # Read the temperature from the Arduino.
    temperature = arduino.readline()

    # Decode the temperature data from the Arduino for a usable output.
    output = temperature.decode("utf8")

    # Ensure the output is not blank or null, and if not, print the output which is converted to a float.
    if output != '' or output is not None:
        print(float(output))

    # Close the connection to the Arduino.
    arduino.close()

except:
    pass