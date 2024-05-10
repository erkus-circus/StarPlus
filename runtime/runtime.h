#ifndef RUNTIME_H
#define RUNTIME_H

#include "data.h"
#include "constants.h"
#include "functions.h"
#include "stack.h"


// script execution
struct Data call_function(unsigned char* file, int index, struct Stack* arguments);

#endif // RUNTIME_H