/*
 * MultimeterDisplayer.h
 *
 * Created: 24/09/2021 15:50:48
 *  Author: SURESH, Harikesha
 */ 
#include "Multimeter.h"
#include "Display.h"
#include <avr/io.h>


#ifndef MULTIMETERDISPLAYER_H_
#define MULTIMETERDISPLAYER_H_



class MultimeterDisplayer {
	private:
		Multimeter multimeter;
				
		uint8_t modeIcons[4];

		void displayMeasurement(uint8_t line, float value);
	public:
		MultimeterDisplayer(Multimeter mult);
		
		void displayMode(void);
		void displayHold(void);
		void displayConnectionSate(void);
		void displayBacklightBar(void);
		void displayMinimum(void);
		void displayCurrent(void);
		void displayMaximum(void);
		
		void refresh(Multimeter newMult);
		
		void clearScreen(void);
		
		void runTest(void);
		
		void decrementBrightness(void);
};

#endif /* MULTIMETERDISPLAYER_H_ */