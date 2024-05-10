#ifndef STACK_C
#define STACK_C
#include <stdio.h>
#include <stdlib.h>


#include "stack.h"

// create stack
struct Stack* createStack(int size) {
    struct Stack* stack = (struct Stack*) malloc(sizeof(struct Stack));
    stack->size = size;
    stack->index = -1;
    stack->arr = (struct Data*) malloc(size * sizeof(struct Data*));
    return stack;
}

// push to stack
void s_push (struct Stack* stack, struct Data data) {
    if (stack->index < stack->size - 1) {
        stack->index++;
        stack->arr[stack->index] = data;
    } else {
        // reallocate the stack array
        stack->size *= 2;
        stack->arr = (struct Data*) realloc(stack->arr, stack->size * sizeof(struct Data*));
    }
}

// pop from stack
struct Data s_pop (struct Stack* stack) {
    // there is no error checking here
    struct Data data = stack->arr[stack->index];
    stack->index--;
    return data;
}

// peek from stack
struct Data s_peek (struct Stack* stack) {
    // there is no error checking here
    return stack->arr[stack->index];
}

// free stack
void s_free (struct Stack* stack) {
    free(stack->arr);
    free(stack);
}

// print stack
void s_print (struct Stack* stack) {
    for (int i = 0; i <= stack->index; i++) {
        printf("%d ", stack->arr[i].values[0]);
    }
    printf("\n");
}

#endif // STACK_C