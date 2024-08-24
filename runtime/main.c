#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "stack.h"
#include "binKeys.h"
#include "data.h"
#include "constants.h"
#include "functions.h"
#include "runtime.h"

int main(int argc, char *argv[])
{

    // figure out what file is being run from the command line arguments.

    if (argc < 2)
    {
        printf("Usage: starPlus <filename>\n");
        return -1;
    }

    // open the file
    FILE *fp;

    // set this to false if you do not want debug messages.
    int debug = 0;

    char *Fname = argv[1];

    srand(time(NULL));

    if ((fp = fopen(Fname, "rb")) == NULL)
    {
        printf("Error opening file");

        // Program exits if the file pointer returns NULL.
        exit(1);
    }

    fseek(fp, 0, SEEK_END);
    long int size = ftell(fp);
    fclose(fp);

    // Reading data to array of unsigned chars
    fp = fopen(Fname, "rb");
    


    unsigned char *fileArray = (unsigned char *)malloc(size);
    if (debug)
    {
        printf("\nDEBUG: File Size: %d", (int)size);
    }
    
    fread(fileArray, sizeof(unsigned char), size, fp);
    fclose(fp);
    if (debug)
    {
        printf("\nDEBUG: File read.");
    }

    // the array of constants
    int index = 0;
    struct Data* constants = loadConstants(fileArray, &index);
    if (debug)
    {
        printf("\nDEBUG: Loaded Constants.");
    }

    // set the functions array
    set_functions(fileArray, index, (unsigned int)size);
    if (debug)
    {
        printf("\nDEBUG: Allocated Functions.\n");
    }

    clock_t begin = clock();

    int retVal = call_function(fileArray, 0, NULL, constants).values[0];
    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    if (debug)
    {
        printf("\nDEBUG: Program Returned: %d", retVal);
        printf("\nDEBUG: CPU time: %f seconds.\n", time_spent);
    }

    free(constants);
    free(fileArray);
    return retVal;
}

/* Format of the constants

[unsigned int] number of constants

[bit/byte] length of each chunk data in constant (for example, a char per chuck is 8 bits, while an int would be 16 bits)
[int] number of chunks in constant (how many bytes/ints are in the constant)
byte/int
byte/int
byte/int
... until length of constant is reached
^ repeat above for each constant, until number of constants is reached
*/
/*
new file structure:

Constants,
Functions:
FN_START
C_0
C_1
IADD
...whatever
FN_END




create a stack of functions, and a vector of constants
call function 0 at the start of the program

each function starts with a FUN_HEADER which includes the number of arguments of the function
the function has instructions to call other functions
every variable is copied from the constant vector to the stack

after every function d_copy its return value, then free the function and its stack


*/

// example constant file
/*
2 Contants
0x04 ; 4 bytes per chunk
0x00 0x00 0x00 0x01 ; 1 chunk
0x00 0x00 0x00 0x26 ; 38 int decimal
0x01 ; 1 byte per chunk
0x00 0x00 0x00 0x0b ; 11 chunks
0x48 ; (H)
0x65 ; (e)
0x6C ; (l)
0x6C ; (l)
0x6F ; (o)
0x20 ; (space)
0x57 ; (W)
0x6F ; (o)
0x72 ; (r)
0x6C ; (l)
0x64 ; (d)
0x21 ; (!)
FUN_HEAD
0x01 ; 1 argument, this is the number arguments the function takes
CONST_1 ; load the "Hello World!" constant
OUT ; print the constant
ZERO ; load the number 0
RET ; return 0

; a FUN_HEAD could come and function[1] would be defined

*/
