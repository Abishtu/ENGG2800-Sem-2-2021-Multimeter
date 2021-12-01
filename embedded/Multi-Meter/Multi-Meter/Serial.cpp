/*
 * Serial.cpp
 *
 * Created: 10/09/2021 15:25:04
 *  Author: Harikesha Suresh
 */ 

#include "Serial.h"

Serial::Serial(uint32_t baud, uint8_t highSpeed) {
	uart_init(baud, highSpeed);
}

void Serial::send(uint8_t data) {
	uart_send_byte(data);
}

int Serial::send_IO(char data, FILE *stream) {
	uart_send_byte_IO(data, stream);
}

void Serial::send(uint8_t *data, uint16_t length) {
	uart_send_array(data, length);
}

void Serial::send(uint8_t *data) {
	uart_send_string(data);
}

uint16_t Serial::getReadCount(void) {
	return uart_read_count();
}

uint8_t Serial::read(void) {
	return uart_read();
}

uint8_t Serial::read(char *string) {
	uint8_t ch = 0;
	static uint8_t len = 0;
	if (getReadCount() > 0) {
		ch = read();
		send(ch);
		
		if ((ch == '\n') || (ch == '\r')) {
			string[len] = 0;
			len = 0;
		} else if ((ch == '\b') && (len != 0)) {
			len--;
		} else {
			string[len] = ch;
			len++;
		}
	}
	
	return len;
}
