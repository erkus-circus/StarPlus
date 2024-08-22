#ifndef CONSTANTS_C
#define CONSTANTS_C

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "constants.h"
#include "data.h"
#include "binKeys.h"

// for transforming a short into an int
int shortToInt(unsigned char byte1, unsigned char byte2)
{
    // no idea if this works copilot gave it to me
    return (int)byte1 << 8 | byte2;
}


int fourBytesToInt(unsigned char *buf)
{
    return (buf[0] << 24) | (buf[1] << 16) | (buf[2] << 8) | buf[3];
}

float fourBytesToFloat(unsigned char *buf)
{
    int intVal = fourBytesToInt(buf);
    float retVal = 0;
    memcpy(&retVal, &intVal, sizeof(float));
    return retVal;
}

// for getting a constant from the array (this copies the data using d_copy)
struct Data getConstant(int index, struct Data* constants)
{
    // get the constant
    struct Data constant = constants[index];
    // copy the constant
    struct Data copy = *d_copy(&constant);
    // return the copy
    return copy;
}

// for loading the constants from the file
// sets the constants array and returns the index in the file at the first FUN_HEAD
struct Data* loadConstants(unsigned char *fileArray, int* indexGlobal)
{

    // the index of where in the fileArray the constants are
    int index = 0;

    // first get the number of constants from the first 4 bytes in the file
    int numConstants = fourBytesToInt(&fileArray[0]);

    // allocate the constants array
    struct Data* constants = (struct Data*) malloc(sizeof(struct Data) * numConstants);

    // how many contants have been parsed
    int constantsRecieved = 0;

    index += 4; // now the index before the first constant, so loop ++index to get chunks per byte
    // loop until a FUN_HEAD is reached

    for (int constantsRecieved = 0; constantsRecieved < numConstants; constantsRecieved++)
    {
        // first get the type of the data (1 is string, 2 is int and 3 is float)
        int dataType = (int)fileArray[index];
        index += 1;

        // get the number of chunks in this constant
        int numChunks = fourBytesToInt(&fileArray[index]);
        // now increment by 4 for the passed bytes
        index += 4;

        // create a data struct for the constant
        struct Data *data = createData(numChunks);

        // for loop adding bytes to the array until number of chunks is reached
        for (int i = 0; i < numChunks; i++)
        {
            if (dataType == 1)
            {
                data->values[i] = (int)fileArray[index];
                index += 1;
            }
            else if (dataType == 2)
            {
                // assume bytesPerChunk is 4
                data->values[i] = fourBytesToInt(&fileArray[index]);
                index += 4;
            }
            else if (dataType == 3)
            {
                float f = fourBytesToFloat(&fileArray[index]);
                // assume float is as wide as an array (32 bits). Pray it is mostly everywhere because otherwise this won't work. 
                memcpy(&data->values[i], &f, sizeof(float));

                index += 4;
            }
        }

        constants[constantsRecieved] = *data;
    }

    // see if this works:
    *indexGlobal = index;



    // the first 4 bytes are the number of constants there are in the program
    return constants;
}

#endif // CONSTANTS_C