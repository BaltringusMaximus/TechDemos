#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include <stdbool.h>

#define sizeBuffer 1000

typedef struct headerFreeMemory
{
	int isFree;
	int offset;
	int size;
}headerFreeMemory;

typedef struct headerPacket
{
	int isFree;
	int offset;
	int size;
}headerPacket;

typedef struct headerQueue
{
	int totalSize;					//in bytes,
	int offset;						//where to copy da next element
	int numberOfElement;			//purely informative to make the struct 12 bytes long
}headerQueue;

typedef struct structPacket
{
	unsigned char* allocatedBufferAddress;
	unsigned char* packetData;
	int packetSize;
	bool FreeOrUsed;
}structPacket;


void bufferInit(unsigned char** buffer, int size);
void printBufferWithSize(unsigned char* buffer, int size);
void queueFromBuffer(unsigned char* buffer, unsigned char* queueAddress);
void packetGenerator(int size, unsigned char** packet);
void packetAllocAndCopyToQueue(unsigned char* queue, structPacket* packet, int sizeOfPacket);
//void packetCopyToQueue(unsigned char* packet, unsigned char* queue);



void packetGenerator(int size, unsigned char** packet)
{
	unsigned char* tempPacket = NULL;
	printf("initial address = %p\n", *packet);
	*packet = malloc(size);

	printf("allocated address = %p\n", *packet);

	for (int i = 0; i < size; i++)
	{
		*(*packet + i) = i;
		printf("%llX ", *(*packet + i));

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
//	memset(&(*buffer)[size], 0xFFFFFFFF, sizeof(int));
	memset((*buffer + size), 0xFFFFFFFF, sizeof(int));
	return;
}

void queueFromBuffer(unsigned char* buffer, unsigned char** queueAddress)
{
	headerQueue headerAllocatedQueue;
	headerFreeMemory headerBuffer;
	memcpy(&headerBuffer, buffer, sizeof(headerFreeMemory));
	memset(&headerAllocatedQueue, 0, sizeof(headerQueue));
	printf("%d %d %d\n", headerBuffer.isFree, headerBuffer.offset, headerBuffer.size);
	headerAllocatedQueue.numberOfElement = 0;
	headerAllocatedQueue.offset = sizeof(headerQueue);
	headerAllocatedQueue.totalSize = headerBuffer.size;

	memcpy(buffer, &headerAllocatedQueue, sizeof(headerQueue));
	*queueAddress = buffer;
	return;
}
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

void packetAllocAndCopyToQueue(unsigned char* queue, structPacket* packet, int sizeOfPacket)
{
	headerQueue *currentQueue = queue;
	headerPacket headerCurrentPacket;
	headerFreeMemory headerFollowingMemory;
	bool addingPadding = 0;
	if (sizeOfPacket + sizeof(headerPacket) > (currentQueue->totalSize - currentQueue->offset)) { printf("not enough room to append packet to the queue\n"); return; }
	if (sizeOfPacket + sizeof(headerPacket) + sizeof(headerFreeMemory) > (currentQueue->totalSize - currentQueue->offset)) { printf("not adding headerFreeMemory, adding padding instead\n "); addingPadding = 1; }
	printf("queue details = %d %d %d\n", currentQueue->numberOfElement, currentQueue->offset, currentQueue->totalSize);
	packet->packetSize = sizeOfPacket;
	packetGenerator(packet->packetSize, &packet->packetData);
	packet->allocatedBufferAddress = queue + currentQueue->offset;
	printf("allocated address at = %p\n", packet->allocatedBufferAddress);



	if (addingPadding == 0)
	{
		headerCurrentPacket.isFree = 0;
		headerCurrentPacket.size = sizeOfPacket;
		headerCurrentPacket.offset = currentQueue->offset;

		currentQueue->offset += (sizeOfPacket + sizeof(headerPacket));
		currentQueue->numberOfElement++;

		headerFollowingMemory.isFree = 1;
		headerFollowingMemory.size = currentQueue->totalSize - currentQueue->offset;
		headerFollowingMemory.offset = currentQueue->offset;
		memcpy(packet->allocatedBufferAddress, &headerCurrentPacket, sizeof(headerPacket));
		memcpy(packet->allocatedBufferAddress + sizeof(headerPacket), packet->packetData, packet->packetSize);
		memcpy(packet->allocatedBufferAddress + sizeof(headerPacket) + sizeOfPacket, &headerFollowingMemory, sizeof(headerFreeMemory));
	}


	else if (addingPadding == 1)
	{
		headerCurrentPacket.isFree = 0;
		headerCurrentPacket.size = currentQueue->totalSize - currentQueue->offset - sizeof(headerPacket);
		headerCurrentPacket.offset = currentQueue->offset;

		currentQueue->offset += (headerCurrentPacket.size + sizeof(headerPacket));
		currentQueue->numberOfElement++;

		memcpy(packet->allocatedBufferAddress, &headerCurrentPacket, sizeof(headerPacket));
		memcpy(packet->allocatedBufferAddress + sizeof(headerPacket), packet->packetData, packet->packetSize);
		memset(packet->allocatedBufferAddress + sizeof(headerPacket) + sizeOfPacket, (unsigned char)0xF, headerCurrentPacket.size - sizeOfPacket);
	}
	
	//if (address == NULL) { printf("alloc failed, no address found, couldn't copy the packet\n"); return; }
	packet->FreeOrUsed = 1;
	return;
}


int main()
{

	unsigned char* pBufferByte = NULL;
	unsigned char* pQueueByte = NULL;
	structPacket packet1;
	structPacket packet2;
	memset(&packet1, 0, sizeof(structPacket));


	printf("Buffer byte  %p\n", pBufferByte);
	bufferInit(&pBufferByte, sizeBuffer);
	printf("Buffer byte  %p\n", pBufferByte);
	printBufferWithSize(pBufferByte, sizeBuffer);
	queueFromBuffer(pBufferByte, &pQueueByte);
	printf("queue address = %p\n", pQueueByte);
	printBufferWithSize(pBufferByte, sizeBuffer);
	packetAllocAndCopyToQueue(pQueueByte, &packet1, 10);
	printBufferWithSize(pBufferByte, sizeBuffer);
	packetAllocAndCopyToQueue(pQueueByte, &packet2, 943);
	printBufferWithSize(pBufferByte, sizeBuffer);
	//packetGenerator(10, &pPacket1);
	return 0;
}
