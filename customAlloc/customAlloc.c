#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include <stdbool.h>
int sizeBuffer = 1000;

typedef struct headerPacket
{
	int isFree;
	int offset;
	int size;
}headerPacket;
typedef struct headerFreeMemory
{
	int isFree;
	int offset;
	int size;
}headerFreeMemory;
typedef struct structPacket
{
	unsigned char* allocatedBufferAddress;
	unsigned char* packetData;
	int packetSize;
	bool FreeOrUsed;
}structPacket;
//typedef struct structPacket structPacket;

// int is 4 bytes so it can hold 255+255*256+255*256²+255*256^3 values

void customAlloc(int size, unsigned char* buffer, long long* address, unsigned char* value);
void customFree(unsigned char* startAddress);
void customCopy(unsigned char* customPacket, unsigned char* buffer, unsigned char* startAddress, int size);
void packetGenerator(int size, unsigned char** packet);
void bufferInit(unsigned char* buffer, int size);
void printBufferWithSize(unsigned char* buffer, int size);
void packetAllocAndCopy(unsigned char* buffer, structPacket* packet, int sizeOfPacket);
void packetFree(structPacket* packet);


void customAlloc(int size, unsigned char* buffer, long long* address, unsigned char* value)
{
	int sumsize = 0;
	int sizeCurrentSegment = 0;
	int offset = 0;
	unsigned char* position = buffer;
	unsigned char* currentPosition = buffer;
	headerFreeMemory headerFreeAllocMemoryInfo;
	bool isLastSegment = 0;
	memset(&headerFreeAllocMemoryInfo, 0, sizeof(headerFreeMemory));
	printf("position value = %X\n", *position);
	size = size + 12;
	*address = NULL;
	printf("hello inside custom alloc buffer = %p,address = %p\n", buffer, address);
	while (*address == NULL && ((int*)currentPosition)[0] != 0xFFFFFFFF)
	{
		position = currentPosition;
//		offset = position[4] + 256 * position[5] + 256 * 256 * position[6] + 256 * 256 * 256 * position[7];
		offset = position[4] + 256 * position[5] + 256 * 256 * position[6] + 256 * 256 * 256 * position[7];
		printf("Current offset = %d\n", offset);

		printf("current position = %d\n", *currentPosition);
		sumsize = 0;
		sizeCurrentSegment = 0;
		printf("current position before checking = %p | %d\n", currentPosition, *currentPosition);
		while (*currentPosition == 1)
		{
			sizeCurrentSegment = currentPosition[8] + 256 * currentPosition[9] + (256 ^ 2) * currentPosition[10] + (256 ^ 3) * currentPosition[11];		
			sumsize = sumsize + sizeCurrentSegment;
			printf("segment size = %d, total freesize = %d\n", sizeCurrentSegment, sumsize);
			currentPosition = &currentPosition[sizeCurrentSegment];
		}
		/*
		for (int i = 0; i < sizeBuffer-sumsize; i++)
		{
			printf("%llX ", ((int*)currentPosition)[i]);
		}
		printf("\n");

		*/
		printf("\n current position value integer %llX\n ", ((int*)currentPosition)[0]);
		printf("current position after first checking = %p | %X\n", currentPosition, *currentPosition);
		if (sumsize >= size)
		{
			printf("found address\n");
			*address = &position[0];
			*value = position[0];
			headerFreeAllocMemoryInfo.isFree = 1;
			headerFreeAllocMemoryInfo.offset = offset;
			headerFreeAllocMemoryInfo.size = sumsize;
			memcpy(position, &headerFreeAllocMemoryInfo, sizeof(headerFreeMemory));
			printf("address = %p\n", *address);
			printf("value = %X at %p\n", *value, &*value);
			printf("buffer address %p\n", &buffer[0]);
			printf("buffer = \n");
			printBufferWithSize(buffer, sizeBuffer);
			break;
		}
		else if (sumsize < size)
		{
			printf("not enough room in this segment\n");
		}
		while (*currentPosition == 0)
		{
			offset = currentPosition[4] + 256 * currentPosition[5] + 256 * 256 * currentPosition[6] + 256 * 256 * 256 * currentPosition[7];
			printf("position not free at offset %d\n",offset);
			sizeCurrentSegment = currentPosition[8] + 256 * currentPosition[9] + (256 ^ 2) * currentPosition[10] + (256 ^ 3) * currentPosition[11];
			printf("current position = %p\n", currentPosition);
			currentPosition = &currentPosition[12 + sizeCurrentSegment];
			printf("current position = %p\n", currentPosition);
		}
		printf("current position after second checking = %p | %d\n", currentPosition,*currentPosition);
		/*
		if (*currentPosition == 1)
		{
			sumsize = sumsize + sizeCurrentSegment;
			if (sumsize >= size)
			{
				printf("found address\n");
				*address = &position[0];
				*value = position[0];
				printf("address = %p\n", *address);
				printf("value = %X at %p\n", *value, &*value);
				printf("buffer address %p\n", &buffer[0]);
			}
			else if (sumsize < size)
			{
				printf("1 current position[8] value = %X,%X,%X,%X\n", currentPosition[8], currentPosition[9], currentPosition[10], currentPosition[11]);
				
				currentPosition = &currentPosition[sizeCurrentSegment];
				printf("1 new position[8] value = %X,%X,%X,%X \n", currentPosition[8], currentPosition[9], currentPosition[10], currentPosition[11]);
				printf("not enough room! new position value = %X \n", *currentPosition);
			}
		}
		else
		{
			printf("0 current position[8] value = %X,%X,%X,%X \n", position[8], position[9], position[10], position[11]);
			position = &currentPosition[12 + sizeCurrentSegment];
			currentPosition = position;
			sumsize = 0;
			printf("sumsize = %llX\n", sizeCurrentSegment);
			printf("0 new position[8] value = %X,%X,%X,%X \n", position[8], position[9], position[10], position[11]);
			printf("memory busy... new position value = %X \n", *position);
		}
		*/
	}
	printf("I'm out\n");
	return;
}

