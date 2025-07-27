// ConsoleTest.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#if defined(_MSC_VER)
	//  Microsoft
#include "pch.h"
#include <windows.h>
#include <conio.h>
#elif defined(__GNUC__)
	//  GCC
#endif
#include <iostream>
#include "H11890api.h"


#if defined(_MSC_VER)
	//  Microsoft
#elif defined(__GNUC__)
	//  GCC
#ifndef _KBHIT_H_
#define _KBHIT_H_

#include <stdbool.h>
#include <termios.h>
#include <unistd.h>

void KB_open(void);
void KB_close(void);
bool _kbhit(void);
char _getch(void);
#endif /* _KBHIT_H_ */

static struct termios Old_set;
static struct termios New_set;
static int ReadChar = -1;

void KB_open()
{
    tcgetattr(0,&Old_set);
    New_set = Old_set;
    New_set.c_lflag &= ~ICANON;
    New_set.c_lflag &= ~ECHO;
    New_set.c_lflag &= ~ISIG;
    New_set.c_cc[VMIN] = 0;
    New_set.c_cc[VTIME] = 0;
    tcsetattr(0,TCSANOW,&Old_set);
}

void KB_close()
{
    tcsetattr(0,TCSANOW, &Old_set);
}

bool _kbhit()
{
    char ch;
    int nread;

    if(ReadChar !=-1) {
        return true;
    }

    New_set.c_cc[VMIN]=0;
    tcsetattr(0,TCSANOW,&New_set);
    nread=read(0,&ch,1);
    New_set.c_cc[VMIN]=1;
    tcsetattr(0,TCSANOW,&New_set);

    if(nread == 1) {
        ReadChar = ch;
        return true;
    }

    return false;
}

char _getch()
{
    char ch;

    if(ReadChar != -1) {
       ch = ReadChar;
       ReadChar = -1;
       return (ch);
    }

    read(0,&ch,1);
    return(ch);
}

#endif



H11890_INF	INF[16];

int main()
{
	DWORD dwRtn;
	BOOL	bRtn;

	for (int i = 0; i < 1; i++) {

	dwRtn = H11890OpenDevices(INF);
	if (dwRtn <= 0) {
		printf("Can't open the device\n");
		//return 0;
	}
	printf("Open %d Device\n", dwRtn);

	for (int j = 0; j < 1; j++) {
	printf("Device %d\n", j);
	printf("S/N:");
	printf(INF[j].cSerialNumber);
	printf("\n");

	printf("Gate Time:");
	printf("%d", INF[j].IT);
	printf("\n");

	printf("Gate Number:");
	printf("%d", INF[j].RN);
	printf("\n");

	printf("High Voltage:");
	if (INF[j].HVON == TRUE)printf("ON");
	else printf("OFF");
	printf("\n");

	INF[j].IT = 10;		//Gate Time 100 ms
	INF[j].RN = 10;		//Number of Gate 1000 times
	INF[j].HVON = TRUE;	//HV ON

	printf("\n");
	printf("Set Infomation\n");
	printf("\n");

	//bRtn = H11890SetInf(INF[j]);
	bRtn = H11890SetInfEx(&INF[j]);
	if (!bRtn) {
		printf("Can't set the information.\n");
		//return 0;
	}

	INF[j].IT = 0;
	INF[j].RN = 0;
	INF[j].HVON = FALSE;

	//bRtn = H11890ReadInf(INF[j]);
	bRtn = H11890ReadInfEx(&INF[j]);
	if (!bRtn) {
		printf("Can't read the information.%d\n", bRtn);
		//return 0;
	}

	printf("Gate Time:");
	printf("%d", INF[j].IT);
	printf("\n");

	printf("Gate Number:");
	printf("%d", INF[j].RN);
	printf("\n");

	printf("High Voltage:");
	if (INF[j].HVON == TRUE)printf("ON");
	else printf("OFF");
	printf("\n");

CountStart:

	bRtn = H11890CountStart(INF[j].hDeviceHandle, FALSE);
	if (!bRtn) {
		printf("Can't start measurement.\n");
		//return 0;
	}

	DWORD	GateNum, DataNum;
	DWORD DataBuf[16];
	CHAR	KeyInput;
	BOOL	OLD;

#if defined(__GNUC__)
	//  GCC
KB_open();
#endif

	while (1) {
		dwRtn = H11890ReadData(INF[j].hDeviceHandle, &GateNum, DataBuf, &OLD);
		if (dwRtn < 0) {
			printf("Can't read data.\n");
			//return 0;
		}
		else if (dwRtn == 1) {
			if (GateNum < INF[j].RN) {
				printf("  Gate Number : %d", GateNum);
				printf("  Count Data : %d", DataBuf[0]);
				if (OLD == TRUE) {
					printf("  OVER LIGHT DETECT");
				}
				printf("\n");
				GateNum++;
			}
		}
		else if (dwRtn == 15) {
			for (DataNum = 0; DataNum < 15; DataNum++) {
				if (GateNum < INF[j].RN) {
					printf("  Gate Number : %d", GateNum);
					printf("  Count Data : %d", DataBuf[DataNum]);
					if (OLD == TRUE) {
						printf("  OVER LIGHT DETECT");
					}
					printf("\n");
					GateNum++;
				}
			}
		}

		if (_kbhit()) {
			H11890CountStop(INF[j].hDeviceHandle);
			printf("Stop measurement.\n");
			KeyInput = _getch();
			break;
		}
		if (GateNum >= INF[j].RN && INF[j].RN != 0)break;
	}

	printf("Press 'Y' Key : Retry  \nPress other Key : End\n");

	KeyInput = _getch();

#if defined(__GNUC__)
	//  GCC
KB_close();
#endif

	if (KeyInput == 'y' || KeyInput == 'Y')goto CountStart;
	}

	H11890CloseDevices(INF);

	}

	printf("End\n");
	return 0;
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
