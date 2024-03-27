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

## Variables

### Syntax

    var variableName: type = value;

## Basic Types

### Integers

    var exampleNumber: int = 42;

Integers can be added, subtracted, multiplied, divided (truncating will occur), and modulused.


### Strings
    var exampleString: string = "Hello StarPlus!";
### Floats
_Functionality in progress_
### Booleans
_Functionality in progress_, use 1 and 0 for now. Casted as integers.
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

## Known Bugs/Issues
- Errors are not descriptive enough and sometimes not even reported
- Modules can act buggy
- Floats are not yet implemented
- Until fixed, to get a negative number type in `(0 - number)`



Version Alpha 1.0