/*
 * MultimeterDisplayer.cpp
 *
 * Created: 24/09/2021 16:08:38
 *  Author: SURESH, Harikesha
 */ 

#include "MultimeterDisplayer.h"

#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>

//Display display(PORTD2, PORTD3, PORTD4); // For breadboard
Display display(PORTD2, PORTD4, PORTD3); // For pcb

MultimeterDisplayer::MultimeterDisplayer(Multimeter mult) {
	multimeter = mult;
	modeIcons[0] = 'V';
	modeIcons[1] = 'V';
	modeIcons[2] = modeIcons[3] = 0xf4;
	
	//refresh();
}

// Reserved positions 0x00 - 0x04
void MultimeterDisplayer::displayMode(void) {
	display.setCursorePosition(0x00);
	uint8_t mode = multimeter.getMode();
	display.writeData(modeIcons[mode]);
	switch (mode) {
		case 0:
			display.displayWord((uint8_t *) "(AC)", 4);
			break;
		case 1:
			display.displayWord((uint8_t *) "(DC)", 4);
			break;
		case 2:
			display.displayWord((uint8_t *)"    ", 4);
			break;
		case 3:
			display.displayWord((uint8_t *) "(co)", 4);
			break;
	}
	
}

void MultimeterDisplayer::displayHold(void) {
	uint8_t hold = multimeter.getHold();
	display.setCursorePosition(0x07);
	if (hold) {
		display.displayWord((uint8_t *)"HOLD", 4);
	} else {
		display.displayWord((uint8_t *)"    ", 4);
	}
}

unsigned char Character1[8] = {
	0b11111,
	0b00000,
	0b01010,
	0b00000,
	0b10001,
	0b01110,
	0b00000,
	0b00000};

void MultimeterDisplayer::displayConnectionSate(void) {
	bool connectionStat = multimeter.isConnected();
	display.setCustomChar(0,Character1);
	
	display.setCursorePosition(0x11);
	if (connectionStat) {
		display.writeData(0);
	} else {
		//display.displayWord((uint8_t *)"NC", 2);
		display.displayWord((uint8_t *)"  ", 2);
	}
}

void MultimeterDisplayer::displayBacklightBar(void) {
	uint8_t bl = multimeter.getBacklightLevel();
	display.setBacklightLevel(bl);
	display.backlightBar(bl);	
}

void MultimeterDisplayer::displayMeasurement(uint8_t line, float value) {
	display.setLine(line);
	switch(line) {
		case 2:
			display.setCursorePosition(0x45);
			break;
		case 3:
			display.setCursorePosition(0x19); //19
			break;
		case 4:
			display.setCursorePosition(0x59); //59
			break;
	}
	
	uint8_t mode = multimeter.getMode();
	char *valueLine = (char *) malloc(sizeof(char) * 9);
	memset(valueLine, 0, 9);
	
	switch(mode) {
		case 3:
			display.setCursorePosition(0x16);
			if (multimeter.isShort()) {
				sprintf(valueLine, "SHORT :: CT: %.1f", (double) multimeter.getContinuityThreshold());
				display.displayWord((uint8_t *) valueLine, strlen(valueLine));
			} else {
				sprintf(valueLine, "OPEN :: CT: %.1f", (double) multimeter.getContinuityThreshold());
				display.displayWord((uint8_t *) valueLine, strlen(valueLine));
			}
			break;
		default:
			if (1000.0 <= fabs(value) && fabs(value) < 1000000.0) {
				float val = value / 1000.0;
				sprintf(valueLine, "%.3f k", (double) val);
				
				display.displayWord((uint8_t *) valueLine, strlen(valueLine));
			} else if (fabs(value) >= 1000000.0) {
				float val = value / 1000000.0;
				sprintf(valueLine, "%.3f M", (double) val);
		
				display.displayWord((uint8_t *) valueLine, strlen(valueLine));
		
			} else if (pow(10, -3) < fabs(value) && fabs(value) < 1) {
				float val = value / pow(10, -3);
				sprintf(valueLine, "%.3f m", (double) val);
		
				display.displayWord((uint8_t *) valueLine, strlen(valueLine));
			} else if (0 < fabs(value) && fabs(value) < pow(10, -3)) {
				float val = value / pow(10, -6);
				sprintf(valueLine, "%.3f ", (double) val);
		
				display.displayWord((uint8_t *) valueLine, strlen(valueLine));
				display.writeData(0xE4);
			} else {
				sprintf(valueLine, "%.3f ", (double) value);
				display.displayWord((uint8_t *) valueLine, strlen(valueLine));
		
			}
	
			display.writeData(modeIcons[mode]);
			break;
	}
	
	free(valueLine);
	
}


void MultimeterDisplayer::displayMinimum(void) {
	switch(multimeter.getMode()) {
		case 3:
			break;
		default:
			display.setLine(2);
			display.displayWord((uint8_t *) "Min: ", 5);
			float min = multimeter.getMinValue();
			displayMeasurement(2, min);
			break;
	}
}

void MultimeterDisplayer::displayMaximum(void) {
	switch(multimeter.getMode()) {
		case 3:
			break;
		default:
			display.setLine(4);
			display.displayWord((uint8_t *) "Max: ", 5);
			float max = multimeter.getMaxValue();
			displayMeasurement(4, max);
			break;
	}
}

void MultimeterDisplayer::displayCurrent(void) {
	switch(multimeter.getMode()) {
		case 3:
			break;
		default:
			display.setLine(3);
			display.displayWord((uint8_t *) "Rec: ", 5);
			break;
	}
	
	float curr = multimeter.getRecentValue();
	displayMeasurement(3, curr);
}

void MultimeterDisplayer::refresh(Multimeter newMult) {
	multimeter = newMult;
	displayMode();
	displayHold();
	displayConnectionSate();

	displayMinimum();
	displayCurrent();
	displayMaximum();
	
	displayBacklightBar();
}

void MultimeterDisplayer::clearScreen(void) {
	display.clearDisplay();
}

void MultimeterDisplayer::runTest(void) {
	display.runTest();
}

void MultimeterDisplayer::decrementBrightness(void) {
	display.decBrightness();
	
}