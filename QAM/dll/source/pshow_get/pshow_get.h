#pragma once

#ifndef __PSHOW_H__
#define __PSHOW_H__

#include "stdint.h"





#if defined(PSHOW_GET_EXPORTS)
#define	EXPORT_API	extern "C" __declspec(dllexport)
#else
#define	EXPORT_API extern "C"	__declspec(dllimport)
#endif

#define	pshow_STATUS_DATA_WAIT		0
#define	pshow_STATUS_DATA_PROCESS	1
#define	pshow_STATUS_DATA_READY		2
#define	pshow_STATUS_DATA_BUSY		3

#define	PSHOW_VER		 0x01
#define	PSHOW_MEM_NAME	 "pshow_shared_mem"
#define	PSHOW_EVENT_NAME "pshow_ready_event"
#define	PSHOW_MAX_CHANNEL_NUM 32
#define	MAX_IQ_DATA_NUM	1

typedef struct IQ_data
{
	int32_t		phase_add;
	uint16_t	data[MAX_IQ_DATA_NUM * 2];
} IQ_data_t;

typedef struct pshow_common_ipc
{
	volatile uint64_t session_id;
	uint32_t		  ver;
	volatile long	  status;

	uint32_t	data_num;
	uint32_t	channel_num;
	IQ_data_t	channel[PSHOW_MAX_CHANNEL_NUM];
} pshow_common_ipc_t;

HANDLE pshow_ready_event;

#define	PSHOW_ERR_TIMEOUT		-1
#define	PSHOW_ERR_VER			-2
#define	PSHOW_ERR_NEW_SESSION	-3
#define	PSHOW_ERR_BUFFER_TO_SMALL	-4

EXPORT_API int test(void);

EXPORT_API int pshow_get(uint32_t *channels_num, int32_t *phase_add, uint16_t *data, uint32_t iq_max_num, uint32_t timeout_ms);

EXPORT_API int pshow_set(	uint32_t channels_num,
							uint32_t index, int channel_phase_add, uint64_t block_id,
							void *data, uint32_t iq_num);
#endif
