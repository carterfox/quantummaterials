// H11890api.cpp : Defines the exported functions for the DLL application.
//
#if defined(_MSC_VER)
	//  Microsoft
#include "stdafx.h"
#include <process.h>
#include <time.h>
#include <memory.h>
#elif defined(__GNUC__)
	//  GCC
//#include <math.h>
//#include <unistd.h>//for usleep
//#include <pthread.h>//To remove pthread_mutex_lock segmentation fault
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "H11890api.h"
#include "libusb.h"

//DEFINE CONSTANT for libusb
#define VENDOR_ID	(0x0661)
#define	PRODUCT_ID			(0x3705)
#define	TIMEOUT				(-1)		
#define	BULK_IN				(0x81)
#define	BULK_OUT			(0x01)
#define	INT_IN				(0x83)
#define	BULK_BUF_SIZE		(64)

#define MAXNUMOFCONNECTEDDEVICES 16

libusb_device *dev, **devs;
ssize_t cnt;
uint8_t path[8];
libusb_device_handle* Handle[MAXNUMOFCONNECTEDDEVICES] = {NULL, NULL, NULL , NULL , NULL , NULL , NULL , NULL, NULL, NULL, NULL , NULL , NULL , NULL , NULL , NULL};

typedef struct _H11890_PMINF {
	CHAR	VerInf[10];
	CHAR	AutoV;
	DWORD	SP;
	DWORD	SK;
	DWORD	DefHV;
	DWORD	Dark;
	DWORD	PulsePair;
	CHAR	BinMode;
	DWORD	WRNUM;
	CHAR	cSerialNumber[10];
	CHAR    cPMTSN[10];
	CHAR    cDate[10];
}H11890_PMINF;



// global value
DWORD	gNumberOfGate;
DWORD	gNumberOfRestData;
DWORD	gGateTime;
int gNumberOfDevice;

BOOL BulkOut(HANDLE handle, BYTE   *Buf, DWORD  *Length)
{
	DWORD	Outlen;
	int size;

	// Libusb‚ÌAPI Ver2.6.0
	Outlen = libusb_bulk_transfer((libusb_device_handle*)handle,
		BULK_OUT,
		(unsigned char*)Buf,
		(int)*Length,
		&size,
		500);		//500 ms

	if ((*Length) == LIBUSB_ERROR_PIPE) {
		libusb_clear_halt((libusb_device_handle*)handle, BULK_OUT);
	}

	if ((*Length) < 0) {
		return false;
	}

	(*Length) = Outlen;
	return true;
}

BOOL  BulkIn(HANDLE handle, BYTE	*Buf, DWORD  *Length)
{
	DWORD   Inlen;
	int size;

	Inlen = libusb_bulk_transfer((libusb_device_handle*)handle,
		BULK_IN,
		(unsigned char*)Buf,
		(int)*Length,
		&size,
		TIMEOUT);

	if ((*Length) == LIBUSB_ERROR_PIPE) {
		libusb_clear_halt((libusb_device_handle*)handle, BULK_OUT);
	}

	if ((*Length) < 0) {
		return false;
	}

	(*Length) = Inlen;
	return true;
}


