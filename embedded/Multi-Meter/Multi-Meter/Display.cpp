/* 
* Display.cpp
*
* Created: 2021-08-27 1:54:15 PM
* Author: HOFFMAN, Arthur
*/


#include "Display.h"

// default constructor
/* Setup appropriate registers for writing to the display.
 * PORTB0 -> E (LCD)
 * PORTB6 -> RS (LCD)
 * PORTB7 -> RW (LCD)
 * PORTD -> Databus (LCD)
 */
Display::Display(uint8_t e, uint8_t rs, uint8_t rw)
{
	E = e;
	RS = rs;
	RW = rw;
	// Set PORTB[7,6,0] as outputs
	DDRD |= (1 << E)|(1 << RW)|(1 << RS);
	// Set lower 4 pins of PORTC as outputs.
	DDRC = 0x0F;
	
	
	PORTD &= ~((1<<RS)|(1<<RW));
	
	// Preliminary function set required for 4-bit mode
	LCD_PORT &= 0xF0;
	LCD_PORT |= (0b00000010);
	toggle_E();
	//_delay_ms(10);
	writeCmd(0b00101000);		// Function set 001100xx;
	//_delay_ms(10);
	writeCmd(0b00001100);		// Display on 00001110;
	//_delay_ms(10);
	writeCmd(0b00000110);		// Return home;
	//_delay_ms(10);
	writeCmd(0b00000001);
	//_delay_ms(10);
	writeCmd(0b00000010);
	
	setupDimming();
	setBacklightLevel(4);

} //Display

// default destructor
Display::~Display()
{
} //~Display

void Display::runTest() 
{
	double voltage = 10.0;
	char* word = (char*)malloc(sizeof(char) * 20);
	sprintf(word, "Voltage: %0.2f", voltage);
	setLine(1);
	displayWord((uint8_t*) word,strlen(word));
	setLine(2);
	displayWord((uint8_t*) word, strlen(word));
	free(word);
	_delay_ms(500);
	clearDisplay();
	_delay_ms(100);	
}

void Display::toggle_E(void)
{
	PORTD |= (1 << E);		// LCD enable high
	_delay_ms(0.5);
	//_delay_ms(1);
	PORTD &= ~(1<<E);	// LCD enable low
}

void Display::writeCmd(uint8_t cmd)
{
	// Set up bit-mask for RW = 0 & RS = 0
	PORTD &= ~((1<<RS)|(1<<RW));
	
	// Output cmd on PORTD
	LCD_PORT &= 0xF0;
	LCD_PORT |= (cmd >> 4);
	// Toggle Enable bit on/off	
	toggle_E();
	//_delay_ms(1);
	LCD_PORT &= 0xF0;
	LCD_PORT |= 0x0F&cmd;
	// Toggle Enable bit on/off
	toggle_E();
	//_delay_ms(1);
	
}  

void Display::writeData(uint8_t data)
{
	// Set up bit-mask for RW = 0 & RS = 0
	PORTD &= ~((1<<RS)|(1<<RW));
	PORTD |= (1 << RS);
	
	// Output cmd on PORTD
	LCD_PORT &= 0xF0;
	LCD_PORT |= data >> 4;
	toggle_E();
	//_delay_ms(1);
	LCD_PORT &= 0xF0;
	LCD_PORT |= 0x0F&data;
	toggle_E();
	//_delay_ms(1);
}

void Display::displayWord(uint8_t word[], int length)
{
	for (int i = 0; i < length; i++) {
		writeData(word[i]);
		_delay_ms(1);
	}	
}

void Display::clearDisplay()
{
	writeCmd(0b00000001);
	//_delay_ms(2);
	writeCmd(0b00000010);		// Return home;
}

// Setup PWM dimming on timer/counter2
void Display::setupDimming()
{
	/* Clear OC0A on OCR0A compare match, set at bottom.
	 * Clock prescale of 1
	 */
	DDRD |= (1 << 6)|(1 << 5);
	TCCR0A |= (1 << COM0A1)|(1 << WGM01)|(1 << WGM00);	
	TCCR0B |= (1 << CS00);
}

void Display::setLevel(uint8_t brightness) 
{
	OCR0A = brightness;	
}

void Display::setLine(uint8_t line)
{
	switch(line) {
		case 1:
			setCursorePosition(0x00);
			break;
		case 2:
			setCursorePosition(0x40);
			break;
		case 3:
			setCursorePosition(0x14);
			break;
		case 4:
			setCursorePosition(0x54);
			break;
	}
}

void Display::setCursorePosition(uint8_t position)
{
	writeCmd(0b10000000 | position);
}

