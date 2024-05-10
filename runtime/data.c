#ifndef DATA_C
#define DATA_C

#include <stdio.h>
#include <stdlib.h>

#include "data.h"


// create data
struct Data* createData(unsigned int size)
{
    struct Data* data = (struct Data*) malloc(sizeof(struct Data));
    data->size = size;
    data->values = (int*) malloc(size * sizeof(int));
    return data;
}

// free data
void d_free(struct Data data)
{
    free(data.values);
}

// print data
void d_print(struct Data* data)
{
    printf("\n");
    for (int i = 0; i < data->size; i++) {
        printf("%d ", data->values[i]);
    }
    printf("\n");
}

// set data
// this will be unsafe if values are not allocated
void d_set(struct Data* data, int value, unsigned int index)
{
    data->values[index] = value;
}

// get data
// this will be unsafe if values are not allocated
int d_get(struct Data* data, unsigned int index)
{
    return data->values[index];
}

// copy data
struct Data* d_copy(struct Data* data)
{
    struct Data* copy = createData(data->size);
    for (int i = 0; i < data->size; i++) {
        copy->values[i] = data->values[i];
    }
    return copy;
}

#endif // DATA_C