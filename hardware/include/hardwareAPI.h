#ifndef HARDWARE_H
#define HARDWARE_H

#include <stdint.h>

int initHardware(void);
void ledToggle(void);
void delay_ms(uint16_t delay);
void delay_sec(uint8_t delay);

#endif // HARDWARE_H
