/*
 * Multi-Meter.cpp
 *
 * Created: 2021-08-20 2:08:18 PM
 * Author : SURESH, Harikesha & HOFFMAN, Arthur
 */ 
#define F_CPU 8000000UL
#include <avr/io.h>
#include <util/delay.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#include <avr/interrupt.h>
#include <avr/delay.h>

#include "Test2.h"
#include "Display.h"
#include "Serial.h"
#include "Multimeter.h"
#include "uart_hal.h"
#include "MultimeterDisplayer.h"
#include "ADC.h"


#define MAXBUFF 256

#define TIMER_TICKS 62500
#define DEBOUNCE_TIME 200

Serial communicationDevice(4800, 0);
Multimeter multimeter;
MultimeterDisplayer displayer(multimeter);
Adc adcDevice;
float calcDC(float);
float calcAC(int, int);
float calcRes(float);
float calcCont(void);

void eeprom_write(uint8_t, uint8_t);
uint8_t eeprom_read(uint8_t);

volatile int next_mode = 0;
int current_mode;

/*
int main(void) {
	Display display(PORTD2, PORTD4, PORTD3); // For pcb
	//_delay_ms(10);
	while (1)
	{
		display.displayWord((uint8_t*) "Hello", 5);
		_delay_ms(250);
		display.clearDisplay();
		_delay_ms(250);
	}
	
}
*/

/*
void setUpTimer(void) 
{
	TCCR1B = (1 << CS11) | (1 << CS10) | (1 << WGM12);
	OCR1A = TIMER_TICKS;
	TIMSK1 = (1 << OCIE1A);
}*/


void updateMeasurements(void) 
{
	float data;
	
	switch (multimeter.getMode()) {
	case 0:
		data = calcAC(250, 0);	
		//data = eeprom_read(0x00)/10.0;
		break;
	case 1:
		data = calcDC(adcDevice.read_adc());
		//data = adcDevice.read_adc();
		break;
	case 2:
		//multimeter.setMaxValue(0);
		//multimeter.setMinValue(0);
		//multimeter.setRecentValue(0);
		//data = adcDevice.read_adc();
		data = calcRes(adcDevice.read_adc() + 0.008);
		break;
	case 3:
		data = calcRes(adcDevice.read_adc());
		break;
	default:
		data = 0;
		break;
	}

	if (data < multimeter.getMinValue()) {
		multimeter.setMinValue(data);
	} else if (data > multimeter.getMaxValue()) {
		multimeter.setMaxValue(data);
	}
	
	multimeter.setRecentValue(data);
	multimeter.updateContinuityState();
}



void updateMultimeterData() 
{
	float max = multimeter.getMaxValue();
	float curr = multimeter.getRecentValue();
	float min = multimeter.getMinValue();
	uint8_t bl = multimeter.getBacklightLevel();
	uint32_t mode = multimeter.getMode();
	bool isHold = multimeter.getHold();
	float contThresh = multimeter.getContinuityThreshold();
	if (!isHold) {
		fprintf(stdout, "MIN:%f\n", (double) min);
		fflush(stdout);
		
		fprintf(stdout, "CURR:%f\n", (double) curr);
		fflush(stdout);
		
		fprintf(stdout, "MAX:%f\n", (double) max);
		fflush(stdout);
		
		fprintf(stdout, "MODE\':%d\n", (int) mode);
		fflush(stdout);
	}	
		fprintf(stdout, "HOLD\':%d\n", (int) isHold);
		fflush(stdout);
		
		fprintf(stdout, "BL\':%d\n", (int) bl);
		fflush(stdout);
		
		fprintf(stdout, "CT\':%.1f\n", (double) contThresh);
		fflush(stdout);
}

float calcDC(float adc_val)
{
	return (adc_val - 1.226)/(0.0625);
}

float calcAC(int maxSample, int currentSample)
{
	int range = maxSample - currentSample;
	float squareSum = 0.0;
	
	while (currentSample < range)
	{
		float sample = calcDC(adcDevice.read_adc());
		squareSum += (sample * sample) / range;
		currentSample++;
		_delay_ms(0.25);
	}
	
	return (float)sqrt(squareSum);
}

float calcRes(float adc_val)
{
	float baseRes = 410000;    //470000
	float vSupplied = 4.64;
	float res;
	if (adc_val <= 0) {
		res = 0;
	} else {
		res = (baseRes/((vSupplied/adc_val) - 1));
	}
	return res;
}

