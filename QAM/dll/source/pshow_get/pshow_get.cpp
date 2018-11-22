// pshow_get.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include "tchar.h"
#include "stdint.h"
#include "process.h"
#include "stdlib.h"
#include "stdio.h"
#include "pshow_get.h"

pshow_common_ipc_t *ipc_map = NULL;
uint16_t session_id = 0;
HANDLE	m_hMapFile;
HANDLE	m_event = NULL;
CRITICAL_SECTION  CriticalSection;

uint64_t	gl_block_id[PSHOW_MAX_CHANNEL_NUM];
uint64_t	gl_collected_block_id;
uint32_t	gl_channel_mask;

DWORD		gl_timeout;

void pshow_init()
{
	InitializeCriticalSection(&CriticalSection);
	m_event = CreateEvent(NULL, TRUE, FALSE, _T(PSHOW_EVENT_NAME));
}

void pshow_close()
{
	EnterCriticalSection(&CriticalSection);
	
	if (ipc_map)
	{
		UnmapViewOfFile(ipc_map);
		CloseHandle(m_hMapFile);
	}

	ipc_map = NULL;
	m_hMapFile = NULL;

	LeaveCriticalSection(&CriticalSection);

	CloseHandle(m_event);
}


EXPORT_API int test(void) {

	return 666;
}

EXPORT_API int pshow_set(	uint32_t channels_num,
							uint32_t index, int channel_phase_add, uint64_t block_id,
							void *data, uint32_t iq_num)
{
	if ((channels_num > PSHOW_MAX_CHANNEL_NUM) ||
		(index >= channels_num) ||
		(data == NULL))
		return -1;

	if (index == 0)
	{
		if (m_hMapFile == NULL)
		{
			m_hMapFile = CreateFileMapping(INVALID_HANDLE_VALUE,
				NULL,
				PAGE_READWRITE,
				0,
				sizeof(pshow_common_ipc_t),
				_T(PSHOW_MEM_NAME));
		}

		if ((ipc_map == NULL) && m_hMapFile)
		{
			EnterCriticalSection(&CriticalSection);
			ipc_map = (pshow_common_ipc_t *)MapViewOfFile(m_hMapFile,	// handle to map object
				FILE_MAP_ALL_ACCESS,									// read/write permission
				0,
				0,
				sizeof(pshow_common_ipc_t));

			if (ipc_map)
			{
				srand(GetTickCount());

				ipc_map->ver = PSHOW_VER;
				ipc_map->session_id = rand() | 1;
				InterlockedExchange(&ipc_map->status, pshow_STATUS_DATA_WAIT);
				ipc_map->channel_num = channels_num;
				ipc_map->data_num = (iq_num > MAX_IQ_DATA_NUM) ? (MAX_IQ_DATA_NUM) : (iq_num);

				gl_collected_block_id = MAXDWORD64;
				for (int i = 0; i < PSHOW_MAX_CHANNEL_NUM; i++)
					ipc_map->channel[i].phase_add = 0;
			}
			LeaveCriticalSection(&CriticalSection);
		}
	}

	if (ipc_map)
	{
		IQ_data_t *iq_data = &ipc_map->channel[index];

		long status = InterlockedAdd(&ipc_map->status, 0);

		switch (status)
		{
		case pshow_STATUS_DATA_WAIT:
			InterlockedExchange(&ipc_map->status, pshow_STATUS_DATA_PROCESS);
		case pshow_STATUS_DATA_PROCESS:
		{
			EnterCriticalSection(&CriticalSection);

			if ((gl_block_id[index] == MAXDWORD64) &&
				(gl_collected_block_id < block_id))
				gl_collected_block_id = MAXDWORD64;

			if (gl_collected_block_id == MAXDWORD64)
			{
				gl_channel_mask = 0;
				gl_collected_block_id = block_id;
				for (int i = 0; i < channels_num; i++)
					gl_block_id[i] = MAXDWORD64;
			}

			if (gl_collected_block_id == block_id)
			{
				LeaveCriticalSection(&CriticalSection);

				iq_data->phase_add = channel_phase_add;
				uint32_t size = (iq_num > MAX_IQ_DATA_NUM) ? (MAX_IQ_DATA_NUM * 4) : (iq_num * 4);
				memcpy(iq_data->data, data, size);

				EnterCriticalSection(&CriticalSection);

				if (gl_collected_block_id == block_id)
				{
					gl_block_id[index] = block_id;
					gl_channel_mask |= (1 << index);

					if (gl_channel_mask == ((1 << channels_num) - 1))
					{
						LeaveCriticalSection(&CriticalSection);

						if (InterlockedCompareExchange(&ipc_map->status, pshow_STATUS_DATA_READY, pshow_STATUS_DATA_PROCESS) == pshow_STATUS_DATA_PROCESS)
						{
							//if (WaitForSingleObject(m_event, 0) != WAIT_OBJECT_0)
								SetEvent(m_event);

							gl_timeout = GetTickCount();
						}

						EnterCriticalSection(&CriticalSection);

						gl_collected_block_id = MAXDWORD64;
					}
				}
			}

			LeaveCriticalSection(&CriticalSection);
			break;
		}
		case pshow_STATUS_DATA_READY:
			gl_timeout = GetTickCount();
			break;
		case pshow_STATUS_DATA_BUSY:
			if ((GetTickCount() - gl_timeout) < 1000)
				break;

		default:
			UnmapViewOfFile(ipc_map);
			CloseHandle(m_hMapFile);

			ipc_map = NULL;
			m_hMapFile = NULL;
			break;
		}
	}

	return 0;
}

