/*
 * Mulitmeter.h
 *
 * Created: 10/09/2021 15:48:27
 *  Author: Harikesha Suresh
 */ 

#include <avr/io.h>

#ifndef MULITMETER_H_
#define MULITMETER_H_

class Multimeter {
private:
	uint32_t maxValue;
	uint32_t minValue;
	uint32_t recentValue;
	uint8_t mode;
	uint8_t hold;
	uint16_t backlightLevel;
	
	uint8_t *baseUnit;
	
public:
	Multimeter(void);

	void setMaxValue(uint32_t value);
	void setMinValue(uint32_t value);
	void setRecentValue(uint32_t value);
	void setMode(uint32_t mode);
	void setHold(uint8_t holdState);
	void setBackLightLevel(uint16_t level);
	void setBaseUnit(uint8_t *unit);
	
	uint32_t getMaxValue(void);
	uint32_t getMinValue(void);
	uint32_t getRecentValue(void);
	uint8_t getMode(void);
	uint8_t getHold(void);
	uint16_t getBacklightLevel(void);
	uint8_t *getBaseUnit(void);
};



#endif /* MULITMETER_H_ */