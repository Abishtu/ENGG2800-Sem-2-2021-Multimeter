/* 
* Test2.h
*
* Created: 2021-08-25 11:42:31 AM
* Author: Owner
*/


#ifndef __TEST2_H__
#define __TEST2_H__

#include <avr/io.h>
#include <util/delay.h>


class Test2
{
//variables
public:
protected:
private:

//functions
public:
	Test2();
	~Test2();
	
	void runTest();
protected:
private:
	Test2( const Test2 &c );
	Test2& operator=( const Test2 &c );

}; //Test2

#endif //__TEST2_H__
