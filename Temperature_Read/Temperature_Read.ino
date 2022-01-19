/*****************************************************************************************************
  This reads the temperature and returns the value.
******************************************************************************************************/

/*****************
    Libraries
******************/
// Include the libraries needed
#include <SPI.h>
#include <Adafruit_MAX31855.h>

/*********************************************************
    Thermocouple pin and calibration value definitions
**********************************************************/
// Software SPI for thermcouple. This defines which pins connect from the Arduino to the MAX31855.
#define MAXDO   6
#define MAXCS   7
#define MAXCLK  9

// Calibration for thermocouple
// Define altitude in feet
#define altitude 950

//Define temperature readings and actual temperatures
#define RawLowF 34.25
#define RawLowC 0.50
#define RawHighF 206.60
#define RawHighC 96.00
#define RawRangeF 172.35
#define RawRangeC 95.50
#define RefLowF 32.0
#define RefLowC 0.0
#define RefHighF 212.0
#define RefHighC 100.0
#define RefRangeF 180.0
#define RefRangeC 100.0

/***************************
  Define Global Variables
****************************/
double initialTemp;


/************************
      Initialization
*************************/
// Initializing devices
// Thermocouple
Adafruit_MAX31855 thermocouple(MAXCLK, MAXCS, MAXDO);


/******************************
   Get Median Method
 ******************************/
/*
double GetMedian(array inputArray) {
    // Create an empty array which will be ordered
    double orderedArray[sizeof(inputArray)];
    unsigned int arrLength = 0;

    // Create temporary variables and arrays used
    double min;
    double array[si

    while (arrLength < (sizeof(inputArray) + 1)) {
        double tempArray[(sizeof(inputArray) + 1) - arrLength];
        
    }
 }
 */

/******************************
   Temperature Read Method
 ******************************/
double GetTemp(char tempUnit, bool isCorrectedTemp = true) {
    // Defines c and f as a decimal digit
    double c = thermocouple.readCelsius();
    double f = thermocouple.readFahrenheit();

    // Create variable to hold the current temperature
    double currentTemp;
    
    // Determine unit to output
    // Celsius
    if (tempUnit == 'C') {
        // Corrected temperature output
        if (isCorrectedTemp) {
            currentTemp = double((((c - RawLowC) * RefRangeC) / RawRangeC) + RefLowC);
        }
        // Raw temperature output
        else if (!isCorrectedTemp) {
            currentTemp = c;
        }
    }
    // Fahrenheit
    else if (tempUnit == 'F') {
        // Corrected temperature output
        if (isCorrectedTemp) {
            currentTemp = double((((f - RawLowF) * RefRangeF) / RawRangeF) + RefLowF);
        }
        // Raw temperature output
        else if (!isCorrectedTemp) {
            currentTemp = f;
        }
    }
    
    return currentTemp;
}


/******************************
   Setup Method
 ******************************/
void setup() {
    // Open port at specified baud rate.
    Serial.begin(9600);
    
    // Create an array to hold five temperature readings
    // to calculate the median and set an initial
    // reading.
    double tempArray[5];
    unsigned int arrLength = 0;

    /* Will be used once median function is ready
    while (arrLength < 5) {
        tempArray[arrLength++] = GetTemp('F');
    }
    */

    while (!Serial) {
        delay(0500);   // half of a second
    }

    initialTemp = GetTemp('F');

}


/******************************
        Looping Method
*******************************/
void loop() {
    // Create a set local variables
    double previousTemp = initialTemp;
    double marginOfError = 0.50;
    double minAcceptableTemp;
    double maxAcceptableTemp;

    // Validation to ensure output temperature is not error
    while (true) {
      // Set minimum and maximum acceptable values
      if (previousTemp < 0) {
          minAcceptableTemp = previousTemp + (previousTemp * marginOfError);
          maxAcceptableTemp = previousTemp - (previousTemp * marginOfError);
      } 
      else {
          minAcceptableTemp = previousTemp - (previousTemp * marginOfError);
          maxAcceptableTemp = previousTemp + (previousTemp * marginOfError); 
      }
    
      // Collect temperature at the moment
      double currentTemp = GetTemp('F');

      // Compare current temperature to previous temperature
      if (currentTemp < minAcceptableTemp || currentTemp > maxAcceptableTemp) {
          Serial.println(previousTemp);
      }
      else {
          Serial.println(currentTemp);
          previousTemp = currentTemp;
      }
    }
}
