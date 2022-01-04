#ifndef RUNTIME_C
#define RUNTIME_C

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "binKeys.h"
#include "runtime.h"
#include "constants.h"
#include "data.h"
#include "functions.h"

struct Data call_function(unsigned char *file, int index, struct Stack *argumentsStack)
{
    // get the function
    function func = copy_function(index);

    // create a new stack
    struct Stack *stack = createStack(4);

    // create the variable array
    // TODO: possible number of variables in the function, but for now just realloc it if there are too many variables
    struct Data *variables = (struct Data *)malloc(sizeof(struct Data) * func.num_args);
    int numVariables = func.num_args;

    // TOOD: push the arguments onto the variable array

    // start the function
    while (func.pc < func.start_index + func.num_instructions)
    {
        // get the instruction
        int instruction = file[func.pc];
        func.pc++;

        // print the instr
        // printf("instruction: %d\n", instruction);

        // switch on the instruction
        switch (instruction)
        {
        case ZERO:
        {
            // push 0 onto the stack
            struct Data *data = createData(1);
            data->values[0] = 0;
            s_push(stack, *data);
        }
        break;
        case CONST_0:
            // push constant 0 onto the stack
            s_push(stack, *d_copy(&constants[0]));
            break;
        case CONST_1:
            // push constant 1 onto the stack
            s_push(stack, *d_copy(&constants[1]));
            break;
        case CONST_2:
            // push constant 2 onto the stack
            s_push(stack, *d_copy(&constants[2]));
            break;
        case CONST_3:
            // push constant 3 onto the stack
            s_push(stack, *d_copy(&constants[3]));
            break;
        case CONST_4:
            // push constant 4 onto the stack
            s_push(stack, *d_copy(&constants[4]));
            break;
        case CONST_5:
            // push constant 5 onto the stack
            s_push(stack, *d_copy(&constants[5]));
            break;

        case CONST_BYTE:
            // push a constant with index of the next byte onto the stack
            s_push(stack, *d_copy(&constants[file[func.pc]]));
            func.pc++;
            break;
        case CONST_SHORT:
            // push a constant with index of the next 2 bytes onto the stack
            s_push(stack, *d_copy(&constants[shortToInt(file[func.pc], file[func.pc + 1])]));
            func.pc += 2;
            break;

        case LOAD_0:
            // push the variable 0 onto the stack
            s_push(stack, *d_copy(&variables[0]));
            break;
        case LOAD_1:
            // push the variable 1 onto the stack
            s_push(stack, *d_copy(&variables[1]));
            break;
        case LOAD_2:
            // push the variable 2 onto the stack
            s_push(stack, *d_copy(&variables[2]));
            break;
        case LOAD_3:
            // push the variable 3 onto the stack
            s_push(stack, *d_copy(&variables[3]));
            break;
        case LOAD_4:
            // push the variable 4 onto the stack
            s_push(stack, *d_copy(&variables[4]));
            break;
        case LOAD_5:
            // push the variable 5 onto the stack
            s_push(stack, *d_copy(&variables[5]));
            break;

        case LOAD_BYTE:
            // push a variable with index of the next byte onto the stack
            s_push(stack, *d_copy(&variables[file[func.pc]]));
            func.pc++;
            break;
        case LOAD_SHORT:
            // push a variable with index of the next 2 bytes onto the stack
            s_push(stack, *d_copy(&variables[shortToInt(file[func.pc], file[func.pc + 1])]));
            func.pc += 2;
            break;

        case STORE_0:
            // store the top of the stack in variable 0
            variables[0] = s_pop(stack);
            break;
        case STORE_1:
            // store the top of the stack in variable 1
            variables[1] = s_pop(stack);
            break;
        case STORE_2:
            // store the top of the stack in variable 2
            variables[2] = s_pop(stack);
            break;
        case STORE_3:
            // store the top of the stack in variable 3
            variables[3] = s_pop(stack);
            break;
        case STORE_4:
            // store the top of the stack in variable 4
            variables[4] = s_pop(stack);
            break;
        case STORE_5:
            // store the top of the stack in variable 5
            variables[5] = s_pop(stack);
            break;

        case STORE_BYTE:
            // store the top of the stack in variable with index of the next byte
            variables[file[func.pc]] = s_pop(stack);
            func.pc++;
            break;
        case STORE_SHORT:
            // store the top of the stack in variable with index of the next 2 bytes
            variables[shortToInt(file[func.pc], file[func.pc + 1])] = s_pop(stack);
            func.pc += 2;
            break;

        case ADD:
        {
            // pop the top two values off the stack
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            // add them together
            struct Data *result = createData(1);
            result->values[0] = a.values[0] + b.values[0];

            // push the result back onto the stack
            s_push(stack, *result);

            // free the memory
            d_free(a);
            d_free(b);

            break;
        }

        case SUB:
        {
            // pop the top two values off the stack
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            // subtract them
            struct Data *result = createData(1);
            result->values[0] = a.values[0] - b.values[0];

            // push the result back onto the stack
            s_push(stack, *result);

            // free the memory
            d_free(a);
            d_free(b);

            break;
        }

        case MUL:
        {
            // pop the top two values off the stack
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            // multiply them
            struct Data *result = createData(1);
            result->values[0] = a.values[0] * b.values[0];

            // push the result back onto the stack
            s_push(stack, *result);

            // free the memory
            d_free(a);
            d_free(b);

            break;
        }

        case DIV:
        {
            // pop the top two values off the stack
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            // divide them
            struct Data *result = createData(1);
            result->values[0] = a.values[0] / b.values[0];

            // push the result back onto the stack
            s_push(stack, *result);

            // free the memory
            d_free(a);
            d_free(b);

            break;
        }

        case MOD:
        {
            // pop the top two values off the stack
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            // mod them
            struct Data *result = createData(1);
            result->values[0] = a.values[0] % b.values[0];

            // push the result back onto the stack
            s_push(stack, *result);

            // free the memory
            d_free(a);
            d_free(b);

            break;
        }

        case EXP:
        {
            // pop the top two values off the stack
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            // exponentiate them
            struct Data *result = createData(1);
            result->values[0] = pow(a.values[0], b.values[0]);

            // push the result back onto the stack
            s_push(stack, *result);

            // free the memory
            d_free(a);
            d_free(b);

            break;
        }

        case EQ:
        {
            // pop the top two values off the stack
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            // compare them
            struct Data *result = createData(1);
            result->values[0] = a.values[0] == b.values[0];

            // push the result back onto the stack
            s_push(stack, *result);

            // free the memory
            d_free(a);
            d_free(b);

            break;
        }

        case GT:
        {
            // pop the top two values off the stack
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            // compare them
            struct Data *result = createData(1);
            result->values[0] = a.values[0] > b.values[0];

            // push the result back onto the stack
            s_push(stack, *result);

            // free the memory
            d_free(a);
            d_free(b);

            break;
        }

        case LT:
        {
            // pop the top two values off the stack
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            // compare them
            struct Data *result = createData(1);
            result->values[0] = a.values[0] < b.values[0];

            // push the result back onto the stack
            s_push(stack, *result);

            // free the memory
            d_free(a);
            d_free(b);

            break;
        }

        case GTE:
        {
            // pop the top two values off the stack
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            // compare them
            struct Data *result = createData(1);
            result->values[0] = a.values[0] >= b.values[0];

            // push the result back onto the stack
            s_push(stack, *result);

            // free the memory
            d_free(a);
            d_free(b);

            break;
        }

        case LTE:
        {
            // pop the top two values off the stack
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            // compare them
            struct Data *result = createData(1);
            result->values[0] = a.values[0] <= b.values[0];

            // push the result back onto the stack
            s_push(stack, *result);

            // free the memory
            d_free(a);
            d_free(b);

            break;
        }

        case NEQ:
        {
            // pop the top two values off the stack
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            // compare them
            struct Data *result = createData(1);
            result->values[0] = a.values[0] != b.values[0];

            // push the result back onto the stack
            s_push(stack, *result);

            // free the memory
            d_free(a);
            d_free(b);

            break;
        }

        case COMPARE:
        {
            // pop the number of values to skip off of the stack
            int skip = s_pop(stack).values[0];

            // pop the comparison value off of the stack
            int value = s_pop(stack).values[0];

            // check if the value is not true, and if condition is false then skip
            if (!value)
            {
                func.pc += skip;
            }
        }

        case OUT:
        {

            // pop the top of the stack and print it
            struct Data data = s_pop(stack);
            for (size_t i = 0; i < data.size; i++)
            {
                putchar(data.values[i]);
            }

            break;
        }
        case IN:
        {
            // get one char and push it onto the stack
            struct Data *data = createData(1);
            data->values[0] = getchar();
            s_push(stack, *data);

            break;
        }

        case SLEEP:
        {
            // pop the top of the stack and sleep for that many seconds
            struct Data data = s_pop(stack);
            // sleep(data.values[0]);

            break;
        }

        case DUP:
        {
            // duplicate the top of the stack
            struct Data data = s_pop(stack);
            s_push(stack, *d_copy(&data));
            s_push(stack, *d_copy(&data));

            break;
        }

        case CALL:
        {
            // get the index of the function to call
            int funcIndex = s_pop(stack).values[0];

            // call the function
            struct Data returnValue = call_function(file, funcIndex, stack);
            s_push(stack, returnValue);
            break;
        }

        case RET:
        {
            // pop the top of the stack and return it
            struct Data data = s_pop(stack);
            return data;
        }

        case DATACOPY:
        {
            // pop the top two values off the stack
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            // copy the data
            struct Data *result = createData(a.size + b.size);

            memcpy(result->values, a.values, a.size * sizeof(int));
            memcpy(result->values + a.size, b.values, b.size * sizeof(int));

            // push the result back onto the stack
            s_push(stack, *result);

            // free the memory
            d_free(a);
            d_free(b);

            break;
        }

        case DATAGET:
        {
            // pop the top two values off the stack
            struct Data indexOfData = s_pop(stack);
            struct Data data = s_pop(stack);

            // get the data
            struct Data *result = createData(1);
            result->values[0] = data.values[indexOfData.values[0]];

            // push the result back onto the stack
            s_push(stack, *result);

            // free the memory
            d_free(indexOfData);
            d_free(data);

            break;
        }

        case DATASIZE:
        {
            // pop the top two values off the stack
            struct Data data = s_pop(stack);

            // get the size of the data
            struct Data *result = createData(1);
            result->values[0] = data.size;

            // push the result back onto the stack
            s_push(stack, *result);

            // free the memory
            d_free(data);

            break;
        }

        case DATARESIZE:
        {
            // pop the top two values off the stack
            struct Data size = s_pop(stack);
            struct Data data = s_pop(stack);

            // resize the data
            struct Data *result = createData(size.values[0]);
            memcpy(result->values, data.values, data.size * sizeof(int));

            // push the result back onto the stack
            s_push(stack, *result);

            // free the memory
            d_free(data);

            break;
        }

        case DATASET:
        {
            // pop the top two values off the stack
            struct Data value = s_pop(stack);
            struct Data indexOfData = s_pop(stack);
            struct Data data = s_pop(stack);

            // put the data
            data.values[indexOfData.values[0]] = value.values[0];

            // push the result back onto the stack
            s_push(stack, data);

            // free the memory
            d_free(value);
            d_free(indexOfData);

            break;
        }
        }
    }
}

#endif // RUNTIME_C