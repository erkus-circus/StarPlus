"""
Takes a Node tree, from actionTree.py
Then converts it into a string containing the bytecode and data to be transpiled into actual bytecode
Eric Diskin
Created: 4-19-21, in TLP class
"""

from syntaxTree import Node
from createData import bytesFromNumber, createData
from actionTree import Function, functionData, specialFunctionData, constants, functions
from debugging import DebugFlags
constantsData = ""
output = ""

# this is how many spaces are in between line and its comment.
commentWidth = 4 * " "

# wraps a bunch of code into a function
#


def wrapInFunction(code: str, functionIndex: int) -> str:
    # TODO: bytes from number gives it a 4 long hex, when it should be 2 long hex number.
    argumentsLen = ' '.join(bytesFromNumber(
        len(functionData[functionIndex].paramTypes)).split()[2:])
    return "\nFUN_HEAD" + " ; Index: " + str(functionIndex) + "\n" + argumentsLen + " ; " + str(len(functionData[functionIndex].paramTypes)) + " parameters.\n" + code + "\nINSTR_END\n"


def createExpression(expression: list[Node]) -> str:
    # the dictionary for comparing operators to their bytecode values.
    operatorDict = {
        '+': "IADD ; Add",
        '-': "ISUB ; Subtract",
        '*': "IMUL ; Multiply",
        '/': "IDIV ; Divide",
        '%': "IMOD ; Modulo",

        # not sure if these would work
        "<=": "LTE ; Less Than or Equal To",
        ">=": "GTE ; Greater Than Or Equal To",
        "<": "LT ; Less Than",
        ">": "GT ; Greater Than",
        "==": "EQ ; Equal To"
    }

    currentOutput = ""
    # loop through the expression and create an currentOutput
    for i in expression:
        if i.nodeName == "call":
            # do something special here.
            currentOutput += createCall(i)
        elif i.nodeName == "variableReference":
            currentOutput += '\n' + \
                getString(i.name, "L_") + " ; Variable Index: " + str(i.name)
        elif i.nodeName == "constantReference":
            currentOutput += '\n' + \
                getString(i.value, "C_") + " ; " + \
                str(constants[i.value]) + ", Index: " + str(i.value)
        elif i.nodeName == "operator":
            currentOutput += '\n' + operatorDict[i.value]
    return currentOutput


def createCall(node: Node) -> str:
    currentOutput = ""

    # parse its arguments
    for i in node.children[0].children:
        currentOutput += '\n' + createExpression(i.children)

    # this is a builtin function.
    if node.special:
        currentOutput += '\n' + specialFunctionData[node.name].assembly
    else:
        # get call index
        currentOutput += '\n' + getString(constants.index(node.name), "C_") + " ; " + str(
            functions[node.name]) + ", Function Index: " + str(node.name)
        # call the function
        currentOutput += '\n' + "CALL"
    return currentOutput

# turn like get 5 to C_5 or C_3 or if it is greater than 5, C_B 0x06 or something.
# number is the index of the string, prefix is the prefix like C_ or P_ or S_ or L_


def getString(number: int, prefix: str, forceByte=False) -> str:
    if number <= 5 and not forceByte:
        return prefix + str(number)
    else:
        # not sure if hex is the correct function, should work for now tho.
        hexedNum = hex(number)
        if len(hexedNum) < 4:
            # fixes something
            hexedNum = "0x0" + hexedNum[2]
        return prefix + "B" + "\n" + hexedNum


def createVariableAssignment(node: Node) -> str:
    # the output for the expression
    currentOutput = ""
    # get expression as children.
    # node.children is the expression array
    # should this work?
    if len(node.children) > 0:
        # child length is greater than zero.
        currentOutput += createExpression(node.children[0].children)
    else:
        currentOutput += "\nZERO"
    currentOutput += "\n" + getString(node.name, "S_")
    return currentOutput

# create a higher level constants string, then output it


def createConstants(constants: list) -> str:
    global constantsData

    for i in constants:
        if type(i) == int:
            # int
            constantsData += "\nN " + str(i)
        else:
            # string uses less bits to hold values
            constantsData += "\nS " + i
    # comment this out later:
    if DebugFlags.showHumanConstants:
        print("=============== Constants in human readable format ===============")
        print(constantsData)
    # above line
    return createData(constantsData.strip())

# number of functions
functionCount = 0

