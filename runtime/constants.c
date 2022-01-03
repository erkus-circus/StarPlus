#ifndef CONSTANTS_C
#define CONSTANTS_C

#include <stdio.h>
#include <stdlib.h>

#include "constants.h"
#include "data.h"
#include "binKeys.h"


// for transforming a short into an int
int shortToInt(unsigned char byte1, unsigned char byte2)
{
    // no idea if this works copilot gave it to me
    return (int) byte1 << 8 | byte2;
}

int fourBytesToInt (unsigned char* buf)
{
    int total = 0;
    for (int i = 0; i < 4; i++)
    {
        for (int j = 8; j >= 0; j--)
        {
            total <<= 1;
            if ((buf[i] >> j) & 0x01) total^=1;
        }
    }
    return total;
}


// for getting a constant from the array (this copies the data using d_copy)
struct Data getConstant(int index)
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
int loadConstants(unsigned char* fileArray)
{

    // the index of where in the fileArray the constants are
    int index = 0;

    // first get the number of constants from the first 4 bytes in the file
    int numConstants = fourBytesToInt(fileArray);

    // allocate the constants array
    constants = malloc(sizeof(struct Data) * numConstants);

    // how many contants have been parsed
    int constantsRecieved = 0;

    index += 4; // now the index before the first constant, so loop ++index to get chunks per byte
    // loop until a FUN_HEAD is reached

    for (int constantsRecieved = 0; constantsRecieved < numConstants; constantsRecieved++)
    {
        // first get the number of bytes per chunk, (has to be 1 or 4, later this will support more values)
        int bytesPerChunk = (int) fileArray[index];

        // get the number of chunks in this constant
        int numChunks = fourBytesToInt(fileArray + ++index);
        // now increment by 4 for the passed bytes
        index += 4;

        // create a data struct for the constant
        struct Data* data = createData(numChunks);

        // for loop adding bytes to the array until number of chunks is reached
        for (int i = 0; i < numChunks; i++)
        {
            if (bytesPerChunk == 1)
            {
                data->values[i] = (int) fileArray[index];
                index += 1;
            } else {
                // assume bytesPerChunk is 4
                data->values[i] = fourBytesToInt(&fileArray[index]);
                index += 4;
            }
        }

        constants[constantsRecieved] = *data;
    }

    // the first 4 bytes are the number of constants there are in the program
    return index;
}





#endif // CONSTANTS_C