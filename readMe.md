# StarPlus Language Guide

## Basics
StarPlus is a statically typed and basic programming language. It has features similar to C, Java, and Javascript. It is a compiled language and runs with a custom stack based virtual process.

Like in C, the entry-point of every program is the __main__ function.


## Functions
Functions are blocks of repeatable code. Functions must contain a name, return type, and a body. _Nested functions are not supported at this time_
### Syntax

    func name: returnType (argOne@type, argTwo@type) {
        ...
    }

### Built-In Functions
The following function names are reserved
- `print(variable)` -- prints a variable to the console 
- `input()` -- recieves input from the console and returns it as a string
- `strcpy(strOne, strTwo)` -- appends the values of strTwo to strOne
- `getIndex(string, index)` -- returns the value of a string at the given index. 
- `setIndex(string, newValue, index)` -- changes the value of string at index to newValue
- `size(variable)` -- returns the size of a variable.
- `sleep(n)` -- sleeps for n seconds.
- `rsize(variable, newSize)` -- reallocates the memory of a variable to a new size of newSize
- `intToString(integer)` -- returns a string representation of an integer.
- `iprint(integer)` -- prints an integer to the console.
- `random()` -- returns a random number.
- `fprint(float)` -- prints a float to the console.
- `int(float | string)` -- casts a float to an integer. THIS DOES NOT CHANGE THE VALUE STORED IN MEMORY, ONLY CHANGES THE TYPE OF THE VARIABLE
- `float(int)` -- casts an integer OR STRING to a float.
- `string(int)` -- casts an int or a float to a string. THIS DOES NOT CHANGE THE VALUE STORED IN MEMORY, ONLY CHANGES THE TYPE OF THE VARIABLE
- `fti(float)` -- converts a float to an integer (eg. 4.0 to 4)
- `itf(int)` -- converts an integer to a float (eg. 5 to 5.0)

## Variables

### Syntax

    var variableName: type = value;

## Basic Types

### Integers

    var exampleInteger: int = 42;

Integers can be added, subtracted, multiplied, divided (truncating will occur), and modulused.


### Strings
    var exampleString: string = "Hello StarPlus!";
### Floats

    var exampleFloat: float = 3.1415;

Floats can be created by just adding a '.0' to any number. Using the fprint command, they can be printed to the terminal as a string. 

### Booleans
_Functionality in progress_, use 1 and 0 for now. Cast as integers.

## If statements

### Syntax

    if condition {
        ...
    }

### Comparison Operators
- `==` -- Equal to
- `!=` -- Not equal to
- `<` -- Less than
- `>` -- Greater than
- `<=` -- Less than or equal to
- `>=` -- Greater than or equal to

## Loops
While loops are currently the only loops in the language, _`for` loop functionality is in progress_ 
### Syntax

    while condition {
        ...
    }

## Comments

Single line comments start with the __^__ symbol. In a line (except in strings), anything after the __^__ symbol will not be parsed by the compiler.

## Modules

### string.starp
Includes functions that are helpful for manipulating strings. Currently, including this module also includes the math.starp module by default.
### math.starp

Includes functions that are helpful when working with numbers.

## Expressions & Conditions
__TODO__

## Compilation

To compile a program, run the following command in a terminal:
    
    starpc fileName.starp

This command will create a file named fileName.starpc, which contains the runnable bytecode.

## Runtime

To run a .starpc program, type into a terminal:

    starp fileName.starpc

If there were no errors during compilation, the script should run.

## Building from source
If you would like to build the runtime (C code) from source, you need to have Clang, zip, and Python 3.9+ installed. _(If you are on Windows, edit the `make-release.sh` script to build using a Windows compiler instead if you would so like.)_

To build the project, run the following command in the terminal:

    source make-releash.sh

This creates a build folder which contains both the starp and starpc programs. You can then add them to your path. (zip and clang must be installed)
## Known Bugs/Issues
- If your computer does not use IEEE-754 when storing floats in memory (most computers do), there may be issues with how floats operate.

Eric Diskin
Version Alpha 2.0