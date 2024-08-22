// this file parses the constants into an array of Data structs

#ifndef CONSTANTS_H
#define CONSTANTS_H

#include <stdio.h>
#include <stdlib.h>


// for transforming a byte into an int
int byteToInt(unsigned char byte);

// for transforming a short into an int
int shortToInt(unsigned char byte1, unsigned char byte2);

// for transforming a four bytes into an int
int fourBytesToInt(unsigned char* buf);



// for getting a constant from the array (this copies the data using d_copy)
struct Data getConstant(int index, struct Data* constants);

// pre execution functions

// for loading the constants from the file
// sets the constants array and returns the index in the file at the first FUN_HEAD
struct Data* loadConstants(unsigned char* fileArray, int* index);



#endif /* CONSTANTS_H */