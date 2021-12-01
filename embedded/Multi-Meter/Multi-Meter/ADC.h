/* 
* ADC.h
*
* Created: 2021-09-16 12:31:20 PM
* Author: HOFFMAN, Arthur
*/


#ifndef __ADC_H__
#define __ADC_H__

#define F_CPU 8000000UL

#include <avr/io.h>
#include <util/delay.h>

#define TW_SCL_PIN PORTC5
#define TW_SDA_PIN PORTC4

#define ADS1115_ADDR 0b01001000

class Adc
{
//variables
public:
protected:
private:

//functions
public:

	Adc();
	~Adc();
	void setup();
	float runTest();
	float read_adc();
	void set_analog_in(uint8_t);
	
protected:
private:
	Adc( const Adc &c );
	Adc& operator=( const Adc &c );

}; //ADC

#endif //__ADC_H__
