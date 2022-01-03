// new and revised stack.h
// created by Eric Diskin on 12/27/2021


#ifndef STACK_H
#define STACK_H

// for Data struct
#include "data.h"

// stack
struct Stack
{
    int size;
    int index;

    struct Data* arr;
};

////////////////////
// stack functions//
////////////////////

// create stack
struct Stack* createStack(int size);

// push to stack
void s_push(struct Stack* stack, struct Data data);

// pop from stack
struct Data s_pop(struct Stack* stack);

// peek at stack
struct Data s_peek(struct Stack* stack);

// free stack
void s_free(struct Stack* stack);

// print stack
void s_print(struct Stack* stack);


#endif /* STACK_H */