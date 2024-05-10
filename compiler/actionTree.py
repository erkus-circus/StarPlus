"""
Eric Diskin
Created: 4/3/21
This file takes a parsed AST and turns it into an action tree. 
It also type checks and makes sure that there will be no runtime errors invlolving function calls and all that.
It also creates the indexes for functions, variables, and constants.
After this step is code generation, which takes the action tree and turns it into assembly.
After that the assembly is compiled into bytecode which is then able to be run by my stack machine, and the language is finished
"""


import sys
from syntaxTree import Node
from error import errorTrace
VariableDataTypes = [
    "float",
    "int",
    "string",
    "void",
    "bool"
]

# Function is a class that holds data about the function, like params, return value, and other things like that.
class Function:
    def __init__(self, paramTypes: list[str], returnValue: str, assembly: str=""):
        self.paramTypes = paramTypes
        
        # assembly is for special functions
        self.assembly = assembly
        self.returnValue = returnValue



# functions is a list of function names, and each one can be found at the respective index
# all the builtin functions can be added later to the start or end. To start i will add print and input functions:
functions: list[str] = [
    0
]
# holds a list in parallel with functions
functionData: list[Function] = [
    # main function:
    Function([], None)
]

# special functions, builtin ones.
specialFunctionData: list[Function] = [
    # print function:
    Function(["string"], "void", assembly="OUT"),
    # input:
    Function([], "string", assembly="IN"),
    # strcpy
    Function(["string", "string"], "string", assembly="DATACOPY"),
    # getIndex:
    Function(["string", "int"], "string", assembly="DATAGET"),
    # setIndex:
    Function(["string", "int"], "void", assembly="DATASET"),
    # size function:
    Function(["Any"], "int", assembly="DATASIZE"),
    # sleep:
    Function(["int"], None, assembly="SLEEP"),
    # rsize takes a Data block, and a new size, then reallocs it to the new size:
    Function(["void", "int"], "void", assembly="DATARSIZE"),
    # intToString:
    Function(["int"], "string", assembly="INTTOSTR"),
    # iprint: converts an integer into a string and prints it.
    Function(["int"], "void", assembly="INTTOSTR\nOUT"),
    # returns a random integer.
    Function([], "int", "RANDINT"),
    # prints out a float TODO: make this default formatted in regular print (do after data type checking and allat.)
    Function(["float"], "void", assembly="FOUT"),
    # casts an int to a float
    Function(["int"], "float", assembly="ITF"),
    # casts a float to an int
    Function(["float"], "int", assembly="FTI"),
    # casts a casts an int to a string, does nothing in compiled bytecode, just does stuff.
    Function(["int"], "string", "")
]

specialFunctions = [
    "print",
    "input",
    "strcpy",
    "getIndex",
    "setIndex",
    "size",
    "sleep",
    "rsize",
    "intToString",
    "iprint",
    "random",
    "fprint",
    "float",
    "int",
    "string"
]

# constants is the list of all of the constants in the program. at the end it can generate from the constants generator or something.
constants: list[str] = []

# an array of ints
# each int is the total of variables and parameteres per function
totalVariablesList: list[int] = []

def parseConstants(node: Node):
    for i in node.children:
        if i.nodeName == "string" or i.nodeName == "int":
            i.nodeName = "constantReference"
            if i.value in constants:
                # the constant is already defined
                i.value = constants.index(i.value)
            else:
                # make the value the current len of constants, then append the new constant to the constants array
                constants.append(i.value)
                i.value = len(constants) - 1
        if i.nodeName == "float":
            i.nodeName = "floatConstantReference"
            if i.value in constants:
                # the constant is already defined
                i.value = constants.index(i.value)
            else:
                # make the value the current len of constants, then append the new constant to the constants array
                constants.append(i.value)
                i.value = len(constants) - 1
        else:
            parseConstants(i)

    # probably a more efficient method here but since its 12:17am i am just gonna copy paste
    # TODO make this actually work, IT DOES WORK JUST IS A BIT INEFFICIETN i think
    # no idea why im using caps lock
    for i in node.arguments:
        if i.nodeName == "string" or i.nodeName == "int":
            i.nodeName = "constantReference"
            if i.value in constants:
                # the constant is already defined
                i.value = constants.index(i.value)
            else:
                # make the value the current len of constants, then append the new constant to the constants array
                constants.append(i.value)
                i.value = len(constants) - 1
        if i.nodeName == "float":
            i.nodeName = "floatConstantReference"
            if i.value in constants:
                # the constant is already defined
                i.value = constants.index(i.value)
            else:
                # make the value the current len of constants, then append the new constant to the constants array
                constants.append(i.value)
                i.value = len(constants) - 1
        else:
            parseConstants(i)