DWORD SetIT(HANDLE handle, DWORD IT) {
	DWORD len;
	CHAR Buf[64], ChkBuf[8];
	int i;
	//Value Check
	IT = IT * 100;
	if (IT < 100 || IT > 1000000) {
		return -1;
	}
	for (i = 0; i < 64; i++)Buf[i] = 0;
	//Send Value
	Buf[0] = 'I';
	Buf[4] = *(unsigned char*)&IT;
	Buf[5] = *((unsigned char*)&IT + 1);
	Buf[6] = *((unsigned char*)&IT + 2);
	Buf[7] = *((unsigned char*)&IT + 3);
	for (i = 0; i < 8; i++)ChkBuf[i] = Buf[i];
	len = 8;
	if (!BulkOut(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -12;
	}
	len = 64;
	if (!BulkIn(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -13;
	}
	//Return Data Check
	for (i = 0; i < 8; i++) {
		if (!(ChkBuf[i] == Buf[i])) {
			return -14;
		}
	}
	gGateTime = IT;
	return 0;
}

DWORD ReadIT(HANDLE handle, DWORD *IT) {
	DWORD len;
	CHAR Buf[64];

	Buf[0] = 'I';
	len = 1;
	if (!BulkOut(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -22;
	}
	len = 64;
	if (!BulkIn(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -23;
	}
	*IT = *(unsigned long*)&Buf[4];
	gGateTime = *IT;
	*IT = *IT / 100;
	return 0;
}

DWORD SetRN(HANDLE handle, DWORD RN) {
	DWORD len;
	CHAR Buf[64], ChkBuf[8];
	int i;
	//Value Check
	if (RN < 0 || RN > 0xFFFFFFFF) {
		return -11;
	}
	for (i = 0; i < 64; i++)Buf[i] = 0;
	//Send Value
	Buf[0] = 'R';
	Buf[4] = *(unsigned char*)&RN;
	Buf[5] = *((unsigned char*)&RN + 1);
	Buf[6] = *((unsigned char*)&RN + 2);
	Buf[7] = *((unsigned char*)&RN + 3);
	for (i = 0; i < 8; i++)ChkBuf[i] = Buf[i];
	len = 8;
	if (!BulkOut(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -32;
	}
	len = 64;
	if (!BulkIn(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -33;
	}
	//Return Data Check
	for (i = 0; i < 8; i++) {
		if (!(ChkBuf[i] == Buf[i])) {
			return -34;
		}
	}
	gNumberOfGate = RN;
	return 0;
}

DWORD ReadRN(HANDLE handle, DWORD *RN) {
	DWORD len;
	CHAR Buf[64];

	Buf[0] = 'R';
	len = 1;
	if (!BulkOut(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -42;
	}
	len = 64;
	if (!BulkIn(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -43;
	}
	*RN = *(unsigned long*)&Buf[4];
	gNumberOfGate = *RN;
	return 0;
}

DWORD SetHV(HANDLE handle, DWORD HV) {
	DWORD len;
	CHAR Buf[64], ChkBuf[8];
	int i;
	//Value Check
	if (HV < 0 || HV > 1300) {
		return -51;
	}
	for (i = 0; i < 64; i++)Buf[i] = 0;
	//Send Value
	Buf[0] = 'V';
	Buf[4] = *(unsigned char*)&HV;
	Buf[5] = *((unsigned char*)&HV + 1);
	Buf[6] = *((unsigned char*)&HV + 2);
	Buf[7] = *((unsigned char*)&HV + 3);
	for (i = 0; i < 8; i++)ChkBuf[i] = Buf[i];
	len = 8;
	if (!BulkOut(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -52;
	}
	len = 64;
	if (!BulkIn(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -53;
	}
	//Return Data Check
	for (i = 0; i < 8; i++) {
		if (!(ChkBuf[i] == Buf[i])) {
			return -54;
		}
	}
	return 0;
}

DWORD ReadHV(HANDLE handle, DWORD *HV) {
	DWORD len;
	CHAR Buf[64];

	Buf[0] = 'V';
	len = 1;
	if (!BulkOut(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -62;
	}
	len = 64;
	if (!BulkIn(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -63;
	}
	*HV = *(unsigned long*)&Buf[4];
	return 0;
}

DWORD SetDL(HANDLE handle, DWORD DL) {
	DWORD len;
	CHAR Buf[64], ChkBuf[8];
	int i;
	//Value Check
	if (DL < 0 || DL > 3300) {
		return -31;
	}
	for (i = 0; i < 64; i++)Buf[i] = 0;
	//Send Value
	Buf[0] = 'L';
	Buf[4] = *(unsigned char*)&DL;
	Buf[5] = *((unsigned char*)&DL + 1);
	Buf[6] = *((unsigned char*)&DL + 2);
	Buf[7] = *((unsigned char*)&DL + 3);
	for (i = 0; i < 8; i++)ChkBuf[i] = Buf[i];
	len = 8;
	if (!BulkOut(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -72;
	}
	len = 64;
	if (!BulkIn(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -73;
	}
	//Return Data Check
	for (i = 0; i < 8; i++) {
		if (!(ChkBuf[i] == Buf[i])) {
			return -74;
		}
	}
	return 0;

}

DWORD SetDefHV(HANDLE handle) {
	DWORD len;
	CHAR Buf[64], ChkBuf[8];
	int i;
	Buf[0] = 'D';
	Buf[1] = 'V';
	for (i = 0; i < 2; i++)ChkBuf[i] = Buf[i];
	len = 2;
	if (!BulkOut(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -82;
	}
	len = 64;
	if (!BulkIn(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -83;
	}
	//Return Data Check
	for (i = 0; i < 2; i++) {
		if (!(ChkBuf[i] == Buf[i])) {
			return -84;
		}
	}
	return 0;
}

DWORD SetDefDL(HANDLE handle) {
	DWORD len;
	CHAR Buf[64], ChkBuf[8];
	int i;
	Buf[0] = 'D';
	Buf[1] = 'L';
	for (i = 0; i < 2; i++)ChkBuf[i] = Buf[i];
	len = 2;
	if (!BulkOut(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -92;
	}
	len = 64;
	if (!BulkIn(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -93;
	}
	//Return Data Check
	for (i = 0; i < 2; i++) {
		if (!(ChkBuf[i] == Buf[i])) {
			return -94;
		}
	}
	return 0;
}


DWORD ReadDL(HANDLE handle, DWORD *DL) {
	DWORD len;
	CHAR Buf[64];

	Buf[0] = 'L';
	len = 1;
	if (!BulkOut(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -102;
	}
	len = 64;
	if (!BulkIn(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -103;
	}
	*DL = *(unsigned long*)&Buf[4];
	return 0;
}

DWORD PMEN(HANDLE handle) {
	DWORD len;
	CHAR Buf[64], ChkBuf[8];
	int i;
	sprintf(Buf, "PMEN");
	for (i = 0; i < 4; i++)ChkBuf[i] = Buf[i];
	len = 4;
	if (!BulkOut(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -112;
	}
	len = 64;
	if (!BulkIn(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -113;
	}
	//Return Data Check
	for (i = 0; i < 4; i++) {
		if (!(ChkBuf[i] == Buf[i])) {
			return -114;
		}
	}
	return 0;
}

DWORD PMRD(HANDLE handle, H11890_PMINF *PMInf) {
	DWORD len;
	CHAR Buf[64], ChkBuf[8];
	int i;
	sprintf(Buf, "PMRD");
	for (i = 0; i < 4; i++)ChkBuf[i] = Buf[i];
	len = 4;
	if (!BulkOut(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -122;
	}
	len = 64;
	if (!BulkIn(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -123;
	}
	//Return Data Check
	for (i = 0; i < 4; i++) {
		if (!(ChkBuf[i] == Buf[i])) {
			return -124;
		}
	}
	for (i = 0; i < 10; i++) {
		PMInf[0].VerInf[i] = 0;
		PMInf[0].cSerialNumber[i] = 0;
		PMInf[0].cPMTSN[i] = 0;
		PMInf[0].cDate[i] = 0;
	}
	//Version
	strncpy(PMInf[0].VerInf, &Buf[4], 4);
	//AutoVoltage
	strncpy(&PMInf[0].AutoV, &Buf[8], 1);
	//SP
	PMInf[0].SP = *((DWORD*)&Buf[12]);
	//SK
	PMInf[0].SK = *((DWORD*)&Buf[16]);;
	//DefaultVoltage
	PMInf[0].DefHV = *((DWORD*)&Buf[20]);
	//Dark Count
	PMInf[0].Dark = *((DWORD*)&Buf[24]);
	//PulsePair
	PMInf[0].PulsePair = *((DWORD*)&Buf[28]);
	//Binary Mode for 232C
	strncpy(&PMInf[0].BinMode, &Buf[32], 1);
	//Write Number
	PMInf[0].WRNUM = *((DWORD*)&Buf[36]);
	//SN
	strncpy(PMInf[0].cSerialNumber, &Buf[40], 8);
	//PMTSN
	strncpy(PMInf[0].cPMTSN, &Buf[48], 8);
	//Date
	strncpy(PMInf[0].cDate, &Buf[56], 8);
	return 0;
}

DWORD PMWR(HANDLE handle, H11890_PMINF PMInf) {
	DWORD len;
	CHAR Buf[64];
	int i;
	for (i = 0; i < 64; i++)Buf[i] = 0;
	sprintf(Buf, "PMWR");


	//AutoVoltage
	strncpy(&Buf[8], &PMInf.AutoV, 1);
	//SP
	sprintf(&Buf[12], (char*)(&(PMInf.SP)));
	//SK
	sprintf(&Buf[16], (char*)(&(PMInf.SK)));
	//DefaultVoltage
	sprintf(&Buf[20], (char*)(&(PMInf.DefHV)));
	//Dark Count
	sprintf(&Buf[24], (char*)(&(PMInf.Dark)));
	//PulsePair
	sprintf(&Buf[28], (char*)(&(PMInf.PulsePair)));

	//Binary Mode for 232C
	strncpy(&Buf[32], (char*)&PMInf.BinMode, 1);
	//SN
	strncpy(&Buf[40], PMInf.cSerialNumber, 8);
	//PMTSN
	strncpy(&Buf[48], PMInf.cPMTSN, 8);
	//Date
	strncpy(&Buf[56], PMInf.cDate, 8);


	len = 64;
	if (!BulkOut(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -132;
	}
	len = 64;
	if (!BulkIn(handle, (unsigned char*)Buf, &len)) {
		//Error
		return -133;
	}
	return 0;
}

EXTERN_C HANDLE H11890API H11890Open(char* cSerialNumber) {
	DWORD i, j;
	DWORD len;

	CHAR Buf[0xFF];
	CHAR SN[10];
	H11890_INF Inf[16];
	for (i = 0; i < 10; i++) {
		SN[i] = 0;
	}

	for (i = 0; i < 16; i++) {
		Inf[i].hDeviceHandle = NULL;
		for (j = 0; j < 10; j++) {
			Inf[i].cSerialNumber[j] = 0;
		}
	}

	//gNumberOfReceivedData = 0;
	gNumberOfGate = 0;
	gGateTime = 0;
	gNumberOfRestData = 0;

	//If there is 
	if (gNumberOfDevice > 0) {
		for (i = 0; i < MAXNUMOFCONNECTEDDEVICES; i++) {
			if (Handle[i] != NULL) {
				libusb_release_interface(Handle[i], 0);
				libusb_close(Handle[i]);
				gNumberOfDevice--;
				Handle[i] = NULL;
			}
			if (gNumberOfDevice <= 0) {
				break;
			}
		}
	}

	int ret = libusb_init(NULL);
	if (ret < 0)
		return NULL;

	cnt = libusb_get_device_list(NULL, &devs);
	if (cnt < 0)
		return NULL;


	i = 0;
	while ((dev = devs[i++]) != NULL) {
		struct libusb_device_descriptor desc;
		int ret = libusb_get_device_descriptor(dev, &desc);
		if (ret < 0) {
			//fprintf(stderr, "failed to get device descriptor");
			return NULL;
		}
		if (desc.idVendor == VENDOR_ID && desc.idProduct == PRODUCT_ID) {
			ret = libusb_open(dev, &(Handle[gNumberOfDevice]));
			if (LIBUSB_SUCCESS == ret) {
				ret = libusb_claim_interface(Handle[gNumberOfDevice], 0);
				//CHAR chstr[128];
				//sprintf_s(chstr, "ret = %d", ret);
				if ((short)ret < 0) {
					//MessageBox(NULL, chstr, "libusb_claim_interface() error", MB_OK);
				}
				if (ret != LIBUSB_SUCCESS) {
					libusb_close(Handle[gNumberOfDevice]);
					printf("libusb_claim_interface failed: %s\n", libusb_error_name(ret));
				}
				else {
					gNumberOfDevice++;
					if (gNumberOfDevice == MAXNUMOFCONNECTEDDEVICES) break;
				}
			}
			else {
				return NULL;
			}
		}
	}

	for (i = 0; i < gNumberOfDevice; i++) {
		Inf[i].hDeviceHandle = (HANDLE)Handle[i];
		//‚q‚n‚lƒf[ƒ^‚Ì“Çž
		sprintf(Buf, "PMRD");
		len = 4;
		if (!BulkOut(Inf[i].hDeviceHandle, (unsigned char*)Buf, &len)) {
			//Error
			return NULL;
		}
		len = 64;
		if (!BulkIn(Inf[i].hDeviceHandle, (unsigned char*)Buf, &len)) {
			//Error
			return NULL;
		}

		//SN
		strncpy(Inf[i].cSerialNumber, &Buf[40], 8);

		strncpy(SN, cSerialNumber, 8);
		//‚q‚`‚lƒf[ƒ^‚Ì“Çž
		//Œ»Ý‚Ì‚o‚l‚sˆó‰Á“dˆ³
		DWORD HV;
		ReadHV(Inf[i].hDeviceHandle, &HV);

		if (HV == 0) {
			Inf[i].HVON = FALSE;
		}
		else {
			Inf[i].HVON = TRUE;
		}
		//Œ»Ý‚ÌÏŽZŽžŠÔ
		ReadIT(Inf[i].hDeviceHandle, &Inf[i].IT);

		//Œ»Ý‚ÌŒJ•Ô‰ñ”
		ReadRN(Inf[i].hDeviceHandle, &Inf[i].RN);

	}
	//ˆê’v‚µ‚½ƒnƒ“ƒhƒ‹‚ð•Ô‚·B

	for (i = 0; i < gNumberOfDevice; i++) {
		if (strcmp(Inf[i].cSerialNumber, SN) == 0) {
			return Inf[i].hDeviceHandle;
		}
	}
	return NULL;
}

EXTERN_C DWORD H11890API H11890OpenDevices(H11890_INF Inf[16]) {
	DWORD i, j;
	DWORD len;

	CHAR Buf[64];

	//If there is 
	if (gNumberOfDevice > 0) {
		for (i = 0; i < MAXNUMOFCONNECTEDDEVICES; i++) {
			if (Handle[i] != NULL) {
				libusb_release_interface(Handle[i], 0);
				libusb_close(Handle[i]);
				gNumberOfDevice--;
				Handle[i] = NULL;
				for (j = 0; j < 10; j++) {
					Inf[i].cSerialNumber[j] = 0;
				}
			}
			Inf[i].hDeviceHandle = NULL;
			if (gNumberOfDevice <= 0) {
				break;
			}
		}
	}


	//gNumberOfReceivedData = 0;
	gNumberOfGate = 0;
	gGateTime = 0;
	gNumberOfRestData = 0;


	int ret = libusb_init(NULL);
	if (ret < 0)
		return FALSE;

	cnt = libusb_get_device_list(NULL, &devs);
	if (cnt < 0)
		return FALSE;
	
	i = 0;
	while ((dev = devs[i++]) != NULL) {
		struct libusb_device_descriptor desc;
		int ret = libusb_get_device_descriptor(dev, &desc);
		if (ret < 0) {
			//fprintf(stderr, "failed to get device descriptor");
			return FALSE;
		}
		if (desc.idVendor == VENDOR_ID && desc.idProduct == PRODUCT_ID) {
			ret = libusb_open(dev, &(Handle[gNumberOfDevice]));
			if (LIBUSB_SUCCESS == ret) {
				ret = libusb_claim_interface(Handle[gNumberOfDevice], 0);
				//CHAR chstr[128];
				//sprintf_s(chstr, "ret = %d", ret);
				if ((short)ret < 0) {
					//MessageBox(NULL, chstr, "libusb_claim_interface() error", MB_OK);
				}
				if (ret != LIBUSB_SUCCESS) {
					libusb_close(Handle[gNumberOfDevice]);
					printf("libusb_claim_interface failed: %s\n", libusb_error_name(ret));
				}
				else {
					Inf[gNumberOfDevice].hDeviceHandle = Handle[gNumberOfDevice];
					gNumberOfDevice++;
					if (gNumberOfDevice == MAXNUMOFCONNECTEDDEVICES) break;
				}
			}
			else {
				return FALSE;
			}
		}
	}


	//ƒfƒoƒCƒXî•ñ‚ÌŽæ“¾
	for (i = 0; i < gNumberOfDevice; i++) {
		//‚q‚n‚lƒf[ƒ^‚Ì“Çž
		sprintf(Buf, "PMRD");
		len = 4;
		if (!BulkOut(Inf[i].hDeviceHandle, (unsigned char*)Buf, &len)) {
			//Error
			return -1;
		}
		len = 64;
		if (!BulkIn(Inf[i].hDeviceHandle, (unsigned char*)Buf, &len)) {
			//Error
			return -1;
		}

		//SN
		strncpy(Inf[i].cSerialNumber, &Buf[40], 8);
		//‚q‚`‚lƒf[ƒ^‚Ì“Çž
		//Œ»Ý‚Ì‚o‚l‚sˆó‰Á“dˆ³
		DWORD HV;
		ReadHV(Inf[i].hDeviceHandle, &HV);

		if (HV == 0) {
			Inf[i].HVON = FALSE;
		}
		else {
			Inf[i].HVON = TRUE;
		}
		//Œ»Ý‚ÌÏŽZŽžŠÔ
		ReadIT(Inf[i].hDeviceHandle, &Inf[i].IT);

		//Œ»Ý‚ÌŒJ•Ô‰ñ”
		ReadRN(Inf[i].hDeviceHandle, &Inf[i].RN);

	}
	return gNumberOfDevice;

}


EXTERN_C BOOL H11890API H11890Close(HANDLE hDeviceHandle) {
	int i = 0;

	if (hDeviceHandle == NULL) return FALSE;

	if (gNumberOfDevice <= 0) {
		//No handle
		return FALSE;
	}

	if (hDeviceHandle != NULL) {
		int handlenum;
		for (int j = 0; j < MAXNUMOFCONNECTEDDEVICES; j++) {
			if (hDeviceHandle == (HANDLE)Handle[j]) {
				handlenum = j;
				break;
			}
		}
		libusb_release_interface((libusb_device_handle*)hDeviceHandle, 0);
		libusb_close((libusb_device_handle*)hDeviceHandle);
		gNumberOfDevice--;
		Handle[handlenum] = NULL;
	}
	return TRUE;

}
//**************************************************************************************************************
//
//	ƒfƒoƒCƒXƒNƒ[ƒY
//
//**************************************************************************************************************
EXTERN_C void H11890API H11890CloseDevices(H11890_INF Inf[16]) {

	if (gNumberOfDevice <= 0) {
		//No handle
		return;
	}

	for (int i = 0; i < MAXNUMOFCONNECTEDDEVICES; i++) {
		if (Inf[i].hDeviceHandle != NULL) {
			libusb_release_interface((libusb_device_handle*)Inf[i].hDeviceHandle, 0);
			libusb_close((libusb_device_handle*)Inf[i].hDeviceHandle);
			gNumberOfDevice--;
			Handle[i] = NULL;
			Inf[i].hDeviceHandle = NULL;
			if (gNumberOfDevice <= 0) break;
		}
	}

	return;

}
//**************************************************************************************************************
//
//	ƒfƒoƒCƒXÝ’è‘‚«ž‚Ý
//
//**************************************************************************************************************
EXTERN_C BOOL H11890API H11890SetInf(H11890_INF &Inf) {
	DWORD	RetVal;

	if (Inf.hDeviceHandle != NULL) {
		//IT = from 1 ms to 10 s
		if (Inf.IT < 1 || Inf.IT>10000) {
			return FALSE;
		}
		//RN = from 0 to 0xFFFFFFFF
		if (Inf.RN < 0 || Inf.RN>0xFFFFFFFF) {
			return FALSE;
		}
		RetVal = SetIT(Inf.hDeviceHandle, Inf.IT);
		if (RetVal)return FALSE;
		RetVal = SetRN(Inf.hDeviceHandle, Inf.RN);
		if (RetVal)return FALSE;
		if (Inf.HVON) {
			RetVal = SetDefHV(Inf.hDeviceHandle);
			if (RetVal)return FALSE;
		}
		else {
			RetVal = SetHV(Inf.hDeviceHandle, 0);
			if (RetVal)return FALSE;
		}
		return TRUE;
	}
	return FALSE;
}


EXTERN_C BOOL H11890API H11890SetInfEx(H11890_INF *Inf) {
	DWORD	RetVal;

	if (Inf->hDeviceHandle != NULL) {
		//IT = from 1 ms to 10 s
		if (Inf->IT < 1 || Inf->IT>10000) {
			return FALSE;
		}
		//RN = from 0 to 0xFFFFFFFF
		if (Inf->RN < 0 || Inf->RN>0xFFFFFFFF) {
			return FALSE;
		}
		RetVal = SetIT(Inf->hDeviceHandle, Inf->IT);
		if (RetVal)return FALSE;
		RetVal = SetRN(Inf->hDeviceHandle, Inf->RN);
		if (RetVal)return FALSE;
		if (Inf->HVON) {
			RetVal = SetDefHV(Inf->hDeviceHandle);
			if (RetVal)return FALSE;
		}
		else {
			RetVal = SetHV(Inf->hDeviceHandle, 0);
			if (RetVal)return FALSE;
		}
		return TRUE;
	}
	return FALSE;
}
//**************************************************************************************************************
//
//	ƒfƒoƒCƒXÝ’è“Çž
//
//**************************************************************************************************************
EXTERN_C BOOL H11890API H11890ReadInf(H11890_INF &Inf) {
	DWORD 	HV;
	DWORD	RetVal;
	if (Inf.hDeviceHandle != NULL) {
		RetVal = ReadIT(Inf.hDeviceHandle, &Inf.IT);
		if (RetVal)return false;
		RetVal = ReadRN(Inf.hDeviceHandle, &Inf.RN);
		if (RetVal)return false;
		RetVal = ReadHV(Inf.hDeviceHandle, &HV);
		if (RetVal)return false;
		if (HV == 0) {
			Inf.HVON = FALSE;
		}
		else {
			Inf.HVON = TRUE;
		}
		return true;
	}

	return false;

}


EXTERN_C BOOL H11890API H11890ReadInfEx(H11890_INF *Inf) {
	DWORD 	HV;
	DWORD	RetVal;
	if (Inf->hDeviceHandle != NULL) {
		RetVal = ReadIT(Inf->hDeviceHandle, &(Inf->IT));
		if (RetVal)return false;
		RetVal = ReadRN(Inf->hDeviceHandle, &(Inf->RN));
		if (RetVal)return false;
		RetVal = ReadHV(Inf->hDeviceHandle, &HV);
		if (RetVal)return false;
		if (HV == 0) {
			Inf->HVON = FALSE;
		}
		else {
			Inf->HVON = TRUE;
		}
		return true;
	}

	return false;

}
//**************************************************************************************************************
//
//@ƒJƒEƒ“ƒgƒXƒ^[ƒg
//
//**************************************************************************************************************
EXTERN_C BOOL H11890API H11890CountStart(HANDLE handle, BOOL Correction) {
	CHAR	Buf[64];
	DWORD 	len;

	if (handle == NULL)return false;

	//
	if (!(gNumberOfRestData == 0)) {
		len = 64;
		while (gNumberOfRestData > 0) {
			BulkIn(handle, (unsigned char*)Buf, &len);
			gNumberOfRestData--;
		}
	}
	//ƒQ[ƒgŽžŠÔ‚ªÝ’è‚³‚ê‚Ä‚¢‚È‚¢ê‡
	if (gGateTime == 0) {
		return false;
	}

	//Žc‚èƒf[ƒ^”‚ðƒQ[ƒg”•ª‚ÉÝ’è
	gNumberOfRestData = gNumberOfGate;
	//ŽóMƒf[ƒ^”‚ðƒNƒŠƒA
	//gNumberOfReceivedData = 0;
	//ƒXƒ^[ƒgƒRƒ}ƒ“ƒh‚ð‘—M
	if (Correction == FALSE) {
		Buf[0] = 'C';	//normal acquisition
	}
	else {
		Buf[0] = 'M';  	//acquisition with correction
	}
	len = 1;
	if (!BulkOut(handle, (unsigned char*)Buf, &len)) {
		return false;
	}
	return true;
}
//**************************************************************************************************************
//
//@ƒJƒEƒ“ƒgƒXƒgƒbƒv
//
//**************************************************************************************************************
EXTERN_C BOOL H11890API H11890CountStop(HANDLE handle) {
	CHAR	Buf[64];
	DWORD 	len;
	//clock_t	start, finish;
	//DWORD	RestData;
	//SHORT	num;

	if (handle == NULL)return false;

	// ƒXƒgƒbƒv‚ÌƒRƒ}ƒ“ƒh‚ð‘—M‚·‚é
	Buf[0] = 0x0d;	//normal acquisition
	len = 1;
	if (!BulkOut(handle, (unsigned char*)Buf, &len)) {
		return false;
		//if(!BulkOut(handle,(unsigned char*)Buf,&len))return FALSE;
	}
	len = 64;
	if (gNumberOfRestData == 0) {
		if (!BulkIn(handle, (unsigned char*)Buf, &len)) {
			return false;
		}
	}
	gNumberOfRestData = 0;

	//usb_resetep((usb_dev_handle*)handle, BULK_IN);//karp

	return true;
}
//**************************************************************************************************************
//
//@ƒf[ƒ^ƒŠ[ƒh
//
//**************************************************************************************************************
EXTERN_C DWORD H11890API H11890ReadData(HANDLE handle, DWORD *GateNum, DWORD *DataBuf, BOOL *OLD) {
	CHAR	Buf[64];
	DWORD 	len;
	BOOL		aOLD = FALSE;
	//short	num;
	int i;

	if (handle == NULL) {
		return -2;
	}
	*OLD = FALSE;
	if (!(gNumberOfGate == 0)) {
		//if(gNumberOfReceivedData >= gNumberOfGate){
		if (gNumberOfRestData == 0) {
			return -3;
		}
	}
	//ƒf[ƒ^‚Ì“Çž
	len = 64;
	if (!BulkIn(handle, (unsigned char*)Buf, &len)) {
		return -4;	//Error
	}
	if (gGateTime > 1000) {						// 1000/100 = 10msˆÈã
		//gNumberOfReceivedData++;
		gNumberOfRestData--;
		*GateNum = *(unsigned long*)&Buf[0];
		*DataBuf = *(unsigned long*)&Buf[4];
		if ((*DataBuf) & 0x80000000) {
			*OLD = TRUE;
		}
		else {
			*OLD = FALSE;
		}
		*DataBuf = *DataBuf & 0x7FFFFFFF;
		return 1;
	}
	else {
		*GateNum = *(unsigned long*)&Buf[0];
		for (i = 0; i < 15; i++) {
			//gNumberOfReceivedData++;
			if (gNumberOfRestData > 0) {
				gNumberOfRestData--;
			}
			*DataBuf = *(unsigned long*)&Buf[4 + 4 * i];
			if ((*DataBuf) & 0x80000000)aOLD = TRUE;
			*DataBuf = *DataBuf & 0x7FFFFFFF;
			DataBuf++;
		}
		if (aOLD == TRUE)*OLD = TRUE;
		return 15;
	}

}


EXTERN_C BOOL H11890API H11890SetIT(HANDLE handle, DWORD IT) {
	DWORD	dwRtn;
	if (IT < 1 || IT>10000) {
		return false;
	}
	dwRtn = SetIT(handle, IT);
	if (dwRtn == 0) {
		return true;
	}
	else {
		return false;
	}
}
//
EXTERN_C BOOL H11890API H11890ReadIT(HANDLE handle, DWORD *IT) {
	DWORD dwRtn;
	dwRtn = ReadIT(handle, IT);
	if (dwRtn == 0) {
		return true;
	}
	else {
		return false;
	}
}
//
EXTERN_C BOOL H11890API H11890SetRN(HANDLE handle, DWORD RN) {
	DWORD dwRtn;
	if (RN < 0 || RN>0xFFFFFFFF) {
		return false;
	}
	dwRtn = SetRN(handle, RN);
	if (dwRtn == 0) {
		return true;
	}
	else {
		return false;
	}
}
//
EXTERN_C BOOL H11890API H11890ReadRN(HANDLE handle, DWORD *RN) {
	DWORD dwRtn;
	dwRtn = ReadRN(handle, RN);
	if (dwRtn == 0) {
		return true;
	}
	else {
		return false;
	}
}
//
EXTERN_C BOOL H11890API H11890SetHV(HANDLE handle, BOOL HV) {
	DWORD dwRtn;

	if (HV == TRUE) {
		dwRtn = SetDefHV(handle);
		if (dwRtn == 0) {
			return true;
		}
		else {
			return false;
		}
	}
	else {
		dwRtn = SetHV(handle, (DWORD)0);
		if (dwRtn == 0) {
			return true;
		}
		else {
			return false;
		}
	}
}
//
EXTERN_C BOOL H11890API H11890ReadHV(HANDLE handle, BOOL *HV) {
	DWORD dwRtn;
	DWORD	HVVAL;
	HVVAL = 0;
	dwRtn = ReadHV(handle, &HVVAL);
	if (dwRtn == 0) {
		if (HVVAL == 0) {
			*HV = FALSE;
		}
		else {
			*HV = TRUE;
		}
		return true;
	}
	else {
		return false;
	}
}
