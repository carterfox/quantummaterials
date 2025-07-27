#ifndef _H11890_API_Header
#define _H11890_API_Header
// 以下の ifdef ブロックは DLL から簡単にエクスポートさせるマクロを作成する標準的な方法です。 
// この DLL 内のすべてのファイルはコマンドラインで定義された H11890API_EXPORTS シンボル
// でコンパイルされます。このシンボルはこの DLL が使用するどのプロジェクト上でも未定義でなけ
// ればなりません。この方法ではソースファイルにこのファイルを含むすべてのプロジェクトが DLL 
// からインポートされたものとして H11890API_API 関数を参照し、そのためこの DLL はこのマク 
// ロで定義されたシンボルをエクスポートされたものとして参照します。

#ifdef H11890API_EXPORTS
#define H11890API __declspec(dllexport)
#else
#define H11890API __declspec(dllimport)
#endif


typedef struct _H11890_INF{
	HANDLE  hDeviceHandle;
	CHAR    cSerialNumber[10];
	DWORD 	IT;               	//from 1(1 ms) to 10000(10s)
	DWORD 	RN;             		//from 0(continuous) to 0xFFFFFFFF
	BOOL	HVON;									//FALSE -> OFF / TRUE -> ON(plateau voltage)
}H11890_INF;


// -----------------------------------------------

//
// DLL Export Function
//
#ifdef __cplusplus
extern "C" {
#endif

//Open Device
HANDLE		H11890API __stdcall H11890Open(char* cSerialNumber);
//Close Device
BOOL			H11890API __stdcall H11890Close(HANDLE hDeviceHandle);
//Open Multi Device 
DWORD			H11890API __stdcall H11890OpenDevices(H11890_INF Inf[16]);
//Close Device
void			H11890API __stdcall H11890CloseDevices(H11890_INF Inf[16]);
//Set Device Information	Inf.IT & Inf.RN & Inf.HVON
BOOL			H11890API __stdcall H11890SetInf(H11890_INF &Inf);
//Read Device Information	Inf.IT & Inf.RN & Inf.HVON
BOOL			H11890API __stdcall H11890ReadInf(H11890_INF &Inf);
//Count Start
BOOL 			H11890API __stdcall H11890CountStart(HANDLE handle,BOOL Correction);
//
BOOL			H11890API __stdcall H11890CountStop(HANDLE handle);
//
DWORD			H11890API __stdcall H11890ReadData(HANDLE handle,DWORD *GateNum,DWORD *DataBuf,BOOL *OLD);
//
BOOL			H11890API	__stdcall H11890SetIT(HANDLE handle,DWORD IT);
//
BOOL			H11890API	__stdcall H11890ReadIT(HANDLE handle,DWORD *IT);
//
BOOL			H11890API __stdcall H11890SetRN(HANDLE handle,DWORD RN);
//
BOOL			H11890API __stdcall H11890ReadRN(HANDLE handle,DWORD *RN);
//
BOOL			H11890API __stdcall H11890SetHV(HANDLE handle,BOOL HV);
//
BOOL			H11890API __stdcall H11890ReadHV(HANDLE handle,BOOL *HV);
//
#ifdef __cplusplus
}
#endif

#endif