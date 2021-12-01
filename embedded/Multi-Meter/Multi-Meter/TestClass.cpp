#include "TestClass.h"

void TestClass::runTest() {
	DDRC |= (1 << 5);
	
	while (1) {
		PORTC |= (1 << 5);
		_delay_ms(250);
		PORTC &= (0b11011111);
		_delay_ms(250);
	}
	
	
}