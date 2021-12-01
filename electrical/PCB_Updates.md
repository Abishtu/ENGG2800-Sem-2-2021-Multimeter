#PCB UPDATE - CURRENT (1/10/2021)

**Initial schematic for our PCB was designed for the multimeter. We will be only utilising a few modes for the WEEK 10 Demo.**

**Voltage Measurement (DC)** - We implemented a DC measurement circuit for our multimeter taking an input signal which will sum with out battery voltage (after being buffered) and this will return a voltage to the ADC which will then be calculated given the 
				       formula for conversion V = Resolution/ (2^16 - 1). This will then be outputted to the PC and LCD in the right units.

**Resistance Measurement** - We implemented a Resistance measurement mode which takes voltage from the Battery as an input across a voltage division circuit. We placed test points after the first resistor  and at ground for our "unknown resistor" and this will change oue Voltage ouput, allowing our ADC to return a voltage and then the software can then calculate the resistance from R2 = (Vo R1) / (Vin - Vo). This will give an accurate result for the resistance across the circuit and will be represented in appropriate units.

**Continuity Mode**	   - This mode will be derived from the above method for resistance, however, we will mostly utilise the software to represent if the circuit is shorted or is open.

