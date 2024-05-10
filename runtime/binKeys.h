#ifndef BINKEYS_H
#define BINKEYS_H

// script execution
enum binKeys
{
    // the start of every function
    FUN_HEAD,

    // the value zero
    ZERO,

    // for placing constants onto the stack
    // const at 0th index
    CONST_0,
    CONST_1,
    CONST_2,
    CONST_3,
    CONST_4,
    CONST_5,
    // for loading a const from a byte
    // the next byte is the index of the const from the const array
    CONST_BYTE,
    // for loading a const from a short (if there are that many constants)
    // the next 2 bytes are the index of the const from the const array
    CONST_SHORT,

    // placing variables on the stack
    // from the variable array (parameters take first few indexes and then other variables come after that)
    LOAD_0,
    LOAD_1,
    LOAD_2,
    LOAD_3,
    LOAD_4,
    LOAD_5,
    // for loading a variable from a byte
    // the next byte is the index of the variable from the variable array
    LOAD_BYTE,
    // for loading a variable from a short (if there are that many variables)
    // the next 2 bytes are the index of the variable from the variable array
    LOAD_SHORT,

    // for storing and setting a variable to a value
    STORE_0,
    STORE_1,
    STORE_2,
    STORE_3,
    STORE_4,
    STORE_5,
    // for storing a variable to a byte in the variable array (if there are that many variables)
    // the next byte is the index of the variable from the variable array
    STORE_BYTE,
    // for storing a variable to a short (if there are that many variables)
    // the next 2 bytes are the index of the variable from the variable array
    STORE_SHORT,

    // the following is for math operations on the stack

    // addition
    ADD,
    // subtraction
    SUB,
    // multiplication
    MUL,
    // division
    DIV,
    // modulus
    MOD,
    // exponentiation
    EXP,

    // TODO: the following are for bitwise operations
    // bitwise and
    AND,
    // bitwise or
    OR,
    // bitwise xor
    XOR,
    // bitwise not
    NOT,
    // bitwise left shift
    LSHIFT,
    // bitwise right shift
    RSHIFT,

    // the following is for comparison operations on the stack
    // compare runs the code below if the top of the stack evaluates to true, otherwise it skips over the code below it based on the number of lines it is said to skip.
    COMPARE,
    // equal
    EQ,
    // greater than
    GT,
    // less than
    LT,
    // greater than or equal to
    GTE,
    // less than or equal to
    LTE,
    // not equal
    NEQ,
    // negate the value
    NEG,

    // for development things:
    // breakpoint for debugging
    BREAKPOINT,

    // the following adds a value to the program counter (for loops and things)
    // the top of the stack is how much is being added to the program counter
    MVU, // short for move up

    // for outputting to the screen
    // the top of the stack is the value to be outputted
    // for now only supports outputting to the screen, later will add support for outputting to a file and other streams
    OUT,

    // for inputting from the user
    // the top of the stack is the variable to be inputted into
    // for now only supports inputting from the screen, later will add support for inputting from a file and other streams
    IN,

    // for sleeping the script
    // the top of the stack is the number of milliseconds to sleep
    SLEEP,

    // for exiting the script
    // the top of the stack is the exit code
    EXIT,

    // for calling a function
    // the top of the stack is the index of the function to be called
    CALL,

    // for returning from a function
    // the top of the stack is the value being returned from the function
    RET,

    // for duplicating the thing on the top of the stack
    DUP,


    // for manipulating Data

    // for copying a Data struct onto another Data struct
    // the top of the stack is the Data struct to be copied/duplicated
    DATACOPY,

    // for freeing a Data struct
    // the top of the stack is the Data struct to be freed
    // make sure constants are never freed
    DATAFREE,

    // for getting a value from a Data struct at a certain index
    // the top of the stack is the Data struct
    // the second value on the stack is the index of the value to be retrieved
    DATAGET,

    // for setting a value in a Data struct at a certain index
    // the top of the stack is the Data struct
    // the second value on the stack is the index of the value to be set
    // the third value on the stack is the value to be set
    DATASET,

    // for getting the size of a Data struct
    // the top of the stack is the Data struct
    DATASIZE,

    // for resizing a Data struct
    // the top of the stack is the Data struct
    // the second value on the stack is the new size of the Data struct
    DATARESIZE,

    // convert an integer to a string
    // the top of the stack is the integer to be converted
    INTTOSTR,

    // pushes a random integer onto the stack
    RANDINT,

    // for float operations:
    FADD,
    FSUB,
    FDIV,
    FMUL,
    FMOD,

    // float to int
    FTI,
    // int to float
    ITF,
    // outputs a float to the screen
    FOUT,

    // comparison operations for floats:
    // equal
    FEQ,
    // greater than
    FGT,
    // less than
    FLT,
    // greater than or equal to
    FGTE,
    // less than or equal to
    FLTE,
    // not equal
    FNEQ
};

#endif /* BINKEYS_H */