void Display::backlightBar(uint8_t level)
{
	unsigned char brightness1[8] = {
		0b00000,
		0b01110,
		0b11011,
		0b10001,
		0b10001,
		0b10001,
		0b11111,
		0b11111};
	unsigned char brightness2[8] = {
		0b00000,
		0b01110,
		0b11011,
		0b10001,
		0b10001,
		0b11111,
		0b11111,
		0b11111};
	unsigned char brightness3[8] = {
		0b00000,
		0b01110,
		0b11011,
		0b10001,
		0b11111,
		0b11111,
		0b11111,
		0b11111};
	unsigned char brightness4[8] = {
		0b00000,
		0b01110,
		0b11111,
		0b11111,
		0b11111,
		0b11111,
		0b11111,
		0b11111};
	int barIconAddr = 1;
	uint8_t barChar = 0xFF;
	uint8_t barIconPos = 0x67;
	
	//uint8_t barCursorPositions[4] = {0x67, 0x27, 0x53, 0x13};

	switch (level) {
		case 0:
			setCustomChar(barIconAddr,brightness1);
			break;
		case 1:
			setCustomChar(barIconAddr,brightness1);
			break;
		case 2:
			setCustomChar(barIconAddr,brightness2);
			break;
		case 3:
			setCustomChar(barIconAddr,brightness3);
			break;
		case 4:
			setCustomChar(barIconAddr,brightness4);
			break;
	}
	setCursorePosition(barIconPos);
	writeData(barIconAddr);
	
}

void Display::busy()
{
	uint8_t flag = 0x0F;
	PORTD &= ~((1<<E)|(1<<RS));	// LCD enable low
	PORTD |= (1<<RW);
	PORTC = 0;
	DDRC = 0;
	
	while ((flag&0x08) == 0x08) {
		flag = PINC&0xFF;
		PORTD |= (1<<E);
		_delay_ms(1);
		PORTD &= 0xFF^(1<<E);
	}

	DDRC = 0xFF;
}

void Display::updateBackLight()
{
	switch (brightnessLevel) {
	case OFF:
		TCCR0A &= ~(1 << COM0A1);
		PORTD &= ~(1 << PORTD6);
		PORTD |= (1 << PORTD5);
		break;
	case L1:
		TCCR0A |= (1 << COM0A1);
		setLevel(255/4);
		PORTD &= ~(1 << PORTD5);
		break;
	case L2:
		TCCR0A |= (1 << COM0A1);
		setLevel(255/2);
		PORTD &= ~(1 << PORTD5);
		break;
	case L3:
		TCCR0A |= (1 << COM0A1);
		setLevel(3*255/4);
		PORTD &= ~(1 << PORTD5);
		break;
	case L4:
		TCCR0A |= (1 << COM0A1);
		setLevel(255);
		PORTD &= ~(1 << PORTD5);
		break;	
	}
}

void Display::incBrightness()
{
	switch (brightnessLevel) {
		case OFF:
			brightnessLevel = L1;
			break;
		case L1:
			brightnessLevel = L2;
			break;
		case L2:
			brightnessLevel = L3;
			break;
		case L3:
			brightnessLevel = L4;
			break;
		case L4:
			brightnessLevel = OFF;
			break;
	}
	updateBackLight();
}

void Display::decBrightness()
{
	switch (brightnessLevel) {
		case OFF:
			brightnessLevel = L4;
			break;
		case L1:
			brightnessLevel = OFF;
			break;
		case L2:
			brightnessLevel = L1;
			break;
		case L3:
			brightnessLevel = L2;
			break;
		case L4:
			brightnessLevel = L3;
			break;
	}
	updateBackLight();
}

void Display::setBacklightLevel(uint8_t bl) {
	switch(bl) {
		case 0:
			brightnessLevel = OFF;
			break;
		case 1:
			brightnessLevel = L1;
			break;
		case 2:
			brightnessLevel = L2; 
			break;
		case 3:
			brightnessLevel = L3;
			break;
		case 4:
			brightnessLevel = L4;
			break;
	}
	
	updateBackLight();
}

void Display::setCustomChar(unsigned char loc, unsigned char *msg) {
	
	unsigned char i;
	if(loc < 8)
	{
		writeCmd(0x40 + (loc*8));
		_delay_ms(10);
		for(i=0; i<8; i++)
		{
			writeData(msg[i]);
		}
	}
	
}

const uint8_t Display::ascii[] = {
	0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9,

	0xa, 0xb, 0xc, 0xd, 0xe, 0xf, 0x10, 0x11, 0x12, 0x13,

	0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d,

	0x1e, 0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27,

	0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31,

	0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3a, 0x3b,

	0x3c, 0x3d, 0x3e, 0x3f, 0x40, 0x41, 0x42, 0x43, 0x44, 0x45,

	0x46, 0x47, 0x48, 0x49, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e, 0x4f,

	0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59,

	0x5a, 0x5b, 0x5c, 0x5d, 0x5e, 0x5f, 0x60, 0x61, 0x62, 0x63,

	0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 0x6b, 0x6c, 0x6d,

	0x6e, 0x6f, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77,

	0x78, 0x79, 0x7a, 0x7b, 0x7c, 0x7d, 0x7e
};