# extract all function definitions and then assign them to the functions thing.
# include return type and all that stuff somehow in maybe a different list of functions or something
# or functions list is actually a class that contains the data about the function: (argument types, return value...)
def parseFunctions(node: Node) -> None:
    # loop through to get all function definitions. No repeat functions for at least now.
    for i in node.children:
        if i.nodeName == "function":
            totalVariablesList.append(parseVariables(i, [], []))
            paramTypes = []
            for argument in i.arguments:
                if not argument.type in VariableDataTypes:
                    print("TypeError: Variable type is undefined.")
                    errorTrace(i)

                paramTypes.append(argument.type)
                
            if i.name in functions:
                # error: function already defined
                print("AssignmentError: Function already defined.")
                errorTrace(i)
                sys.exit(-1)
            
            elif i.name == "main":
                # the main function, treat this special
                functions[0] = "main"
                functionData[0] = Function(paramTypes=paramTypes, returnValue=i.type)
                i.name = 0
            else:
                functions.append(i.name)
                 # append the function data to the array.
                functionData.append(Function(paramTypes=paramTypes, returnValue=i.type))
                i.name = len(functions) - 1
               
        
        parseFunctions(i)


def parseCalls(node: Node):
    for i in node.children:
        # parse a call node
        if i.nodeName == "call":
            if not i.name in functions and not i.name in specialFunctions:
                print("ReferenceError: Function '" + i.name + "' is undefined.")
                errorTrace(i)
                sys.exit(-1)
            elif i.name in specialFunctions:
                # this is a special function
                i.name = specialFunctions.index(i.name)
                i.special = True
                i.type = specialFunctionData[i.name].returnValue
            else:
                i.name = functions.index(i.name)
                i.type = functionData[i.name].returnValue

        parseCalls(i)

    for i in node.arguments:
        # parse a call node
        if i.nodeName == "call":
            if not i.name in functions and not i.name in specialFunctions:
                print("ReferenceError: function call is undefined.")
                errorTrace(i)

            elif i.name in specialFunctions:
                # this is a special function
                i.name = specialFunctions.index(i.name)
                i.type = specialFunctionData[i.name].returnValue
                i.special = True
            else:
                i.name = functions.index(i.name)
                i.type = functionData[i.name].returnValue

        parseCalls(i)





# parse a body for variable definitions. Make sure it is in the correct frame, might make a variable stack thing to do this
# like stack of arrays of variables, then when one body ends its var array gets popped, but a new one appears
# also check for duplicate variables and inconsistant typing when calling other functions.
# Do this part last, after constants and functions have been done.

class ScopeStack:

    def __init__(self) -> None:
        self.scopes: list[list[Node]] = []

    def addScope(self):
        self.scopes.append([])

    def popScope(self):
        self.scopes.pop()

    def addVar(self, var):
        self.scopes[-1].append(var)

    # check if a variable has already been defined
    def isDefined(self, var: Node):
        for i in self.scopes[-1]:
            if var in i:
                # error: already defined
                print("Variable already defined!")

"""
To make results come faster, i am going to inneficiently make variable indexes not recycle and prob screw this up. So anyways i hope this goes slightly well.
anything after this is prob half-assed
"""


