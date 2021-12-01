/*
 * Serial.h
 *
 * Created: 10/09/2021 15:24:52
 *  Author: Harikesha Suresh
 */ 

#include "uart_hal.h"
#include <stdio.h>
#include <stdlib.h>

#ifndef SERIAL_H_
#define SERIAL_H_

class Serial {
public:
	Serial(uint32_t baud, uint8_t highSpeed);
	
	void send(uint8_t data);
	int send_IO(char data, FILE *stream);
	void send(uint8_t *data, uint16_t length);
	void send(uint8_t *data);
	
	
	uint16_t getReadCount(void);
	uint8_t read(void);
	uint8_t read(char *string);
	
	
};



#endif /* SERIAL_H_ */