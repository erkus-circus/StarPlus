//
//  dataTypes.h
//  Emulator - XCode Verson
//
//  Created by Eric Diskin on 3/14/21.
//

#ifndef DATA_H
#define DATA_H

// for supporting more than one value at one place in the stack
struct Data {
    int* values;
    unsigned int size;
};
////////////////////
// Data functions //
////////////////////

// create data
struct Data* createData(unsigned int size);

// free data
void d_free(struct Data data);

// print data
void d_print(struct Data* data);

// set data
void d_set(struct Data* data, int value, unsigned int index);

// get data
int d_get(struct Data* data, unsigned int index);

// copy data
struct Data* d_copy(struct Data* data);

#endif /* DATA_H */