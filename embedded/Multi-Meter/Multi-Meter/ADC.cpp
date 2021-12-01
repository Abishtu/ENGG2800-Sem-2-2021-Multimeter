/* 
* ADC.cpp
*
* Created: 2021-09-16 12:31:19 PM
* Author: HOFFMAN, Arthur
*/


#include "ADC.h"
#include <math.h>

extern "C"
{
	#include "twi_master.h"
}

void setup_adc(void)
{
	
	tw_init(TW_FREQ_250K, false);
	
	uint8_t data[3] = {0b00000001, 0b11000010, 0b11100011};	// ADC points to config register, changes MSB to do continuous conversions
	tw_master_transmit(ADS1115_ADDR, data, 3, true);
	
	
}

// default constructor
Adc::Adc()
{
	setup_adc();
} //ADC

// default destructor
Adc::~Adc()
{
} //~ADC

float Adc::read_adc(void)
{
	uint8_t write_data[1] = {0};	// ADC points to conversion register
	tw_master_transmit(ADS1115_ADDR, write_data, 1, true);
	
	uint8_t recv_data[2] = {1,1};
	tw_master_receive(ADS1115_ADDR,recv_data,2);
	int16_t data = recv_data[0] << 8 | recv_data[1];
	
	float finalData = (float)(data * 4.096) / (float)(pow(2, 15) - 1);
	
	
	return finalData;
}


float Adc::runTest()
{
	setup_adc();
	_delay_ms(1000);
	float data = read_adc();
	return data;
}

void Adc::set_analog_in(uint8_t input)
{
	uint8_t mux_mask = (4+input) << 4;
	uint8_t upper_config = 0x80 | mux_mask | 0x02;
	uint8_t data[3] = {0b00000001, upper_config, 0b11100011};	// ADC points to config register, changes MSB to do continuous conversions
	tw_master_transmit(ADS1115_ADDR, data, 3, true);
}