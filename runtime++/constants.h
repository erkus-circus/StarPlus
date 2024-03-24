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

// the number of constants
int numConstants;


#endif /* CONSTANTS_H */