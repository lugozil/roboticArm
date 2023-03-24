#include <stdio.h>
#include <windows.h>
#include <time.h>
HANDLE wHnd;

HANDLE openPort(const char * portName, unsigned int baudRate)
{
	HANDLE port;
	DCB commState;
	BOOL success; 
	COMMTIMEOUTS timeouts;

	/* Open the serial port. */
	port = CreateFileA(portName, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	if (port == INVALID_HANDLE_VALUE)
	{
		switch(GetLastError())
		{
		case ERROR_ACCESS_DENIED:	
			fprintf(stderr, "Error: Access denied.  Try closing all other programs that are using the device.\n");
			break;
		case ERROR_FILE_NOT_FOUND:
			fprintf(stderr, "Error: Serial port not found.  "
				"Make sure that \"%s\" is the right port name.  "
				"Try closing all programs using the device and unplugging the "
				"device, or try rebooting.\n", portName);
			break;
		default:
			fprintf(stderr, "Error: Unable to open serial port.  Error code 0x%lx.\n", GetLastError());
			break;
		}
		return INVALID_HANDLE_VALUE;
	}

	/* Set the timeouts. */
	success = GetCommTimeouts(port, &timeouts);
	if (!success)
	{
		fprintf(stderr, "Error: Unable to get comm timeouts.  Error code 0x%lx.\n", GetLastError());
		CloseHandle(port);
		return INVALID_HANDLE_VALUE;
	}
	timeouts.ReadIntervalTimeout = 1000;
	timeouts.ReadTotalTimeoutConstant = 1000;
	timeouts.ReadTotalTimeoutMultiplier = 0;
	timeouts.WriteTotalTimeoutConstant = 1000;
	timeouts.WriteTotalTimeoutMultiplier = 0;
	success = SetCommTimeouts(port, &timeouts);
	if (!success)
	{
		fprintf(stderr, "Error: Unable to set comm timeouts.  Error code 0x%lx.\n", GetLastError());
		CloseHandle(port);
		return INVALID_HANDLE_VALUE;
	}

	/* Set the baud rate. */
	success = GetCommState(port, &commState);
	if (!success)
	{
		fprintf(stderr, "Error: Unable to get comm state.  Error code 0x%lx.\n", GetLastError());
		CloseHandle(port);
		return INVALID_HANDLE_VALUE;
	}
	commState.BaudRate = baudRate;
	success = SetCommState(port, &commState);
	if (!success)
	{
		fprintf(stderr, "Error: Unable to set comm state.  Error code 0x%lx.\n", GetLastError());
		CloseHandle(port);
		return INVALID_HANDLE_VALUE;
	}

	/* Flush out any bytes received from the device earlier. */
	success = FlushFileBuffers(port);
	if (!success)
	{
		fprintf(stderr, "Error: Unable to flush port buffers.  Error code 0x%lx.\n", GetLastError());
		CloseHandle(port);
		return INVALID_HANDLE_VALUE;
	}

	return port;
}

BOOL SetTarget(HANDLE port, unsigned char channel, unsigned short target)
{
	unsigned char command[4];
	DWORD bytesTransferred;
	BOOL success;

	// Compose the command.
	command[0] = 0x84;
	command[1] = channel;
	command[2] = target & 0x7F;
	command[3] = (target >> 7) & 0x7F;

	// Send the command to the device.
	success = WriteFile(port, command, sizeof(command), &bytesTransferred, NULL);
	if (!success)
	{
		fprintf(stderr, "Error: Unable to write Set Target command to serial port.  Error code 0x%lx.\n", GetLastError());
		 return 0;
	}
	if (sizeof(command) != bytesTransferred)
	{
		fprintf(stderr, "Error: Expected to write %d bytes but only wrote %ld.\n", (int)sizeof(command), bytesTransferred);
		return 0;
	}

	return 1;
}

// move the robot to its starting position
int startrobot(port, a1, a2, a3, a4, a5) {

	BOOL s1, s2, s3, s4, s5, s6;
	char error = "Uno de los pulsos esta vacio";
	s2 = SetTarget(port, 2, a2);
	Sleep(1000);
	s3 = SetTarget(port, 4, a3);
	//Sleep(1000);
	s5 = SetTarget(port, 8, a5);
	//Sleep(1000); //10000 = 10 segundos 
	s4 = SetTarget(port, 6, a4);
	//Sleep(1000);
	s1 = SetTarget(port, 0, a1);
	//Sleep(1000);
	s6 = SetTarget(port, 10, 944);
	if (!s1 || !s2 || !s3 || !s4 || !s5) { return error; }

	return 1;
}

// move the robot to collect the jenga
int destination(port, a1, a2, a3, a4, a5,newq5) {

	BOOL s1, s2, s3, s4, s5, s6;
	char error = "Uno de los pulsos esta vacio";
	s1 = SetTarget(port, 0, a1 * 4);
	s5 = SetTarget(port, 8, newq5 * 4); // para poner la pinza siempre recta a la linea central.
	//Sleep(1000);
	s5 = SetTarget(port, 8, a5 * 4); // se mueve los grados que debe. 
	//Sleep(1000);
	s4 = SetTarget(port, 6, a4 * 4);
	//Sleep(1000);
	s3 = SetTarget(port, 4, a3 * 4);
	//Sleep(1000);
	Sleep(2300);
	s2 = SetTarget(port, 2, a2 * 4);
	Sleep(1500);
	s6 = SetTarget(port, 10, 1680 * 4); //1450
	Sleep(1000);
	if (!s1 || !s2 || !s3 || !s4 || !s5) { return error; }

	return 1;
}

// move the robot to unloading the jenga
int unloading(port, lugar,a1) {
	BOOL s1, s2, s6, s3,s4, s5;
	int tiempo = 0; 
	char error = "Uno de los pulsos esta vacio";
	// movimiento de s2 para arriba 
	s2 = SetTarget(port, 2, 1408 * 4);
	Sleep(1200);
	// left = 1 y right = 2 
	// left == 2496 y right = 496 

	// izq con descarga en derecha 
	if(a1<1296 && lugar == 1){
		tiempo = 2800;
	}
	// izq con descarga en izq 
	if(a1<1296 && lugar == 2){
		tiempo = 1000;
	}

	// derecha con descarga en derecha
	if(a1>1696 && lugar == 1){
		tiempo = 1000;
	}
	// derecha con descarga en izq
	if(a1>1696 && lugar == 2){
		tiempo = 2800;
	}

	if(a1>1296 && a1<1696){
		tiempo = 1800;
	}

	if (lugar ==1) {
		// s1 para derecha  
		s3 = SetTarget(port, 4, 1480 * 4);
		s1 = SetTarget(port, 0, 2496 * 4);
		s4 = SetTarget(port, 6, 2427 * 4);
		//Sleep(1000);
		s5 = SetTarget(port, 8, 920 * 4);
		Sleep(tiempo);
		s6 = SetTarget(port, 10, 944);

		return 1;
	}
	else {
		// s2 para izquierda
		s3 = SetTarget(port, 4, 1507 * 4);
		s1 = SetTarget(port, 0, 496 * 4);
		s4 = SetTarget(port, 6, 2427 * 4);
		s5 = SetTarget(port, 8, 920 * 4);
		Sleep(tiempo);
		s6 = SetTarget(port, 10, 944);

	 	return 1;
	}

	printf("Error en el parametro de lugar");
}

int main(int argc, char * argv[])
{
	//define size window
	wHnd = GetStdHandle(STD_OUTPUT_HANDLE);
	SMALL_RECT windowSize = {0, 0, 30, 15};
    SetConsoleWindowInfo(wHnd, 1, &windowSize); 

	HANDLE port;
	char * portName;
	int baudRate;
	BOOL success;
	unsigned short target, position;
	int a1, a2, a3, a4, a5, newQ5, descarga = 0; // se elimina luego de modificar main a tipo funcion 
	unsigned short inia1, inia2, inia3, inia4, inia5, inia6 = 0;

	// initial position of the robot
	inia1 = 1496 * 4; 
	inia2 = 1408 * 4; 
	inia3 = 1507 * 4; 
	inia4 = 2464 * 4; 
	inia5 = 920 * 4; // 973
	inia6 = 900 * 4; 

	a1= (int) strtol(argv[1], NULL, 10); // pulso1
	a2= (int) strtol(argv[2], NULL, 10); // pulso2 
	a3= (int) strtol(argv[3], NULL, 10); // pulso3 
	a4= (int) strtol(argv[4], NULL, 10); // pulso4
	a5= (int) strtol(argv[5], NULL, 10); // pulso5
	descarga= (int) strtol(argv[6], NULL, 10); // destino
	newQ5= (int) strtol(argv[7], NULL, 10); // newq5 

	portName = "\\\\.\\COM7"; 
	baudRate = 9600;

	/* Open the Maestro's serial port. */
	port = openPort(portName, baudRate);
	if (port == INVALID_HANDLE_VALUE){ return 0; }

	startrobot(port,inia1,inia2,inia3,inia4,inia5);

	success = 0; 

	destination(port, a1, a2, a3, a4, a5, newQ5); // para jenga  newq5 = 1868
	unloading(port, descarga,a1); //para descargar 2 izquierda y 1 derecha. 
	startrobot(port,inia1,inia2,inia3,inia4,inia5); 

	CloseHandle(port);

	return 0;
}