void setupButtons(void) 
{
	// Brightness -> PD7 (PCINT23)
	// Brightness -> PB0 (PCINT0)
	// HOLD -> PB1 (PCINT1)
	// Reset -> PB2 (PCINT2)
	// Mode switch -> PB7 (PCINT7)
	// Zeroing -> PB6 (PCINT6)
	// PCIE0 -> PCINT[7:0]
	// PCIE1 -> PCINT[14:8]
	// PCIE2 -> PCINT[23:16]
	//set pin as input
	DDRB &= ~(PINB0 << DDRB);
	
	DDRB &= ~((1 << DDB0)|(1 << DDB1)|(1 << DDB2)|(1 << DDB6)|(1 << DDB7));
	DDRD &= ~(1 << DDD7);
	PORTB |= (1 << PORTB0)|(1 << PORTB7)|(1 << PORTB1)|(1 << PORTB2)|(1 << PORTB6);		// Enable pull-up res on PORTB0
	PORTD |= (1 << PORTD7);
	PCICR |= (1 << PCIE0)|(1 << PCIE2);
	PCMSK0 |= ((1 << PCINT0)|(1 << PCINT1)|(1 << PCINT2)|(1 << PCINT6)|(1 << PCINT7));
	PCMSK2 |= (1 << PCINT23);
}

void resetMultimeter() 
{
	multimeter.setMaxValue(0);
	multimeter.setMinValue(0);
	multimeter.setRecentValue(0);
}

int main(void)
{	
		
	multimeter.setContinuityThreshold(((float)eeprom_read(0x00))/10.0);
	adcDevice.set_analog_in(0);
	//adcDevice.set_analog_in(1);
	FILE uartStrWrite;
	uartStrWrite.put = uart_send_byte_IO;
	uartStrWrite.get = NULL;
	uartStrWrite.flags = _FDEV_SETUP_WRITE;
	
	FILE uartStrRead;
	uartStrRead.put = NULL;
	uartStrRead.get = uart_read_IO;
	uartStrRead.flags = _FDEV_SETUP_READ;
	
	stdout = &uartStrWrite;
	stdin = &uartStrRead;
	
	//setUpTimer();
	setupButtons();
	sei();
	

	while(1) {		
		displayer.clearScreen();
		_delay_ms(10);
		
		//multimeter.setMode(next_mode);
		
		displayer.refresh(multimeter);
		
		switch(multimeter.getMode()) {
			case 0:
			case 1:
				adcDevice.set_analog_in(0);
				break;
			case 2:
			case 3:
				adcDevice.set_analog_in(2);
				break;
		}
		
		char *line = (char *) malloc(sizeof(char)*MAXBUFF);
		memset(line, 0, MAXBUFF);
			//printf("%s\r", line);
			while(communicationDevice.read(line) > 0) {
				if (strstr(line, "CONNECT:")) {
					multimeter.connect();
					communicationDevice.send((uint8_t *)"\nOK:\n");
					_delay_ms(10);
				} else if (strstr(line, "HOLD:0")) {
					//communicationDevice.send((uint8_t *)"HOLD\':0\n");
					multimeter.setHold(false);
				} else if (strstr(line, "HOLD:1")) {
					//communicationDevice.send((uint8_t *)"HOLD\':1\n");
					multimeter.setHold(true);
				} else if (strstr(line, "BL:")) {
					char *bl_val_str = line + strlen("BL:");
					int bl = atoi(bl_val_str);
				multimeter.setBackLightLevel(bl);
				} else if (strstr(line, "MODE:")) {
					char *mode_val_str = line + strlen("MODE:");
					int mode = atoi(mode_val_str);
					if (multimeter.getHold() == 1) {
						multimeter.setHold(0);
					}
					multimeter.setZeroValue(0);
					multimeter.setMode(mode);
					resetMultimeter();
				} else if (strstr(line, "DISS:")) {
					multimeter.disconnect();
					communicationDevice.send((uint8_t *)"\nBYE:\n");
					_delay_ms(10);
				} else if (strstr(line, "RESET:")) {
					resetMultimeter();
				} else if (strstr(line, "CT:")) {
					char *contThresholdString = line + strlen("CT:");
					float contThreshold = atof(contThresholdString);
					multimeter.setContinuityThreshold(contThreshold);
					eeprom_write(0x00, contThreshold*10);
				} else if (strstr(line, "Y:")) {
					
				}
			}
			free(line);
			
			if (!multimeter.getHold()) {
				updateMeasurements();
			}
			
			if (multimeter.isConnected()) {
				updateMultimeterData();
			}
			
			
			displayer.clearScreen();
			_delay_ms(1);
			displayer.refresh(multimeter);
			_delay_ms(100);
	}
}

