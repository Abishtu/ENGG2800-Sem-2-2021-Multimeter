/*
 * Multimeter.h
 *
 * Created: 03/09/2021 15:07:04
 *  Author: SURESH, Harikesha
 */ 

#include <stdint.h>
#include <stdbool.h>


#ifndef MULTIMETER_H_
#define MULTIMETER_H_

class Multimeter {
private:
	float maxValue; // max recorded value
	float minValue; // min recorded value
	float recentValue; // current recorded value
	
	float zeroValue; // probe zeroing value
	
	float continuityThreshold;
	
	uint8_t mode; // current mode (0 or 1 or 2 or 3)
	uint8_t hold; // hold state
	uint8_t backlightLevel; // back light level
	
	uint8_t *baseUnit; // base unit, defunct and useless variable
	
	bool connectionState; // if the device is connected to PC
	bool isShorted;
public:
	Multimeter(void);

	void setMaxValue(float value);
	void setMinValue(float value);
	void setRecentValue(float value);
	void setZeroValue(float value);
	void setContinuityThreshold(float value);
	void setMode(uint8_t md);
	void setHold(uint8_t holdState);
	void setBackLightLevel(uint16_t level);
	void setBaseUnit(uint8_t *unit);
	void updateContinuityState(void);
	
	float getMaxValue(void);
	float getMinValue(void);
	float getRecentValue(void);
	float getZeroValue(void);
	float getContinuityThreshold(void);
	uint8_t getMode(void);
	uint8_t getHold(void);
	uint8_t getBacklightLevel(void);
	uint8_t *getBaseUnit(void);
	
	void connect(void); // set's connection state to true
	void disconnect(void); // set's connection state to false
	bool isConnected(void); // returns the connection state with PC
	bool isShort(void);
	
};

#endif /* MULTIMETER_H_ */