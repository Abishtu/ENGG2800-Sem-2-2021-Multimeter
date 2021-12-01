/* 
* Test2.cpp
*
* Created: 2021-08-25 11:42:31 AM
* Author: Owner
*/


#include "Test2.h"

// default constructor
Test2::Test2()
{
} //Test2

// default destructor
Test2::~Test2()
{
} //~Test2

void Test2::runTest() {
	DDRC |= (1 << 5);
	
	while (1) {
		PORTC |= (1 << 5);
		_delay_ms(1000);
		PORTC &= (0b11011111);
		_delay_ms(1000);
	}
}