bool isDebounced(int pin, int pinNum) {
	int counter = 0;
	bool pressValid = false;
	
	while(!(pin & (1 << pinNum))) {
		counter++;
		if (counter >= DEBOUNCE_TIME) {
			pressValid = true;
			return pressValid;
		}
		_delay_ms(1);
	}
	
	return pressValid;
}

// For mode buttons
ISR(PCINT0_vect)
{
	// Btn pressed
	if (!(PINB & (1 << PINB0))) {
		bool pressValid = isDebounced(PINB, PINB0);
		//while (!(PINB & (1 << PINB0))) {
			//// Loop till button was pressed for > debounce time
			//counter++;
			//if (counter >= DEBOUNCE_TIME) {
				//// Press is valid, exit the loop
				//pressValid = true;
				//break;
			//}
			//_delay_ms(1);
		//}
		if (pressValid) {
			uint8_t bl = multimeter.getBacklightLevel();
			switch(bl) {
				case 0:
					multimeter.setBackLightLevel(4);
					break;
				case 1:
					multimeter.setBackLightLevel(0);
					break;
				case 2:
					multimeter.setBackLightLevel(1);
					break;
				case 3:
					multimeter.setBackLightLevel(2);
					break;
				case 4:
					multimeter.setBackLightLevel(3);
					break;
			}
		}
	} else if (!(PINB & (1 << PINB1))) {
		bool presValid = isDebounced(PINB, PINB1);
		//while (!(PINB & (1 << PINB1))) {
			//counter++;
			//
			//if (counter >= DEBOUNCE_TIME) {
				//presValid = true;
				//break;
			//}
			//_delay_ms(1);
		//}
		
		if (presValid) {
			uint8_t hold = multimeter.getHold();
			switch (hold) {
				case 0:
					multimeter.setHold(1);
					break;
				case 1:
					multimeter.setHold(0);
					break;
			}
		}

	} else if (!(PINB & (1 << PINB2))) {
		bool presValid = isDebounced(PINB, PINB2);
		if(presValid) {
			resetMultimeter();
		}
	} else if (!(PINB & (1 << PINB6))) {
		bool presValid = isDebounced(PINB, PINB6);
		
		if (presValid) {
			multimeter.setZeroValue(multimeter.getRecentValue());
		}
		
	} else if (!(PINB & (1 << PINB7))) {
		bool presValid = isDebounced(PINB, PINB7);
		
		if (presValid) {
			
			uint8_t mode = multimeter.getMode();
			
			switch(mode) {
				case 0:
					multimeter.setMode(1);
					break;
				case 1:
					multimeter.setMode(2);
					break;
				case 2:
					multimeter.setMode(3);
					break;
				case 3:
					multimeter.setMode(0);
					break;
			}
			multimeter.setZeroValue(0);
			resetMultimeter();
		}
	}
}

ISR(PCINT2_vect)
{
	if (!(PIND & (1 << PIND7))) {
		bool presValid = isDebounced(PIND, PIND7);
		
		if (presValid) {
			uint8_t bl = multimeter.getBacklightLevel() + 1;
			bl = bl % 5;
			multimeter.setBackLightLevel(bl);
		}
	}
}


void eeprom_write(uint8_t addr, uint8_t data)
{
	/* Wait for completion of previous write */
	while(EECR & (1<<EEPE))
	;
	/* Set up address and Data Registers */
	EEAR = addr;
	EEDR = data;
	/* Write logical one to EEMPE */
	EECR |= (1<<EEMPE);
	/* Start eeprom write by setting EEPE */
	EECR |= (1<<EEPE);
}

uint8_t eeprom_read(uint8_t addr)
{
	/* Wait for completion of previous write */
	while(EECR & (1<<EEPE))
	;
	/* Set up address register */
	EEAR = addr;
	/* Start eeprom read by writing EERE */
	EECR |= (1<<EERE);
	/* Return data from Data Register */
	return EEDR;
}

/* For when it is eventually added
// For reset button
ISR(PCINTn_vect)
{
	if (PINn & (1 << PINnX)) {
		resetMultimeter();
	}
}

// For brightness up button
ISR(PCINTn_vect)
{
	if (PINn & (1 << PINnX)) {
		uint8_t bl = multimeter.getBacklightLevel() + 1;
		bl = bl % 5;
		multimeter.setBackLightLevel(bl);
	}
}

// For brightness down button
ISR(PCINTn_vect)
{
	if (PINn & (1 << PINnX)) {
		uint8_t bl = multimeter.getBacklightLevel() - 1;
		bl = bl % 5;
		multimeter.setBackLightLevel(bl);
	}
}
*/
