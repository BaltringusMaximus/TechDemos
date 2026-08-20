/*
INFO: 
total queue size INCLUDES the queue header size
when appending a packet to the queue, it checks if there is enough room in the queue by checking the total size minus the offset, the offset starts at sizeof(headerqueue)
splitBufferIntoSegments takes a big fat buffer and turns it into N queues if bQueue == 1, otherwise it'll simply turn it into N normal bufferinos

TO DO: make a mapping of queue ID - pointer
*/


#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<stdbool.h>

#define sizeBuffer 10000
#define numberOfQueue 10

typedef struct queueMapping
{
	int id;
	int queueOffset;

	unsigned char* buffer;
	
	unsigned char* queueAddress;
}queueMapping;

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
	int id;
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
void queueFromBuffer(unsigned char* buffer, unsigned char* queueAddress, int id);
void packetGenerator(int size, unsigned char** packet);
void packetAllocAndCopyToQueue(unsigned char* queue, structPacket* packet, int sizeOfPacket);
void splitBufferIntoSegments(unsigned char* buffer, int numberOfSegment, bool bQueue, unsigned char* queueMappingArray);
void printQueueMappingArray(unsigned char* queueMappingArray, int numOfQueue);
void printQueueMappingArrayReadable(unsigned char* queueMappingArray, int numOfQueue);
//void packetCopyToQueue(unsigned char* packet, unsigned char* queue);



