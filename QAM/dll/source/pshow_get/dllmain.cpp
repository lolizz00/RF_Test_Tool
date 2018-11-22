// dllmain.cpp : Defines the entry point for the DLL application.
#include "stdafx.h"

extern void pshow_init();
extern void pshow_close();

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
					 )
{
	switch (ul_reason_for_call)
	{
	case DLL_PROCESS_ATTACH:
		pshow_init();
		break;
	case DLL_PROCESS_DETACH:
		pshow_close();
		break;

	case DLL_THREAD_ATTACH:
	case DLL_THREAD_DETACH:
		break;
	}
	return TRUE;
}
