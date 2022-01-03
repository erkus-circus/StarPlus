#ifndef FUNCTIONS_C
#define FUNCTIONS_C

#include <stdio.h>
#include <stdlib.h>

#include "functions.h"
#include "constants.h"

// set_functions
// sets the functions array
void set_functions(unsigned char* file, unsigned int index, unsigned int fileSize)
{
    // the size of the file
    unsigned int numFunctions = 0;

    functions = malloc(sizeof(function) * fourBytesToInt(&file[index]));
    index += 4;

    // loop through the file until the end of the file
    while (index < fileSize)
    {

        // then get the number of arguments from the next 2 bytes
        unsigned char byte1 = file[index];
        unsigned char byte2 = file[index + 1];
        int numArguments = shortToInt(byte1, byte2);
        index += 2;

        // then get the number of instructions from the next byte
        int numInstructions = fourBytesToInt(&file[index]);
        index += 4;

        // create the function
        function func = {numArguments, numInstructions, index, index};

        // add the function to the array
        functions[numFunctions] = func;
        numFunctions++;

        // then skip the instructions
        index += numInstructions;
    }
}

void print_function(function f)
{
    printf("\n");
    printf("numArguments: %d\n", f.num_args);
    printf("numInstructions: %d\n", f.num_instructions);
    printf("index: %d\n", f.start_index);
    printf("\n");
}


function copy_function(int index)
{
    function func = functions[index];
    function copy = {func.num_args, func.num_instructions, func.start_index, func.pc};
    return copy;
}

#endif // FUNCTIONS_C