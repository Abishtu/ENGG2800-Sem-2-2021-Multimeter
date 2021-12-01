/*
 * Multimeter.cpp
 *
 * Created: 10/09/2021 15:48:42
 *  Author: SURESH, Harikesha
 */

#include "Multimeter.h"

Multimeter::Multimeter(void) {
	maxValue = 0;
	minValue = 0;
	recentValue = 0;
	zeroValue = 0;
	continuityThreshold = 2.0;
	
	mode = 0;
	hold = 0;
	
	backlightLevel = 4;
	
	baseUnit = (uint8_t *)"";
	
	isShorted = false;
}

void Multimeter::setMaxValue(float value) {
	
	maxValue = value;
	switch (mode) {
		case 2:
			maxValue = value - zeroValue;	
			if (maxValue < 0) {
				maxValue = 0;
			}		
			break;
	}
}

void Multimeter::setMinValue(float value) {
	minValue = value;
	switch (mode) {
		case 2:
		minValue = value - zeroValue;
		if (minValue < 0) {
			minValue = 0;
		}
		break;
	}
	
}

void Multimeter::setRecentValue(float value) {
	recentValue = value;
	switch (mode) {
		case 2:
		recentValue = value - zeroValue;
		if (recentValue < 0) {
			recentValue = 0;
		}
		break;
	}
}

void Multimeter::setZeroValue(float value) {
	zeroValue = value;
}

void Multimeter::setContinuityThreshold(float value) {
	if (value >= 0.0 && value <= 20.0) {
		continuityThreshold = value;
	}
}

void Multimeter::setMode(uint8_t md) {
	uint8_t mode_array[] = {0, 1, 2, 3};
	if (md >= 0 && md < 4) {
		mode = mode_array[md];
	}
}

void Multimeter::setHold(uint8_t holdState) {
	hold = holdState;
}

void Multimeter::setBackLightLevel(uint16_t level) {
	if (level >= 0 && level < 5) {
		backlightLevel = level;
	}
}

void Multimeter::setBaseUnit(uint8_t *unit) {
	baseUnit = unit;
}

void Multimeter::updateContinuityState(void) {
	if (recentValue <= continuityThreshold) {
		isShorted = true;
	} else {
		isShorted = false;
	}
}

float Multimeter::getMaxValue(void) {
	return maxValue;
}

float Multimeter::getMinValue(void) {
	return minValue;
}

float Multimeter::getRecentValue(void) {
	return recentValue;
}

float Multimeter::getZeroValue(void) {
	return zeroValue;
}

float Multimeter::getContinuityThreshold(void) {
	return continuityThreshold;
}

uint8_t Multimeter::getMode(void) {
	return mode;
}

uint8_t Multimeter::getHold(void) {
	return hold;
}

uint8_t Multimeter::getBacklightLevel(void) {
	return backlightLevel;
}

uint8_t* Multimeter::getBaseUnit(void) {
	return baseUnit;
}

void Multimeter::connect(void) {
	connectionState = true;
}

void Multimeter::disconnect(void) {
	connectionState = false;
}

bool Multimeter::isConnected(void) {
	return connectionState;
}

bool Multimeter::isShort(void) {
	return isShorted;
}