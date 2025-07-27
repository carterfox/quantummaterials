#ifdef __cplusplus
extern "C" {
#endif //__cplusplus
#if defined(_MSC_VER)
	//  Microsoft
#ifdef H11890API_EXPORTS
#define H11890API __declspec(dllexport)
#else
#define H11890API __declspec(dllimport)
#endif
#elif defined(__GNUC__)
	//  GCC
#define EXTERN_C //add by karp
#ifdef H11890API_EXPORTS
#define H11890API __attribute__ ((visibility("default")))
#else
#define H11890API 
#endif

#define TRUE 1
#define FALSE 0
    typedef char CHAR;
	typedef unsigned char BYTE;
	typedef unsigned char UCHAR;
	typedef short SHORT;
	typedef unsigned short WORD;
	typedef unsigned long DWORD;
	typedef unsigned long ULONG;
	typedef void* HANDLE;
	typedef int BOOL;

#else
	//  do nothing and hope for the best?
#define H11890API 
#pragma warning Unknown dynamic link export/import semantics.
#endif

//structure
	typedef struct _H11890_INF {
		HANDLE  hDeviceHandle;
		CHAR    cSerialNumber[10];
		DWORD 	IT;               	//from 1(1 ms) to 10000(10s)
		DWORD 	RN;             		//from 0(continuous) to 0xFFFFFFFF
		BOOL	HVON;									//FALSE -> OFF / TRUE -> ON(plateau voltage)
	}H11890_INF;

// Functions
	DWORD	H11890API H11890OpenDevices(H11890_INF Inf[16]);
	void	H11890API H11890CloseDevices(H11890_INF Inf[16]);
	BOOL	H11890API H11890SetInf(H11890_INF &Inf);
	BOOL	H11890API H11890ReadInf(H11890_INF &Inf);
	BOOL	H11890API H11890SetInfEx(H11890_INF *Inf);
	BOOL	H11890API H11890ReadInfEx(H11890_INF *Inf);
	BOOL	H11890API H11890CountStart(HANDLE handle, BOOL Correction);
	BOOL	H11890API H11890CountStop(HANDLE handle);
	DWORD	H11890API H11890ReadData(HANDLE handle, DWORD *GateNum, DWORD *DataBuf, BOOL *OLD);
	HANDLE	H11890API H11890Open(char* cSerialNumber);
	BOOL	H11890API H11890Close(HANDLE hDeviceHandle);
	BOOL	H11890API H11890ReadHV(HANDLE handle, BOOL *HV);
	BOOL	H11890API H11890ReadIT(HANDLE handle, DWORD *IT);
	BOOL	H11890API H11890ReadRN(HANDLE handle, DWORD *RN);
	BOOL	H11890API H11890SetHV(HANDLE handle, BOOL HV);
	BOOL	H11890API H11890SetIT(HANDLE handle, DWORD IT);
	BOOL	H11890API H11890SetRN(HANDLE handle, DWORD RN);

#ifdef __cplusplus
}
#endif //__cplusplus
