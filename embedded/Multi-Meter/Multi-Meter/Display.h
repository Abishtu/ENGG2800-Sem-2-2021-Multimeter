/* 
* Display.h
*
* Created: 2021-08-27 1:54:16 PM
* Author: HOFFMAN, Arthur
*/


#ifndef __DISPLAY_H__
#define __DISPLAY_H__

#define F_CPU 8000000UL

#include <avr/io.h>
#include <util/delay.h>
#include <avr/cpufunc.h> 
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#define LCD_PORT PORTC

class Display {
//variables
private:
	enum BacklightLvl {OFF, L1, L2, L3, L4};
	
	BacklightLvl brightnessLevel;
	uint8_t E;
	uint8_t RS;
	uint8_t RW;
	uint8_t backlightLevel;
	
	void setupDimming();
	void updateBackLight();
	
	
	//Display( const Display &c );
	//Display& operator=( const Display &c );
	
	void busy(void);
	
	const static uint8_t ascii[];

//functions
public:
	Display(uint8_t e, uint8_t rs, uint8_t rw);
	~Display();
	
	void writeCmd(uint8_t);
	void writeData(uint8_t);
	void displayWord(uint8_t [], int);
	void setLine(uint8_t);
	void setCursorePosition(uint8_t);
	void clearDisplay();
	void backlightBar(uint8_t);
	void runTest();	
	void setLevel(uint8_t);
	
	void incBrightness();
	void decBrightness();
	
	uint8_t getBacklightLevel();
	void setBacklightLevel(uint8_t bl);
	void setCustomChar(unsigned char loc, unsigned char *msg);
	
	void toggle_E();

}; //Display

#endif //__DISPLAY_H__
