#include <stdio.h>
#include <stdlib.h>

#include "stack.h"
#include "binKeys.h"
#include "data.h"
#include "constants.h"
#include "functions.h"
#include "runtime.h"
void doTests ()
{

    FILE *fp = fopen("test.bin", "wb");
    // unsigned char OneConstantTestFile[] = {
    //     0x00, 0x00, 0x00, 0x01, // 1 constant        //0-3
    //     0x01,                   // 1 byte per chunk        //4
    //     0x00, 0x00, 0x00, 0x0c, // 11 chunks        //5-8
    //     0x48,                   // (H)        //9
    //     0x65,                   // (e)        //10
    //     0x6C,                   // (l)        //11
    //     0x6C,                   // (l)        //12
    //     0x6F,                   // (o)        //13
    //     0x20,                   // (space)        //14
    //     0x57,                   // (W)        //16
    //     0x6F,                   // (o)        //17
    //     0x72,                   // (r)        //18
    //     0x6C,                   // (l)        //19
    //     0x64,                   // (d)        //20
    //     0x21,                   // (!)        //21
    //     FUN_HEAD,               // FUN_HEAD        //22
    // };

    unsigned char TwoConstantsTestFile[] = {
        0x00,
        0x00,
        0x00,
        0x03, // 2 constants
        0x01, // 1 byte per chunk
        0x00,
        0x00,
        0x00,
        0x0c, // 11 chunks
        0x48, // (H)
        0x65, // (e)
        0x6C, // (l)
        0x6C, // (l)
        0x6F, // (o)
        0x20, // (space)
        0x57, // (W)
        0x6F, // (o)
        0x72, // (r)
        0x6C, // (l)
        0x64, // (d)
        0x21, // (!)
        0x01, // 1 byte per chunk
        0x00,
        0x00,
        0x00,
        0x05, // 5 chunks
        0x47, // (G)
        0x41, // (A)
        0x4D, // (M)
        0x45, // (E)
        0x46, // (F)
        0x04, // 4 bytes per chunk
        0x00,
        0x00,
        0x00,
        0x02, // 2 chunks
        0x00,
        0x00,
        0x00,
        0x01,     // int (1)
        0x00,
        0x00,
        0x00,
        0x0A,     // int (32)
        0x00, 0x00, 0x00, 0x03, // 3 functions
        // FUN_HEAD, // FUN_HEAD
        0x00,
        0x00, // the number of arguments
        0x00,
        0x00,
        0x00,
        0x0A, // the number of instructions
        CONST_0,
        OUT,
        CONST_2,
        CONST_2,
        ADD,
        CALL,
        CONST_2,
        CALL,
        ZERO,
        RET,
        // FUN_HEAD,
        0x00,
        0x00, // the number of arguments
        0x00,
        0x00,
        0x00,
        0x04, // the number of instructions
        CONST_1,
        OUT,
        ZERO,
        RET,

        // FUN_HEAD,
        0x00,
        0x00, // the number of arguments
        0x00,
        0x00,
        0x00,
        0x06, // the number of instructions
        CONST_2,
        CONST_2,
        DATAGET,
        OUT,
        ZERO,
        RET,

    };

    unsigned char subStringProgramTest[] = {
        0x00, 0x00, 0x00, 0x05, // 5 constants
        0x04, // 4 bytes per chunk
        0x00, 0x00, 0x00, 0x01, // 1 chunk
        0x00, 0x00, 0x00, 0x01, // number 1
        0x04, // 4 bytes per chunk
        0x00, 0x00, 0x00, 0x01, // 1 chunk
        0x00, 0x00, 0x00, 0x04, // number 4
        0x01, // 1 byte per chunk
        0x00, 0x00, 0x00, 0x05, // 5 chunks
        0x47, // (G)
        0x41, // (A)
        0x4D, // (M)
        0x45, // (E)
        0x46, // (F)
        0x04, // 1 byte per chunk
        0x00, 0x00, 0x00, 0x01, // 1 chunk
        0x00, 0x00, 0x00, 0x0F, // 15 
        0x04, // 1 byte per chunk
        0x00, 0x00, 0x00, 0x01, // 1 chunk
        0x00, 0x00, 0x00, 0x0A, // 10
        0x00, 0x00, 0x00, 0x01, // 1 functions
        // FUN_HEAD
        0x00, 0x00, // 0 arguments
        0x00, 0x00, 0x00, 0x13, // TODO: number of instructions
        
        // store zero in counter variable (V_0)
        ZERO,
        STORE_0,

        // check if the counter is equal to 4

        // counter
        LOAD_0,
        // 4
        CONST_1,
        // check if equal
        GT,
        // lines to skip if false
        CONST_4, // (number 10)
        // compare
        COMPARE,
        // load the string
        CONST_2,
        // load the counter
        LOAD_0,
        // get the data
        DATAGET,
        // print the letter
        OUT,

        // number 1
        CONST_0,
        // counter
        LOAD_0,
        // increment the counter
        ADD,
        // store the counter
        STORE_0,

        // TODO MAKE ANOTHER CONSTANT FOR MVU
        CONST_3, // (15)
        MVU,

        // end program
        ZERO,
        RET,

    };

    unsigned char return0Test[] = {
        0, 0, 0, 1, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 52
    };

    // this is for writing a test
    fwrite(return0Test, sizeof(unsigned char), sizeof(return0Test), fp);
    fclose(fp);
}

int doMain()
{
    // open the file
    FILE *fp;

    char *Fname = "test.bin";

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
    fread(fileArray, sizeof(unsigned char), size, fp);
    fclose(fp);

    unsigned int index = loadConstants(fileArray);
    // set the functions array
    set_functions(fileArray, index, (unsigned int) size);

    printf("\n\nProgram returned: %d\n", call_function(fileArray, 0, NULL).values[0]);

    return 0;
}

int main()
{
    // doTests();
    return doMain();
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
