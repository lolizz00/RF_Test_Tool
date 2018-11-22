// pshow_test.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "windows.h"
#include "pshow_get.h"


int main()
{
	int iq_max_num = 1024 * 1024;
	uint16_t *iq_buffer = new uint16_t[iq_max_num * 2];
	int32_t	  phase_add[PSHOW_MAX_CHANNEL_NUM];

	while (1)
	{
		uint32_t channels_num;
		int result = pshow_get(&channels_num, phase_add, iq_buffer, iq_max_num, INFINITE);

		if (result > 0)
		{
			uint32_t *iq_val = (uint32_t *)iq_buffer;
			uint32_t iq_num = result;

			uint32_t temp = *iq_val;

			for (int i = 0; i < channels_num; i++)
			{
				if (*iq_val != temp)
				{
					printf_s("counter not in sync\n");
				}
				iq_val += iq_num;
			}
		}
	}


    return 0;
}