def parseVariables(node: Node, variables: list[str], variableTypes: list[str]):
    declared = 0

    # do variable declarations first, then references after because otherwise it does not work.
    for i in node.children:
        if i.nodeName == "varDeclaration":
            if i.name in variables:
                # error already defined:
                print("ALREADY DEFINED")

            # makeshift fix, works but i should not need to add this here.
            # this would only happen if a variable has already been given an integer name, aka its already been parsed through and assigned an index.
            if type(i.name) == int:
                continue
            placeholderName = i.name

            if not i.type in VariableDataTypes:
                print("TypeError: Variable's type is of an undefined type.")
                errorTrace(i)
                sys.exit(-1)
            
            
            i.name = len(variables)
            variables.append(placeholderName)
            variableTypes.append(i.type)
            

        # parseVariables(i, variables)

    # do the same but with arguments.
    for i in node.arguments:
        if i.nodeName == "varDeclaration":
            # this is for indexing when codeGeneration happens
            declared += 1
            if i.name in variables:
                # error already defined:
                print("Error: This variable has already been defined.")
                errorTrace(i)
                sys.exit(-1)

            # makeshift fix, works but i should not need to add this here.
            if type(i.name) == int:
                continue

            if not i.type in VariableDataTypes:
                print("TypeError: Variable's type is of an undefined type.")
                errorTrace(i)
                sys.exit(-1)
            
            placeholderName = i.name
            i.name = len(variables)
            variables.append(placeholderName)
            variableTypes.append(i.type)
            
        declared += parseVariables(i, variables, variableTypes)

    for i in node.children:
        if i.nodeName == "reference":
            # variable name is a number when it should be a string.
            
            if not i.name in variables:
                # error not defined
                print("ReferenceError: Variable ", i.name, " is not defined.")
                errorTrace(i)
                sys.exit(-1)
            else:
                i.nodeName = "variableReference"
                i.name = variables.index(i.name)
                i.type = variableTypes[i.name]
        elif i.nodeName == "assignment":
            
            # an assignment node.
            if type(i.name) == int:
                continue
            i.name = variables.index(i.name)
            i.type = variableTypes[i.name]

            # TODO: check to make sure the thing that is getting assigned to the variable is of the correct type.
            


        declared += parseVariables(i, variables, variableTypes)
    return declared
    

def shuntingYard(node: Node) -> Node:
    output: list[Node] = []
    operatorStack: list[Node] = []
    queue: list[Node] = node.children

    
    operatorsPrecedence = {
        "+": 2,
        "-": 2,
        "/": 3,
        "*": 3,
        "%": 4,
        # not sure if these would work
        "<=": 0,
        ">=": 0,
        "<": 0,
        ">": 0,
        "==": 0
    }

    # first, check to make sure every part of the expression is of the same type.
    # if not, throw an error
    # this includes the return types of the functions being called
    typesFound = []

    for token in queue:
        if token.nodeName == "float" or token.nodeName == "int" or token.nodeName == "string" and token.nodeName not in typesFound:
            typesFound.append(token.nodeName)
        if token.nodeName == "call":
            print(token.name, len(functionData))
            # the calls should have been parsed first, so the name of the function is its index
            if token.special and not specialFunctionData[token.name].returnValue in typesFound:
                typesFound.append(specialFunctionData[token.name].returnValue)
            elif not token.special and not functionData[token.name].returnValue in typesFound:
                typesFound.append(functionData[token.name].returnValue)
    if len(typesFound) > 1:
        print("TypeError: Cannot do operations between " + ", ".join(typesFound) + ". Cast one type to the other.")
        errorTrace(node)
    elif len(typesFound) > 0:
        node.type = typesFound[0]
        

    # then, parse the expression using shunting yard.
    for token in queue:
        if token.nodeName == "float" or token.nodeName == "int" or token.nodeName == "string" or token.nodeName == "reference" or token.nodeName == "call" or token.nodeName == "constantReference" or token.nodeName == "variableReference":
            output.append(token)
        elif token.nodeName == "call":
            operatorStack.append(token)
        elif token.nodeName == "operator":
            while len(operatorStack) > 0 and (operatorStack[-1].nodeName == "operator") and (operatorsPrecedence[operatorStack[-1].value] >= operatorsPrecedence[token.value]) and queue[-1].nodeName != "openingParenthesis":
                output.append(operatorStack[-1])
                operatorStack.pop()
            operatorStack.append(token)
        elif token.nodeName == "openingParenthesis":
            operatorStack.append(token)
        elif token.nodeName == "closingParenthesis":
            while operatorStack[-1].nodeName != "openingParenthesis":
                output.append(operatorStack[-1])
                operatorStack.pop()
            if operatorStack[-1].nodeName == "openingParenthesis":
                operatorStack.pop()

    while operatorStack != []:
        output.append(operatorStack[-1])
        operatorStack.pop()

    node.children = output
    return node

def parseExpressions(node: Node) -> Node:
    # apply the shunting yard algorithm to every single expression inside the node.
    for i in node.children:
        # run this recursively
        if i.nodeName == "expression":
            shuntingYard(i)

        parseExpressions(i)
        

    for i in node.arguments:
        # run this recursively
        if i.nodeName == "expression":
            shuntingYard(i)

        parseExpressions(i)
        