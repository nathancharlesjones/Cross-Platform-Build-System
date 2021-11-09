// Needed for clock_gettime()
// Has to be at the begining of the file
#define _GNU_SOURCE

#include <stdio.h>
#include <time.h>
#include "hardwareAPI.h"

int initHardware(void)
{
	// No hardware to init
	return 0;
}

void ledToggle(void)
{
	printf("Toggling the LED!\n");
}

void delay_ms(uint16_t delay)
{
    struct timespec startTime;
    struct timespec currentTime;

    clock_gettime(CLOCK_THREAD_CPUTIME_ID, &startTime);
    do
    {
    	clock_gettime(CLOCK_THREAD_CPUTIME_ID, &currentTime);
    } while( ( ( currentTime.tv_nsec - startTime.tv_nsec ) / 1000000 ) < delay );
}

void delay_sec(uint8_t delay)
{
    struct timespec startTime;
    struct timespec currentTime;

    clock_gettime(CLOCK_THREAD_CPUTIME_ID, &startTime);
    do
    {
    	clock_gettime(CLOCK_THREAD_CPUTIME_ID, &currentTime);
    } while( ( currentTime.tv_sec - startTime.tv_sec ) < delay );
}