//zeroes out memory
void customFree(unsigned char* startAddress)
{
	int sizeToRemove = 0;
	int isFreeMemory = 1;
	struct headerFreeMemory headerFreed;
	headerFreed.isFree = 1;
	headerFreed.offset = startAddress[4];
	unsigned char* packetFollowingMemoryAddress = &startAddress[sizeof(headerFreed) + startAddress[8] + startAddress[9] * 256 + startAddress[10] * 256 * 256 + startAddress[11] * 256 * 256];
	printf("packetFollowingMemoryAddress %llX,%llX,%llX\n", packetFollowingMemoryAddress[0],packetFollowingMemoryAddress[4],packetFollowingMemoryAddress[8]);
	unsigned char* currentAddress = startAddress;
	printf("hello from the freeing routine\n");
	printf("intial status, offset, size = %llX,%llX,%llX\n", startAddress[0],startAddress[4],startAddress[8]);
	/*
	while (isFreeMemory == 1)
	{
		if (currentAddress[0] == 1)
		{
			sizeToRemove += (currentAddress[8] + currentAddress[9] * 256 + currentAddress[10] * 256 * 256 + currentAddress[11] * 256 * 256 * 256);
		}
		else if (currentAddress[0] == 0)
		{
			sizeToRemove += (currentAddress[8] + currentAddress[9] * 256 + currentAddress[10] * 256 * 256 + currentAddress[11] * 256 * 256 * 256) + 12;
		}
		currentAddress = &currentAddress[12 + currentAddress[8]];
		isFreeMemory = currentAddress[0];
		printf("is free? = %d, sizeToRemove so far = %d\n", isFreeMemory,sizeToRemove);

	}
	*/
	sizeToRemove += (currentAddress[8] + currentAddress[9] * 256 + currentAddress[10] * 256 * 256 + currentAddress[11] * 256 * 256 * 256) + 12;
	headerFreed.size = sizeToRemove;
	memcpy(startAddress, &headerFreed, sizeof(headerFreed));
	printf("following status, offset, size = %llX,%llX,%llX\n", startAddress[0 + startAddress[8] + 12], startAddress[4 + startAddress[8] + 12], startAddress[8 + startAddress[8] + 12]);
	
	return;
}
void customCopy(unsigned char* customPacket,unsigned char* buffer, unsigned char* startAddress, int size)
{
	struct headerPacket headerCustomPacket;
	struct headerFreeMemory headerFollowingMemory;
	long long sizeFreeMemory = startAddress[8] + startAddress[9]*256 + startAddress[10]*256*256 + startAddress[11]*256*256;

	printf("size of free memory = %d", sizeFreeMemory);
	printf("offset = %p - %p\n", startAddress, buffer);
	long long offsetCopy = (long long)startAddress - (long long)buffer;
	printf("testOffset = %llX\n", offsetCopy);
	if (sizeFreeMemory < size + 2*sizeof(headerFreeMemory))
	{
		printf("not enough freememory to add headerFreeMemory, adding padding instead\n");
		headerCustomPacket.isFree = 0;
		headerCustomPacket.offset = offsetCopy;
		headerCustomPacket.size = sizeFreeMemory - 12;
		printf("size of custom packet = %llX\n", headerCustomPacket.size);
		memcpy(&startAddress[0], &headerCustomPacket, sizeof(headerCustomPacket));
		memcpy(&startAddress[sizeof(headerCustomPacket)], customPacket, size);
		memset(&startAddress[sizeof(headerCustomPacket) + size], (unsigned char)0xF, sizeFreeMemory - (size+12));
	}
	else
	{ 
		printf("enough memory to add headerFreeMemory\n");
		headerCustomPacket.isFree = 0;
		headerCustomPacket.offset = offsetCopy;
		headerCustomPacket.size = size;
		printf("size of custom packet = %llX\n", headerCustomPacket.size);
		headerFollowingMemory.isFree = 1;
		headerFollowingMemory.offset = offsetCopy + sizeof(headerCustomPacket) + size;
		headerFollowingMemory.size = sizeFreeMemory - (sizeof(headerCustomPacket) + size);
		printf("size of remaining memory after packet = %llX\n", headerFollowingMemory.size);
		memcpy(&startAddress[0], &headerCustomPacket, sizeof(headerCustomPacket));
		memcpy(&startAddress[sizeof(headerCustomPacket)], customPacket, size);
		memcpy(&startAddress[sizeof(headerCustomPacket) + size], &headerFollowingMemory, sizeof(headerFollowingMemory));
	}	
	return;
}
void packetGenerator(int size, unsigned char** packet)
{
	unsigned char * tempPacket = NULL;
	printf("initial address = %p\n", *packet);
	*packet = malloc(size);

	printf("allocated address = %p\n", *packet);
	
	for (int i = 0; i < size; i++)
	{
		*(* packet + i) = i;
		printf("%llX ", *(*packet+i));

	}

	return;
}
void bufferInit(unsigned char** buffer, int size)
{

	*buffer = malloc(sizeBuffer * sizeof(unsigned char) + sizeof(int));
	
	struct headerFreeMemory headerInit;
	headerInit.isFree = 1;
	headerInit.offset = 0;
	headerInit.size = size;
	memset(*buffer, 0, size);
	memcpy(*buffer, &headerInit, sizeof(struct headerFreeMemory));
	memset(&(*buffer)[size], 0xFFFFFFFF, sizeof(int));
	/*
	for (int i = 0; i < size + sizeof(int); i++)
	{
		printf("%d ", (*buffer)[i]);
		//or you coud just:
		//printf("%d ", *(*buffer + i));
	}
	printf("\n");
	*/
	return;
}

