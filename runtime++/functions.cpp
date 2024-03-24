#include "constants.h"

// set_functions
// sets the functions array
void set_functions(unsigned char* file, unsigned int index, unsigned int fileSize)
{
    // the number of functions found
    unsigned int numFunctions = 0;
    // the total number of functions
    unsigned int totalFunctions = fourBytesToInt(&file[index]);
    index += 4;

    while (index < fileSize)
    {
        unsigned char byte1 = file[index];
        unsigned char byte2 = file[index + 1];
        int numArguments = shortToInt(byte1, byte2);
        index += 2;

        // then get the number of instructions from the next byte
        int numInstructions = fourBytesToInt(&file[index]);
        index += 4;
    }
}