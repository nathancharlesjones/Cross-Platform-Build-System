#include "hardwareAPI.h"

int main(void)
{
	initHardware();

	while(1)
	{
		ledToggle();
		delay_sec(1);
	}

	return 0;
}