EXPORT_API int pshow_get(uint32_t *channels_num, int32_t *phase_add, uint16_t *data, uint32_t iq_max_num, uint32_t timeout_ms)
{
	DWORD tick = GetTickCount();
	
	if (ipc_map == NULL)
	{
		EnterCriticalSection(&CriticalSection);

		while (ipc_map == NULL)
		{
			m_hMapFile = OpenFileMapping(FILE_MAP_ALL_ACCESS,	// read/write access
				FALSE,					// do not inherit the name
				_T(PSHOW_MEM_NAME));

			if (m_hMapFile != NULL)
			{

				// Map to the file
				ipc_map = (pshow_common_ipc_t *)MapViewOfFile(m_hMapFile,				// handle to map object
					FILE_MAP_ALL_ACCESS,	// read/write permission
					0,
					0,
					sizeof(pshow_common_ipc_t));

				if (ipc_map)
				{
					session_id = ipc_map->session_id;
					break;
				}
				else
				{
					CloseHandle(m_hMapFile);
					m_hMapFile = NULL;
				}
			}

			if (timeout_ms)
			{
				if ((timeout_ms == INFINITE) || (timeout_ms < (GetTickCount() - tick)))
				{
					LeaveCriticalSection(&CriticalSection);
					Sleep(10);
					EnterCriticalSection(&CriticalSection);
					continue;
				}
			}
			break;
		}

		LeaveCriticalSection(&CriticalSection);
	}

	if ((ipc_map == NULL) || (m_event = NULL))
		return PSHOW_ERR_TIMEOUT;	// нет источника данных

	if (ipc_map->ver != PSHOW_VER)
		return PSHOW_ERR_VER; //  версии не совпадают
		
	while (ipc_map->session_id == session_id)
	{
		if (InterlockedCompareExchange(&ipc_map->status, pshow_STATUS_DATA_BUSY, pshow_STATUS_DATA_READY) == pshow_STATUS_DATA_READY)
		{
			uint32_t num = ipc_map->channel_num;
			uint32_t data_num = ipc_map->data_num;

			if (channels_num)
				*channels_num = num;

			if (iq_max_num >= data_num * num)
			{
				uint16_t *iq_data = data;
				for (int i = 0; i < num; i++)
				{
					if (iq_data)
					{
						memcpy(iq_data, &ipc_map->channel[i].data[0], data_num * 4);
						iq_data += data_num * 2;
					}
					if (phase_add)
						phase_add[i] = ipc_map->channel[i].phase_add;
				}
			}

			if (InterlockedCompareExchange(&ipc_map->status, pshow_STATUS_DATA_WAIT, pshow_STATUS_DATA_BUSY) == pshow_STATUS_DATA_BUSY)
			{
				if (iq_max_num >= data_num * num)
					return data_num;

				return PSHOW_ERR_BUFFER_TO_SMALL;
			}
			break;
		}
		
		DWORD elapsed_tick = GetTickCount() - tick;

		if (timeout_ms && ((timeout_ms == INFINITE) || (timeout_ms < elapsed_tick)))
		{
			if (timeout_ms != INFINITE)
				WaitForSingleObject(m_event, timeout_ms - elapsed_tick);
			else
				WaitForSingleObject(m_event, timeout_ms);

			ResetEvent(m_event);
			continue;
		}
		return PSHOW_ERR_TIMEOUT;
	}

	UnmapViewOfFile(ipc_map);
	CloseHandle(m_hMapFile);

	ipc_map = NULL;
	m_hMapFile = NULL;
	return PSHOW_ERR_NEW_SESSION; // переподключение
}