
/*****************************************************************************************************
  This reads the temperature and returns the value every one second.
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


/************************
      Initialization
*************************/
// Initializing devices
// Thermocouple
Adafruit_MAX31855 thermocouple(MAXCLK, MAXCS, MAXDO);


void setup() {
  Serial.begin(9600);

}

/******************************
        Looping Method
*******************************/
void loop() {

// Print to serial monitor.
    
  Serial.println(temp());

  delay(1000);
}

/******************************
   Temperature Read Method
 ******************************/
int temp(){
  
  // Defines c and f as a decimal digit
   float c = thermocouple.readCelsius();
   float f = thermocouple.readFahrenheit();
  
  //Testing purposes
   
    // Raw reading of thermocouple in Celsius
    //Serial.print("Raw Reading: C = ");
    //Serial.println(c);
    //float CurrentTemp = c;
    
    // Corrected reading of thermocouple in Celsius
    //Serial.print("Corrected Reading: C =");
    //float CurrentTemp = float((((c-RawLowC)*RefRangeC)/RawRangeC)+RefLowC);
    
    // Raw reading of thermocouple in Fahrenheit
    //Serial.print("Raw Reading: F = ");
    //Serial.println(f);
    //float CurrentTemp = f;
  
  // Corrected reading of thermocouple in Fahrenheit set to CurrentTemp variable.
  float CurrentTemp = float((((f - RawLowF) * RefRangeF) / RawRangeF) + RefLowF);
  
  return CurrentTemp;
}