void packetGenerator(int size, unsigned char** packet)
{
	unsigned char* tempPacket = NULL;
	printf("initial address = %p\n", *packet);
	*packet = malloc(size);

	printf("allocated address = %p\n", *packet);

	for (int i = 0; i < size; i++)
	{
		*(*packet+i)  = i;
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

void queueFromBuffer(unsigned char* buffer, unsigned char** queueAddress, int id)
{
	headerQueue headerAllocatedQueue;
	headerFreeMemory headerBuffer;
	memcpy(&headerBuffer, buffer, sizeof(headerFreeMemory));
	memset(&headerAllocatedQueue, 0, sizeof(headerQueue));
	printf("%d %d %d\n", headerBuffer.isFree, headerBuffer.offset, headerBuffer.size);
	headerAllocatedQueue.id = id;
	headerAllocatedQueue.numberOfElement = 0;
	headerAllocatedQueue.offset = sizeof(headerQueue);
	headerAllocatedQueue.totalSize = headerBuffer.size;

	memcpy(buffer, &headerAllocatedQueue, sizeof(headerQueue));
	if (queueAddress != NULL){ *queueAddress = buffer; }
	else { printf("no queueAddress pointer provided\n"); }
//	*queueAddress = buffer;
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

// must be preinitialized buffer USE BEFORE TURNING IT INTO A FUCKING QUEUE

void splitBufferIntoSegments(unsigned char* buffer, int numberOfSegment, bool bQueue, unsigned char* queueMappingArray)
{
	headerFreeMemory headerCurrentSegment;
	queueMapping* currentQueueMapping = queueMappingArray;
	printf("currentQueueMapping = %p queueMappingArray = %p\n", currentQueueMapping, queueMappingArray);
	memcpy(&headerCurrentSegment, buffer, sizeof(headerCurrentSegment));
	int totalSize = headerCurrentSegment.size;
	if (totalSize % numberOfSegment != 0) { printf("can't split da buffer into %d segments cuz the requested number of segments doesn't divide the total size of the buffer supplied\n", numberOfSegment); return; }
	for (int i = 0; i < numberOfSegment; i++)
	{
		headerCurrentSegment.isFree = 1;
		headerCurrentSegment.offset = ( i * totalSize / numberOfSegment );
		headerCurrentSegment.size = totalSize / numberOfSegment;
		printf("%d %d %d\n", headerCurrentSegment.isFree, headerCurrentSegment.offset, headerCurrentSegment.size);
		printf("%p\n", buffer + headerCurrentSegment.offset);
//		printBufferWithSize(buffer, sizeBuffer);
		memcpy((buffer + headerCurrentSegment.offset), &headerCurrentSegment, sizeof(headerFreeMemory));
		if (bQueue == 1) { queueFromBuffer(buffer + headerCurrentSegment.offset, NULL, 0x11 + i); }
		if (queueMappingArray != NULL) 
		{ 
			currentQueueMapping->id = 0x11 + i; 
			currentQueueMapping->buffer = buffer;
			currentQueueMapping->queueAddress = buffer + headerCurrentSegment.offset;
			currentQueueMapping->queueOffset = headerCurrentSegment.offset;
			currentQueueMapping = currentQueueMapping + 1; // understand "+ 1*sizeof(queueMapping)" basically, what an odd behaviour
			printf("currentQueueMapping = %p\n", currentQueueMapping); 
		}
		
		printf("exiting the split function\n");
//		printBufferWithSize(buffer, sizeBuffer);
	}
	
	return;
}

void printQueueMappingArray(unsigned char* queueMappingArray, int numOfQueue)
{
	
	for (int j = 0; j < numOfQueue; j++)
	{
		for (int i = 0; i < sizeof(queueMapping); i++)
		{
			printf("%d ", queueMappingArray[i]);
		}
		printf("\n");
		queueMappingArray += sizeof(queueMapping);
	}

	return;
}

void printQueueMappingArrayReadable(unsigned char* queueMappingArray, int numOfQueue)
{
	queueMapping* currentQueue = queueMappingArray;
	printf("list of all registered Queues\n");
	for (int j = 0; j < numOfQueue; j++)
	{
		printf("queue ID = %X\nqueue offset = %d\nqueue address = %p\nbuffer address = %p\n", currentQueue->id, currentQueue->queueOffset, currentQueue->queueAddress, currentQueue->buffer);
		currentQueue += 1;
		printf("\n");
		queueMappingArray += sizeof(queueMapping);
	}

	return;
}

int main()
{

	unsigned char* pBufferByte = NULL;
	unsigned char* pQueueByte = NULL;
	int idQueue1 = 0x11;
	int idQueue2 = 0x12;
	unsigned char* queueMappingArray = NULL;
	structPacket packet1;
	structPacket packet2;
	memset(&packet1, 0, sizeof(structPacket));

	queueMappingArray = malloc(numberOfQueue * sizeof(queueMapping));
	memset(queueMappingArray, 0, numberOfQueue * sizeof(queueMapping));
	printf("size of queuemappingarray = %d\n", numberOfQueue * sizeof(queueMapping));
	printQueueMappingArray(queueMappingArray, numberOfQueue);
	printf("Buffer byte  %p\n", pBufferByte);
	bufferInit(&pBufferByte, sizeBuffer);
	printf("Buffer byte  %p\n", pBufferByte);
	printBufferWithSize(pBufferByte, sizeBuffer);
	splitBufferIntoSegments(pBufferByte, numberOfQueue, 1, queueMappingArray);
	printf("back to main\n");
	printQueueMappingArray(queueMappingArray, numberOfQueue);
	printQueueMappingArrayReadable(queueMappingArray, numberOfQueue);
	printBufferWithSize(pBufferByte, sizeBuffer);
	printf("back to main again\n");
	//packetGenerator(11, &packet1.packetData);

	
	
	
	/*
	queueFromBuffer(pBufferByte, &pQueueByte,idQueue1);
	printf("queue address = %p\n", pQueueByte);
	printBufferWithSize(pBufferByte, sizeBuffer);
	packetAllocAndCopyToQueue(pQueueByte, &packet1, 10);
	printBufferWithSize(pBufferByte, sizeBuffer);
	packetAllocAndCopyToQueue(pQueueByte, &packet2, 943);
	printBufferWithSize(pBufferByte, sizeBuffer);
	//packetGenerator(10, &pPacket1);
	*/
	return 0;
}