// print full buffer and stop int
void printBufferWithSize(unsigned char* buffer, int size)
{
	printf("\n");
	for (int i = 0; i < size + sizeof(int); i++)
	{
		printf("%d ", buffer[i]);
	}
	printf("\n");
	return;
}
void packetAllocAndCopy(unsigned char* buffer,  structPacket * packet, int sizeOfPacket)
{
	long long* address = NULL;
	unsigned char value = 0;
	packet->packetSize = sizeOfPacket;
	packetGenerator(packet->packetSize, &packet->packetData);
	customAlloc(packet->packetSize, buffer, &address, &value);
	packet->allocatedBufferAddress = (unsigned char*)address;
	if (address == NULL) { printf("alloc failed, no address found, couldn't copy the packet\n"); return; }
	customCopy(packet->packetData, buffer, packet->allocatedBufferAddress, packet->packetSize);
	packet->FreeOrUsed = 1;
	return;
}
void packetFree(structPacket* packet)
{
	customFree(packet->allocatedBufferAddress);
	packet->FreeOrUsed = 0;
	return;
}
int main()
{
	int intCopyFreeExit = 1;
	int intPacketName = 0;
	unsigned char * pBufferByte = NULL;
	struct headerFreeMemory header0;
	unsigned char value = NULL;
	long long* address = NULL;

	unsigned char* charAddress = (unsigned char*)address;
	
	int chosenPacketSize = 0;

	structPacket packet1;
	structPacket packet2;
	structPacket packet3;
	structPacket packet4;
	structPacket packet5;
	structPacket packet6;
	structPacket packet7;
	structPacket packet8;
	structPacket packet9;
	structPacket packet10;
	memset(&packet1, 0, sizeof(structPacket));
	memset(&packet2, 0, sizeof(structPacket));
	memset(&packet3, 0, sizeof(structPacket));
	memset(&packet4, 0, sizeof(structPacket));
	memset(&packet5, 0, sizeof(structPacket));
	memset(&packet6, 0, sizeof(structPacket));
	memset(&packet7, 0, sizeof(structPacket));
	memset(&packet8, 0, sizeof(structPacket));
	memset(&packet9, 0, sizeof(structPacket));
	memset(&packet10, 0, sizeof(structPacket));
	printf("\n");
//	pBufferByte = malloc(sizeBuffer *sizeof(unsigned char));
//	printf("%d\n", sizeof(pBufferByte));
	printf("Buffer byte  %p\n", &pBufferByte);
	bufferInit(&pBufferByte, sizeBuffer);
	printf("Buffer byte  %p\n", pBufferByte);
	printBufferWithSize(pBufferByte, sizeBuffer);


	packetAllocAndCopy(pBufferByte, &packet1, 10);
	printBufferWithSize(pBufferByte, sizeBuffer);

	packetFree(&packet1);

	printBufferWithSize(pBufferByte, sizeBuffer);
	while (intCopyFreeExit != 0)
	{
		
		printf("input intCopyFreeExit\n");
		scanf_s("%d", &intCopyFreeExit);

		printf("input packet name\n");
		scanf_s("%d", &intPacketName);
		switch (intPacketName)
		{
//packet 1
		case 1:
		{
			switch (intCopyFreeExit)
			{
			case 0:
			{
				printf("exit\n");
				break;
			}
			case 1:
			{
				printf("copy routine\n");
				if (packet1.FreeOrUsed == 1)
				{
					printf("packet 1 not free\n");
				}
				else if (packet1.FreeOrUsed == 0)
				{
					printf("input packet size\n");
					scanf_s("%d", &chosenPacketSize);
					packetAllocAndCopy(pBufferByte, &packet1, chosenPacketSize);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				break;
			}
			case 2:
			{
				printf("freeing routine\n");
				if (packet1.FreeOrUsed == 1)
				{
					printf("freeing packet 1\n");
					packetFree(&packet1);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				else if (packet1.FreeOrUsed == 0)
				{
					printf("Packet 1 already Free\n");
				}
				break;
			}
			default:
			{
				printf("unknown command entered, try again retard\n");
				break;
			}
			}
			break;
		}
// packet 2
		case 2:
		{
			switch (intCopyFreeExit)
			{
			case 0:
			{
				printf("exit\n");
				break;
			}
			case 1:
			{
				printf("copy routine\n");
				if (packet2.FreeOrUsed == 1)
				{
					printf("packet 2 not free\n");
				}
				else if (packet2.FreeOrUsed == 0)
				{
					printf("input packet size\n");
					scanf_s("%d", &chosenPacketSize);
					packetAllocAndCopy(pBufferByte, &packet2, chosenPacketSize);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				break;
			}
			case 2:
			{
				printf("freeing routine\n");
				if (packet2.FreeOrUsed == 1)
				{
					printf("freeing packet 2\n");
					packetFree(&packet2);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				else if (packet2.FreeOrUsed == 0)
				{
					printf("Packet 2 already Free\n");
				}
				break;
			}
			default:
			{
				printf("unknown command entered, try again retard\n");
				break;
			}
			}
			break;
		}
//packet 3
		case 3:
		{
			switch (intCopyFreeExit)
			{
			case 0:
			{
				printf("exit\n");
				break;
			}
			case 1:
			{
				printf("copy routine\n");
				if (packet3.FreeOrUsed == 1)
				{
					printf("packet 3 not free\n");
				}
				else if (packet3.FreeOrUsed == 0)
				{
					printf("input packet size\n");
					scanf_s("%d", &chosenPacketSize);
					packetAllocAndCopy(pBufferByte, &packet3, chosenPacketSize);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				break;
			}
			case 2:
			{
				printf("freeing routine\n");
				if (packet3.FreeOrUsed == 1)
				{
					printf("freeing packet 3\n");
					packetFree(&packet3);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				else if (packet3.FreeOrUsed == 0)
				{
					printf("Packet 3 already Free\n");
				}
				break;
			}
			default:
			{
				printf("unknown command entered, try again retard\n");
				break;
			}
			}
			break;
		}
//packet 4
		case 4:
		{
			switch (intCopyFreeExit)
			{
			case 0:
			{
				printf("exit\n");
				break;
			}
			case 1:
			{
				printf("copy routine\n");
				if (packet4.FreeOrUsed == 1)
				{
					printf("packet 4 not free\n");
				}
				else if (packet4.FreeOrUsed == 0)
				{
					printf("input packet size\n");
					scanf_s("%d", &chosenPacketSize);
					packetAllocAndCopy(pBufferByte, &packet4, chosenPacketSize);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				break;
			}
			case 2:
			{
				printf("freeing routine\n");
				if (packet4.FreeOrUsed == 1)
				{
					printf("freeing packet 4\n");
					packetFree(&packet4);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				else if (packet4.FreeOrUsed == 0)
				{
					printf("Packet 4 already Free\n");
				}
				break;
			}
			default:
			{
				printf("unknown command entered, try again retard\n");
				break;
			}
			}
			break;
		}
// packet 5
		case 5:
		{
			switch (intCopyFreeExit)
			{
			case 0:
			{
				printf("exit\n");
				break;
			}
			case 1:
			{
				printf("copy routine\n");
				if (packet5.FreeOrUsed == 1)
				{
					printf("packet 5 not free\n");
				}
				else if (packet5.FreeOrUsed == 0)
				{
					printf("input packet size\n");
					scanf_s("%d", &chosenPacketSize);
					packetAllocAndCopy(pBufferByte, &packet5, chosenPacketSize);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				break;
			}
			case 2:
			{
				printf("freeing routine\n");
				if (packet5.FreeOrUsed == 1)
				{
					printf("freeing packet 5\n");
					packetFree(&packet5);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				else if (packet5.FreeOrUsed == 0)
				{
					printf("Packet 5 already Free\n");
				}
				break;
			}
			default:
			{
				printf("unknown command entered, try again retard\n");
				break;
			}
			}
			break;
		}
//packet 6
		case 6:
		{
			switch (intCopyFreeExit)
			{
			case 0:
			{
				printf("exit\n");
				break;
			}
			case 1:
			{
				printf("copy routine\n");
				if (packet6.FreeOrUsed == 1)
				{
					printf("packet 6 not free\n");
				}
				else if (packet6.FreeOrUsed == 0)
				{
					printf("input packet size\n");
					scanf_s("%d", &chosenPacketSize);
					packetAllocAndCopy(pBufferByte, &packet6, chosenPacketSize);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				break;
			}
			case 2:
			{
				printf("freeing routine\n");
				if (packet6.FreeOrUsed == 1)
				{
					printf("freeing packet 6\n");
					packetFree(&packet6);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				else if (packet6.FreeOrUsed == 0)
				{
					printf("Packet 6 already Free\n");
				}
				break;
			}
			default:
			{
				printf("unknown command entered, try again retard\n");
				break;
			}
			}
			break;
		}
// packet 7
		case 7:
		{
			switch (intCopyFreeExit)
			{
			case 0:
			{
				printf("exit\n");
				break;
			}
			case 1:
			{
				printf("copy routine\n");
				if (packet7.FreeOrUsed == 1)
				{
					printf("packet 7 not free\n");
				}
				else if (packet7.FreeOrUsed == 0)
				{
					printf("input packet size\n");
					scanf_s("%d", &chosenPacketSize);
					packetAllocAndCopy(pBufferByte, &packet7, chosenPacketSize);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				break;
			}
			case 2:
			{
				printf("freeing routine\n");
				if (packet7.FreeOrUsed == 1)
				{
					printf("freeing packet 7\n");
					packetFree(&packet7);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				else if (packet7.FreeOrUsed == 0)
				{
					printf("Packet 7 already Free\n");
				}
				break;
			}
			default:
			{
				printf("unknown command entered, try again retard\n");
				break;
			}
			}
			break;
		}
//packet 8
		case 8:
		{
			switch (intCopyFreeExit)
			{
			case 0:
			{
				printf("exit\n");
				break;
			}
			case 1:
			{
				printf("copy routine\n");
				if (packet8.FreeOrUsed == 1)
				{
					printf("packet 8 not free\n");
				}
				else if (packet8.FreeOrUsed == 0)
				{
					printf("input packet size\n");
					scanf_s("%d", &chosenPacketSize);
					packetAllocAndCopy(pBufferByte, &packet8, chosenPacketSize);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				break;
			}
			case 2:
			{
				printf("freeing routine\n");
				if (packet8.FreeOrUsed == 1)
				{
					printf("freeing packet 8\n");
					packetFree(&packet8);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				else if (packet8.FreeOrUsed == 0)
				{
					printf("Packet 8 already Free\n");
				}
				break;
			}
			default:
			{
				printf("unknown command entered, try again retard\n");
				break;
			}
			}
			break;
		}
//packet 9
		case 9:
		{
			switch (intCopyFreeExit)
			{
			case 0:
			{
				printf("exit\n");
				break;
			}
			case 1:
			{
				printf("copy routine\n");
				if (packet9.FreeOrUsed == 1)
				{
					printf("packet 9 not free\n");
				}
				else if (packet9.FreeOrUsed == 0)
				{
					printf("input packet size\n");
					scanf_s("%d", &chosenPacketSize);
					packetAllocAndCopy(pBufferByte, &packet9, chosenPacketSize);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				break;
			}
			case 2:
			{
				printf("freeing routine\n");
				if (packet9.FreeOrUsed == 1)
				{
					printf("freeing packet 9\n");
					packetFree(&packet9);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				else if (packet9.FreeOrUsed == 0)
				{
					printf("Packet 9 already Free\n");
				}
				break;
			}
			default:
			{
				printf("unknown command entered, try again retard\n");
				break;
			}
			}
			break;
		}
		case 10:
		{
			switch (intCopyFreeExit)
			{
			case 0:
			{
				printf("exit\n");
				break;
			}
			case 1:
			{
				printf("copy routine\n");
				if (packet10.FreeOrUsed == 1)
				{
					printf("packet 10 not free\n");
				}
				else if (packet10.FreeOrUsed == 0)
				{
					printf("input packet size\n");
					scanf_s("%d", &chosenPacketSize);
					packetAllocAndCopy(pBufferByte, &packet10, chosenPacketSize);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				break;
			}
			case 2:
			{
				printf("freeing routine\n");
				if (packet10.FreeOrUsed == 1)
				{
					printf("freeing packet 10\n");
					packetFree(&packet10);
					printBufferWithSize(pBufferByte, sizeBuffer);
				}
				else if (packet10.FreeOrUsed == 0)
				{
					printf("Packet 10 already Free\n");
				}
				break;
			}
			default:
			{
				printf("unknown command entered, try again retard\n");
				break;
			}
			}
			break;
		}
		default:
		{
			printf("packet doesn't exist\n");
			break;
		}
		}
	}

	/*
	packet1.packetSize = 10;
	packetGenerator(packet1.packetSize, &packet1.packetData);
	customAlloc(packet1.packetSize, pBufferByte, &address, &value);
	packet1.allocatedBufferAddress = (unsigned char*)address;
	customCopy(packet1.packetData, pBufferByte, packet1.allocatedBufferAddress, packet1.packetSize);
	*/


	free(pBufferByte);
	printf("\n");
	return 0;
}