#ifndef RUNTIME_C
#define RUNTIME_C

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif

#include "binKeys.h"
#include "runtime.h"
#include "constants.h"
#include "data.h"
#include "functions.h"

#define VARIABLE_LIST_SIZE 1024

int* itoa(int value, int* result, int base) {
        if (value == 0) { return "0"; }
		// check that the base if valid
		if (base < 2 || base > 36) { *result = '\0'; return result; }

		int* ptr = result, *ptr1 = result, tmp_char;
		int tmp_value;

		do {
			tmp_value = value;
			value /= base;
			*ptr++ = "zyxwvutsrqponmlkjihgfedcba9876543210123456789abcdefghijklmnopqrstuvwxyz" [35 + (tmp_value - value * base)];
		} while ( value );

		// Apply negative sign
		if (tmp_value < 0) *ptr++ = '-';
		*ptr-- = '\0';
		while(ptr1 < ptr) {
			tmp_char = *ptr;
			*ptr--= *ptr1;
			*ptr1++ = tmp_char;
		}
		return result;
	}

// the function
struct Data *scanToData() {
    int c;
    int i = 0;
    int *string = malloc(sizeof(int)); // allocate memory for a single element

    while ((c = getchar()) != '\n' && c != EOF && i < 100) {
        string[i++] = c;
        string = realloc(string, (i + 1) * sizeof(int)); // reallocate memory for the next element
    }

    // turn the string into a data block
    struct Data *data = createData(i);
    data->values = string;
    return data;
}

// for recursion purposes
int depth = 0;
struct Data call_function(unsigned char *file, int index, struct Stack *argumentsStack)
{
    // ^
    depth++;
    int numExecuted = 0;
    // get the function
    function func = copy_function(index);
    func.pc = 0;
    // create a new stack
    struct Stack *stack = createStack(4);

    // create the variable array
    // TODO: possible number of variables in the function, but for now just realloc it if there are too many variables
    // struct Data *variables = (struct Data *)malloc(sizeof(struct Data) * func.num_args);
    struct Data *variables = (struct Data *)malloc(VARIABLE_LIST_SIZE * sizeof(struct Data));
    
    // puts all of the arguments passed in the functon to
    for (int i = func.num_args - 1; i >= 0; i--)
    {
        variables[i] = s_pop(argumentsStack);
    }

    // start the function
    while (func.pc <= func.start_index + func.num_instructions)
    {
        // get the instruction
        int instruction = file[func.pc + func.start_index];
        func.pc++; // is this going to be a problem? i think it is
        numExecuted++;
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

            break;
        }
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
        {
            // push a constant with index of the next byte onto the stack
            s_push(stack, *d_copy(&constants[(int)file[func.pc + func.start_index]]));
            func.pc++;
            break;
        }
        case CONST_SHORT:
            // push a constant with index of the next 2 bytes onto the stack
            s_push(stack, *d_copy(&constants[shortToInt(file[func.pc + func.start_index], file[func.pc + func.start_index + 1])]));
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
            s_push(stack, *d_copy(&variables[shortToInt(file[func.pc + func.start_index], file[func.pc + func.start_index + 1])]));
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
            variables[file[func.pc + func.start_index]] = s_pop(stack);
            func.pc++;
            break;
        case STORE_SHORT:
            // store the top of the stack in variable with index of the next 2 bytes
            variables[shortToInt(file[func.pc + func.start_index], file[func.pc + func.start_index + 1])] = s_pop(stack);
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
            result->values[0] = b.values[0] - a.values[0];

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
            result->values[0] = (int)(b.values[0] / a.values[0]);

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
            result->values[0] = (b.values[0] % a.values[0]);

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
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            struct Data *result = createData(1);
            result->values[0] = (a.values[0] == b.values[0]);

            d_free(a);
            d_free(b);
            s_push(stack, *result);

            break;
        }

        case GT:
        {
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            struct Data *result = createData(1);
            result->values[0] = (a.values[0] > b.values[0]);

            d_free(a);
            d_free(b);
            s_push(stack, *result);

            break;
        }

        case LT:
        {
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            struct Data *result = createData(1);
            result->values[0] = (a.values[0] < b.values[0]);

            d_free(a);
            d_free(b);
            s_push(stack, *result);

            break;
        }

        case GTE:
        {
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            struct Data *result = createData(1);
            result->values[0] = (a.values[0] >= b.values[0]);

            d_free(a);
            d_free(b);
            s_push(stack, *result);

            break;
        }
        case LTE:
        {
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            struct Data *result = createData(1);
            result->values[0] = (a.values[0] <= b.values[0]);

            d_free(a);
            d_free(b);
            s_push(stack, *result);

            break;
        }
        case NEQ:
        {
            struct Data a = s_pop(stack);
            struct Data b = s_pop(stack);

            struct Data *result = createData(1);
            result->values[0] = (a.values[0] != b.values[0]);

            d_free(a);
            d_free(b);
            s_push(stack, *result);

            break;
        }

        case NEG:
        {
            // negate the value
            struct Data res = s_pop(stack);
            struct Data data = *createData(1);
            data.values[0] = res.values[0];
            d_free(res);
            s_push(stack, data);
            break;
        }

        case COMPARE:
        {
            int linesToSkip = s_pop(stack).values[0];
            int result = s_pop(stack).values[0];

            if (!result)
            {
                func.pc += linesToSkip;
            }
            break;
        }

        case OUT:
        {

            // pop the top of the stack and print it
            struct Data data = s_pop(stack);
            for (size_t i = 0; i < data.size; i++)
            {
                putchar(data.values[i]);
                fflush(stdout);
            }

            break;
        }
        case IN:
        {
            // get one char and push it onto the stack
            s_push(stack, *scanToData());

            break;
        }

        case SLEEP:
        {
            // pop the top of the stack and sleep for that many milliseconds
            struct Data data = s_pop(stack);
            sleep(data.values[0]);

            d_free(data);
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
            depth--;
            return data;
        }

        case DATACOPY:
        {
            // pop the top two values off the stack
            struct Data b = s_pop(stack);
            struct Data a = s_pop(stack);

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

        case INTTOSTR:
        {
            struct Data data = s_pop(stack);
            int value = data.values[0];

            int isNegative = (value < 0);

            // log10(0) is an error, which is why this never works
            int length = 1;
            if (value != 0)
            {
                // the length of the string
                length = (int)floor(log10(isNegative ? -value : value) + 1) + isNegative;
            }

            // create the string
            int *str = (int *)malloc(sizeof(int) * (length + 1));

            // itoa the string
            itoa(value, str, 10);
            struct Data res;
            res.size = length;
            res.values = str;

            s_push(stack, res);
            break;
        }

        case MVU:
        {
            func.pc -= s_pop(stack).values[0];
            break;
        }
        case RANDINT:
        {
            struct Data *data = createData(1);
            data->values[0] = rand();
            s_push(stack, *data);

            break;
        }
        default:
        {
            printf("\nUnknown opcode: %d\n", instruction);
            exit(1);
            break;
        }
        }
    }
    struct Data *errRet = createData(1);
    errRet->values[0] = -1;
    depth--;
    return *errRet;
}
#endif // RUNTIME_C