def createBody(node: Node) -> str:
    global functionCount
    # the current output, this will go into wrapFunction to turn it into a function before going into the output.

    currentOutput = ""
    # TODO: thinking maybe here count how many lines currentOutput is
    # so then i am able to count how many statements execute
    # which then is used for skipping the correct amout of if statements if it does not work.
    ## TODO: almost 2022 take: do a wrapInIf and wrapInIfElse

    for i in node.children:
        # parse a variable declaration
        if i.nodeName == "varDeclaration" or i.nodeName == "assignment":
            currentOutput += createVariableAssignment(i)
        elif i.nodeName == "function":
            # assumes i has at least one child, because if not then it is broken.
            currentOutput += wrapInFunction(createBody(
                i.children[0]), functionIndex=functionCount)
            # increment the number of functiions parsed.
            functionCount += 1
        elif i.nodeName == "call":
            currentOutput += createCall(i)
        elif i.nodeName == "return":
            currentOutput += createExpression(i.children[0].children)
            currentOutput += "\nRET"
        elif i.nodeName == "if":
            currentOutput += createIf(i)
        elif i.nodeName == "whileLoop":
            currentOutput += createWhileLoop(i)
    return currentOutput

# create an if statement


def createIf(node: Node):
    ifOutput = ""
    # first is the expression to check if is true, then after is the number of lines to skip if the expression evaluates to FALSE.
    ifOutput += createExpression(node.arguments[0].children)
    ifBody = createBody(node)
    if ifBody.strip() != "":

        numStatements = len(ifBody.strip().split("\n"))
        if numStatements in constants:
            # the constant is already defined
            numStatements = "\n" + getString(constants.index(numStatements), "C_") + " ; " + str(
                constants[constants.index(numStatements)]) + ", Index: " + str(constants.index(numStatements))
        else:
            # make the value the current len of constants, then append the new constant to the constants array
            constants.append(numStatements)
            numStatements = "\n" + getString(len(constants) - 1, "C_") + " ; " + str(
                constants[len(constants) - 1]) + ", Index: " + str(len(constants) - 1)
        ifOutput += numStatements
    else:
        ifOutput += "\nZERO"
    # [1:] gets rid of the \n at the start of the body.
    # this makes the bytecode much more readable.
    ifOutput += "\nCOMP\n" + ifBody[1:] + "\n"
    return ifOutput


def createWhileLoop(node: Node):
    loopOutput = "\n"
    # first is the expression to check if is true, then after is the number of lines to skip if the expression evaluates to FALSE.
    loopOutput += createExpression(node.arguments[0].children)
    loopBody = createBody(node)

    numStatementsPreMVU = len(loopBody.strip().split(
        '\n')) + len(loopOutput.strip().split('\n'))

    # + 4 for C_B 0x00 and MVU (MVU needs to add one extra so it works), and then the C_B 0x00 for skipping lines
    if not numStatementsPreMVU + 5 in constants:
        constants.append(numStatementsPreMVU + 5)

    loopBody += '\n' + \
        getString(constants.index(numStatementsPreMVU + 5),
                  'C_', forceByte=True) + '\nMVU\n'

    # now we get the number of statements to skip if the while loop breaks out.
    # - 2 so it doesnt skip the INSTR_END or similar command after the loop
    numStatementsPostMVU = len(loopBody.strip().split('\n')) - 1

    if not numStatementsPostMVU in constants:
        constants.append(numStatementsPostMVU)

    numStatementsStr = "\n" + getString(constants.index(numStatementsPostMVU), "C_", forceByte=True) + " ; " + str(
        constants[constants.index(numStatementsPostMVU)]) + ", Index: " + str(constants.index(numStatementsPostMVU))

    loopOutput += numStatementsStr + "\nCOMP\n" + loopBody[1:] + "\n"
    return loopOutput


def createCode(node: Node, functions: list[str], functionData: list[str], constants: list):
    functionsOut = createBody(node)
    # is below because more constants can be added (from if statements)
    constants = createConstants(constants)
    # - 1 i think for function count?

    # get the longest line:
    longestLine = 0
    for i in functionsOut.splitlines():
        if len(i) > longestLine:
            longestLine = len(i)
    codeOut = ""
    index = 0
    skipNext = False
    for i in functionsOut.split('\n'):
        i = i.strip()
        if skipNext:
            skipNext = False
            codeOut += i + '\n'
            continue
        if len(i) > 0:
            if i.startswith("FUN_HEAD"):
                index = 0
                codeOut += "FUN_HEAD\n"
                skipNext = True
                continue

            codeOut += i + ((longestLine + 8 - len(i)) * " ") + \
                "; PC: " + str(index) + "\n"
            index += 1
        else:
            codeOut += '\n'

    output = constants + \
        str(' '.join(bytesFromNumber(functionCount).split()[2:])) + codeOut
    return output
